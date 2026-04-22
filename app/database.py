import sqlite3

DB_NAME = "leads.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        empresa TEXT,
        telefono TEXT,
        email TEXT,
        web TEXT,
        direccion TEXT,
        score INTEGER DEFAULT 0,
        contacted INTEGER DEFAULT 0,
        last_contact TEXT,
        status TEXT DEFAULT 'new'
    )
    """)




    conn.commit()
    conn.close()
