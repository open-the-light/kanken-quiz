import requests
import re
import pandas as pd
import sqlite3
from typing import List, Dict
from bs4 import BeautifulSoup


def get_vocab_from_jpdb(kanji_to_search: List[str]) -> pd.DataFrame:
    kanji = []
    goi_index = []
    goi = []
    reading = []
    meaning = []
    for k in kanji_to_search:
        url = f"https://jpdb.io/kanji/{k}?expand=v#used_in_{k}_v"
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
            kanji.append(k)
            goi_index.append(i+1)
            goi.append(jp_text[0])
            reading.append(jp_text[1])
            meaning.append(eng[0])
    
    r_dict = {
        'kanji': kanji,
        'goi_index': goi_index,
        'goi': goi,
        'reading': reading,
        'meaning': meaning
    }
    return pd.DataFrame(r_dict)


def write_goi_to_database(df: pd.DataFrame) -> None:
    con = sqlite3.connect("./data/kanken_quiz.db")
    
    df.to_sql('goi_list', con, if_exists='append', index=False)
    con.close()


if __name__ == "__main__":
    test_kanji = ['胤', '軋', '洟', '学']
    results = get_vocab_from_jpdb(test_kanji)
    print(results)
    write_goi_to_database(results)
