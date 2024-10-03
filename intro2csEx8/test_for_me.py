from puzzle_solver import *
LEFT = "l"
RIGHT = "r"
DOWN = "d"
UP = "u"


def test_next_index():
    example = [[0, -1, -1, 3],
               [-1, -1, 5, -1],
               [1, -1, -1, -1]]
    assert get_next_indexes(example, UP, (1, 1)) == (0, 1)
    assert get_next_indexes(example, DOWN, (1, 1)) == (2, 1)
    assert get_next_indexes(example, RIGHT, (1, 1)) == (1, 2)
    assert get_next_indexes(example, LEFT, (1, 1)) == (1, 0)
    assert get_next_indexes(example, RIGHT, (2, 3)) == (-1, -1)
    assert get_next_indexes(example, UP, (0, 0)) == (-1, -1)
def test_max_seen_index():
    example_2 = [[-1, 0, 1, -1],
                 [0, 1, -1, 1],
                 [1, 0, 1, 0]]
    example_3 = [[-1, 0, 1, 1],
                 [0, 1, -1, 1],
                 [1, 0, 1, -1]]
    assert max_seen_cells(example_2, 0, 0) == 1
    assert max_seen_cells(example_2, 1, 0) == 0
    assert max_seen_cells(example_2, 1, 2) == 5
    assert max_seen_cells(example_2, 1, 1) == 3
    assert max_seen_cells(example_3, 0, 3) == 4

def test_min_seen_index():
    example_2 = [[-1, 0, 1, -1],
                 [0, 1, -1, 1],
                 [1, 0, 1, 0]]
    example_3 = [[-1, 0, 1, 1],
                 [0, 1, -1, 1],
                 [1, 0, 1, -1]]
    assert min_seen_cells(example_2, 0, 0) == 0
    assert min_seen_cells(example_2, 1, 0) == 0
    assert min_seen_cells(example_2, 1, 2) == 0
    assert min_seen_cells(example_3, 0, 3) == 3

def test_check_constraints():
    picture1 = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]
    picture2 = [[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
    picture3 = [[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, -1]]
    assert check_constraints(picture1, {(0, 3, 5), (1, 2, 5), (2, 0, 1)}) == 0
    assert check_constraints(picture2, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 1
    assert check_constraints(picture1, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 2
    assert check_constraints(picture3, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 2



def test_solve_puzzle():
    assert solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 0)}, 3, 4) == [
        [0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
    assert solve_puzzle(
        {(0, 3, 3), (1, 2, 5), (2, 0, 1), (2, 3, 5)}, 3, 4) == None
    assert solve_puzzle({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3) in [
        [[0, 0, 1], [1, 1, 1], [1, 1, 1]], [[1, 0, 1], [1, 1, 1], [1, 1, 1]]]

def test_how_many_solutions():
    assert how_many_solutions(
        {(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 0)}, 3, 4) == 1
    assert how_many_solutions(
        {(0, 3, 3), (1, 2, 5), (2, 0, 1), (2, 3, 5)}, 3, 4) == 0
    assert how_many_solutions({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3) == 2
    assert how_many_solutions(
        {(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 1)}, 3, 4) == 1
    assert how_many_solutions({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3) == 2
    assert how_many_solutions({(i, j, 0) for i in range(3)
                              for j in range(3)}, 3, 3) == 1
    assert how_many_solutions(set(), 2, 2) == 16
    assert how_many_solutions({(0, 3, 3), (2, 0, 1)}, 3, 4) == 64

if __name__ == '__main__':
    test_next_index()
    test_max_seen_index()
    test_min_seen_index()
    test_check_constraints()
    test_solve_puzzle()
    test_how_many_solutions()