import pytest
from ex7 import *
from ex7_helper import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def mult_test():
    assert mult(3,4) == 12
    assert mult(1,0) == 0
    assert mult(5, 5) == 25
    assert mult(1, 5) == 5
def log_mult_test():
    assert log_mult(3, 4) == 12
    assert log_mult(1, 0) == 0
    assert log_mult(5, 5) == 25
    assert log_mult(1, 5) == 5
def is_even_test():
    assert is_even(10) == True
    assert is_even(0) == True
    assert is_even(1) == False
    assert is_even(13) == False

def is_power_test():
    assert is_power(2,128) == True
    assert is_power(4, 128) == False
    assert is_power(2, 8) == True

def reverse_helper_test():
    assert reverse("intro")  == reverse("intro")
    assert reverse("hello world") == reverse("hello world")
    assert reverse("abba") == reverse("abba")
    assert reverse("") == reverse("")
    assert reverse(" ") == reverse(" ")
    assert reverse("a") == reverse("a")

def number_of_ones_test():
    assert number_of_one(1) == 1 #helper function only for me
    assert number_of_one(0) == 0 #helper function only for me
    assert number_of_one(11) == 2 #helper function only for me
    assert number_of_one(10) == 1 #helper function only for me
    assert number_of_one(121212) == 3
    assert number_of_ones(13) == 6
    assert number_of_ones(21) == 13


def compare_lists_test(): #helper function only for me
    assert compare_lists([1, 2, 3, 4, 5], [1, 2, 3, 4]) == False
    assert compare_lists([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == True
    assert compare_lists([1, 2, 3, 4, 5], [1, 2, 33, 4, 5]) == False
    assert compare_lists([1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]) == False
    assert compare_lists([], []) == True
    assert compare_lists([1], [1]) == True

def compare_2d_lists_test():
    assert compare_2d_lists([[1, 2], [3, 4]], [[1, 2], [3, 4]]) == True
    assert compare_2d_lists([[1, 2], [3, 4], [3, 4]], [[1, 2], [3, 4]]) == False
    assert compare_2d_lists([[1, 2], [3, 4]], [[1, 2], [3, 4], [3, 4]]) == False
    assert compare_2d_lists([[1, 2], [1, 4]], [[1, 2], [3, 4]]) == False
    assert compare_2d_lists([[1, 1], [3, 4]], [[1, 2], [3, 4]]) == False
    assert compare_2d_lists([[1, 2, 3], [3, 4]], [[1, 2], [3, 4]]) == False
    assert compare_2d_lists([[1, 2], [3, 4]], [[1, 2], [3, 4, 5]]) == False
    assert compare_2d_lists([[]],[[]]) == True
    assert compare_2d_lists([[],[1]], [[],[1]]) == True
    assert compare_2d_lists([],[]) == True


def tests():
    mult_test()
    reverse_helper_test()
    log_mult_test()
    is_even_test()
    number_of_ones_test()
    compare_2d_lists_test()
    is_power_test()

tests()