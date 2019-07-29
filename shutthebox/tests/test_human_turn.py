"""
Tests for the HumanTurn class of shutthebox.
"""

from nose.tools import raises, assert_raises
import shutthebox

# pylint: disable=missing-docstring
# pylint: disable=no-self-use
# pylint: disable=attribute-defined-outside-init

class TestHumanTurn:
    def setup(self):
        box = shutthebox.Box()
        dice = shutthebox.Dice()
        self.turn = shutthebox.HumanTurn(box, dice)

    def test_human_turn_is_subclass_of_turn(self):
        isinstance(self.turn, shutthebox.Turn)

    @raises(ValueError)
    def test_check_num_dice_non_str(self):
        self.turn.check_num_dice_decision(string = 1)

    def test_check_num_dice_non_int(self):
        assert not self.turn.check_num_dice_decision(string = '1.5')

    def test_check_num_dice_too_few(self):
        assert not self.turn.check_num_dice_decision(string = '0')

    def test_check_num_dice_too_many(self):
        assert not self.turn.check_num_dice_decision(string = '3')

    def test_check_num_dice_single_when_flap_sum_too_large(self):
        # all flaps still up
        assert not self.turn.check_num_dice_decision(string = '1')

    def test_check_num_dice_single_allowed(self):
        # leave only flaps 1, 2 and 3 (sum 6 = max_flap_sum_single_die)
        for this_flap_num in range(4, self.turn.box.num_flaps + 1):
            self.turn.box.flaps[this_flap_num].lower()
        assert self.turn.check_num_dice_decision(string = '1') == 1

    def test_check_num_dice_all_allowed_when_could_use_single(self):
        # leave only flaps 1, 2 and 3 (sum 6 = max_flap_sum_single_die)
        for this_flap_num in range(4, self.turn.box.num_flaps + 1):
            self.turn.box.flaps[this_flap_num].lower()
        assert self.turn.check_num_dice_decision(string = '2') == 2

    def test_check_num_dice_all_allowed_when_all_flaps_up(self):
        # all flaps still up
        assert self.turn.check_num_dice_decision(string = '2') == 2

    @raises(ValueError)
    def test_check_flaps_decision_non_str(self):
        self.turn.check_flaps_decision(1, 1)

    def test_check_flaps_decision_non_number(self):
        assert not self.turn.check_flaps_decision('1 banana', 1)

    def test_check_flaps_decision_number_but_not_valid_flap(self):
        assert not self.turn.check_flaps_decision('1 10', 11)

    def test_check_flaps_decision_flap_already_down(self):
        self.turn.box.flaps[1].lower()
        assert not self.turn.check_flaps_decision('2 1', 3)

    def test_check_flaps_decision_valid_flaps_but_incorrect_sum(self):
        assert not self.turn.check_flaps_decision('1 2 3', 7)

    def test_check_flaps_decision_no_flaps(self):
        assert self.turn.check_flaps_decision('', 1) == []

    def test_check_flaps_decision_valid(self):
        assert self.turn.check_flaps_decision('9 1 7', 17) == [9, 1, 7]

    def test_check_flaps_decision_valid_duplicate(self):
        assert self.turn.check_flaps_decision('1 1 2 3 2', 6) == [1, 2, 3]
