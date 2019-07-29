"""
Defines the HumanTurn class of shutthebox.
"""

from .turn import Turn

class HumanTurn(Turn):
    """
    A subclass of Turn to represent turns taken by a human player.
    """

    def __init__(self, box, dice):
        super(HumanTurn, self).__init__(box, dice)

    def check_num_dice_decision(self, string):
        """
        Check player's input for how many dice they want to use. Return
        number of dice (int) if valid and False if invalid, printing a
        reason if invalid.

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
        Check player's input for which flaps to lower. Return True if
        valid and False if invalid, printing a reason if invalid. Raise
        ValueError if string is not a str.

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
        Perform a dice roll and lower flaps based on the player's
        decisions.
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
        Performs this turn and returns the resulting score i.e. sum of
        flap numbers.
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

