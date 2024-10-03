##############################################################################
# FILE: car.py
# EXERCISE: Intro2cs2 ex9 2021-2022
# DESCRIPTION:
##############################################################################
class Car:
    """
    Class car- one dimension in the board of the game
    """
    DIRECTIONS = {"r": (0, 1), "l": (0, -1), "u": (-1, 0), "d": (1, 0)}

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        self.name = str(name)
        self.length = int(length)
        self.location = tuple(location)
        self.orientation = int(orientation) #0 for vertical (|) and 1 for Horizontal (-)


    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        list_of_coordinates = []
        if self.orientation == 0: # vertical (|) down\up
            for i in range(self.length):
                list_of_coordinates.append((self.location[0]+i,self.location[1]))
            return list_of_coordinates
        else:
            for i in range(self.length):
                list_of_coordinates.append(
                    (self.location[0], self.location[1] + i))
            return list_of_coordinates
    def set_car_location(self, new_location):
        """
        set car location
        :return: None
        """
        self.location = new_location

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        #For this car type, keys are from 'udrl'
        #The keys for vertical cars are 'u' and 'd'.
        #The keys for horizontal cars are 'l' and 'r'.
        #You may choose appropriate strings.
        # implement your code and erase the "pass"
        #The dictionary returned should look something like this:
        #result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        #A car returning this dictionary supports the commands 'f','d','a'.
        result = {'u':"Driving up! The sky's the limit",
                  'd':"Driving down! Do not forget to take plenty of air",
                  'r':"Driving right! we have a right of way",
                  'l':"Driving left! give right ahead"}
        if self.orientation == 0: # vertical
            result.pop("r")
            result.pop("l")
            return result
        result.pop("u")
        result.pop("d")
        return result

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
         move to be legal.
        """
        #For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        #be empty in order to move down (with a key 'd').
        if self.orientation == 0:
            max_height = self.location[0]
            min_height = self.location[0] + self.length-1
            if movekey == "u":
                return [(max_height-1, self.location[1])]
            if movekey == "d":
                return [(min_height+1, self.location[1])]
            return []
        min_width = self.location[1]
        max_width = self.location[1] + self.length-1
        if movekey == "r":
            return [(self.location[0], max_width + 1)]
        if movekey == "l":
            return [(self.location[0], min_width - 1)]
        return []



    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        location = list(self.location)
        if self.orientation == 0: # vertical
            if movekey == "u":
                location[0] -= 1
                self.location = tuple(location)
                return True
            if movekey == "d":
                location[0] += 1
                self.location = tuple(location)
                return True
            return False
        else: # horizontal
            if movekey == "l":
                location[1] -= 1
                self.location = tuple(location)
                return True
            if movekey == "r":
                location[1] += 1
                self.location = tuple(location)
                return True
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name

if __name__ == '__main__':
    pass