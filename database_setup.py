import sqlite3
from jamdict import Jamdict
import pandas as pd

def read_kanken_kanji_list() -> pd.DataFrame:
    df = pd.read_csv("./data/kanken_kanji_list.csv")
    df.columns = ["page_no", "type_no", "char_id", "kanji", "image", "style", "grade", "link", "addition", "note", "edit"]

    df = df[["char_id", "kanji", "grade", "link"]]
    df.dropna(inplace=True)
    return df

def write_kanken_kanji_list_to_db(df: pd.DataFrame) -> None:
    con = sqlite3.connect("./data/kanken_quiz.db")
    
    df.to_sql('kanji', con, if_exists='replace', index=True)
    con.close()




if __name__ == "__main__":
    df = read_kanken_kanji_list()
    write_kanken_kanji_list_to_db(df)