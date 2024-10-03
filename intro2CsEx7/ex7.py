##############################################################################
# FILE: ex7.py
# EXERCISE: Intro2cs2 ex7 2021-2022
##############################################################################
from typing import *
from ex7_helper import *


def mult(x: float, y: int) -> float:
    """A function that receives a number x (float) and a number y that is
     a non-negative integer (int,) and returns the result"""
    if y <= 0:
        return 0
    return add(mult(x, subtract_1(y)), x)


def is_even(n: int) -> bool:
    """function that accepts the integer n (int) is non-negative, and returns
     True if n Is an even number, and False another"""
    if n == 1:
        return False
    if n == 0:
        return True
    return is_even(subtract_1(subtract_1(n)))


def log_mult(x: float, y: int) -> float:
    """function that works similar to the mult function from section 1, but
     this time the implementation
     Its must be while logarithmic running"""
    if y == 0:
        return 0
    val = log_mult(x, divide_by_2(y))
    if is_odd(y):
        return add(add(val, val), x)
    else:
        return add(val, val)


def helper_is_power(b: int, x: int, n: int = 1) -> bool:
    """An auxiliary function that strongly raises the base each time in a
    larger number (1,2 ...) and thus the function tests whether it is
    possible for b to be a base for x"""
    if n == 1:
        val_mult = int(log_mult(b, b))
    else:
        val_mult = int(log_mult(n, b))
    if val_mult == x:
        return True
    if val_mult > x:
        return False
    return helper_is_power(b, x, val_mult)


def is_power(b: int, x: int) -> bool:
    """Function which receives two non-negative integers (int) b and x,
       and checks Is there a non-negative integer n such that b to the
       power of n is equal to x, otherwise False."""
    return helper_is_power(b, x)



def helper_reverse(s: str, index: int, new_s: str = "") -> str:
    """reverse function, which receives a string of characters (str) s, and
    returns the string containing the Same characters as s, but in reverse
     order"""
    if index < 0:
        return new_s
    return helper_reverse(s, index - 1, append_to_end(new_s, s[index]))


def reverse(s: str) -> str:
    """reverse function, which receives a string of characters (str) s, and
    returns the string containing the Same characters as s, but in reverse
     order"""
    return helper_reverse(s, len(s) - 1)


def play_hanoi(Hanoi: Any, n: int, src: Any, dst: Any, temp: Any) -> Any:
    """to implement the tower of hanoi game ad recursive function"""
    # get help from "https://en.wikipedia.org/wiki/Tower_of_Hanoi"
    # get help from https://www.youtube.com/watch?v=jWqu9Ot9j-Q
    # and: https://www.youtube.com/watch?v=rf6uf3jNjbo
    if n > 0:
        play_hanoi(Hanoi, n - 1, src, temp, dst)
        Hanoi.move(src, dst)
        play_hanoi(Hanoi, n - 1, temp, dst, src)


def number_of_one(n: int) -> int:
    """check the number of "1" in number"""
    if n < 10:
        if n == 1:
            return 1
        return 0
    digit = n % 10
    n = n // 10
    if digit == 1:
        return number_of_one(n) + 1
    else:
        return number_of_one(n)


def number_of_ones(n: int) -> int:
    """Receives a natural number (int) n, and returns the number The times the
     digit '1' appears in all numbers from 1 to n (including (including
      duplicates of the digit '1' in the same The number."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return number_of_one(n) + number_of_ones(n - 1)


def compare_lists_helper(l1: List[int], l2: List[int], index: int = 0) -> bool:
    """compare 1D list with recursion with the index"""
    if len(l1) != len(l2):
        return False
    if len(l1) == 0 and len(l1) == 0:
        return True
    if l1[index] != l2[index]:
        return False
    if len(l1) - 1 == index:
        return True
    return compare_lists_helper(l1, l2, index + 1)


def compare_lists(l1: List[int], l2: List[int]) -> bool:
    """compare 1D list with recursion"""
    return compare_lists_helper(l1, l2)


def compare_2d_lists_helper(l1: List[List[int]], l2: List[List[int]]
                            , index: int = 0) -> bool:
    """The lists_2d_compare function that receives two two-dimensional lists of
    numbers (each One of them is represented by a list of number lists). The
    function will return True if the two listsIdentical dimensions in all their
    values, and False if there is at least one limb in which they differ"""
    if len(l1) != len(l2):
        return False
    if len(l1) == 0 and len(l1) == 0:
        return True
    if not compare_lists(l1[index], l2[index]):
        return False
    if len(l1) - 1 == index:
        return True
    return compare_2d_lists_helper(l1, l2, index + 1)


def compare_2d_lists(l1: List[List[int]], l2: List[List[int]]) -> bool:
    """The lists_2d_compare function that receives two two-dimensional lists of
    numbers (each One of them is represented by a list of number lists). The
    function will return True if the two listsIdentical dimensions in all their
    values, and False if there is at least one limb in which they differ"""
    return compare_2d_lists_helper(l1, l2)


def magic_list_helper(n: int, magic: List[Any]) -> List[Any]:
    """to implement magic list from the rules of the TA"""
    if n == 0:
        return []
    current_list = magic_list_helper(n - 1, magic)
    length_of_list = len(current_list)
    new_list = magic_list_helper(length_of_list, [])
    magic.append(new_list)
    return magic


def magic_list(n: int) -> List[Any]:
    """to implement magic list from the rules of the TA"""
    return magic_list_helper(n, [])
