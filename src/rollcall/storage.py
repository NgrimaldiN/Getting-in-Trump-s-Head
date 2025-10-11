
import sqlite3

def store_urls(urls):
    conn = sqlite3.connect("data/speeches.db")
    for url in urls:
        conn.execute("INSERT OR IGNORE INTO Speeches (url) VALUES (?)", (url,))

    conn.commit()
    conn.close()
