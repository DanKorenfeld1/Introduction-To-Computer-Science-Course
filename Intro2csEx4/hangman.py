#############################################################################
# FILE: hangman.py
# EXERCISE: ex4 build the hangman game
# DESCRIPTION:
#############################################################################
from hangman_helper import *

PATH_WORDS = "words.txt"
DEBUG_TEST_MESSAGE = "the word: {}   list of guess: {}  pattern guess: {}"
ERROR_MESSAGE_THE_INPUT_INVALID = "XXXX  the input is Invalid XXXX"
THE_CHOICE_GUESSED_ALREADY = "<> the choice already guessed <>"
MESSAGE_THE_HINT_NOT_FINISH = "->> the option to get a hint isn't work now <<-"
HANGMAN_STARTER = """
██   ██   █████   ███    ██   ██████   ███    ███   █████   ███    ██ 
██   ██  ██   ██  ████   ██  ██        ████  ████  ██   ██  ████   ██ 
███████  ███████  ██ ██  ██  ██   ███  ██ ████ ██  ███████  ██ ██  ██ 
██   ██  ██   ██  ██  ██ ██  ██    ██  ██  ██  ██  ██   ██  ██  ██ ██ 
██   ██  ██   ██  ██   ████   ██████   ██      ██  ██   ██  ██   ████                                
                  """


def update_word_pattern(word, pattern, letter):
    """
    function that update the pattern of the word
    :param word: the word that the software chose
    :param pattern: the current pattern of the word in the game
    :param letter: the current guess letter
    :return: the new pattern of the word
    """
    list_of_word = list(word)
    list_of_pattern = list(pattern)
    if letter in word:
        for i in range(len(list_of_word)):
            if list_of_word[i] == letter:
                list_of_pattern[i] = letter
    return "".join(list_of_pattern)


def check_if_the_word_guess_correct(the_word, pattern_guess, the_guess):
    """
    check if the player guess correct all the word
    :param the_word: (string) the hide word
    :param pattern_guess: (string) the current pattern
    :param the_guess: (string) the word that the player guess
    :return: a tuple of 2 values:
             if the player guess correct, return (True, number filling letter)
             if the player guess wrong return (False, 0)
    """
    if the_word == the_guess:  # correct
        return True, pattern_guess.count("_")
    else:
        return False, 0


def word_is_fit(word, pattern, wrong_guess_list):
    """
    check if the word fit to be the answer to the pattern
    :param word: the option answer
    :param pattern: the current pattern
    :return: boolean
    """
    if len(word) != len(pattern):  # not equal length -> not fit
        return False
    wrong_guess_list = set(wrong_guess_list)
    for i in range(len(word)):
        if word[i] in wrong_guess_list:  # not fit word
            return False
        if word[i] in pattern:  # the char in founded
            if not (word.count(word[i]) == pattern.count(word[i])):
                return False
        if pattern[i] != "_":
            if pattern[i] != word[i]:
                return False

    return True


def filter_words_list(words, pattern, wrong_guess_lst):
    """"""
    new_list = []
    for word in words:
        if word_is_fit(word, pattern, wrong_guess_lst):
            new_list.append(word)
    return new_list


def run_single_game(words_list, score):
    """
    run a single game
    :param words_list: list of the option words (list[string])
    :param score: the current score (int)
    :return: score (int) the score of the player
    """
    print(HANGMAN_STARTER)
    the_word = get_random_word(words_list)
    wrong_guess_lst = []
    list_of_past_guess = []
    message = "start the game"
    pattern_guess = "_" * len(the_word)
    while pattern_guess.count("_") > 0 and score > 0:
        display_state(pattern_guess, wrong_guess_lst, score, message)
        message = ""  # in the instruction don't write about wrong \ good guess
        code_of_input, the_guess = get_input()  # code_of_input: the code
        # (LETTER=1, WORD=2, HINT=3)(int)
        # the guess of player(str\None)

        if code_of_input == 1:  # the player want to guess a letter

            # invalid input
            if not ((the_guess.islower()) and len(the_guess) == 1):
                message = ERROR_MESSAGE_THE_INPUT_INVALID
            elif the_guess in list_of_past_guess:
                # if the player tried this letter
                message = THE_CHOICE_GUESSED_ALREADY

            else:  # the input valid
                score -= 1
                new_pattern_guess = update_word_pattern(the_word,
                                                        pattern_guess,
                                                        the_guess)
                list_of_past_guess.append(the_guess)  # update list-past- guess
                if new_pattern_guess != pattern_guess:  # the guess was correct
                    n = new_pattern_guess.count(the_guess)
                    # the number of the letter in the new patter
                    score += (n * (n + 1)) // 2
                    pattern_guess = new_pattern_guess  # update the new pattern
                else:  # wrong try-> the letter isn't in the word
                    if the_guess not in wrong_guess_lst:
                        wrong_guess_lst.append(the_guess)
        elif code_of_input == 2:
            score -= 1
            # function that check if the player guess the word
            is_succeeded, number_of_good_try = check_if_the_word_guess_correct(
                the_word, pattern_guess,
                the_guess)
            if is_succeeded:  # the player succeeded to guess the word
                number = number_of_good_try
                score += (number * (number + 1)) // 2  # new-score
                for i in the_guess:
                    pattern_guess = update_word_pattern(the_word,
                                                        pattern_guess, i)
        else:  # the code_of_input = 3 (the player want hint)
            score -= 1
            list_of_all_hint = filter_words_list(words_list, pattern_guess,
                                                 wrong_guess_lst)
            if len(list_of_all_hint) > HINT_LENGTH:
                list_hint = [list_of_all_hint[0]]
                count = 1
                for i in range(1, HINT_LENGTH):
                    if count < HINT_LENGTH:
                        list_hint.append(list_of_all_hint[(count
                                                           * len(list_of_all_hint)) //
                                                          HINT_LENGTH])
                        count += 1
                show_suggestions(list_hint)
            else:
                list_hint = list_of_all_hint
                show_suggestions(list_hint)

    if score > 0:  # win
        win_state = "you win!! the word was: ->> {} <<-".format(the_word)
        display_state(pattern_guess, wrong_guess_lst, score, win_state)
    else:
        lose_state = "you loose the word was ->> {} <<-".format(the_word)
        display_state(pattern_guess, wrong_guess_lst, score, lose_state)

    return score


def main():
    """
    the main funtion of the game
    :return: None
    """
    num_game = 1
    list_word = load_words()
    score = POINTS_INITIAL
    while True:
        score = run_single_game(list_word, score)
        if score > 0:
            message = "you have {} points, and you played {} games.".format(
                score,
                num_game)
            message += " do you want to play again?"
            is_want_play_again = play_again(message)
            if is_want_play_again:
                num_game += 1
            else:  # don't want another play
                break
        else:
            message = "you have {} points, and you played {} games.".format(
                score,
                num_game)
            message += " do you want to play a new round game?"
            is_want_play_again = play_again(message)
            score = POINTS_INITIAL
            num_game = 1


if __name__ == '__main__':
    main()
