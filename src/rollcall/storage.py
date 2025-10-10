import os
import sqlite3

def store_urls(urls):
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/speeches.db")
    for url in urls:
        conn.execute("INSERT OR IGNORE INTO Speeches (url, soup) VALUES (?, ?)", (url, None))

    conn.commit()
    conn.close()
