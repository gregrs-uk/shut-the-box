#!/usr/bin/env python3

"""
Simulate many turns of Shut the Box using Durango Bill's optimal
strategy. Output the score for each turn to the command line.
"""

import shutthebox

# pylint: disable=invalid-name

box = shutthebox.Box()
dice = shutthebox.Dice()

turn = shutthebox.ComputerTurn(box, dice)

for n in range(0, 10000):
    print(turn.perform_turn(
        flap_decision_method=turn.make_flap_decision_bill))
