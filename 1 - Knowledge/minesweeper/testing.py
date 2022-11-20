# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 21:32:11 2022

@author: Rohan
"""

from minesweeper import *

# ai = MinesweeperAI()
# ai.add_knowledge((2, 2), 3)
# ai.add_knowledge((2, 3), 2)
# ai.add_knowledge((1, 1), 1)
# ai.add_knowledge((4, 1), 0)
# ai.add_knowledge((1, 2), 2)

ai3x3 = MinesweeperAI(3, 3)
ai3x3.add_knowledge((0, 0), 1)
ai3x3.add_knowledge((0, 1), 1)
ai3x3.add_knowledge((0, 2), 1)
ai3x3.add_knowledge((2, 1), 2)