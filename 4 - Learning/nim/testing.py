# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 12:11:29 2022

@author: Rohan
"""
from nim import *



def unexplored(ai):
    i = 0
    for k, v in ai.q.items():
        if v == 0:
            i += 1
    return i

def ai_v_ai(ai0, ai1):
    """
    Play AI game against other AI.
    """
    # Create new game
    game = Nim()

    # Game loop
    while True:
        # Compute available actions
        available_actions = Nim.available_actions(game.piles)

        # Let AI0 move
        pile, count = ai0.choose_action(game.piles, epsilon=False)
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            return game.winner

        # Let AI1 move
        pile, count = ai1.choose_action(game.piles, epsilon=False)
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            return game.winner

        
def evaluate_ai_v_self(ai, n):
    wins_0 = 0
    wins_1 = 0
    for i in range(n):
        winner = ai_v_ai(ai, ai)
        if winner == 0:
            wins_0 += 1
        else:
            wins_1 += 1
    print("Player 1 won {} times\nPlayer 2 won {} times".format(wins_0, wins_1))


ai = train(30000)
print("AI does not know q-values of {} (state, action) pairs".format(unexplored(ai)))
evaluate_ai_v_self(ai, 1000)

