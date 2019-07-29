"""
Defines the Box class of shutthebox.
"""

from .flap import Flap

class Box:
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
        return {num: flap for num, flap in self.flaps.items()
                if not flap.is_down}

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
                for _ in str(this_flap_no):
                    up_string += ' '
                down_string += str(this_flap_no)
            else:
                up_string += str(this_flap_no)
                for _ in str(this_flap_no):
                    down_string += ' '
            if this_flap_no != flap_range[-1]: # if not last flap
                up_string += ' '
                down_string += ' '

        return up_string + '\n' + down_string

