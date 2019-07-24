import random
import itertools
import collections
import sys

if sys.version_info.major < 3: # pragma: no cover
    sys.exit('Python 3 is required. You are currently using Python ' +
             str(sys.version_info.major) + '.' +
             str(sys.version_info.minor) + '.')

class Flap(object):
    """
    One of the flaps on the box. They start raised and can be lowered.

    number (int): the number shown on the flap
    """

    def __init__(self, number):
        if not (isinstance(number, int) and number >= 1):
            raise ValueError('number must be an integer >= 1')

        self.number = number
        self.is_down = False

    def lower(self):
        """
        Lower this flap.
        """

        if self.is_down:
            raise RuntimeError('Trying to lower a flap that is already down')
        self.is_down = True

class Box(object):
    """
    The box, which contains a number of flaps.

    num_flaps (int): how many flaps the box has (default 9)
    """

    def __init__(self, num_flaps = 9):
        if not (isinstance(num_flaps, int) and num_flaps >= 1):
            raise ValueError('num_flaps must be an integer >= 1')

        self.num_flaps = num_flaps

        self.flaps = {}
        for this_flap_num in range(1, num_flaps + 1):
            self.flaps[this_flap_num] = Flap(this_flap_num)

    def get_available_flaps(self):
        """
        Returns a dict of objects for the flaps that are currently up.
        """
        available_flaps = {}
        for this_flap_num, this_flap in self.flaps.items():
            if not this_flap.is_down:
                available_flaps[this_flap.number] = this_flap

        return available_flaps

    def sum_available_flaps(self):
        """
        Returns the sum of the numbers of the available flaps.
        """
        return sum(self.get_available_flaps().keys())

    def __str__(self):
        """
        Get a string representation of the state of the flaps e.g.
          UP: 1 2 3 4 5 6   8 9
        DOWN:             7
        """
        up_string =   '  UP: '
        down_string = 'DOWN: '

        # add flap numbers / equivalent number of spaces to up/down strings
        flap_range = range(1, self.num_flaps + 1)
        for this_flap_no in flap_range:
            if self.flaps[this_flap_no].is_down:
                for this_char in str(this_flap_no):
                    up_string += ' '
                down_string += str(this_flap_no)
            else:
                up_string += str(this_flap_no)
                for this_char in str(this_flap_no):
                    down_string += ' '
            if this_flap_no != flap_range[-1]: # if not last flap
                up_string += ' '
                down_string += ' '

        return up_string + '\n' + down_string

class Dice(object):
    """
    One or more dice used in playing the game.

    num_dice (int): how many dice are being used in the game (default 2)
    """

    def __init__(self, num_dice = 2):
        if not (isinstance(num_dice, int) and num_dice >= 1):
            raise ValueError('num_dice must be an integer >= 1')

        self.num_dice = num_dice

    def roll(self, roll_dice = None):
        """
        Roll one or more of the dice.

        roll_dice (int): how many dice to roll (default all)
        """

        # if roll_dice not supplied, use all dice
        if roll_dice is None:
            roll_dice = self.num_dice

        if not (isinstance(roll_dice, int) and
                roll_dice >= 1 and roll_dice <= self.num_dice):
            raise ValueError('roll_dice must be an integer between 1 and ' +
                             '{}'.format(self.num_dice))

        total = 0
        for this_die in range(0, roll_dice):
            total += random.randint(1, 6)
        return total

class Turn(object):
    """
    A turn (taken by the computer or a human) in which the dice are rolled 
    and flaps are lowered, probably multiple times, until the player either 
    cannot or decides not to lower any more flaps, or until there are no flaps 
    remaining up.
    """

    def __init__(self, box, dice):
        assert isinstance(box, Box)
        self.box = box

        assert isinstance(dice, Dice)
        self.dice = dice

        # max sum of flap numbers to be allowed to roll a single die
        self.max_flap_sum_single_die = 6

class ComputerTurn(Turn):
    """
    A subclass of Turn to represent turns taken by the computer.
    """

    def __init__(self, box, dice):
        super(ComputerTurn, self).__init__(box, dice)

        # create dict of probabilities for rolling particular dice sums

        dice_sums = []
        # for each possible outcome of n dice, sum dice numbers
        for dice_numbers in itertools.product(range(1, 6 + 1),
                                              repeat = dice.num_dice):
            dice_sums.append(sum(dice_numbers))

        # calculate frequency of each dice sum
        frequencies = collections.Counter(dice_sums)

        # calculate proportion for each dice sum
        self.dice_sum_probabilities = {}
        for dice_sum, freq in frequencies.items():
            self.dice_sum_probabilities[dice_sum] = freq / len(dice_sums)

    def remove_greater_than(self, list, n):
        """
        From a supplied list, returns a new list with any original elements 
        which were greater than n removed.

        list (list): original list from which to remove elements
        """
        new_list = [x for x in list if not x > n]
        return new_list

    def make_flap_decision_highest(
            self, flap_nums, dice_total, num_dice_decision_method = None):
        """
        Returns a list of numbers which sum to the dice total from a list of
        possible flap numbers, or False if this is impossible. Always prefers 
        to use a higher-numbered flap whenever possible.

        flap_nums (list of ints): flap numbers available
        dice_total (int): total shown on dice
        """
        # just the flaps that are <= the dice total
        flap_nums = self.remove_greater_than(flap_nums, dice_total)

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
            self, flap_nums, dice_total, num_dice_decision_method = None):
        """
        Returns a list of numbers which sum to the dice total from a list of 
        possible flap numbers, or False if this is impossible. Always prefers 
        to use a lower-numbered flap whenever possible.

        flap_nums (list of ints): flap numbers available
        dice_total (int): total shown on dice
        """
        # just the flaps that are <= the dice total
        flap_nums = self.remove_greater_than(flap_nums, dice_total)

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
        Calculate the probability of being able to close at least one flap if
        the flaps in the flap_nums list are left open. Use the decision method
        supplied to decide how many dice to use.
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
                            prob += 1/float(6)
                        else:
                            prob += self.dice_sum_probabilities[dice_sum]
                        this_dice_sum_success = True
                        # stop trying combinations of this length
                        break
                # stop trying combinations of any length
                if this_dice_sum_success: break

        return prob

    def make_flap_decision_next_roll_probability(
            self, flap_nums, dice_total, num_dice_decision_method):
        """
        Returns a list of numbers which sum to the dice total from a list of
        possible flap numbers, or False if this is impossible. Chooses flap
        numbers which maximise the probability of success on the next roll using
        the calculate_success_probability() method. Uses the decision method
        supplied to decide how many dice to use in calculating probabilities
        for the next roll.
        """

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
                if sum(this_combination) != dice_total: continue

                # flaps that would be left if we closed this combination
                remaining_flaps = [n for n in flap_nums if n not in this_combination]

                probabilities[this_combination] = \
                    self.calculate_success_probability(
                        remaining_flaps, num_dice_decision_method)

        # if no flaps can be closed
        if not len(probabilities):
            return False

        # choose flap combination with best probability of success on next roll
        chosen_flaps = max(probabilities, key = probabilities.get)

        return list(chosen_flaps) # instead of tuple

    def make_num_dice_decision_one_if_poss(self):
        """
        Returns how many dice to roll if we're allowed to roll a single die. 
        In this method, we'll choose to always roll a single die if allowed.
        """
        return 1

    def make_num_dice_decision_always_all(self):
        """
        Returns how many dice to roll if we're allowed to roll a single die. 
        In this method, we'll choose to always roll a single die if allowed.
        """
        return self.dice.num_dice

    def perform_roll(self, num_dice_decision_method = None,
                     flap_decision_method = None, debug = False):
        """
        Perform a dice roll based on the number-of-dice decision method 
        supplied and lower flaps based on the flap decision method supplied.

        num_dice_decision_method (method): default
            make_num_dice_decision_one_if_poss
        flap_decision_method (method): default
            make_flap_decision_next_roll_probability
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
            if debug: print('Rolling single die')
            dice_total = self.dice.roll(1)
        else:
            dice_total = self.dice.roll()
            if debug: print('Rolling all dice')
        if debug: print('Dice total:', dice_total)

        # decide which flaps to lower and lower them
        available_flap_nums = list(self.box.get_available_flaps().keys())
        flap_nums_to_lower = flap_decision_method(
            available_flap_nums, dice_total, num_dice_decision_method)
        if not flap_nums_to_lower: # if impossible to lower any flaps
            if debug: print('Impossible to lower any flaps')
            return False
        if debug: print('Lowering flaps:', flap_nums_to_lower)
        for this_flap_num in flap_nums_to_lower:
            self.box.flaps[this_flap_num].lower()

        return True

    def perform_turn(self, num_dice_decision_method = None,
                     flap_decision_method = None, debug = False):
        """
        Performs this turn and returns the resulting score i.e. sum of flap 
        numbers.

        debug (bool): print debug information relating to this turn?
        """

        if debug:
            print(self.box)
            print('Flap sum:', self.box.sum_available_flaps())

        # check whether all flaps are already down before each roll
        # if roll performed and no flaps could be lowered, stop the turn
        while (self.box.sum_available_flaps() > 0 and
               self.perform_roll(
                   debug = debug,
                   num_dice_decision_method = num_dice_decision_method,
                   flap_decision_method = flap_decision_method)):
            if debug:
                print('\n', self.box)
                print('Flap sum:', self.box.sum_available_flaps())

        score = self.box.sum_available_flaps()
        self.box.__init__() # re-initialise our box with all flaps up
        return score

class HumanTurn(Turn):
    """
    A subclass of Turn to represent turns taken by a human player.
    """

    def __init__(self, box, dice):
        super(HumanTurn, self).__init__(box, dice)

    def check_num_dice_decision(self, string):
        """
        Check player's input for how many dice they want to use. Return number
        of dice (int) if valid and False if invalid, printing a reason if
        invalid.

        string (str): number of dice chosen
        """
        if not isinstance(string, str):
            raise ValueError(
                'Error: check_num_dice_decision requires a str\n' +
                'Got this instead: {}'.format(string))

        msg_invalid = ('Number of dice chosen must be an integer between 1 ' +
                       'and {}'.format(self.dice.num_dice))

        # can't convert string to integer
        try:
            n = int(string)
        except ValueError:
            print(msg_invalid)
            return False

        # invalid number of dice
        if not (n >= 1 and n <= self.dice.num_dice):
            print(msg_invalid)
            return False

        # single die chosen but not allowed
        if (n == 1 and
            self.box.sum_available_flaps() > self.max_flap_sum_single_die):
            print('You can only use a single die when the flap numbers add ' +
                  'up to {} or less'.format(self.max_flap_sum_single_die))
            return False

        return n

    def check_flaps_decision(self, string, dice_total):
        """
        Check player's input for which flaps to lower. Return True if valid 
        and False if invalid, printing a reason if invalid. Raise ValueError 
        if string is not a str.

        string (str): player's input
        dice_total (int): sum of dice
        """
        if not isinstance(string, str):
            raise ValueError(
                'Error: check_flaps_decision requires a str\n' +
                'Got this instead: {}'.format(string))

        flap_num_strings = string.split()
        flap_nums = [] # empty list to hold integers

        for this_string in flap_num_strings:
            try:
                # check this flap not already specified
                if not int(this_string) in flap_nums:
                    flap_nums.append(int(this_string))
            except ValueError:
                print('{} is not a valid flap number'.format(this_string))
                return False

        for this_flap_num in flap_nums:
            if not this_flap_num in self.box.flaps.keys():
                print('{} is not a valid flap number'.format(this_flap_num))
                return False
            if self.box.flaps[this_flap_num].is_down:
                print('Flap {} is already down'.format(this_flap_num))
                return False

        if len(flap_nums) and sum(flap_nums) != dice_total:
            print('Flaps chosen do not add up to dice total')
            return False

        return flap_nums

    def perform_roll(self): # pragma: no cover
        """
        Perform a dice roll and lower flaps based on the player's decisions.
        """
        print(self.box, '\n')

        # if flap sum <= max_flap_sum_single_die, ask how many dice to roll
        if self.box.sum_available_flaps() <= self.max_flap_sum_single_die:
            while True: # until we get a valid response
                num_dice_input = input(
                    'How many dice would you like to roll? (between ' +
                    '1 and {}) '.format(self.dice.num_dice))
                num_dice = self.check_num_dice_decision(num_dice_input)
                if num_dice != False:
                    break
        else: # use all dice
            num_dice = self.dice.num_dice

        dice_total = self.dice.roll(num_dice)
        print('Dice total:', dice_total)

        while True: # until we get a list of flap nums or empty list
            flaps_input = input(
                'Which flaps would you like to lower?\n' +
                '(Separate with spaces and leave blank for none) ')
            flap_nums = self.check_flaps_decision(flaps_input, dice_total)
            if isinstance(flap_nums, list):
                if len(flap_nums):
                    break
                else: # empty list i.e. no flaps
                    return False

        # lower flaps
        for this_flap_num in flap_nums:
            self.box.flaps[this_flap_num].lower()

        print()
        return True

    def perform_turn(self): # pragma: no cover
        """
        Performs this turn and returns the resulting score i.e. sum of flap 
        numbers.
        """
        while self.box.sum_available_flaps() > 0 and self.perform_roll():
            pass

        print()
        score = self.box.sum_available_flaps()
        if score == 0:
            print('You have lowered all the flaps and shut the box. Well done!')
        else:
            print('Your score was', score)

        self.box.__init__() # re-initialise our box with all flaps up
        return score
