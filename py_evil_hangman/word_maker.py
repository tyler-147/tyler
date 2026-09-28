from __future__ import annotations
from collections import defaultdict # You might find this useful
import os

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

class WordMakerHuman():
    def __init__(self, words_file, verbose):
        # we need to prompt the player for a word, then clear the screen so that player 2 doesn't see the word.
        self.verbose = verbose
        self.words = {} # Make sure that you understand dictionaries. They will be extremely useful for this project.
        with open(words_file) as wordfile:
            for line in wordfile:
                word = line.strip()
                if len(word) > 0:
                    self.words[word] = True # I could have made this a set() instead.

    def reset(self, word_length):
        # Your AI code should not call input() or print().
        question = ""
        while True:
            question = input(f"Please type in your word of length {word_length}: ")
            if question in self.words and len(question) == word_length:
                break
            print("Invalid word.")
        if not self.verbose:
            print("\n" * 100) # Clear the screen
        self.word = question

    def get_valid_word(self):
        return self.word

    def get_amount_of_valid_words(self):
        return 1 # the only possible word is self.word

    def guess(self, guess_letter):
        idx = self.word.find(guess_letter)
        ret = []
        while idx != -1:
            ret.append(idx)
            idx = self.word.find(guess_letter, idx + 1)
        return ret




class WordMakerAI():
    """
    A new WordMakerAI is instantiated every time you launch the game with evil_hangman.py.
    (However, the test harness can make multiple instances.)
    Between games, the reset() function is called. This should clear any internal gamestate that you have.
    The number of guesses, input gathering, winning, losing, etc. is all managed by the GameManager, so you don't
     have to prompt the user at all. All you need to do is keep track of the active dictionary of still-valid words
     in this game.

    Do not assume anything about the lengths of the words. You will be tested on dictionaries with extremely long words.
    """
    def __init__(self, words_file: str, verbose=False):
        # This initializer should read in the words into any data structures you see fit
        # The input format is a file of words separated by newlines
        # Use open() to open the file, and remember to split up words by word length!

        # Feel free to use this parameter to toggle extra print statments. Verbose mode can be turned on via the --verbose flag.
        self.verbose = verbose

        # Use this code if you like.
        # generate empty list made of lists that will be appended for each element of the dictionary
        max_len = 0
        with open(
                words_file) as wordfile:  # this run through the text file finds the max length of the word in the list to create the empty list
            for line in wordfile:
                current_len = len(line.strip())
                if current_len > max_len:
                    max_len = current_len  # overwrite max_length when we find a larger one
        dict_sorted = [[] for i in range(max_len)]  # create empty list of lists

        # iterate through the dictionary, appending each word to the appropriate list sorted by length (indexed by len(word) - 1)
        with open(words_file) as wordfile:
            for line in wordfile:
                current_len = len(line.strip())
                dict_sorted[current_len - 1].append(line.strip())

        # create two copies of sorted dictionary, one that will not be changed and one that will be narrowed down as the guesses are made
        self.dictionary = dict_sorted
        self.curr_dict = dict_sorted

    def reset(self, word_length: int) -> None:
        # This function starts a new game with a word length of `word_length`. This will always be called before guess() or get_valid_word() are called.
        # You should try to make this function should be O(1). That is, you shouldn't have to process over the entire dictionary here (find somewhere else to preprocess it)
        # Your AI code should not call input() or print().

        self.curr_dict = self.dictionary[word_length - 1] #reset the current dictionary to the set of words of length word_length

    def get_valid_word(self) -> str:
        # Get a valid word in the active dictionary, to return when you lose
        # Can return any word, as long as it satisfies the previous guesses

        # Get the first word in the set of the remaining words to return if a valid word is asked for
        valid_word = self.curr_dict[0]
        if isinstance(valid_word,
                      str):  # this is to ensure the answer is a string? the else condition shouldn't ever come up
            told_you_so = valid_word
        else:
            told_you_so = 'This should never show up but if it does, something has gone very wrong with processing the dictionary'

        return told_you_so

    def get_amount_of_valid_words(self) -> int:
        # This function gets the total amount of possible words "remaining" (i.e., that satisfy all the guesses since self.reset was last called)
        # This should also be O(1)
        # Note: This is used extensively in the autograder! Be sure to verify that this function works
        # via the provided test cases.
        # You can see this number by running with the verbose flag, i.e. `python3 evil_hangman.py --verbose`

        # Get length of current dictionary
        len_remaining = len(self.curr_dict)

        return len_remaining

    def get_letter_positions_in_word(self, word: str, guess_letter: str) -> tuple[int, ...]:
        # This function should return the positions of guess_letter in word. For instance:
        #  get_letter_positions_in_word("hello", "l") should return (2, 3). The list should
        #  be sorted ascending and 0-indexed.
        # You can assume that word is lowercase with at least length 1 and guess_letter has exactly length 1 and is a lowercase a-z letter.

        #iterate over letters in word and append index if it does
        letter_index = []
        for i in range(len(word)):
            if word[i] == guess_letter:
                letter_index.append(i)

        return tuple(letter_index)
        

    def guess(self, guess_letter) -> list[int]:
        # This is the meat of the project. This function is called by the GameManager.
        # Using get_letter_positions_in_word, this function should sort all remaining words
        #  into their respective letter families. Then, it should pick the largest family,
        #  resolving ties by picking the set with fewer guess_letters. If the amount of
        #  guess_letter's are equal, then either set can be picked to become the new active
        #  dictionary.
        # This function should return the positions of where a guess_letter should appear.
        # For instance, if you want an "e" to appear in positions 0 and 2, return [0, 2].
        # Make sure the list is sorted.

        # Here is an example run of guess():
        #  If the guess is "a" and the words left are ["ah", "ai", "bo"], then we should return [0], because
        #  we are picking the family of words with an "a" in the 0th position. If this function decides that the biggest family
        #  has no a's, then we would have returned [].

        # In the case of a tie (multiple families have the same amount of words), we should pick the set of words with fewer guess_letter's.
        #  That is, if the guess is "a" and the words left are ["ah", "hi"], we should return [] (picking the set ["hi"]), 
        #  since ["hi"] and ["ah"] are equal length and "hi" has fewer a's than "ah".
        # Again, if both sets have an equal number of guess_letter's, then it is ok to pick either.
        #  For example, if the guess is "a" and the words left are ["aha", "haa"], you can return either [0, 2] or [1, 2].

        # The order of the returned list should be sorted. You can assume that 'guess_letter' has not been seen yet since the last call to self.reset(),
        #  and that guess_letter has len of 1 and is a lowercase a-z letter.

        # run through the current dictionary and save all the positions to a list
        all_pos = []
        for i in self.curr_dict:
            all_pos.append(self.get_letter_positions_in_word(i, guess_letter))

        # count how many times each unique index pops up
        uniq_pos = list(set(all_pos))
        max_pos = ()  # set the initial max position to override
        max_num = 0
        for i in range(len(uniq_pos)):

            num_pos = all_pos.count(uniq_pos[i])  # count how many times each position pops up

            # decide if num_pos is larger than previous and handle the edge/match cases
            if max_num < num_pos:
                max_pos = uniq_pos[i]
                max_num = num_pos
            elif num_pos == max_num:  # the default assumption is to keep the current max_pos the same unless the new one is empty or shorter. For simplicity, I will always just keep the current max_pos if there are the same number of occurrences in the set
                if not uniq_pos[i] or len(uniq_pos[i]) < len(max_pos):
                    max_pos = uniq_pos[
                        i]  # update the position if the new one is empty, but the number doesn't need to be updated. If the old one is empty, a later if statemen will take care of this

        # update the curr_dict to be the ones with the remaining letters
        # create empty curr_dict to fill in
        rep_curr_dict = []
        for i in range(len(all_pos)):
            if all_pos[i] == max_pos:
                rep_curr_dict.append(self.curr_dict[i])

        # replace the curr_dict with the new curr_dict
        self.curr_dict = rep_curr_dict

        return list(max_pos)
