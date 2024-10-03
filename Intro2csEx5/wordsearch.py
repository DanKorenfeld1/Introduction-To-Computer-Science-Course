############################################################################
# FILE: wordsearch.py
# EXERCISE: ex5
# DESCRIPTION: ctrl+"/" write a note ctrl+"." minimize function
############################################################################
import sys, os

LEFT = "l"
RIGHT = "r"
DOWN = "d"
UP = "u"
RISE_TO_RIGHT = "w"
RISE_TO_LEFT = "x"
DESCEND_TO_RIGHT = "y"
DESCEND_TO_LEFT = "z"


# read_word_list
def read_wordlist(filename):
    """
    function that return list of words from file
    :param filename: the path of the file
    :return: list[string] -> the list of the words
    """
    list_of_word = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.readlines():
            list_of_word.append(line[:-1])
        return list_of_word


# read_matrix
def read_matrix(filename):
    """
    function that return the matrix of the game, from the file
    :param filename: the path of the file
    :return: list[list]
    """
    matrix = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            one_line = line.split(",")
            matrix.append(one_line)
        return matrix


# print_matrix
def print_matrix(matrix):
    """
    Auxiliary function that prints the indexes and value of the matrix
    :param matrix: the matrix of the game
    :return: None
    """
    for i, value in enumerate(matrix):
        lis = []
        for j, val in enumerate(value):
            print("  ", end="  ")
            if j == len(value) - 1:
                print(val)

            else:
                print(val, end="    ")
            lis.append(["{},{}".format(i, j)])
        print(lis)


# matrix_2d_list_to_dictionary
def matrix_2D_list_to_dict(matrix):
    """
    funciton that change the data structure to dictionary
    :param matrix: list[list] the matrix of the game
    :return: dictionary: the keys is the "x,y" indexes and value is the value
    """
    matrix_dict = {}
    for i, value in enumerate(matrix):
        for j, val in enumerate(value):
            matrix_dict[(i, j)] = val
    return matrix_dict


# the_same_word
def same_word(list_of_char, word):
    """
    check if the list of char is the same word
    :param list_of_char: list of char from the matrix
    :param word: word from the list of the word
    :return: boolean
    """
    if "".join(list_of_char) == word:
        return True
    return False


# from_indexes_and_direction_get_word
def from_indexes_and_direction_get_word(dict_matrix, word_list,
                                        direction, current_index):
    """
    function that get specific direction and current index, and return the
    right word from the list of the word that there in the right conditions
    :param dict_matrix: the matrix as dictionary
    :param word_list: list of the words
    :param current_index: tuple (x,y) that present specific cell
    :return: list of word (string)
    """
    right_words = {}
    optional_words = []  # the list of the char that the program check
    optional_words.append(dict_matrix[current_index])
    relevant_words = word_list[:]  # the current list with the word

    for word in word_list:
        if word == dict_matrix[current_index]:
            right_words[word] = 1

    while True:
        if get_next_char_ver2(dict_matrix,
                              direction, current_index) != (-1, -1):
            index_next_char = get_next_char_ver2(dict_matrix, direction,
                                                 current_index)
            optional_words.append(dict_matrix[index_next_char])
            current_index = index_next_char
        else:
            break
        count = 0
        # check if there are right option for this combination:
        for word in word_list:
            if same_word(optional_words, word):
                if word not in right_words:
                    right_words[word] = 1
                else:
                    right_words[word] += 1
            if word[:len(optional_words)] == "".join(optional_words):
                # it's good, there are option for right words
                count += 1
            else:
                relevant_words.remove(word)
        if count == 0:
            break
        word_list = relevant_words[:]
    return right_words


def add_number_of_right_word(result_of_right_word, right_word):
    """
    get the current right word and the value (as dictionary) and the
    dictionary with the new right words and add the new word and update the num
    :param result_of_right_word: dictionary[word]=number_appearance form matrix
    :param right_word: new word and number appearance
    :return:
    """
    for key in right_word.keys():
        if key in result_of_right_word.keys():
            result_of_right_word[key] += right_word[key]
        else:
            result_of_right_word[key] = right_word[key]
    return result_of_right_word


def search_word_per_direction(word_list, dict_matrix, direction):
    """
    search words in "up" as the direction
    :param word_list: the list of all the word
    :param dict_matrix: dictionary that present the matrix
    :param direction: the direction that need to search
    :return: dictionary with the founded word
    """
    result_of_right_word = {}
    for i in dict_matrix.keys():
        right_word = from_indexes_and_direction_get_word(dict_matrix,
                                                         word_list, direction,
                                                         i)
        if right_word != {}:
            result_of_right_word = add_number_of_right_word(
                result_of_right_word, right_word)
    return result_of_right_word


def find_words(word_list, list_matrix, directions):
    """"""
    set_of_directions = set(directions)
    right_word = {}
    dict_matrix = matrix_2D_list_to_dict(list_matrix)
    for direction in set_of_directions:
        if direction == UP:
            words = search_word_per_direction(word_list, dict_matrix, UP)
        elif direction == DOWN:
            words = search_word_per_direction(word_list, dict_matrix, DOWN)
        elif direction == RIGHT:
            words = search_word_per_direction(word_list, dict_matrix, RIGHT)
        elif direction == LEFT:
            words = search_word_per_direction(word_list, dict_matrix, LEFT)
        elif direction == RISE_TO_RIGHT:
            words = search_word_per_direction(word_list, dict_matrix,
                                              RISE_TO_RIGHT)
        elif direction == RISE_TO_LEFT:
            words = search_word_per_direction(word_list, dict_matrix,
                                              RISE_TO_LEFT)
        elif direction == DESCEND_TO_RIGHT:
            words = search_word_per_direction(word_list, dict_matrix,
                                              DESCEND_TO_RIGHT)
        elif direction == DESCEND_TO_LEFT:
            words = search_word_per_direction(word_list, dict_matrix,
                                              DESCEND_TO_LEFT)
        right_word = add_number_of_right_word(right_word, words)
    return from_dictionary_to_list_and_tuple_and_sort(right_word, word_list)


def from_dictionary_to_list_and_tuple_and_sort(right_word, word_list):
    """
    function that conver the dictionary [word]:number_appearance
    to list and tuples
    :param right_word: the dictionary with the word
    :param word_list: the list of all the word
    :return: list[tuple(word, number)]
    """
    list_of_word = []
    for word in word_list:
        if word in right_word.keys():
            list_of_word.append((word, right_word[word]))
    return list_of_word


# get next char ver 2
def get_next_char_ver2(dict_matrix, direction, current_index):
    """
    function that return the next index that the program need
    :param dict_matrix: the matrix as dictionary
    :param direction: string(one) that present the direction of the searching
    :param current_index: (x,y) the current index that the program check
    :return: tuple (x,y) with the next indexes. if the tuple is (-1,-1)
    it's the end of the row\column\slant
    """
    x_index = current_index[0]
    y_index = current_index[1]
    NOT_EXIST = (-1, -1)
    if direction == UP:  # up
        desirable_cell = (x_index - 1, y_index)
    elif direction == DOWN:  # down
        desirable_cell = (x_index + 1, y_index)
    elif direction == RIGHT:  # right
        desirable_cell = (x_index, y_index + 1)
    elif direction == LEFT:  # left
        desirable_cell = (x_index, y_index - 1)
    elif direction == RISE_TO_RIGHT:  # Diagonal rises to the right
        desirable_cell = (x_index - 1, y_index + 1)
    elif direction == RISE_TO_LEFT:  # Diagonal rises to the left
        desirable_cell = (x_index - 1, y_index - 1)
    elif direction == DESCEND_TO_RIGHT:  # Diagonal descends to the right
        desirable_cell = (x_index + 1, y_index + 1)
    elif direction == DESCEND_TO_LEFT:  # Diagonal descends to the left
        desirable_cell = (x_index + 1, y_index - 1)
    if desirable_cell in dict_matrix:  # check about the desirable cell
        return desirable_cell
    else:
        return NOT_EXIST


def write_output(results, filename):
    """
    function that write to a file the words and the number from funciton
    find_words
    :param results: list[tuple] the result of the words
    :param filename: the path of the file name
    :return: None (file)
    """
    with open(filename, "w", encoding="utf-8") as file:
        for word in results:
            file.write(str(word[0] + "," + str(word[1]) + "\n"))
        file.close()


def directions_is_ok(directions):
    """
    check if the directions that the program get is ok
    :param directions: the directions that the program get
    :return: boolean
    """
    good_directions = list("udlrxwzy")
    for i in list(directions):
        if i not in good_directions:
            return False
    return True


def main():
    ERROR_PARAM = "There is a problem with the amount of inputs, there should"\
                  " be 4 inputs"
    ERROR_FILE_WORD_NOT_EXIST = "The word list file does not exist"
    ERROR_FILE_MATRIX_NOT_EXIST = "the file of the matrix not exist"
    ERROR_WRONG_DIRECTION = "the direction isn't allow"
    if len(sys.argv) != 5:
        print(ERROR_PARAM)
    else:
        path_word_file = sys.argv[1]
        path_matrix_file = sys.argv[2]
        path_output_file = sys.argv[3]
        directions = sys.argv[4]
        if not os.path.isfile(path_matrix_file) and not os.path.isfile(
                path_word_file):
            print(ERROR_FILE_WORD_NOT_EXIST)
        elif not os.path.isfile(path_word_file):
            print(ERROR_FILE_WORD_NOT_EXIST)
        elif not os.path.isfile(path_matrix_file):
            print(ERROR_FILE_MATRIX_NOT_EXIST)
        elif not directions_is_ok(directions):
            print(ERROR_WRONG_DIRECTION)
        else:
            list_matrix = read_matrix(path_matrix_file)
            word_list = read_wordlist(path_word_file)
            list_of_word = find_words(word_list, list_matrix, directions)
            write_output(list_of_word, path_output_file)


if __name__ == '__main__':
    main()
