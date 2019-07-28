"""
Defines the Dice class of shutthebox.
"""

import random

# pylint: disable=too-few-public-methods

class Dice:
    """
    One or more dice used in playing the game.

    num_dice (int): how many dice are being used in the game (default 2)
    """

    def __init__(self, num_dice=2):
        if not (isinstance(num_dice, int) and num_dice >= 1):
            raise ValueError('num_dice must be an integer >= 1')

        self.num_dice = num_dice

    def roll(self, roll_dice=None):
        """
        Roll one or more of the dice.

        roll_dice (int): how many dice to roll (default all)
        """

        # if roll_dice not supplied, use all dice
        if roll_dice is None:
            roll_dice = self.num_dice

        if (not isinstance(roll_dice, int) or roll_dice < 1 or
                roll_dice > self.num_dice):
            raise ValueError('roll_dice must be an integer between 1 and ' +
                             '{}'.format(self.num_dice))

        total = 0
        for _ in range(0, roll_dice):
            total += random.randint(1, 6)
        return total
