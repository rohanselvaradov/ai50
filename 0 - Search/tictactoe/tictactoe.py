"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flattened = [square for row in board for square in row if square is not None]
    if len(flattened) % 2 == 0:
        return "X"
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                possible.add((i, j))
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not a valid move!")
    else:
        turn = player(board)
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = turn
        return new_board 


def check_rows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    
def check_cols(board):
    for row in np.transpose(board):
        if len(set(row)) == 1:
            return row[0]
    
def check_diags(board):
    if len(set([board[i][i] for i in range(3)])) == 1:
        return board[0][0]
    if len(set([board[i][2 - i] for i in range(3)])) == 1:
        return board[0][2]

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_rows(board) is not None:
        return check_rows(board)
    elif check_cols(board) is not None:
        return check_cols(board)
    elif check_diags(board) is not None:
        return check_diags(board)
    return

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or len(actions(board)) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    payoffs = {"X": 1, None: 0, "O": -1}
    return payoffs[winner(board)]



def recursion(board):
    if terminal(board):
        return (utility(board), None)
    if player(board) == "X":
        value = -2
        best_action = None
        for action in actions(board):
            new_value = recursion(result(board, action))[0]
            if new_value > value:
                value = new_value
                best_action = action
        return (value, best_action)
    else:
        value = 2
        best_action = None
        for action in actions(board):
            new_value = recursion(result(board, action))[0]
            if new_value < value:
                value = new_value
                best_action = action
        return (value, best_action)
    


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    return recursion(board)[1]        