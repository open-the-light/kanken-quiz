import click
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_toolkit import prompt
from scripts.dictionary_mode import DictionaryMode
from scripts.quiz_mode import QuizMode

def generate_openai_client() -> OpenAI:
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return client


@click.group(help="KanKen Quiz")
def cli():
    pass


@cli.command(help="Enter dictionary mode")
def dict():
    client = generate_openai_client()
    print("Entering Kanji Dictionary Mode!")
    kanji_dict = DictionaryMode()
    print("Here you can search the database for details on particular kanji.")
    print("Enter a word you would like to seach the dictionary for:")
    while True:
        search_term = prompt(">>> ")
        if search_term in ["exit", "quit"]:
            print("Leaving search screen")
            break
        kanji_dict.handle_search(search_term, client)
    kanji_dict.shutdown()


@cli.command(help="Enter quiz mode")
@click.option("--grade", "-g", type=float, help="The 漢検 grade(s) you wish to draw the questions from")
@click.option("--number", "-n", default=10, show_default=True, type=int)
@click.option("--level", "-l", default=1, show_default=True, type=click.IntRange(1, 4))
def quiz(grade, number, level):
    print("Beginning Quiz Mode!")
    client = generate_openai_client()
    quiz = QuizMode(grade, number, level, client)
    quiz.start_quiz()


if __name__ == "__main__":
    cli()
