##############################################################################
# FILE: logic.py
# WRITERS: Matan Kaminski
#          Dan Korenfeld
# EXERCISE: Intro2cs2 ex12 2021-2022
# DESCRIPTION:
##############################################################################
from ex12_utils import *

WORDS_FILE = "boggle_dict.txt"


class GameLogic:
    """ This class control the logic of the game """

    def __init__(self, board):
        self.score = 0
        self.board = board
        self.guest_correct_words = []
        self.guest_wrong_words = ['']
        self.words = build_set_of_words(WORDS_FILE, board)

    def get_words(self):
        """ return the words dictionary """
        return self.words

    def set_score(self, path):
        """
        The method check if a path is valid and change the score
        :param path: list of tuples representing a word
        :return: The word anf true or false if the word is words dictionary
        """
        word = is_valid_path(self.board, path, self.words)
        if not word or word in self.guest_correct_words:
            if not word:
                word = from_path_get_word(self.board, path)
            return False, word

        elif word:
            self.score += len(path) ** 2
            return True, word

    def get_guest_correct_words(self):
        """ return the list of words that guest correctly """
        return self.guest_correct_words

    def get_guest_wrong_words(self):
        """ return the list of words that guest wrongly """
        return self.guest_wrong_words

    def set_guest_correct_words(self, word):
        """ add a correct guest word to the list """
        self.guest_correct_words.append(word)

    def set_guest_wrong_words(self, word):
        """ add a wrong guest word to the list """
        self.guest_wrong_words.append(word)

    def get_score(self):
        """ return the score """
        return self.score
