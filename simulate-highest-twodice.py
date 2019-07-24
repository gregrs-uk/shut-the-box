import shutthebox

box = shutthebox.Box()
dice = shutthebox.Dice()

turn = shutthebox.ComputerTurn(box, dice)

for n in range(0, 10000):
    print turn.perform_turn(
        flap_decision_method = turn.make_flap_decision_highest,
        num_dice_decision_method = turn.make_num_dice_decision_always_all
    )