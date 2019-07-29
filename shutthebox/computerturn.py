"""
Defines the ComputerTurn class of shutthebox.
"""

import itertools
import collections
import os

from .turn import Turn

def import_bill(file_path):
    """
    Import Durango Bill's optimal strategy file and return it as a dict.

    file_path (str): path of text file downloaded from
        http://www.durangobill.com/ShutTheBoxExtra/STB_1DIE.txt
    """
    bill = [line.rstrip('\n') for line in open(file_path)]
    bill = bill[21:533]

    # create a dict: eventually the key will be a tuple of flap numbers
    # already closed and the value will be a dict with the flaps to close
    # for each possible dice sum
    table = {}

    for this_row in bill:
        this_row = this_row.split()

        # split numbers from first column into a list to be the dict key
        flaps_down = [int(c) for c in this_row[0]]
        if flaps_down == [0]:
            flaps_down = []

        # for each dict value, create another dict
        # where the key is the dice sum and the value is the flaps to close
        dice_sum = 1
        flaps_to_lower = {}
        for col in range(2, 13 + 1):
            flaps_to_lower[dice_sum] = [int(c) for c in this_row[col]
                                        if c != '0']
            # if cell not blank, check that flaps to lower sum to dice sum
            if (flaps_to_lower[dice_sum] and
                    dice_sum != sum(flaps_to_lower[dice_sum])):
                raise RuntimeError("Flaps to lower don't sum to dice sum")
            dice_sum += 1

        # add this row's data to the table dict
        table[tuple(flaps_down)] = flaps_to_lower

    return table

class ComputerTurn(Turn):
    """
    A subclass of Turn to represent turns taken by the computer.

    box: instance of Box class to use for this turn
    dice: instance of Dice class to use for this turn
    """

    def __init__(self, box, dice):
        super(ComputerTurn, self).__init__(box, dice)

        # create dict of probabilities for rolling particular dice sums

        dice_sums = []
        # for each possible outcome of n dice, sum dice numbers
        for dice_numbers in itertools.product(range(1, 6 + 1),
                                              repeat=dice.num_dice):
            dice_sums.append(sum(dice_numbers))

        # calculate frequency of each dice sum
        frequencies = collections.Counter(dice_sums)

        # calculate proportion for each dice sum
        self.dice_sum_probabilities = {}
        for dice_sum, freq in frequencies.items():
            self.dice_sum_probabilities[dice_sum] = freq / len(dice_sums)

        self.bill_filename = 'bill-optimal-strategy.txt'
        try:
            # look for file in shutthebox directory
            file_path = os.path.join(
                os.path.dirname(__file__), self.bill_filename)
            self.bill_table = import_bill(file_path)
        except FileNotFoundError:
            self.bill_table = False

    @staticmethod
    def remove_greater_than(lst, num):
        """
        From a supplied list, returns a new list with any original
        elements which were greater than num removed.

        lst (list): original list from which to remove elements
        num (int)
        """
        return [x for x in lst if not x > num]

    # flap decision methods need the same arguments even if they don't
    # use all of them
    # pylint: disable=unused-argument

    def make_flap_decision_highest(
            self, dice_total, num_dice_decision_method=None):
        """
        Returns a list of numbers which sum to the dice total from a
        list of possible flap numbers, or False if this is impossible.
        Always prefers to use a higher-numbered flap whenever possible.

        dice_total (int): sum of dice rolled
        """
        # just the flaps that are <= the dice total
        flap_nums = self.remove_greater_than(
            self.box.get_available_flaps().keys(), dice_total)

        # if we can make the dice total using a single flap, do that
        for flap_num in flap_nums:
            if flap_num == dice_total:
                return [flap_num]

        # otherwise, use combinations of flaps, preferring higher numbers
        # sort because flaps dict not returned in any specific order
        flap_nums.sort()
        flap_nums.reverse()

        # for each possible number of flaps (apart from a single flap),
        # starting with fewest flaps i.e. highest flap numbers
        for length in range(2, len(flap_nums) + 1):
            # check whether each combination sums to dice total
            for this_combination in itertools.combinations(flap_nums, length):
                if sum(this_combination) == dice_total:
                    this_combination = list(this_combination)
                    this_combination.reverse()
                    return this_combination

        return False

    def make_flap_decision_lowest(
            self, dice_total, num_dice_decision_method=None):
        """
        Returns a list of numbers which sum to the dice total from a
        list of possible flap numbers, or False if this is impossible.
        Always prefers to use a lower-numbered flap whenever possible.

        dice_total (int): sum of dice rolled
        """
        # just the flaps that are <= the dice total
        flap_nums = self.remove_greater_than(
            self.box.get_available_flaps().keys(), dice_total)

        # use combinations of flaps, preferring lower numbers
        # sort because flaps dict not returned in any specific order
        flap_nums.sort()

        # for each possible number of flaps
        # starting with most flaps i.e. lowest flap numbers
        for length in range(len(flap_nums), 0, -1):
            # check whether each combination sums to dice total
            for this_combination in itertools.combinations(flap_nums, length):
                if sum(this_combination) == dice_total:
                    return list(this_combination)

        return False

    def calculate_success_probability(
            self, flap_nums, num_dice_decision_method):
        """
        Calculate the probability of being able to close at least one
        flap if the flaps in flap_nums are left open and a specific
        number of dice are rolled.

        flap_nums (list)
        num_dice_decision_method (method): used to decide how many dice
            would be rolled
        """
        single_die = False
        # if allowed to use a single die and we decide to
        if (sum(flap_nums) <= self.max_flap_sum_single_die and
                num_dice_decision_method() == 1):
            single_die = True
            possible_dice_sums = range(1, 6 + 1)
        else:
            possible_dice_sums = self.dice_sum_probabilities.keys()

        prob = 0

        for dice_sum in possible_dice_sums:
            this_dice_sum_success = False
            # try all lengths of combinations of flaps supplied
            for length in range(1, len(flap_nums) + 1):
                for this_combination in itertools.combinations(
                        flap_nums, length):
                    # if we find one, add probability of rolling this dice sum
                    if sum(this_combination) == dice_sum:
                        if single_die:
                            prob += 1/6
                        else:
                            prob += self.dice_sum_probabilities[dice_sum]
                        this_dice_sum_success = True
                        # stop trying combinations of this length
                        break
                # stop trying combinations of any length
                if this_dice_sum_success:
                    break

        return prob

    def make_flap_decision_next_roll_probability(
            self, dice_total, num_dice_decision_method):
        """
        Returns a list of numbers which sum to the dice total from a
        list of possible flap numbers, or False if this is impossible.
        Chooses flap numbers which maximise the probability of success
        on the next roll using the calculate_success_probability()
        method.

        dice_total (int): sum of dice rolled
        num_dice_decision_method (method): in calculating probabilities
            it is assumed that this method will be used to decide how
            many dice to use for the next roll
        """

        flap_nums = self.box.get_available_flaps().keys()

        # create an empty dict to hold next-turn success probabilities
        # key: tuple of flap numbers (can't use a list)
        # value: probability of being able to close at least one flap on the
        #   next roll if these flaps are closed i.e. not failing on next roll
        probabilities = {}

        # just the flaps that are <= the dice total
        closeable_flap_nums = self.remove_greater_than(flap_nums, dice_total)

        # use combinations of flaps, preferring higher numbers
        # sort because flaps dict not returned in any specific order
        closeable_flap_nums.sort()
        closeable_flap_nums.reverse()

        # for each possible number of flaps starting with fewest flaps
        for length in range(1, len(closeable_flap_nums) + 1):
            # for each combination with this number of flaps
            for this_combination in itertools.combinations(
                    closeable_flap_nums, length):
                # check combination sums to dice total and try next if not
                if sum(this_combination) != dice_total:
                    continue

                # flaps that would be left if we closed this combination
                remaining_flaps = [n for n in flap_nums
                                   if n not in this_combination]

                probabilities[this_combination] = \
                    self.calculate_success_probability(
                        remaining_flaps, num_dice_decision_method)

        # if no flaps can be closed
        if not probabilities:
            return False

        # choose flap combination with best probability of success on next roll
        chosen_flaps = max(probabilities, key=probabilities.get)

        return list(chosen_flaps) # instead of tuple

    def make_flap_decision_bill(
            self, dice_total, num_dice_decision_method):
        """
        Returns a list of numbers which sum to the dice total from a
        list of possible flap numbers, or False if this is impossible.
        Chooses flap numbers using Durango Bill's optimal strategy
        table.

        dice_total (int): sum of dice rolled
        num_dice_decision_method (method): it is assumed that this
            method will be used to decide how many dice to use for the
            next roll
        """
        if not self.bill_table:
            raise RuntimeError(
                "Couldn't find " + self.bill_filename + " so couldn't use " +
                "make_flap_decision_bill.")

        if num_dice_decision_method() != 1:
            print(num_dice_decision_method(), self.dice.num_dice)
            raise NotImplementedError(
                "Can't (yet) use make_flap_decision_bill without option to " +
                "use one die e.g. with make_num_dice_decision_always_all")

        flaps_lowered = self.box.get_lowered_flaps().keys()
        flaps_chosen = self.bill_table[tuple(flaps_lowered)][dice_total]

        if not flaps_chosen:
            return False

        return flaps_chosen

    # pylint: enable=unused-argument

    @staticmethod
    def make_num_dice_decision_one_if_poss():
        """
        Returns how many dice to roll if we're allowed to roll a single
        die. In this method, we'll choose to always roll a single die if
        allowed.
        """
        return 1

    def make_num_dice_decision_always_all(self):
        """
        Returns how many dice to roll if we're allowed to roll a single
        die. In this method, we'll choose to always roll a single die if
        allowed.
        """
        return self.dice.num_dice

    def perform_roll(self, num_dice_decision_method=None,
                     flap_decision_method=None, debug=False):
        """
        Perform a dice roll and lower flaps. Return True if at least one
        flap was lowered, otherwise False.

        num_dice_decision_method (method): used in deciding how many
            dice to roll, default make_num_dice_decision_one_if_poss
        flap_decision_method (method): used in deciding which flaps to
            lower, default make_flap_decision_next_roll_probability
        debug (bool): print debug information relating to this roll?
        """
        if num_dice_decision_method is None:
            num_dice_decision_method = self.make_num_dice_decision_one_if_poss
        if flap_decision_method is None:
            flap_decision_method = self.make_flap_decision_next_roll_probability

        # roll all the dice or a single die
        # if our decision method returns 1 (die) and we're allowed to roll a
        # single die, do this
        if (num_dice_decision_method() == 1 and
                self.box.sum_available_flaps() <= self.max_flap_sum_single_die):
            if debug:
                print('Rolling single die')
            dice_total = self.dice.roll(1)
        else:
            dice_total = self.dice.roll()
            if debug:
                print('Rolling all dice')
        if debug:
            print('Dice total:', dice_total)

        # decide which flaps to lower and lower them
        flap_nums_to_lower = flap_decision_method(
            dice_total, num_dice_decision_method)
        if not flap_nums_to_lower: # if impossible to lower any flaps
            if debug:
                print('Impossible to lower any flaps')
            return False
        if debug:
            print('Lowering flaps:', flap_nums_to_lower)
        for this_flap_num in flap_nums_to_lower:
            self.box.flaps[this_flap_num].lower()

        return True

    def perform_turn(self, num_dice_decision_method=None,
                     flap_decision_method=None, debug=False):
        """
        Perform this turn and return the resulting score i.e. sum of
        flap numbers.

        num_dice_decision_method (method): used in deciding how many
            dice to roll, passed to perform_roll
        flap_decision_method (method): used in deciding which flaps to
            lower, passed to perform_roll
        debug (bool): print debug information relating to this turn?
        """

        if debug:
            print(self.box)
            print('Flap sum:', self.box.sum_available_flaps())

        # check whether all flaps are already down before each roll
        # if roll performed and no flaps could be lowered, stop the turn
        while (self.box.sum_available_flaps() > 0 and
               self.perform_roll(
                   debug=debug,
                   num_dice_decision_method=num_dice_decision_method,
                   flap_decision_method=flap_decision_method)):
            if debug:
                print('\n', self.box)
                print('Flap sum:', self.box.sum_available_flaps())

        score = self.box.sum_available_flaps()
        self.box.__init__() # re-initialise our box with all flaps up
        return score
