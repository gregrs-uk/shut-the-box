"""
Tests for the ComputerTurn class of shutthebox.
"""

from nose.tools import raises
import shutthebox

# pylint: disable=missing-docstring
# pylint: disable=no-self-use
# pylint: disable=attribute-defined-outside-init

class TestComputerTurn:
    def setup(self):
        box = shutthebox.Box()
        dice = shutthebox.Dice()
        three_dice = shutthebox.Dice(num_dice = 3)
        self.turn = shutthebox.ComputerTurn(box, dice)

        self.one_to_nine = list(range(1, 9 + 1))
        assert len(self.one_to_nine) == 9
        self.one_to_four = list(range(1, 4 + 1))
        assert len(self.one_to_four) == 4

    def test_computer_turn_is_subclass_of_turn(self):
        isinstance(self.turn, shutthebox.Turn)

    def test_two_dice_sum_probabilities_length(self):
        assert len(self.turn.dice_sum_probabilities) == 11

    def test_two_dice_sum_probabilities_sum(self):
        assert round(sum(self.turn.dice_sum_probabilities.values()), 2) == 1

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

    def test_calculate_success_probability_1_3_4(self):
        # possible combinations of flaps 1, 3, 4 are:
        # 1 + 3 + 4 = 8
        # 1 + 3 = 4
        # 1 + 4 = 5
        # 3 + 4 = 7
        # 1 (can't roll with two dice)
        # 3
        # 4 (don't count this twice though)
        # success for 3, 4, 5, 7, 8 = 20/36
        prob = self.turn.calculate_success_probability(
            [1, 3, 4], self.turn.make_num_dice_decision_one_if_poss)
        # floats might not be quite equal
        assert prob - (20 / float(36)) < 0.001

    def test_calculate_success_probability_1_2_5(self):
        # possible combinations of flaps 1, 2, 5 are:
        # 1 + 2 + 5 = 8
        # 1 + 2 = 3
        # 1 + 5 = 6
        # 2 + 5 = 7
        # 1 (can't roll with two dice)
        # 2
        # 5
        # success for 2, 3, 5, 6, 7, 8 = 23/36
        prob = self.turn.calculate_success_probability(
            [1, 2, 5], self.turn.make_num_dice_decision_one_if_poss)
        # floats might not be quite equal
        assert prob - (23 / float(36)) < 0.001

    def test_calculate_success_probability_1_2_3_single_die(self):
        prob = self.turn.calculate_success_probability(
            [1, 2, 3], self.turn.make_num_dice_decision_one_if_poss)
        # can make 1, 2, 3, 4, 5, 6 with flaps 1, 2, 3 = probability 1
        # can't == with float
        assert prob - 1 < 0.001

    def test_calculate_success_probability_1_2_3_two_dice(
            self):
        prob = self.turn.calculate_success_probability(
            [1, 2, 3], self.turn.make_num_dice_decision_always_all)
        # can make 1, 2, 3, 4, 5, 6 with flaps 1, 2, 3
        # matching dice sums: 2, 3, 4, 5, 6 = probability 1+2+3+4+5 / 36
        # can't == with float
        assert prob - (15 / float(36)) < 0.001

    def test_flap_decision_next_roll_prob_1to5_roll_7(self):
        # for comparison with test below
        # (c.f. calculate_success_probability tests above)
        flaps = self.turn.make_flap_decision_next_roll_probability(
            list(range(1, 5 + 1)), 7, self.turn.make_num_dice_decision_one_if_poss)
        assert flaps == [4, 3]

    def test_flap_decision_highest_1to5_roll_7(self):
        # for comparison with test above
        flaps = self.turn.make_flap_decision_highest(
            list(range(1, 5 + 1)), 7, self.turn.make_num_dice_decision_one_if_poss)
        print(flaps)
        assert flaps == [2, 5]

    def test_flap_decision_next_roll_prob_impossible(self):
        flaps = self.turn.make_flap_decision_next_roll_probability(
            [3], 2, self.turn.make_num_dice_decision_one_if_poss)
        assert flaps == False

    def test_num_dice_decision_always_all(self):
        assert self.turn.make_num_dice_decision_always_all() == 2

    def test_num_dice_decision_one_if_poss(self):
        assert self.turn.make_num_dice_decision_one_if_poss() == 1

    def test_turn_returns_valid_score(self):
        # try 1000 turns
        for _ in range(0, 1000):
            score = self.turn.perform_turn() 
            assert isinstance(score, int) and score >= 0 and score <= 45

    def test_turn_with_debug(self):
        score = self.turn.perform_turn(debug=True) 
        assert isinstance(score, int) and score >= 0 and score <= 45
