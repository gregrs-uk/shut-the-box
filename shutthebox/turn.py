"""
Defines the Turn class of shutthebox, inherited by HumanTurn and
ComputerTurn.
"""

from .box import Box
from .dice import Dice

# pylint: disable=too-few-public-methods

class Turn:
    """
    A turn (taken by the computer or a human) in which the dice are
    rolled and flaps are lowered, probably multiple times, until the
    player either cannot or decides not to lower any more flaps, or
    until there are no flaps remaining up.
    """

    def __init__(self, box, dice):
        assert isinstance(box, Box)
        self.box = box

        assert isinstance(dice, Dice)
        self.dice = dice

        # max sum of flap numbers to be allowed to roll a single die
        self.max_flap_sum_single_die = 6
