import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_toolkit import prompt
from scripts.dictionary_mode import DictionaryMode
from scripts.quiz_mode import QuizMode

def setup_command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="KanKen Quiz"
    )
    parser.add_argument("--dict", "-d", action="store_true", help="Enter dictionary mode")
    parser.add_argument("--quiz", "-q", action="store_true", help="Enter quiz mode")
    parser.add_argument("--grade", "-g", help="The 漢検 grade(s) you wish to draw the questions from")
    parser.add_argument("--number", "-n", help="Number of questions to be asked")

    return parser

def generate_openai_client() -> OpenAI:
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return client

def main():
    parser = setup_command_line_parser()
    args = parser.parse_args()
    client = generate_openai_client()

    if args.dict and args.quiz:
        exit(1)

    if args.quiz:
        print("Beginning Quiz Mode!")
        quiz = QuizMode(float(args.grade), int(args.number))
        quiz.start_quiz()

    if args.dict:
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

if __name__ == "__main__":
    main()
