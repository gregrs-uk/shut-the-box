"""
Look for differences between the flap decision methods
make_flap_decision_highest and make_flap_decision_next_roll_probability.
"""

import shutthebox
import itertools

box = shutthebox.Box()
dice = shutthebox.Dice()

turn = shutthebox.ComputerTurn(box, dice)

for length in range(9, 4 - 1, -1):
    for this_combination in itertools.combinations(range(1, 9 + 1), length):
        for this_dice_sum in turn.dice_sum_probabilities.keys():
            highest = turn.make_flap_decision_highest(
                this_combination,
                this_dice_sum,
                turn.make_num_dice_decision_one_if_poss)
            if highest == False: break
            highest.sort()

            next_roll_prob = turn.make_flap_decision_next_roll_probability(
                this_combination,
                this_dice_sum,
                turn.make_num_dice_decision_one_if_poss)
            if next_roll_prob == False: break
            next_roll_prob.sort()

            if highest != next_roll_prob:
                print("flaps:", this_combination)
                print("dice sum:", this_dice_sum)
                print("highest:", highest)
                print("next_roll_prob:", next_roll_prob, '\n')
