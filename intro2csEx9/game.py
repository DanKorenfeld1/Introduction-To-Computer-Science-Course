##############################################################################
# FILE: game.py
# EXERCISE: Intro2cs2 ex9 2021-2022
# DESCRIPTION:
##############################################################################
import helper, sys
from board import *
from car import *


class Game:
    """
    the Game Class- there are the rules and actions that need to be done in
    the game itself
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        #You may assume board follows the API
        # implement your code here (and then delete the next line - 'pass')
        self.board = board

    def the_player_win(self):
        """
        check if the player win of not
        :return: boolean TRUE if the player win FALSE otherwise
        """
        if self.board.cell_content(self.board.target_location()) != None:
            return True
        return False




    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        print(self.board)
        ok = None
        if self.the_player_win():
            print("you win!")
            ok = True # the player win #remember- it's allow to return in this function??
        else:
            user_in = input("Input the color and the direction that you want to move for "
                            "example: Y,r {to exit write: '!'}")
            if user_in == "!":
                ok = False
            # I did not check with the "split" function because the input could
            # have been significantly incorrect and I did not want to cause the
            # program to crash
            elif user_in[0] not in "YBRGOW" or user_in[1] != "," or user_in[2] not in "rlud":
                print("Invalid input")
            else:
                name_car = user_in[0]
                move_key = user_in[-1]
                self.board.move_car(name_car,move_key)
                print(self.board)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        ok = True
        while not self.the_player_win() and ok:
            output = self.__single_turn()
            if output != None:
                ok = False

def add_cars_from_json(path_json):
    """
    function that create new board and add all the car from the JSON file
    :param path_json: the path of the JSON file
    :return: board (Board class) after add the car
    """
    dictionary_of_car = helper.load_json(path_json)
    board = Board()
    # add cars to the board:
    for car in dictionary_of_car:

        name_car = car
        # check if name_car valid
        if type(name_car) != str or len(
                name_car) != 1 or name_car not in "YBRGOW":
            continue

        length_car = dictionary_of_car[car][0]
        # check if length_car valid
        if type(length_car) != int or length_car > 4 or length_car < 2:
            continue

        location_car = dictionary_of_car[car][1]
        # check if location_car valid
        if type(location_car) != list or len(location_car) != 2:
            continue
        elif not board.check_cell_in_the_range(location_car[0],
                                               location_car[1]):
            continue

        orientation_car = dictionary_of_car[car][2]
        if type(orientation_car) != int and (
                orientation_car != 1 or orientation_car != 0):
            continue
        new_car = Car(str(name_car), int(length_car), tuple(location_car),
                      int(orientation_car))
        board.add_car(new_car)
    return board

if __name__== "__main__":
    #Your code here
    #All access to files, non API constructors, and such must be in this
    #section, or in functions called from this section.
    # path_json = sys.argv[1]
    path_json = "car_config.json"
    board = add_cars_from_json(path_json)
    game = Game(board)

    if game.the_player_win():
        print("the player win!")
    else:

        game.play()

