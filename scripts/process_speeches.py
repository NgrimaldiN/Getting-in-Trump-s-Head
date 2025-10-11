import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..','src')))
from rollcall.url_soupper import url_soupper
from rollcall.speech_decomposer import (get_title, get_date, get_cleaned_categories, get_nbr_sentences_nbr_words_nbr_seconds, get_trump_transcriptions)
import sqlite3
import json
def process_speeches():
    conn=sqlite3.connect("data/speeches.db")
    cur=conn.cursor()
    rows=cur.execute("Select id, url from Speeches where title is NULL").fetchall()
    for id, url in rows:
        soup=url_soupper(url)
        title=get_title(soup)
        date=get_date(soup)
        nbr_sentences, nbr_words, nbr_seconds = get_nbr_sentences_nbr_words_nbr_seconds(soup)
        categories=get_cleaned_categories(soup)
        categories_str = json.dumps(categories, ensure_ascii=False)
        trump_transcript=get_trump_transcriptions(soup)

        cur.execute(""" Update Speeches Set title=?, date=?, nbr_sentences=?, nbr_words=?, nbr_seconds=?,categories=? where id=?""", (title, date, nbr_sentences, nbr_words, nbr_seconds, categories_str, id))
        for transcription in trump_transcript:
            cur.execute("""
            INSERT INTO Transcriptions (speech_id, timestamp, text)
            VALUES (?, ?, ?);
        """, (id, transcription[0], transcription[1]))
        conn.commit()
    conn.close()

if __name__=='__main__':
    process_speeches()