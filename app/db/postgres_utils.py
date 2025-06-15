import os
import psycopg2

def connect():
    return psycopg2.connect(
        host=os.getenv("PG_DB_HOST"),
        user=os.getenv("PG_DB_USER"),
        password=os.getenv("PG_DB_PASSWORD"),
        dbname=os.getenv("PG_DB_NAME")
    )

def get_schema(conn):
    esquema_db = ""
    cursor = conn.cursor()
    query = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    cursor.execute(query)
    tabela_atual = ""
    for row in cursor.fetchall():
        nome_tabela, nome_coluna, tipo_dado = row
        if nome_tabela != tabela_atual:
            tabela_atual = nome_tabela
            esquema_db += f"\nTabela '{tabela_atual}':\n"
        esquema_db += f" - {nome_coluna} ({tipo_dado})\n"
    cursor.close()
    return esquema_db