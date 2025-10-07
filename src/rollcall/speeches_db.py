import sqlite3

def init_db():
    conn=sqlite3.connect('data/speeches.db')
    conn.executescript("Create Table if not exists Speeches (id, soup)")
