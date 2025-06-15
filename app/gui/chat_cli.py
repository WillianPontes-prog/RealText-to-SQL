import os
import sys
from dotenv import load_dotenv
from tabulate import tabulate

from app.db import mysql_utils, postgres_utils
from app.gemini.gemini_client import get_model
from app import carregar_prompt

load_dotenv()

def main():
    model = get_model()
    while True:
        db_choice = input("Qual banco de dados você quer acessar?\n1. MySQL (employees)\n2. PostgreSQL (dvdrental)\nEscolha (1 ou 2): ")
        if db_choice in ["1", "2"]:
            break
        print("Opção inválida. Por favor, digite 1 ou 2.")

    if db_choice == "1":
        conn = mysql_utils.connect()
        esquema_db = mysql_utils.get_schema(conn)
        prompt_template = carregar_prompt("prompts/prompt_mysql.txt")
        db_type = "MySQL"
    else:
        conn = postgres_utils.connect()
        esquema_db = postgres_utils.get_schema(conn)
        prompt_template = carregar_prompt("prompts/prompt_postgres.txt")
        db_type = "PostgreSQL"

    while True:
        pergunta_usuario = input("\nFaça sua pergunta (ou digite 'sair' para terminar): ")
        if pergunta_usuario.lower() == 'sair':
            break

        prompt_final = prompt_template.format(
            schema=esquema_db,
            pergunta_usuario=pergunta_usuario
        )

        print("\n Gerando consulta SQL")
        try:
            response = model.generate_content(prompt_final)
            sql_gerado = response.text.strip().replace("```sql", "").replace("```", "")
        except Exception as e:
            print(f"ERRO ao chamar a API do Gemini: {e}")
            continue

        if sql_gerado.startswith("ERRO"):
            print(f"\n Resposta do Agente: {sql_gerado}")
            continue

        print(f"\nSQL Gerado:\n{sql_gerado}\n")
        print("Executando a consulta no banco de dados...")
        try:
            cursor = conn.cursor()
            cursor.execute(sql_gerado)
            if cursor.description:
                resultados = cursor.fetchall()
                nomes_colunas = [i[0] for i in cursor.description]
                print(tabulate(resultados, headers=nomes_colunas, tablefmt="psql"))
            else:
                conn.commit()
                print(f"Comando executado com sucesso. {cursor.rowcount} linhas afetadas.")
        except Exception as err:
            print(f"--- ERRO AO EXECUTAR O SQL ---")
            print(f"O SQL gerado pode ser inválido para o dialeto {db_type}. Erro: {err}")
            conn.rollback()
        finally:
            if cursor:
                cursor.close()

    if conn:
        conn.close()
        print("\n Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()