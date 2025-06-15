import os
import sys
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from app.db import mysql_utils, postgres_utils
from app.gemini.gemini_client import get_model
from app import carregar_prompt

load_dotenv()

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Gemini - Banco de Dados")
        self.conn = None
        self.db_type = None
        self.esquema_db = ""
        self.prompt_template = ""
        self.tree = None
        self.create_widgets()
        self.model = get_model()

    def create_widgets(self):
        frame_top = ttk.Frame(self.root)
        frame_top.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame_top, text="Escolha o banco de dados:").pack(side="left")
        self.db_var = tk.StringVar(value="MySQL")
        ttk.Radiobutton(frame_top, text="MySQL", variable=self.db_var, value="MySQL").pack(side="left")
        ttk.Radiobutton(frame_top, text="PostgreSQL", variable=self.db_var, value="PostgreSQL").pack(side="left")
        ttk.Button(frame_top, text="Conectar", command=self.conectar_db).pack(side="left", padx=10)
        ttk.Button(frame_top, text="Configurar Conexão", command=self.abrir_configuracao).pack(side="left", padx=10)

        self.schema_text = scrolledtext.ScrolledText(self.root, height=10, width=80, state="disabled")
        self.schema_text.pack(padx=10, pady=5)

        frame_mid = ttk.Frame(self.root)
        frame_mid.pack(padx=10, pady=5, fill="x")
        ttk.Label(frame_mid, text="Pergunta:").pack(side="left")
        self.pergunta_entry = ttk.Entry(frame_mid, width=60)
        self.pergunta_entry.pack(side="left", padx=5)
        ttk.Button(frame_mid, text="Enviar", command=self.enviar_pergunta).pack(side="left")

        self.result_text = scrolledtext.ScrolledText(self.root, height=8, width=80, state="disabled")
        self.result_text.pack(padx=10, pady=5)
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(padx=10, pady=5, fill="both", expand=True)

    def clear_tree(self):
        if self.tree:
            self.tree.destroy()
            self.tree = None

    def show_table(self, columns, rows):
        self.clear_tree()
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.tree.pack(fill="both", expand=True)

    def conectar_db(self):
        db = self.db_var.get()
        try:
            if db == "MySQL":
                self.conn = mysql_utils.connect()
                self.esquema_db = mysql_utils.get_schema(self.conn)
                self.prompt_template = carregar_prompt("prompts/prompt_mysql.txt")
                self.db_type = "MySQL"
            else:
                self.conn = postgres_utils.connect()
                self.esquema_db = postgres_utils.get_schema(self.conn)
                self.prompt_template = carregar_prompt("prompts/prompt_postgres.txt")
                self.db_type = "PostgreSQL"
            self.schema_text.config(state="normal")
            self.schema_text.delete(1.0, tk.END)
            self.schema_text.insert(tk.END, self.esquema_db)
            self.schema_text.config(state="disabled")
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.config(state="disabled")
            messagebox.showinfo("Conectado", f"Conectado ao banco {db}!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def enviar_pergunta(self):
        pergunta = self.pergunta_entry.get().strip()
        if not pergunta:
            return
        if not self.conn:
            messagebox.showwarning("Aviso", "Conecte-se a um banco de dados primeiro.")
            return

        prompt_final = self.prompt_template.format(
            schema=self.esquema_db,
            pergunta_usuario=pergunta
        )
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, f"\nPergunta: {pergunta}\n")
        self.result_text.insert(tk.END, "Gerando consulta SQL...\n")
        self.result_text.config(state="disabled")
        self.root.update()

        try:
            response = self.model.generate_content(prompt_final)
            sql_gerado = response.text.strip().replace("```sql", "").replace("```", "")
        except Exception as e:
            messagebox.showerror("Erro Gemini", f"ERRO ao chamar a API do Gemini: {e}")
            return

        if sql_gerado.startswith("ERRO"):
            self.result_text.config(state="normal")
            self.result_text.insert(tk.END, f"Resposta do Agente: {sql_gerado}\n")
            self.result_text.config(state="disabled")
            self.clear_tree()
            return

        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, f"SQL Gerado:\n{sql_gerado}\n")
        self.result_text.insert(tk.END, "Executando a consulta no banco de dados...\n")
        self.result_text.config(state="disabled")
        self.root.update()

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_gerado)
            if cursor.description:
                resultados = cursor.fetchall()
                nomes_colunas = [i[0] for i in cursor.description]
                self.show_table(nomes_colunas, resultados)
                self.result_text.config(state="normal")
                self.result_text.insert(tk.END, f"Consulta executada com sucesso.\n")
                self.result_text.config(state="disabled")
            else:
                self.clear_tree()
                self.conn.commit()
                self.result_text.config(state="normal")
                self.result_text.insert(tk.END, f"Comando executado com sucesso. {cursor.rowcount} linhas afetadas.\n")
                self.result_text.config(state="disabled")
        except Exception as err:
            self.clear_tree()
            self.result_text.config(state="normal")
            self.result_text.insert(tk.END, f"--- ERRO AO EXECUTAR O SQL ---\n")
            self.result_text.insert(tk.END, f"O SQL gerado pode ser inválido para o dialeto {self.db_type}. Erro: {err}\n")
            self.result_text.config(state="disabled")
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()

    def abrir_configuracao(self):
        config_win = tk.Toplevel(self.root)
        config_win.title("Configuração do .env")

        campos = [
            ("API_KEY", os.getenv("API_KEY", "")),
            ("MYSQL_DB_HOST", os.getenv("MYSQL_DB_HOST", "")),
            ("MYSQL_DB_USER", os.getenv("MYSQL_DB_USER", "")),
            ("MYSQL_DB_PASSWORD", os.getenv("MYSQL_DB_PASSWORD", "")),
            ("MYSQL_DB_NAME", os.getenv("MYSQL_DB_NAME", "")),
            ("PG_DB_HOST", os.getenv("PG_DB_HOST", "")),
            ("PG_DB_USER", os.getenv("PG_DB_USER", "")),
            ("PG_DB_PASSWORD", os.getenv("PG_DB_PASSWORD", "")),
            ("PG_DB_NAME", os.getenv("PG_DB_NAME", "")),
        ]
        entries = {}

        for i, (campo, valor) in enumerate(campos):
            ttk.Label(config_win, text=campo).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = ttk.Entry(config_win, width=40)
            entry.insert(0, valor)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries[campo] = entry

        def salvar_env():
            linhas = []
            for campo, entry in entries.items():
                linhas.append(f"{campo}={entry.get()}")
            try:
                with open(".env", "w", encoding="utf-8") as f:
                    f.write("\n".join(linhas))
                messagebox.showinfo("Sucesso", ".env atualizado! Reinicie a aplicação para recarregar as configurações.")
                config_win.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o .env: {e}")

        ttk.Button(config_win, text="Salvar", command=salvar_env).grid(row=len(campos), column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()