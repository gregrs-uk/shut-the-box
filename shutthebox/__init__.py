"""
A Python 3 implementation of the dice game Shut the Box
"""

import sys

if sys.version_info.major < 3: # pragma: no cover
    sys.exit('Python 3 is required. You are currently using Python ' +
             str(sys.version_info.major) + '.' +
             str(sys.version_info.minor) + '.')

from .flap import Flap
from .dice import Dice
from .box import Box
from .turn import Turn
from .humanturn import HumanTurn
from .computerturn import ComputerTurn

