#!/usr/bin/env python3

"""
Simulate many turns of Shut the Box using the default decision methods.
Output the score for each turn to the command line.
"""

import shutthebox

box = shutthebox.Box()
dice = shutthebox.Dice()

turn = shutthebox.ComputerTurn(box, dice)

for n in range(0, 10000):
    print(turn.perform_turn())
