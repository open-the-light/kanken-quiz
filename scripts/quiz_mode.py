import sqlite3
import pandas as pd
import click
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
from jaconv import hira2kata, kata2hira
from prompt_toolkit import prompt
from scripts.terminal_helpers import click_center, centered_prompt
from scripts.database_helpers import get_example_sentences_for_kanji

class QuizMode:
    def __init__(self, grade: float, questions: int, difficulty: int, client: OpenAI) -> None:
        self.grade = grade
        self.questions = questions
        self.difficulty = difficulty
        self.selection_factor = 200
        self.db_path = "./data/kanken_quiz.db"
        self.question_df = None
        self.current_score = 0
        self.current_question = 1
        self.ex = ThreadPoolExecutor(2)
        self.client = client

        self.threshold = self.set_frequency_threshold()

        self.collect_vocab_for_questions()

    def set_frequency_threshold(self) -> int:
        if self.difficulty == 1:
            return 25
        elif self.difficulty == 2:
            return 12
        elif self.difficulty == 3:
            return 5
        else:
            return 0

    def collect_vocab_for_questions(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            sql_query = f"""select * from goi_grouped_main
            where grade = {self.grade} and frequency >= {self.threshold}"""
            df = pd.read_sql_query(sql_query, conn)
        self.question_df = df.sample(frac=1)

    def start_quiz(self) -> None:
        click.clear()
        for row in self.question_df.iloc[:self.questions].itertuples():
            sentence_task = self.ex.submit(get_example_sentences_for_kanji, row.text, self.client)
            click.echo("\n\n")
            click_center(f"{self.current_question} / {self.questions}")
            click.echo("\n\n")
            click_center(f"{row.text}")
            click.echo("\n\n")
            answer = centered_prompt()
            click.echo("\n\n")

            mreading = kata2hira(row.main_reading)
            possible_answers = set([kata2hira(x) for x in row.readings.split(',')])

            if answer in possible_answers:
                click_center("正解！", fg="green")
                self.current_score += 1
            else:
                click_center(f"残念！ 正解は「{mreading}」だった。。。", fg="red")
                if len(possible_answers) > 1:
                    others = ", ".join([x for x in possible_answers if x != mreading])
                    click_center(f"又は「{others}」")

            click.echo("\n\n\n")

            try:
                sentences = sentence_task.result()
                click_center("例文：", fg="blue")
                click.echo("\n")
                for e in sentences.itertuples():
                    click_center(f"{e.sentence}", fg="blue")
                    click_center(f"{e.translation}")
                    click.echo("\n")
            except Exception as e:
                click.echo(f"sentence generation failed.... {e}")

            click_center(f"Press Enter for next question...")
            click.pause("")
            click.clear()
            self.current_question += 1
        
        self.display_score_screen()



    def display_score_screen(self) -> None:
        click.echo("\n\n\n\n\n")
        click_center(f"終わり！", fg="blue")
        click.echo("\n\n\n")
        click_center(f"スコア：{self.current_score} / {self.questions}", fg="blue")

        click.echo("\n\n\n")
        click_center(f"Press Enter to end...")
        click.pause("")
        click.clear()

    def __str__(self) -> str:
        return f"QuizMode: Grade={self.grade}, Questions={self.questions}"