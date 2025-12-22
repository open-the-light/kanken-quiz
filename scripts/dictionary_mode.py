import sqlite3
import re
import pandas as pd
from pathlib import Path
from jamdict import Jamdict

class DictionaryMode:
    def __init__(self) -> None:
        print("Setting up Dictionary")
        self.db_path = Path("./data/kanken_quiz.db")
        self.conn = None
        self.cur = None
        self.connect_to_db()

        self.jam = Jamdict()

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
        if len(kanji) == 1:
            print(f"Searching for {kanji}!")
            res = self.cur.execute(f"SELECT * FROM kanji_list where kanji == '{kanji}'")
            raw_data = res.fetchall()
            df = pd.DataFrame(raw_data)
            print(df)

        jresult = self.jam.lookup(kanji)
        for entry in jresult.entries:
            entry = re.sub(r'\(\([^0-9]*\)\)', '', str(entry))
            by_def = re.split(r'\d{1}\.{1}\s{1}', entry)
            print(f"-- {by_def[0]}")
            for i, d in enumerate(by_def[1:]):
                print(f"-- -- {i+1}: {d}")

    def shutdown(self) -> None:
        print("Safely disconnecting from database....")
        self.conn.close()
