"""
Tests for the Dice class of shutthebox.
"""

from nose.tools import raises, assert_raises
import shutthebox

class TestDice:
    def setUp(self):
        self.two_dice = shutthebox.Dice()
        self.one_die = shutthebox.Dice(1)

    def test_default_number_of_dice(self):
        assert self.two_dice.num_dice == 2

    @raises(ValueError)
    def test_number_of_dice_too_small(self):
        shutthebox.Dice(0)

    @raises(ValueError)
    def test_number_of_dice_non_int(self):
        shutthebox.Dice(1.5)

    def test_roll_default_number_of_dice(self):
        # try 1000 rolls
        for i in range(0, 1000):
            total = self.two_dice.roll()
            assert total >= 1 and total <= 12 and isinstance(total, int)

    def test_number_of_dice_single(self):
        assert self.one_die.num_dice == 1

    def test_roll_single_die(self):
        # try 1000 rolls
        for i in range(0, 1000):
            total = self.one_die.roll()
            assert total >= 1 and total <= 6 and isinstance(total, int)

    def test_roll_single_die_from_two(self):
        # try 1000 rolls
        for i in range(0, 1000):
            total = self.two_dice.roll(1)
            assert total >= 1 and total <= 6 and isinstance(total, int)

    @raises(ValueError)
    def test_roll_dice_too_few(self):
        self.one_die.roll(0)

    @raises(ValueError)
    def test_roll_dice_too_many(self):
        self.one_die.roll(2)

    @raises(ValueError)
    def test_roll_dice_non_int(self):
        self.two_dice.roll(1.5)
