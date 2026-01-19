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

def get_example_sentences_for_kanji(kanji: str, client: OpenAI) -> Dict:
    response_object = client.chat.completions.parse(
        model = "gpt-5.2",
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

    return rdata