import sqlite3
import re
from jamdict import Jamdict
import pandas as pd

grade_mapping = {
    "配当外": 1.0,
    "1級": 1.0,
    "1/準1級": 1.5,
    "準1級": 1.5,
    "2級": 2.0,
    "準2級": 2.5,
    "3級": 3.0,
    "4級": 4.0,
    "5級": 5.0,
    "6級": 6.0,
    "7級": 7.0,
    "8級": 8.0,
    "9級": 9.0,
    "10級": 10.0
}

def read_kanken_kanji_list() -> pd.DataFrame:
    df = pd.read_csv("./data/kanken_kanji_list.csv")
    df.columns = ["page_no", "type_no", "char_id", "kanji", "image", "style", "grade", "link", "addition", "note", "edit"]

    df = df[["char_id", "kanji", "grade", "link"]]
    df.dropna(inplace=True)
    df["link"] = df["link"].str[-10:]
    df["grade_number"] = df["grade"].map(grade_mapping)
    return df

def write_kanken_kanji_list_to_db(df: pd.DataFrame) -> None:
    con = sqlite3.connect("./data/kanken_quiz.db")
    
    df.to_sql('kanji_list', con, if_exists='replace', index=False)
    con.close()

def write_word_frequency_to_db() -> None:
    df = pd.read_csv("./data/BCCWJ_frequencylist_luw2_ver1_0.tsv", sep='\t')
    df = df[["rank", "lForm", "lemma", "pos", "frequency"]]
    with sqlite3.connect("./data/kanken_quiz.db") as conn:
        df.to_sql('freq_list', conn, if_exists='replace', index=False)



if __name__ == "__main__":
    df = read_kanken_kanji_list()
    write_kanken_kanji_list_to_db(df)
    #write_word_frequency_to_db()