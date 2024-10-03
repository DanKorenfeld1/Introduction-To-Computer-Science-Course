##############################################################################
# FILE: user_interface.py
# WRITERS: Matan Kaminski
#          Dan Korenfeld
# EXERCISE: Intro2cs2 ex12 2021-2022
# DESCRIPTION: the GUI Class
##############################################################################
from tkinter import Tk, Label, Button, Listbox, END
import tkinter as tk
from logic import *
from board import *
from pygame import mixer

###############################################################################
#                               CONSTANTS
###############################################################################
BACKGROUND_COLOR = 'lightcyan'
BUTTON_COLOR = 'orange'
BUTTON_COLOR_FONT = 'white'
BUTTON_COLOR_PRESSED = 'saddlebrown'
HEIGHT = 900
WIDTH = 500


class VisualGame:

    def __init__(self):
        self.root = Tk()
        self.board = Board()
        self.game = GameLogic(self.board.get_board())
        self.all_the_buttons = dict()
        self.indexes_in_ui_to_board = dict()
        self.index_board_to_ui = dict()
        self.path = []
        self.clicked_button = []
        self.started = False
        self.game_time = 180

    ###########################################################################
    #                             CREATE & RUN GAME
    ###########################################################################

    def create_new_game(self ,end_game):
        """create new game method"""
        end_game.destroy()
        self.__init__()
        self.run_game()

    def run_game(self):
        """run game method"""
        self.create_window()
        self.root.mainloop()

    ###########################################################################
    #                             CREATE GUI
    ###########################################################################

    def create_window(self):
        """create window method that build all the GUI elements"""
        self.root.title("Boggle Game")
        self.root['background'] = BACKGROUND_COLOR
        self.root.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)


        label_title = Label(self.root, text="Boggle Game", bg=BACKGROUND_COLOR,
                            font=("Helvetica bold", 40))
        label_title.pack(side=tk.TOP)

        self.root.after(200, self.score_of_game)
        button_start = self.create_button_start()
        button_start.bind("<Button-1>",
                          lambda event: self.button_start_actions_start_game())
        list_box_of_found = Listbox(self.root, width=30, height=10)
        list_box_of_found.pack()
        list_box_of_found.place(y=700, x=200)
        list_box_of_found.insert(0, "list of found words")
        list_box_of_mistake = Listbox(self.root, width=30, height=10)
        list_box_of_mistake.pack()
        list_box_of_mistake.place(y=700, x=10)
        list_box_of_mistake.insert(0, "list of mistakes tries")

        enter_button = self.create_enter_button()
        enter_button.bind('<Button-1>',
                          lambda event: self.button_enter_actions(
                              list_box_of_found, list_box_of_mistake))

    def create_all_the_buttons(self):
        """build all the buttons of the game (16)"""
        row_for_button = 0
        for row in range(50, 450, 100):
            if row_for_button < len(self.board.get_board()):
                list_of_row = self.from_board_to_row(row_for_button)
                self.create_row_button(row, list_of_row, row_for_button)
            row_for_button += 1

    def create_button_start(self):
        """create the button 'start'"""
        button_start = Button(self.root, text="START", background=BUTTON_COLOR,
                              fg=BUTTON_COLOR_FONT, width=10,
                              height=3)
        button_start.pack()
        button_start.place(y=70, x=400)
        return button_start

    def create_enter_button(self):
        """create the button 'enter'"""
        button_enter = Button(self.root, text="ENTER", background=BUTTON_COLOR,
                              fg=BUTTON_COLOR_FONT, width=10, height=3)
        button_enter.pack()
        button_enter.place(y=750, x=400)
        return button_enter

    def create_row_button(self, row, list_of_char, y_index_in_board):
        """method that create one row of button game"""
        index = 0
        start = 220
        hope = (HEIGHT - 470) // 7
        for i in range(start, HEIGHT - 200, hope):
            if index % 2 == 0:
                self.create_one_button(i, row, list_of_char[index // 2],
                                       index // 2, y_index_in_board)
            index += 1

    def create_one_button(self, row, column, text, x_index_in_board,
                          y_index_in_board):
        """create one button from the 16 game button"""
        btn = Button(self.root, text=text, background=BUTTON_COLOR,
                     fg=BUTTON_COLOR_FONT, width=6,
                     height=3, font=("Helvetica bold", 18), anchor="n")

        if (row, column) not in self.all_the_buttons.keys():
            self.all_the_buttons[(row, column)] = btn
            self.indexes_in_ui_to_board[(row, column)] = \
                (y_index_in_board, x_index_in_board)
            self.index_board_to_ui[(y_index_in_board, x_index_in_board)] = \
                (row, column)

        btn.bind('<Button-1>',
                 lambda event: self.change_path(x_index_in_board,
                                                y_index_in_board))
        btn.pack()
        btn.place(y=row, x=column)

    ###########################################################################
    #                               LOGIC GUI
    ###########################################################################

    def change_path(self, row, col):
        """method that update the pressed buttons (change the color and add to
        the list of the path"""
        y, x = self.index_board_to_ui[(col, row)]
        button = self.all_the_buttons[(y, x)]

        if (row, col) not in self.path:
            if len(self.path) == 0:
                self.path.append((row, col))
                button['background'] = BUTTON_COLOR_PRESSED
                self.clicked_button.append(button)
            else:
                if 0 <= abs(self.path[-1][0] - row) <= 1 and \
                        0 <= abs(self.path[-1][1] - col) <= 1:
                    self.path.append((row, col))
                    button['background'] = BUTTON_COLOR_PRESSED
                    self.clicked_button.append(button)
        elif (row, col) == self.path[-1]:
            self.path.remove((row, col))
            button['background'] = BUTTON_COLOR

    def timer(self):
        """method that create the time of the game and countdown. In the end
        to the game, the method open window of game over and if the player
        want to play again"""
        if self.game_time == -1:
            self.open_game_over()
        else:
            minute, second = self.game_time // 60, self.game_time % 60
            if 0 <= second <= 9:
                second = '0' + str(second)

            if minute == 0 and 10 < int(second) <= 30:
                label_timer = Label(text="{}:{}".format(minute, second),
                                    font=("Helvetica bold", 40),
                                    fg="gold", bg=BACKGROUND_COLOR)
            elif minute == 0 and -1 <= int(second) <= 10:
                label_timer = Label(text="{}:{}".format(minute, second),
                                    font=("Helvetica bold", 40),
                                    fg="red3", bg=BACKGROUND_COLOR)
            else:
                label_timer = Label(text="{}:{}".format(minute, second),
                                    font=("Helvetica bold", 40),
                                    bg=BACKGROUND_COLOR)
            label_timer.pack()
            label_timer.place(y=150, x=187)
            self.game_time -= 1
            if self.started:
                self.root.after(1000, self.timer)

    def play_song(self):
        """method the play song when the player presses start button"""
        mixer.init()
        mixer.music.load('bensound-summer_mp3_music.mp3')
        mixer.music.play()

    def button_start_actions_start_game(self):
        """the action after the pressed button start: create the buttons game,
        start the song, start the countdown timer"""
        if not self.started:
            self.started = True
            self.create_all_the_buttons()
            label_timer = Label(text="Timer: ",
                                font=("Helvetica bold", 40),
                                bg=BACKGROUND_COLOR)
            self.play_song()
            label_timer.pack()
            label_timer.place(y=150, x=20)
            self.timer()

    def button_enter_actions(self, list_box_of_found, list_box_of_mistake):
        """after pressed enter action, this method check if the word is correct
        or not and add to the relevant list"""
        word = self.game.set_score(self.path)
        if word[0]:
            list_box_of_found.insert(END, word[1])
            list_box_of_found.pack()
            list_box_of_found.place(y=700, x=200)
            self.game.set_guest_correct_words(word[1])
        else:
            if word[1] not in self.game.get_guest_wrong_words() and \
                    word[1] not in self.game.get_guest_correct_words():
                list_box_of_mistake.insert(END, word[1])
                list_box_of_mistake.pack()
                list_box_of_mistake.place(y=700, x=10)
                self.game.set_guest_wrong_words(word[1])

        for button in self.clicked_button:
            button['background'] = BUTTON_COLOR
        self.clicked_button.clear()
        self.path.clear()

    def from_board_to_row(self, row):
        """create list of path of specific row"""
        list_of_path = []
        for i in range(len(self.board.get_board())):
            list_of_path.append(self.board.get_letter(i, row))
        return list_of_path

    def score_of_game(self):
        """method that responsibility to the score of the game"""
        label_score = Label(self.root,
                            text="Score: " + str(self.game.get_score()),
                            font=("Helvetica bold", 40), bg=BACKGROUND_COLOR)
        label_score.pack()
        label_score.place(y=70, x=20)
        if self.started:
            self.root.after(500, self.score_of_game)

    ###########################################################################
    #                               GAME LOGIC GUI
    ###########################################################################

    def start_again(self):
        """method that responsibility to start game again and to close the
        last game"""
        self.root.quit()
        self.started = False
        self.run_game()

    def open_game_over(self):
        """method that responsibility to create new window that present to the
        player if he\she want to play another game or not"""
        end_game = Tk()
        label_title = Label(end_game, text="Game over",
                            font=("Helvetica bold", 40))
        label_title.pack(side=tk.TOP)
        label_score = Label(end_game,
                            text="Score: " + str(self.game.get_score()),
                            font=("Helvetica bold", 20))
        label_score.pack()
        restart_button = Button(end_game,
                                command=lambda: self.create_new_game(end_game),
                                text="one more", width=10, height=2,
                                font=("Helvetica bold", 20), bg='sea green')
        restart_button.pack(side=tk.LEFT)
        stop_button = Button(end_game, command=end_game.quit,
                             text="stop playing", bg='firebrick',
                             font=("Helvetica bold", 20), width=10, height=2)
        stop_button.pack(side=tk.RIGHT)
        self.root.destroy()
