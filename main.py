import argparse
from prompt_toolkit import prompt
from scripts.dictionary_mode import DictionaryMode

def setup_command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="KanKen Quiz"
    )
    parser.add_argument("--dict", "-d", action="store_true", help="Enter dictionary mode")

    return parser


def main():
    parser = setup_command_line_parser()
    args = parser.parse_args()

    if args.dict:
        print("Entering Dictionary Mode!")
        kanji_dict = DictionaryMode()
        print("Enter a character you would like to seach the dictionary for:")
        while True:
            search_term = prompt(">>> ")
            if search_term in ["exit", "quit"]:
                print("Leaving search screen")
                break
            kanji_dict.search_db(search_term)
        kanji_dict.shutdown()
    else:
        print("Starting KanKen Quiz!")

if __name__ == "__main__":
    main()
