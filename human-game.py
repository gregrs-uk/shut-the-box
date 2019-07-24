#!/usr/bin/env python3

import shutthebox
from sys import exit

box = shutthebox.Box()
dice = shutthebox.Dice()

def check_another_game_choice(string):
    if string[0].lower() == 'y':
        return True
    elif string[0].lower() == 'n':
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
            exit()
