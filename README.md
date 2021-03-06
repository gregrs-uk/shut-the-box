# Shut the Box

A Python 3 implementation of the dice game, by default using the standard rules as described in the [Wikipedia article](https://en.wikipedia.org/wiki/Shut_the_Box): briefly using flaps numbered 1 to 9 and rolling two dice (optionally one die if the sum of the flaps is 6 or less). The score is the sum of the flaps still raised when the player's turn ends.

![Shut the box game](320px-Shut_the_box.jpg)

Scripts are provided to play the game interactively (`human-game.py`) or to simulate many games (`simulate-*.py`) and output the scores. In the case of simulation, 'decision' methods (e.g. `make_flap_decision_highest`) are used to decide how many dice to roll in the event of the sum of the flaps being 6 or less and which flaps to lower after each roll.

If you wish to use `make_flap_decision_bill` – which uses [Durango Bill](http://www.durangobill.com/ShutTheBox.html)'s optimal strategy – you will need to download his [text file](http://www.durangobill.com/ShutTheBoxExtra/STB_1DIE.txt), rename it to `bill-optimal-strategy.txt` and place it in the `shutthebox/` directory. It cannot be included in this repository because of copyright.

Unit tests are provided in the `shutthebox/tests/` directory for methods that don't require human input. Run them using `run-tests.sh`, which you may need to modify to run the appropriate `nosetests` command for Python 3 installed on your computer.

Pull requests are welcome, for example to provide further decision methods. Please check your code with [`pylint`](https://www.pylint.org) and provide unit tests.

Feel free to get in touch on [Twitter](https://twitter.com/gregrs_uk).

Copyright &copy; [gregrs-uk](https://gregrs-uk.github.io) 2018
