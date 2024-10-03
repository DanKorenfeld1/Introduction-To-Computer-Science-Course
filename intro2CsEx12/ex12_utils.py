##############################################################################
# FILE: ex12_utils.py
# WRITERS: Matan Kaminski
#          Dan Korenfeld
# EXERCISE: Intro2cs2 ex12 2021-2022
# DESCRIPTION:
##############################################################################
from copy import deepcopy


DIRECTIONS = {'LEFT': (0, -1),
              'RIGHT': (0, 1),
              'DOWN': (1, 0),
              'UP': (-1, 0),
              'RISE_TO_RIGHT': (-1, 1),
              'RISE_TO_LEFT': (-1, -1),
              'DESCEND_TO_RIGHT': (1, 1),
              'DESCEND_TO_LEFT': (1, -1)}

# All THE A-B-C
ABC_SET = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}


def build_set_of_words(path_of_file, board):
    """
    The function take the words from dictionary file and create a set only with
    the words that all the letters in the words are on board
    :param path_of_file: A file with all the words from dictionary
    :param board: 2D list with letters
    :return: set only with
    the words that all the letters in the words are on board.
    """
    set_of_words = set()  # set of words
    letters_off_board = ABC_SET - all_letters_on_board(board)
    with open(path_of_file, "r") as file_of_words:
        for line in file_of_words.readlines():
            line = line.replace('\n', '')
            # check if all the letter in word are on board
            if reduce(line, letters_off_board):
                set_of_words.add(line)
        return set_of_words


def all_letters_on_board(board):
    """
    Get all the letter on the board
    :param board: The board of the game
    :return: Set of letters on board
    """
    letters_on_boards = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if len(board[row][col]) == 2:
                letters_on_boards.add(board[row][col][0])
                letters_on_boards.add(board[row][col][1])
            else:
                letters_on_boards.add(board[row][col])
    return letters_on_boards


def reduce(word, letters_off_board):
    """
    check if a letter off board is in word
    :param word: checked word
    :param letters_off_board: all the letters of board
    :return: True if the word is OK, else False
    """
    for letter in letters_off_board:
        if letter in word:
            return False
    return True


def reduce_set(words_set, letters_off_board):
    """
    Go over a set of word, if there is a word with a letter off board,
    remove it
    :param words_set: All the words in dictionary
    :param letters_off_board: All the letters off board
    :return: reduced set
    """
    words = deepcopy(words_set)
    for word in words:
        for letter in letters_off_board:
            if letter in word and word in words_set:
                words_set.remove(word)
    return words_set


def is_valid_path(board, path, words):
    """
    Check if a path is valid (answer all the game's conditions)
    :param board: The board of the game
    :param path: list of tuples representing a word
    :param words: All the words in dictionary
    :return: if the path is valid return the word, else None
    """
    word = ""
    for index, letter in enumerate(path):
        row = letter[0]
        col = letter[1]
        # The tuple is of board
        if not -1 < row < len(board) or not -1 < col < len(board[0]):
            return None
        path_without_letter = path[:]
        path_without_letter.remove(letter)
        # The tuple is twice on list
        if letter in path_without_letter:
            return None
        # There is only one place on path
        if len(path) == 1:
            if board[row][col] in words:
                return board[row][col]
            else:
                return None
        # Check if there is two places on path which are not neighbors
        # There is only one neighbor in index 1
        if index == 0:
            next_row = path[index + 1][0]
            next_col = path[index + 1][1]
            if not 0 <= abs(row - next_row) <= 1 or\
                    not 0 <= abs(col - next_col) <= 1:
                return None
        # There is only one neighbor in index len(path) - 2
        elif index == len(path) - 1:
            prev_row = path[index - 1][0]
            prev_col = path[index - 1][1]
            if not 0 <= abs(row - prev_row) <= 1 or\
                    not 0 <= abs(col - prev_col) <= 1:
                return None
        # There are two neighbors, one in index - 1 and one in index + 1
        else:
            next_row = path[index + 1][0]
            next_col = path[index + 1][1]
            if not 0 <= abs(row - next_row) <= 1 or \
                    not 0 <= abs(col - next_col) <= 1:
                return None
            prev_row = path[index - 1][0]
            prev_col = path[index - 1][1]
            if not 0 <= abs(row - prev_row) <= 1 or \
                    not 0 <= abs(col - prev_col) <= 1:
                return None
        word += board[row][col]
    # Check if word exist
    if word not in words:
        return None
    return word


def start_with(start_word, words):
    """
    Check if there is a word start with a given string
    :param start_word: an opening of word
    :param words: All the words in dictionary
    :return: True if there is, False if not
    """
    for word in words:
        if word.startswith(start_word):
            return True
    return False


def in_words(word_checked, words):
    """
    Check if a word in dictionary
    :param word_checked: The word for check
    :param words: All the words in dictionary
    :return: True if there is, False if not
    """
    for word in words:
        if word == word_checked:
            return True
    return False


def find_length_helper(n, length, board, word, words,
                       path, all_paths_from_one_point, row, col, flag):
    """
    The function get a coordinates on board and return all the valid
    paths in length n
    :param n: Length of the path needed
    :param length: Length of the current path
    :param board: The board of the game
    :param word: The word created from path
    :param words: All the words in dictionary
    :param path:
    :param all_paths_from_one_point:
    :param row:
    :param col:
    :param flag: decide which "main" function called this function
    :return: A list of all the valid paths
    """
    if (row, col) not in path:
        word += board[row][col]
        path.append((row, col))
        if flag:
            length = len(board[row][col])
        else:
            length += 1

    if length == n:
        if in_words(word, words):
            val_path = path[:]
            all_paths_from_one_point.append(val_path)
            return
        return
    if not start_with(word, words):
        return
    for direction, move in DIRECTIONS.items():

        if -1 < row + move[0] < len(board) and \
                -1 < col + move[1] < len(board[0]):
            if (row + move[0], col + move[1]) not in path:
                path.append((row + move[0], col + move[1]))
                word += board[row + move[0]][col + move[1]]
                if flag:  # if flag = True -> check length of word
                    len_cell_char = len(board[row + move[0]][col + move[1]])
                    find_length_helper(n, length + len_cell_char, board, word,
                                       words, path, all_paths_from_one_point,
                                       row + move[0], col + move[1], flag)
                else:  # if flag = False -> check length of path
                    find_length_helper(n, length + 1, board, word, words,
                                       path, all_paths_from_one_point,
                                       row + move[0], col + move[1], flag)
                path.pop()
                word = word[:-len(board[row + move[0]][col + move[1]])]


def find_length_n_paths(n, board, words):
    """
    Find all the valid paths with length n
    :param n: Length of the path needed
    :param board: The board of the game
    :param words: All the words in dictionary
    :return: All the valid paths with length n
    """
    all_paths = []
    letters_off_board = ABC_SET - all_letters_on_board(board)
    words = reduce_set(words, letters_off_board)
    for row in range(len(board)):
        for col in range(len(board[row])):
            all_paths_from_one_point = []
            find_length_helper(n, 0, board, "", words, [],
                               all_paths_from_one_point, row, col, False)
            if len(all_paths_from_one_point) > 0:
                one_point = all_paths_from_one_point[:]
                all_paths += one_point
    return all_paths


def find_length_n_words(n, board, words):
    """
    Find all the valid paths which create word with length n
    :param n: Length of the path needed
    :param board: The board of the game
    :param words: All the words in dictionary
    :return: All the valid paths with length n
    """
    letters_off_board = ABC_SET - all_letters_on_board(board)
    words = reduce_set(words, letters_off_board)
    all_paths = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            all_paths_from_one_point = []
            find_length_helper(n, 0, board, "", words, [],
                               all_paths_from_one_point, row, col, True)
            if len(all_paths_from_one_point) > 0:
                one_point = all_paths_from_one_point[:]
                all_paths += one_point
    return all_paths


def from_path_get_word(board, path):
    """
    Get a path and create the word in which the path represent
    :param board: The board of the game
    :param path: list of tuples representing a word
    :return: A word in which the path represent
    """
    word = ""
    for cell in path:
        y, x = cell[0], cell[1]
        word += board[y][x]
    return word


def max_score_paths(board, words):
    """
    The function find all the path in which create the max score a player can
    get
    :param board: The board of the game
    :param words: All the words in dictionary
    :return: All the path in which create the max score a player can
    """
    found_words = []
    all_paths = []
    letters_off_board = ABC_SET - all_letters_on_board(board)
    words = reduce_set(words, letters_off_board)
    for i in range(16, 0, -1):
        path_size_i = find_length_n_paths(i, board, words)
        if len(path_size_i) == 0:
            continue
        else:
            for path in path_size_i:
                word = from_path_get_word(board, path)
                if word not in found_words and word in words:
                    found_words.append(word)
                    all_paths.append(path)
    return all_paths
