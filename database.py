import sqlite3

DB_NAME = "colecao_hotwheels.db"


def iniciar_banco():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carrinhos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            modelo TEXT,
            cor TEXT,
            ano TEXT,
            foto_path TEXT
        )
    """)

    conn.commit()
    conn.close()