import sqlite3

def init_db():
    conn = sqlite3.connect("data/speeches.db")
    # Table Speeches
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Speeches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            date TEXT,
            nbr_sentences INTEGER,
            nbr_words INTEGER,
            nbr_seconds INTEGER,
            categories TEXT
        );
    """)

    # Table Transcriptions
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Transcriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            speech_id INTEGER NOT NULL,
            timestamp TEXT,
            duration TEXT,
            text TEXT,
            FOREIGN KEY (speech_id) REFERENCES Speeches(id)
        );
    """)
    conn.commit()
    return conn
