##############################################################################
# FILE: board.py
# EXERCISE: Intro2cs2 ex9 2021-2022
# DESCRIPTION:
##############################################################################
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
COLOR = {"Y":bcolors.WARNING+"Y"+bcolors.ENDC,
         "B":bcolors.OKBLUE+"B"+bcolors.ENDC,
         "R":bcolors.FAIL+"R"+bcolors.ENDC,
         "G":bcolors.OKGREEN+"G"+bcolors.ENDC,
         "O":bcolors.WARNING+bcolors.BOLD+"O"+bcolors.ENDC,
         "W":bcolors.BOLD+"W"+bcolors.ENDC}
##############################################################################

class Board:
    """
    Board class-
    Responsible for the board in the game, its use is made by the fact that he
    "knows" the class of cars but he does not know the rules of the game
    (game class).
    """
    LEFT = "l"
    RIGHT = "r"
    DOWN = "d"
    UP = "u"
    VERTICAL = 0
    HORIZONTAL = 1
    DIRECTIONS = {"r": (0, 1), "l": (0, -1), "u": (-1, 0), "d": (1, 0)}
    dictionary_of_car = dict() # key: name value: the car object
    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.board = [["-"] * 7 for x in range(7)]
        self.board[3].append("E")

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        #The game may assume this function returns a reasonable representation
        #of the board for printing, but may not assume details about it.
        board = ""
        for row_index, row in enumerate(self.board):
            for column_index, column in enumerate(row):
                if column in COLOR.keys():
                    board += COLOR[column]
                else:
                    board += column
            board += "\n"
        return board

    # def __str__(self): #remember- real one function- the second with color
    #     """
    #     This function is called when a board object is to be printed.
    #     :return: A string of the current status of the board
    #     """
    #     #The game may assume this function returns a reasonable representation
    #     #of the board for printing, but may not assume details about it.
    #     board = ""
    #     for row in self.board:
    #         for column in row:
    #             board += column
    #         board += "\n"
    #     return board # remember-don't delete it

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        #In this board, returns a list containing the cells in the square
        #from (0,0) to (6,6) and the target cell (3,7)
        list_of_cells = []
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                list_of_cells.append((row_index,col_index))
        return list_of_cells
    def possible_move_one_car(self,name):
        """
        possible moves to specific car returns the legal moves of all cars in
        this board
        :param name: the name of the car
        :return: list of tuples of the form (name,movekey,description)
        """
        list_of_optional = []
        car_object = self.dictionary_of_car[name]
        for orientation in car_object.possible_moves():
            row,col = car_object.movement_requirements(orientation)[0]
            if self.check_cell_in_the_range(row,col):
                if self.board[row][col] in "-E":
                    list_of_optional.append((name, orientation,"you can move to {}".format(orientation)))
        return list_of_optional



    def possible_moves(self): #todo- the function
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        #From the provided example car_config.json file, the return value could be
        #[('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        list_of_optional = []
        for car in self.dictionary_of_car:
            list_of_optional.extend(self.possible_move_one_car(car))
        return list_of_optional

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return (3,7)

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row = coordinate[0]
        column = coordinate[1]
        value = self.board[row][column]
        if value not in "-E":
            return value
        return None
    def set_cell_value(self,coordinate, new_value):
        """
        update the value of specific cell
        :param coordinate: tuple of (row,col) of the coordinate to update
        :param new_value: the new value of the coordinate
        :return: None
        """
        row = coordinate[0]
        column = coordinate[1]
        self.board[row][column] = new_value






    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        #Remember to consider all the reasons adding a car can fail.
        #You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        ok = True
        coordinates = car.car_coordinates()
        for coordinate in coordinates:
            if ok:
                row = coordinate[0]
                col = coordinate[1]
                if coordinate == self.target_location():
                    pass
                elif 0 > row or row > 6:
                    return False
                elif 0 > col or col > 6:
                    return False
                elif self.cell_content(coordinate) != None and ok == True:
                    return False
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if self.cell_content((row_index, col_index)) == car.get_name():
                    return False
        for coordinate in coordinates:
            self.set_cell_value(coordinate, car.get_name())
        self.dictionary_of_car[car.get_name()] = car
        return ok

    def check_cell_in_the_range(self,row, column):
        """function that check if cell is out of the range of the board
        :return: True if the cell in the range otherwise False """
        if (row,column) == self.target_location():
            return True
        elif row >= 0 and row < 7:
            if column >=0 and column < 7:
                return True
        return False

    def from_direction_change_coordinate(self,movekey,coordinate):
        """change the coordinate from direction
        :return: tuple (row, column) new indexes"""
        row =self.DIRECTIONS[movekey][0]+coordinate[0]
        column = self.DIRECTIONS[movekey][1]+coordinate[1]
        return row, column


    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """

        ok = True
        if name not in self.dictionary_of_car.keys():

            return False
        else:
            car_object = self.dictionary_of_car[name]
            if movekey not in car_object.possible_moves():
                print("The direction is invalid")
                return False
            coordinate_of_car = car_object.car_coordinates()
            for coordinate in coordinate_of_car:
                row,column = self.from_direction_change_coordinate(movekey,coordinate)
                if self.check_cell_in_the_range(row, column):
                    if (row,column) == self.target_location():
                        pass
                    elif self.board[row][column] != "-" and self.board[row][column] != name:

                        return False
                else:

                    return False
            if ok:

                if movekey in "dr":
                    # the head coordinate
                    self.set_cell_value(coordinate_of_car[0], "-")
                    row, column = self.from_direction_change_coordinate(movekey,
                                                                    coordinate_of_car[-1])
                    # the update of the new end coordinate
                    self.set_cell_value((row, column),name)
                else:
                    self.set_cell_value(coordinate_of_car[-1], "-")
                    row, column = self.from_direction_change_coordinate(
                        movekey,
                        coordinate_of_car[0])
                    # the update of the new head coordinate
                    self.set_cell_value((row, column),name)
                car_object.move(movekey)


        return ok



if __name__ == '__main__':
    pass
