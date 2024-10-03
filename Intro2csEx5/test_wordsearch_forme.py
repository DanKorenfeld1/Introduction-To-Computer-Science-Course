from wordsearch import *
import pytest

dict_matrix = matrix_2D_list_to_dict(read_matrix("mat2.txt"))
word_list = read_wordlist("word_list2.txt")


def get_next_char_tests(name_function):
    assert name_function(dict_matrix, "d", (2, 2)) == (3, 2)
    assert name_function(dict_matrix, "d", (5, 2)) == (-1, -1)

    assert name_function(dict_matrix, "u", (2, 2)) == (1, 2)
    assert name_function(dict_matrix, "u", (0, 2)) == (-1, -1)

    assert name_function(dict_matrix, "l", (2, 2)) == (2, 1)
    assert name_function(dict_matrix, "l", (4, 0)) == (-1, -1)

    assert name_function(dict_matrix, "r", (2, 2)) == (2, 3)
    assert name_function(dict_matrix, "r", (0, 4)) == (-1, -1)

    assert name_function(dict_matrix, "y", (2, 2)) == (3, 3)
    assert name_function(dict_matrix, "y", (5, 4)) == (-1, -1)

    assert name_function(dict_matrix, "z", (2, 2)) == (3, 1)
    assert name_function(dict_matrix, "z", (3, 0)) == (-1, -1)

    assert name_function(dict_matrix, "w", (2, 2)) == (1, 3)
    assert name_function(dict_matrix, "w", (0, 4)) == (-1, -1)
    assert name_function(dict_matrix, "w", (5, 0)) == (4, 1)

    assert name_function(dict_matrix, "x", (2, 2)) == (1, 1)
    assert name_function(dict_matrix, "x", (0, 0)) == (-1, -1)


def from_indexes_and_direction_get_word_tests(name_function):
    LEFT = "l"
    RIGHT = "r"
    DOWN = "d"
    UP = "u"
    RISE_TO_RIGHT = "w"
    RISE_TO_LEFT = "x"
    DESCEND_TO_RIGHT = "y"
    DESCEND_TO_LEFT = "z"
    assert name_function(dict_matrix, word_list, LEFT, (3, 4)) == ['CAT']
    assert name_function(dict_matrix, word_list, LEFT, (4, 4)) == []
    assert name_function(dict_matrix, word_list, LEFT, (0, 0)) == []
    assert name_function(dict_matrix, word_list, UP, (2, 4)) == ['toe']
    assert name_function(dict_matrix, word_list, RISE_TO_LEFT, (3, 4)) == [
        'Crop']
    assert name_function(dict_matrix, word_list, RIGHT, (0, 0)) == ['apple']


def tests():
    get_next_char_tests(get_next_char_ver2)
    from_indexes_and_direction_get_word_tests(
        from_indexes_and_direction_get_word)


tests()
