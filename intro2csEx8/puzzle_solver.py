##############################################################################
# FILE: puzzle_solver.py
# EXERCISE: Intro2cs2 ex8 2021-2022
##############################################################################
from typing import List, Tuple, Set, Optional
import time, copy

# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]

BLACK = 0
WHITE = 1
UNKNOW = -1
LEFT = "l"
RIGHT = "r"
DOWN = "d"
UP = "u"
DIRECTIONS = {"r": (0, 1), "l": (0, -1), "u": (-1, 0), "d": (1, 0)}


def get_next_indexes(picture: Picture, direction: str,
                     current_index: Tuple) -> Tuple:
    """function that receive the next indexes from current cell and direction
    If the function returns (-1, -1) the index is out of range"""
    row_index = current_index[0]
    column_index = current_index[1]

    next_row_index = row_index + DIRECTIONS[direction][0]
    if next_row_index >= len(picture) or next_row_index < 0:
        return (-1, -1)
    next_column_index = column_index + DIRECTIONS[direction][1]
    if next_column_index >= len(picture[0]) or next_column_index < 0:
        return (-1, -1)
    return (next_row_index, next_column_index)


def get_number_of_optional_write_cell_from_direction(picture: Picture,
                                                     direction: str,
                                                     current_index: Tuple,
                                                     unknown: bool = None) -> \
        int:
    """The function returns the number of cells that can show for a specific
    direction"""
    count = 0
    next_index = get_next_indexes(picture, direction, current_index)
    while next_index != (-1, -1):
        row_index = next_index[0]
        column_index = next_index[1]
        value_of_cell = picture[row_index][column_index]
        if value_of_cell == WHITE:
            count += 1
        elif value_of_cell == UNKNOW and unknown == False:
            count += 1
        else:
            break
        current_index = next_index
        next_index = get_next_indexes(picture, direction, current_index)
    return count


def max_min_exactly_number_seen_cells(type_of_check: str, picture: Picture,
                                      row: int, col: int) -> int:
    """A comprehensive function that checks even if the maximum, minimum and 
    exact number of cells are "visible"""

    if type_of_check == "min":
        type_of_check = True
    elif type_of_check == "max":
        type_of_check = False
    else:  # type of check == exactly
        type_of_check = None
    count = 0
    value_of_cell = picture[row][col]
    if value_of_cell == BLACK:  # if type is max
        return count
    if value_of_cell == UNKNOW and type_of_check != False:  # if type is min
        return count
    else:
        count += 1
    for direction in DIRECTIONS:
        count += get_number_of_optional_write_cell_from_direction(picture,
                                                                  direction,
                                                                  (row, col),
                                                                  type_of_check)
    return count


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """A function that receives a partial image and a position on it, and
    returns the number of "visible" cells From the cell at this location if all
    the unknown cells are considered as whites. Reminder: A cell can "show"
    another cell, if and only If both are white and are in the same row or
    column when there is no black cell between them."""
    return max_min_exactly_number_seen_cells("max", picture, row, col)


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """A function that receives a partial image and a position on it, and
    returns the number of "visible" cells From the cell at this position if all
    the unknown cells are considered black."""
    return max_min_exactly_number_seen_cells("min", picture, row, col)


def check_constraints(picture: Picture,
                      constraints_set: Set[Constraint]) -> int:
    """A function that receives a partial image and a set of constraints, and
    returns an integer between 0 and 2 that indicates success Satisfying the
    constraints in the partial picture."""
    not_exactly = False
    for constraint in constraints_set:
        row = constraint[0]
        col = constraint[1]
        right_value = constraint[2]
        min_value = min_seen_cells(picture, row, col)
        max_value = max_seen_cells(picture, row, col)
        value_of_seen = max_min_exactly_number_seen_cells("exactly", picture,
                                                          row, col)
        if right_value > max_value or right_value < min_value:
            return 0
        if max_value != min_value or max_value != value_of_seen \
                or min_value != value_of_seen:
            not_exactly = True
    if not_exactly:
        return 2
    for row in picture:
        for col in row:
            if col == -1:
                return 2
    return 1


def deepcopy_list(list_of_list: List[List[int]]) -> List[List[int]]:
    """to do a 2D list copy (not really deep copy)"""
    new_list = []
    for lis in list_of_list:
        new_list.append(lis[:])
    return new_list


def add_constraints_to_picture(pic: Picture,
                               constraints_set: Set[Constraint]) -> Picture:
    """add the constraints to picture (only 1\0 in the right place)"""
    for constraint in constraints_set:
        row = constraint[0]
        column = constraint[1]
        val = constraint[2]
        if val == 0:
            pic[row][column] = 0
        else:
            pic[row][column] = 1
    return pic


def solve_puzzle_helper(constraints_set: Set[Constraint], n: int, m: int,
                        picture: Picture, set_of_not_allow: set,
                        ans: List[Picture] = None) -> \
        Optional[Picture]:
    """Comprehensive utility function for solve_puzzle that receives a set of
    constraints and values of rows and columns, a blank image, a set of values
    that already existed and the answer, and returns an image describing one
    solution of the board, if any"""

    if not str(picture) in set_of_not_allow and ans == None:

        pic_for_w = deepcopy_list(picture)
        if check_constraints(picture, constraints_set) == 1:
            set_of_not_allow.add(str(picture))
            return picture
        elif check_constraints(picture, constraints_set) == 0:
            set_of_not_allow.add(str(picture))
        else:
            if m >= len(picture[0]):
                m = 0
                n += 1
            if n >= len(picture):
                return None
            if picture[n][m] == -1:
                picture[n][m] = BLACK
                pic_for_w[n][m] = WHITE
            m += 1

            x = solve_puzzle_helper(constraints_set, n, m, picture,
                                    set_of_not_allow,
                                    ans)
            if x == None:
                y = solve_puzzle_helper(constraints_set, n, m, pic_for_w,
                                        set_of_not_allow,
                                        ans)
            if x != None:
                return x
            if y != None:
                return y
        if ans != None:
            return ans


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> \
        Optional[Picture]:
    """A function that accepts a set of constraints and a table size
    (number of rows and number of columns (representing a table)Plays, and
    returns an image depicting one solution of the board, if any"""
    pic = [[-1] * m for x in range(n)]
    picture = add_constraints_to_picture(pic, constraints_set)
    return solve_puzzle_helper(constraints_set, 0, 0, picture, set())


def picture_to_str(picture):
    """print picture function"""
    s = " " * 2
    b = "\033[40m" + s
    w = "\033[47m" + s
    return "\n".join(
        ["".join([b if c == BLACK else w for c in row] + ["\033[49m"]) for row
         in picture])


def print_picture(picture):
    """print picture function"""
    print(picture_to_str(picture), end="\033[0m\n")
    print(" ")


def how_many_solutions_helper2(constraints_set: Set[Constraint], n: int,
                               m: int,
                               picture: Picture, count: int = 0) -> int:
    """"A function that accepts a set of constraints and a table size
    (number of rows and number of columns (representing a table)Plays, and
    returns an image depicting one solution of the board, if any"""
    pic_for_w = deepcopy_list(picture)
    if check_constraints(picture, constraints_set) == 1:
        return 1
    elif check_constraints(picture, constraints_set) == 0:
        return 0
    else:
        if m >= len(picture[0]):
            m = 0
            n += 1
        if n >= len(picture):
            return 0
        if picture[n][m] == -1:
            picture[n][m] = BLACK
            pic_for_w[n][m] = WHITE
            m += 1
            x = how_many_solutions_helper2(constraints_set, n, m, picture,
                                           count)
            y = how_many_solutions_helper2(constraints_set, n, m, pic_for_w,
                                           count)
            return y + x


def how_many_solutions(constraints_set: Set[Constraint], n: int,
                       m: int) -> int:
    """A function that accepts a set of constraints and a table size
    (number of rows and number of columns (representing a table)Plays, and
    returns an image depicting one solution of the board, if any"""
    pic = [[-1] * m for x in range(n)]
    return how_many_solutions_helper2(constraints_set, 0, 0, pic, 0)


def from_picture_to_constraints_set(picture: Picture) -> Set[Constraint]:
    """from picture return full constraints as a set of tuple"""
    set_of_constraints = set()
    for index_row, row in enumerate(picture):
        for index_column, column in enumerate(row):
            value_of_seen = max_min_exactly_number_seen_cells("exactly",
                                                              picture,
                                                              index_row,
                                                              index_column)
            set_of_constraints.add((index_row, index_column, value_of_seen))
    return set_of_constraints


def gen_puzzle_helper(set_of_constraints: Set[Constraint], n: int, m: int) -> \
        Set[Constraint]:
    """There may be a situation used in Generate Puzzle that I initially add
    constraint, but later in the other constraints may be enough. This is a
    function that makes sure to find the necessary minimum solution"""
    list_of_constraints = list(set_of_constraints)
    for i in range(len(list_of_constraints)):
        new_list = copy.deepcopy(list_of_constraints)
        new_list.remove(new_list[i])
        if how_many_solutions(set(new_list), n, m) == 1:
            return gen_puzzle_helper(new_list, n, m)
    return set(list_of_constraints)


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    """Given a photo we will look for a game board that a pictureThis is his
    only solution. We will want to find a "economical" game board - in the
    sense that all the numbers listed on top of it are needed.That is, removing
    a number from the board the condition that the image describes a single
    solution for the board"""
    n = len(picture)
    m = len(picture[0])
    set_of_constraints = from_picture_to_constraints_set(picture)
    partial_set_of_constraints = set()
    partial_set_of_constraints.add(set_of_constraints.pop())
    while how_many_solutions(partial_set_of_constraints, n, m) > 1:
        partial_set_of_constraints.add(set_of_constraints.pop())
        if len(set_of_constraints) == 0 and how_many_solutions(
                partial_set_of_constraints, n, m) != 1:
            return None
    return gen_puzzle_helper(partial_set_of_constraints, n, m)


if __name__ == '__main__':
    pass
