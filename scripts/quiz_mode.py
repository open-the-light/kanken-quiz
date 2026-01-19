import sqlite3
import pandas as pd
from jaconv import hira2kata
from prompt_toolkit import prompt

class QuizMode:
    def __init__(self, grade: float, questions: int) -> None:
        print("setting up quiz mode")
        print(type(grade), type(questions))
        self.grade = grade
        self.questions = questions
        self.db_path = "./data/kanken_quiz.db"
        self.question_df = None

        self.collect_vocab_for_questions()

    def collect_vocab_for_questions(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            sql_query = f"select distinct text, grade, lForm, frequency from goi_freq where grade = {self.grade} order by frequency desc limit {self.questions}"
            df = pd.read_sql_query(sql_query, conn)
        self.question_df = df

    def start_quiz(self) -> None:
        while True:
            for row in self.question_df.itertuples():
                print(f"Question: {row.text}")
                answer = prompt("Answer>>> ")
                print(f"{row.lForm}, {answer}, {hira2kata(answer)}")
                print(f"{row.lForm == hira2kata(answer)}")
            break

    def __str__(self) -> str:
        return f"QuizMode: Grade={self.grade}, Questions={self.questions}"