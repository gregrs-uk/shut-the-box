#!/usr/bin/env python3

"""
Output the differences between the flap decision methods
make_flap_decision_highest and make_flap_decision_next_roll_probability
for combinations of flaps with length 4-9 i.e. always summing to more
than 6.
"""

import itertools
import shutthebox

DICE = shutthebox.Dice()

# 4-9 flaps i.e. always summing to more than 6
for length in range(9, 4 - 1, -1):
    for this_combination in itertools.combinations(range(1, 9 + 1), length):
        for this_dice_sum in range(2, 12 + 1):
            # prepare instance with particular flaps raised
            box = shutthebox.Box()
            turn = shutthebox.ComputerTurn(box, DICE)
            turn.box.lower_flaps_except(this_combination)

            highest = turn.make_flap_decision_highest(
                this_dice_sum,
                turn.make_num_dice_decision_one_if_poss)
            if highest is False: # not possible to lower any flaps
                break
            next_roll_prob = turn.make_flap_decision_next_roll_probability(
                this_dice_sum,
                turn.make_num_dice_decision_one_if_poss)

            highest.sort()
            next_roll_prob.sort()

            if highest != next_roll_prob:
                print("flaps:", this_combination)
                print("dice sum:", this_dice_sum)
                print("highest:", highest)
                print("next_roll_prob:", next_roll_prob, '\n')
