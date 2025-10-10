import sqlite3

def init_db():
    conn = sqlite3.connect('data/speeches.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Speeches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            soup TEXT
        );
    """)
    conn.commit()
    return conn
