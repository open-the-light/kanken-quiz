import requests
import re
import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from database_helpers import *

# url = "https://www.kanjipedia.jp/kanji/0000138600"
# response = requests.get(url)
# response.raise_for_status()

# soup = BeautifulSoup(response.content, "lxml")

# yomi_list = soup.find('ul', id='onkunList')

# print(yomi_list)
# readings = yomi_list.find_all('p', class_='onkunYomi')

# print(yomi_list)
# print(readings)
# for reading in readings:
#     print("-------")
#     print(reading)
#     stripped = re.sub(r'<[^>]*>', '', str(reading))
#     converted = re.sub(r'・', '/', stripped)
#     print(converted)

def get_kanjipedia_readings(df: pd.DataFrame) -> pd.DataFrame:
    print(df)
    char_id = []
    onyomi = []
    kunyomi = []

    for row in df.itertuples():
        url = f"https://www.kanjipedia.jp/kanji/{row.link}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")
        readings = soup.find_all('p', class_='onkunYomi')
        on = readings[0]
        on_stripped = re.sub(r'<[^>]*>', '', str(on))
        on_converted = re.sub(r'・', '/', on_stripped)
        kun = readings[1]
        kun_stripped = re.sub(r'<[^>]*>', '', str(kun))
        kun_converted = re.sub(r'・', '/', kun_stripped)
        char_id.append(row.char_id)
        onyomi.append(on_converted)
        kunyomi.append(kun_converted)

    r_df = pd.DataFrame({
        'char_id': char_id,
        'onyomi': onyomi,
        'kunyomi': kunyomi
    })    

    return r_df

def write_readings_to_database(df: pd.DataFrame) -> None:
    with sqlite3.connect("./data/kanken_quiz.db") as conn:
        df.to_sql('onkun_list', conn, if_exists='replace', index=False)

if __name__ == "__main__":
    df = get_kanji_by_grade_number(10.0)
    df2 = get_kanjipedia_readings(df)
    write_readings_to_database(df2)