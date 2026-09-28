from py_evil_hangman import parse_args
from py_evil_hangman import GameManager

if __name__ == "__main__":
    cfg = parse_args()
    GameManager(True, cfg.dictionary_file, cfg.guesses, cfg.verbose, cfg.karma).control_loop()
