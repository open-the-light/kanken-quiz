import requests
import re
import pandas as pd
import sqlite3
from typing import List, Dict
from bs4 import BeautifulSoup
from database_helpers import *


def get_vocab_from_jpdb(df: pd.DataFrame) -> pd.DataFrame:
    char_id = []
    goi_index = []
    goi = []
    reading = []
    meaning = []
    for row in df.itertuples():
        print(row.kanji)
        url = f"https://jpdb.io/kanji/{row.kanji}?expand=v#used_in_{row.kanji}_v"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")

        used_in_sec = soup.find('div', class_='subsection-used-in')
        used_in = used_in_sec.find_all('div', class_='used-in')

        for i, el in enumerate(used_in):
            if i > 99:
                break
            jp_link = el.find('a', class_='plain')['href']
            jp = re.search(r'/vocabulary/[0-9]*/(.*)#a$', jp_link)
            jp_text = jp.group(1).split('/')
            eng = el.find('div', class_='en').contents
            char_id.append(row.char_id)
            goi_index.append(i+1)
            goi.append(str(jp_text[0]))
            reading.append(str(jp_text[1]))
            meaning.append(str(eng[0]))
            #print(f"{row.kanji} -- goi: {jp_text[0]} -- reading: {jp_text[1]} -- meaning: {eng[0]}")
    
    r_dict = {
        'char_id': char_id,
        'goi_index': goi_index,
        'goi': goi,
        'reading': reading,
        'meaning': meaning
    }
    return pd.DataFrame(r_dict)


def write_goi_to_database(df: pd.DataFrame) -> None:
    with sqlite3.connect("./data/kanken_quiz.db") as conn:
        df.to_sql('goi_list', conn, if_exists='replace', index=False)


if __name__ == "__main__":
    test_kanji = get_kanji_by_grade_number(10.0)
    results = get_vocab_from_jpdb(test_kanji.head(10))
    write_goi_to_database(results)
