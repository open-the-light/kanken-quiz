import sqlite3
import pandas as pd
from typing import Dict
from openai import OpenAI
from scripts.schema import SentenceList

path = "./data/kanken_quiz.db"


def get_kanji_list_head(n: int) -> pd.DataFrame:
    with sqlite3.connect(path) as conn:
        sql_query = f"select * from kanji_list limit {n}"
        df = pd.read_sql_query(sql_query, conn)
    return df

def get_kanji_by_grade_number(grade: float) -> pd.DataFrame:
    with sqlite3.connect(path) as conn:
        sql_query = f"select * from kanji_list where grade_number = {grade}"
        df = pd.read_sql_query(sql_query, conn)
    return df

def get_kanji_by_grade(grade: str) -> pd.DataFrame:
    with sqlite3.connect(path) as conn:
        sql_query = f"select * from kanji_list where grade = {grade}"
        df = pd.read_sql_query(sql_query, conn)
    return df

def setup_example_sentences_table() -> None:
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()
        sql_query = f"CREATE TABLE IF NOT EXISTS example_sentences(kanji TEXT NOT NULL, no INT NOT NULL, sentence TEXT NOT NULL, translation TEXT NOT NULL)"
        cur.execute(sql_query)

def add_sentences_to_db(sentences: pd.DataFrame) -> None:
    setup_example_sentences_table()
    
    df = sentences[["kanji", "no", "sentence", "translation"]]
    with sqlite3.connect(path) as conn:
        df.to_sql('example_sentences', conn, if_exists='append', index=False)

def get_sentences_from_db(kanji: str) -> pd.DataFrame:
    setup_example_sentences_table()
    with sqlite3.connect(path) as conn:
        q = f"select * from example_sentences where kanji = '{kanji}'"
        df = pd.read_sql_query(q, conn)
    return df

def get_example_sentences_for_kanji(kanji: str, client: OpenAI) -> pd.DataFrame:

    pregen_sentences = get_sentences_from_db(kanji)
    if not pregen_sentences.empty:
        return pregen_sentences

    response_object = client.chat.completions.parse(
        model = "gpt-5-nano",
        messages = [
            {
                "role": "system",
                "content": (
                    "You work for a company that creates dictionaries, and your job is to create example sentences."
                    "You have great pride in your extensive vocabulary, and love to demonstrate this by creating rich, detailed sentences."
                    "You will be generating sentences when provided with a character."
                    "Return the sentences as JSON following the attached schema."
                )
            },
            {
                "role": "user", 
                "content": f"Generate five example sentences in Japanese that contain the character {kanji}."
            }
        ],
        response_format = SentenceList,
    )
    data = response_object.choices[0].message.content

    rdata = SentenceList.model_validate_json(data).model_dump()

    df = pd.DataFrame(rdata['data'])
    add_sentences_to_db(df)

    return df