import sqlite3
import pandas as pd
from pathlib import Path

class DictionaryMode:
    def __init__(self) -> None:
        print("Setting up Dictionary")
        self.db_path = Path("./data/kanken_quiz.db")
        self.conn = None
        self.cur = None
        self.connect_to_db()

    def connect_to_db(self) -> None:
        try:
            conn = sqlite3.connect(self.db_path)
            self.conn = conn
            self.cur = conn.cursor()
            print("Connected to database!")
        except Exception as e:
            print(e)
            print("Could not connect to database for some reason...")

    def search_db(self, kanji: str) -> None:
        print(f"Searching for {kanji}!")
        res = self.cur.execute(f"SELECT * FROM kanji_list where kanji == '{kanji}'")
        raw_data = res.fetchall()
        df = pd.DataFrame(raw_data)
        print(df)

    def shutdown(self) -> None:
        print("Safely disconnecting from database....")
        self.conn.close()
