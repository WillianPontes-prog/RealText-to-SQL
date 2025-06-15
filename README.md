# Chat Gemini Banco de Dados

Este projeto permite que você faça perguntas em português sobre seus bancos de dados MySQL ou PostgreSQL e obtenha respostas automáticas, usando a API Gemini do Google para gerar e executar consultas SQL.  
Você pode usar tanto uma interface gráfica (Tkinter) quanto uma interface de linha de comando (CLI).

---

## 📁 Estrutura do Projeto

```
projetoFinal/
│
├── app/
│   ├── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── mysql_utils.py
│   │   └── postgres_utils.py
│   ├── gemini/
│   │   ├── __init__.py
│   │   └── gemini_client.py
│   ├── gui/
│   │   ├── __init__.py
│   │   └── chat_gui.py
│   └── cli/
│       ├── __init__.py
│       └── chat_cli.py
│
├── prompts/
│   ├── prompt_mysql.txt
│   └── prompt_postgres.txt
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Pré-requisitos

- Python 3.8 ou superior
- MySQL e/ou PostgreSQL instalados e configurados
- Chave de API Gemini (Google AI Studio)

---

## 🛠️ Instalação

1. **Clone o repositório e entre na pasta:**
    ```sh
    git clone <url-do-seu-repositorio>
    cd projetoFinal
    ```

2. **Instale as dependências:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Configure o arquivo `.env`:**

    Preencha com suas credenciais:
    ```
    API_KEY=sua_api_key_gemini

    MYSQL_DB_HOST=localhost
    MYSQL_DB_USER=seu_usuario_mysql
    MYSQL_DB_PASSWORD=sua_senha_mysql
    MYSQL_DB_NAME=nome_do_banco_mysql

    PG_DB_HOST=localhost
    PG_DB_USER=seu_usuario_postgres
    PG_DB_PASSWORD=sua_senha_postgres
    PG_DB_NAME=nome_do_banco_postgres
    ```

4. **Garanta que os arquivos de prompt estejam em `prompts/`:**
    - `prompt_mysql.txt`
    - `prompt_postgres.txt`

---

## ⚙️ Configuração de Conexão

Você pode configurar os dados de acesso aos bancos de dados e à API Gemini de duas formas:

- **Diretamente no arquivo `.env`** (usando um editor de texto)
- **Pela interface gráfica**, clicando no botão **"Configurar Conexão"** e preenchendo os campos:

    - **API_KEY**: Sua chave da API Gemini (veja abaixo como obter)
    - **MYSQL_DB_HOST**: Endereço do seu servidor MySQL (ex: `localhost`)
    - **MYSQL_DB_USER**: Nome de usuário do MySQL (ex: `root`)
    - **MYSQL_DB_PASSWORD**: Senha do MySQL
    - **MYSQL_DB_NAME**: Nome do banco de dados MySQL (ex: `projetobd`)
    - **PG_DB_HOST**: Endereço do seu servidor PostgreSQL
    - **PG_DB_USER**: Nome de usuário do PostgreSQL
    - **PG_DB_PASSWORD**: Senha do PostgreSQL
    - **PG_DB_NAME**: Nome do banco de dados PostgreSQL

Após salvar, reinicie o programa para que as alterações tenham efeito.

---

## 🔑 Como obter uma API Key do Gemini

1. Acesse o [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Faça login com sua conta Google.
3. Clique em **"Create API Key"** (ou "Criar chave de API").
4. Copie a chave gerada.
5. Cole a chave no campo `API_KEY` do seu arquivo `.env` ou na tela de configuração do programa.

**Atenção:**  
Guarde sua chave em segredo. Não compartilhe publicamente.

---

## 🖥️ Como Usar

### Interface Gráfica (Tkinter)

Execute:
```sh
python -m app.gui.chat_gui
```

- Escolha o banco de dados (MySQL ou PostgreSQL)
- Clique em "Conectar"
- Faça perguntas em português sobre os dados
- Veja os resultados em uma tabela gráfica
- Use o botão "Configurar Conexão" para editar o `.env` pela interface

### Interface de Linha de Comando (CLI)

Execute:
```sh
python -m app.cli.chat_cli
```

- Escolha o banco de dados (1 ou 2)
- Faça perguntas em português
- Veja os resultados no terminal

---

## 💡 Exemplos de Perguntas

- "Mostre todos os alunos do curso de Engenharia"
- "Quantos departamentos existem?"
- "Adicione um aluno chamado João no curso 2"

---

## 📝 Observações

- O Gemini gera SQL automaticamente, mas revise comandos de alteração de dados.
- Para comandos INSERT, UPDATE ou DELETE, use com cautela.
- O botão "Configurar Conexão" permite editar o `.env` sem sair do programa (mas reinicie para recarregar as variáveis).

---

## 📄 Licença

Este projeto é apenas para fins acadêmicos e de demonstração.
