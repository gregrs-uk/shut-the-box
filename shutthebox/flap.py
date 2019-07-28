class Flap:
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

