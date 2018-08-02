# run using nosetests --with-coverage --cover-html

from nose.tools import raises, assert_raises
import shutthebox

class TestComputerTurn(object):
    def setUp(self):
        box = shutthebox.Box()
        dice = shutthebox.Dice()
        self.turn = shutthebox.ComputerTurn(box, dice)

        self.one_to_nine = range(1, 9 + 1)
        assert len(self.one_to_nine) == 9
        self.one_to_four = range(1, 4 + 1)
        assert len(self.one_to_four) == 4

    def test_computer_turn_is_subclass_of_turn(self):
        isinstance(self.turn, shutthebox.Turn)

    def test_remove_greater_than(self):
        assert self.turn.remove_greater_than([1, 2, 3, 4], 2) == [1, 2]

    def test_flap_decision_highest_single_flap(self):
        flap_nums = self.one_to_nine
        assert self.turn.make_flap_decision_highest(flap_nums, 7) == [7]

    def test_flap_decision_highest_two_flaps(self):
        flap_nums = self.one_to_nine
        flap_nums.remove(7)
        assert self.turn.make_flap_decision_highest(flap_nums, 7) == [1, 6]
        flap_nums.remove(6)
        assert self.turn.make_flap_decision_highest(flap_nums, 7) == [2, 5]

    def test_flap_decision_highest_three_flaps(self):
        flap_nums = self.one_to_four
        assert self.turn.make_flap_decision_highest(flap_nums, 9) == [2, 3, 4]

    def test_flap_decision_highest_impossible(self):
        flap_nums = self.one_to_four
        flap_nums.remove(2)
        assert self.turn.make_flap_decision_highest(flap_nums, 10) is False

    def test_flap_decision_lowest_single_flap(self):
        flap_nums = self.one_to_nine
        assert self.turn.make_flap_decision_lowest(flap_nums, 2) == [2]

    def test_flap_decision_lowest_two_flaps(self):
        flap_nums = self.one_to_nine
        assert self.turn.make_flap_decision_lowest(flap_nums, 5) == [1, 4]
        flap_nums.remove(1)
        assert self.turn.make_flap_decision_lowest(flap_nums, 5) == [2, 3]

    def test_flap_decision_lowest_three_flaps(self):
        flap_nums = self.one_to_nine
        assert self.turn.make_flap_decision_lowest(flap_nums, 8) == [1, 2, 5]

    def test_flap_decision_lowest_impossible(self):
        flap_nums = self.one_to_four
        flap_nums.remove(2)
        assert self.turn.make_flap_decision_lowest(flap_nums, 10) is False

    def test_num_dice_decision_always_all(self):
        assert self.turn.make_num_dice_decision_always_all() == 2

    def test_turn_returns_valid_score(self):
        # try 1000 turns
        for n in range(0, 1000):
            score = self.turn.perform_turn() 
            assert isinstance(score, int) and score >= 0 and score <= 45

    def test_turn_with_debug(self):
        score = self.turn.perform_turn(debug = True) 
        assert isinstance(score, int) and score >= 0 and score <= 45
