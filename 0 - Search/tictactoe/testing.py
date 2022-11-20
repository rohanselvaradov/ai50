# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 13:11:18 2022

@author: Rohan
"""

from tictactoe import *

empty_board = [[EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY]]

partial_board = [["X", EMPTY, EMPTY],
                 [EMPTY, "X", EMPTY],
                 [EMPTY, EMPTY, "O"]]

easy_win_x = [["X", "X", "O"],
              [EMPTY, "X", EMPTY],
              ["O", EMPTY, "O"]]

easy_win_o = [["X", EMPTY, "O"],
              ["X", "X", EMPTY],
              [EMPTY, EMPTY, "O"]]

full_board = [["O", "X", "X"],
              ["X", "O", "O"],
              ["X", "O", "X"]]

winner_r = [["X", "X", "X"],
            [EMPTY, "O", "O"],
            [EMPTY, EMPTY, EMPTY]]

winner_c = [["X", "X", "O"],
            [EMPTY, "X", "O"],
            [EMPTY, EMPTY, "O"]]

winner_d = [["X", "O", "O"],
            [EMPTY, "X", "X"],
            ["O", EMPTY, "X"]]



boards = [empty_board, partial_board, full_board, winner_r, winner_c, winner_d]

terminal_boards = [full_board, winner_r, winner_c, winner_d]

evaluating_boards = [partial_board, easy_win_x, easy_win_o]

for board in evaluating_boards:
    print("Best move: {}\n\n".format(minimax(board)))