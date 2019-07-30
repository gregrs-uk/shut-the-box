#!/usr/bin/env python3

"""
Play a human game of Shut the Box on the command line.
"""

import sys
import shutthebox

# pylint: disable=invalid-name

box = shutthebox.Box()
dice = shutthebox.Dice()

def check_another_game_choice(string):
    """
    Check whether the user would like to play another game. Return True
    if they would, False if not and None if their choice was invalid.
    """
    if string[0].lower() == 'y':
        return True
    if string[0].lower() == 'n':
        return False
    print('Please enter Y or N')
    return None

while True:
    turn = shutthebox.HumanTurn(box, dice)
    turn.perform_turn()
    while True: # until we get a valid choice
        choice = check_another_game_choice(
            input('Play another turn? [Y/N] '))
        if choice is True:
            print()
            break
        if choice is False:
            sys.exit()
