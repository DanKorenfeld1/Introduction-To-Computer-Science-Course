##############################################################################
# FILE: board.py
# WRITERS: Matan Kaminski
#          Dan Korenfeld
# EXERCISE: Intro2cs2 ex12 2021-2022
# DESCRIPTION: the Board Class
##############################################################################
from boggle_board_randomizer import *


class Board:
    """ This class creates the board to boggle game.  """

    def __init__(self):
        self.board = randomize_board()
        self.dic_board = {}

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.dic_board[(row, col)] = self.board[row][col]

    def get_board(self):
        """ return the board """
        return self.board

    def get_dic_board(self):
        """ return a dictionary when
        keys are coordinates (row, col) and value is the letter on board
        """
        return self.dic_board

    def get_letter(self, row, col):
        """ return a letter based on it's coordinates """
        return self.dic_board[(row, col)]

    def __str__(self):
        return '\n'.join([str(i) for i in self.board])

    def create_word(self, path):
        """
        this function run over tuples of location in path and return the
        letter/s the path create based on the board.
        :param path: list of tuples. each tuple is a location in the board of a
        letter
        :return: word from the path and the board
        """
        word = ""
        for letter in path:
            word += self.get_letter(letter[0], letter[1])
        return word
