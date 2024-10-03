import pytest
from cartoonify import *
from termcolor import colored


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

def test_apply_kernel():
    old = [[10, 20, 30, 40, 50],
           [8, 16, 24, 32, 40],
           [6, 12, 18, 24, 30],
           [4, 8, 12, 16, 20]]
    new = [[12, 20, 26, 34, 44],
           [11, 17, 22, 27,34],
           [10, 16, 20, 24, 29],
           [7, 11, 16, 18, 21]]
    assert apply_kernel(old,blur_kernel(5)) == new
    assert apply_kernel([[0,128,255]],blur_kernel(3)) == [[14,128,241]]
def test_get_edges():
    assert get_edges([[200,50,200]],3,3,10) == [[255,0,255]]

def test_quantize():
    example6 = [[0, 50, 100], [150, 200, 250]]
    ans1 = [[0, 36, 109], [146, 219, 255]]
    example7 = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
    example8 = [[[250, 250, 250], [0, 0, 0]], [[250, 250, 100], [1, 11, 13]]]
    ans2 = [[[250, 250, 250], [2, 2, 3]], [[250, 250, 100], [6, 11, 12]]]
    assert quantize(example6,8) == ans1
    assert add_mask(example7, example8, [[0, 0.5]] * 2) == ans2

def test_add_mask():

    assert add_mask([[50,50,50]],[[200,200,200]],[[0,0.5,1]]) == [[200, 125, 50]]


def tests():
    test_apply_kernel()
    test_get_edges()
    test_quantize()




if __name__ == '__main__':
    tests()



def examples():
    picture_list = load_image("ziggy.png")
    girl_picture_list = load_image("girl.png")
    heart = load_image("img.png")
    example = [[10, 20, 30, 40, 50],
               [8, 16, 24, 32, 40],
               [6, 12, 18, 24, 30],
               [4, 8, 12, 16, 20]]

    #
    example2 = [[10, 20, 30, 40],
                [8, 16, 24, 32],
                [6, 12, 18, 24],
                [4, 8, 12, 16]]
    examplee = combine_channels([example[:], example[:], example[:]])
    example3 = [[0, 64],
                [128, 255]]
    example4 = [[1, 2, 3], [4, 5, 6]]
    example5 = [[[1, 2, 3], [4, 5, 6]],
                [[0, 5, 9], [255, 200, 7]]]
    example6 = [[0, 50, 100], [150, 200, 250]]

    example7 = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
    example8 = [[[250, 250, 250], [0, 0, 0]], [[250, 250, 100], [1, 11, 13]]]




