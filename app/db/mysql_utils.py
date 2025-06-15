import os
import mysql.connector

def connect():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_DB_HOST"),
        user=os.getenv("MYSQL_DB_USER"),
        password=os.getenv("MYSQL_DB_PASSWORD"),
        database=os.getenv("MYSQL_DB_NAME")
    )

def get_schema(conn):
    esquema_db = ""
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tabelas = [t[0] for t in cursor.fetchall()]
    for tabela in tabelas:
        esquema_db += f"Tabela '{tabela}':\n"
        cursor.execute(f"DESCRIBE `{tabela}`")
        colunas = cursor.fetchall()
        for col in colunas:
            esquema_db += f" - {col[0]} ({col[1]})\n"
        esquema_db += "\n"
    cursor.close()
    return esquema_db