"""
Tests for the ComputerTurn class of shutthebox.
"""

import shutthebox

# pylint: disable=missing-docstring
# pylint: disable=no-self-use
# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-public-methods

class TestComputerTurn:
    def setup(self):
        box = shutthebox.Box()
        dice = shutthebox.Dice()
        self.turn = shutthebox.ComputerTurn(box, dice)

    def lower_flaps_except(self, flap_nums):
        """
        Helper method to lower flaps except those supplied.

        flap_nums (list): flap numbers to leave up
        """
        for this_flap_num in self.turn.box.get_available_flaps().keys():
            if this_flap_num not in flap_nums:
                self.turn.box.flaps[this_flap_num].lower()
        return True

    def test_computer_turn_is_subclass_of_turn(self):
        isinstance(self.turn, shutthebox.Turn)

    def test_two_dice_sum_probabilities_length(self):
        assert len(self.turn.dice_sum_probabilities) == 11

    def test_two_dice_sum_probabilities_sum(self):
        assert round(sum(self.turn.dice_sum_probabilities.values()), 2) == 1

    def test_remove_greater_than(self):
        assert self.turn.remove_greater_than([1, 2, 3, 4], 2) == [1, 2]

    def test_flap_decision_highest_single_flap(self):
        assert self.turn.make_flap_decision_highest(7) == [7]

    def test_flap_decision_highest_two_flaps(self):
        self.turn.box.flaps[7].lower()
        assert self.turn.make_flap_decision_highest(7) == [1, 6]
        self.turn.box.flaps[6].lower()
        assert self.turn.make_flap_decision_highest(7) == [2, 5]

    def test_flap_decision_highest_three_flaps(self):
        self.lower_flaps_except([1, 2, 3, 4])
        assert self.turn.make_flap_decision_highest(9) == [2, 3, 4]

    def test_flap_decision_highest_impossible(self):
        self.lower_flaps_except([1, 3, 4])
        assert self.turn.make_flap_decision_highest(10) is False

    def test_flap_decision_lowest_single_flap(self):
        assert self.turn.make_flap_decision_lowest(2) == [2]

    def test_flap_decision_lowest_two_flaps(self):
        assert self.turn.make_flap_decision_lowest(5) == [1, 4]
        self.turn.box.flaps[1].lower()
        assert self.turn.make_flap_decision_lowest(5) == [2, 3]

    def test_flap_decision_lowest_three_flaps(self):
        assert self.turn.make_flap_decision_lowest(8) == [1, 2, 5]

    def test_flap_decision_lowest_impossible(self):
        self.lower_flaps_except([1, 3, 4])
        assert self.turn.make_flap_decision_lowest(10) is False

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

    def test_flap_decision_next_roll_prob_impossible(self):
        self.lower_flaps_except([3])
        flaps = self.turn.make_flap_decision_next_roll_probability(
            2, self.turn.make_num_dice_decision_one_if_poss)
        assert flaps is False

    def test_flap_decision_bill_impossible(self):
        self.lower_flaps_except([3])
        flaps = self.turn.make_flap_decision_bill(
            2, self.turn.make_num_dice_decision_one_if_poss)
        assert flaps is False

    def test_flap_decision_next_roll_prob_1to5_roll_7(self):
        # for comparison with tests below
        # (c.f. calculate_success_probability tests above)
        self.lower_flaps_except([1, 2, 3, 4, 5])
        flaps = self.turn.make_flap_decision_next_roll_probability(
            7, self.turn.make_num_dice_decision_one_if_poss)
        assert flaps == [4, 3]

    def test_flap_decision_highest_1to5_roll_7(self):
        # for comparison with tests above and below
        self.lower_flaps_except([1, 2, 3, 4, 5])
        flaps = self.turn.make_flap_decision_highest(
            7, self.turn.make_num_dice_decision_one_if_poss)
        assert flaps == [2, 5]

    def test_flap_decision_bill_1to5_roll_7(self):
        # for comparison with tests above
        self.lower_flaps_except([1, 2, 3, 4, 5])
        flaps = self.turn.make_flap_decision_bill(
            7, self.turn.make_num_dice_decision_one_if_poss)
        assert flaps == [3, 4]

    def test_num_dice_decision_always_all(self):
        assert self.turn.make_num_dice_decision_always_all() == 2

    def test_num_dice_decision_one_if_poss(self):
        assert self.turn.make_num_dice_decision_one_if_poss() == 1

    def test_turn_returns_valid_score(self):
        # try 1000 turns
        for _ in range(0, 1000):
            score = self.turn.perform_turn()
            assert isinstance(score, int) and 0 <= score <= 45

    def test_turn_with_debug(self):
        score = self.turn.perform_turn(debug=True)
        assert isinstance(score, int) and 0 <= score <= 45
