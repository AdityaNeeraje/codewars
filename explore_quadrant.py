from random import randint

percent_chance = lambda percent_chance: randint(1, 100) <= percent_chance

def explore_main_quadrant(pirate, move_1, move_2):
    pirate_signal = list(pirate.getSignal())

    # The information about the last move is stored in index 5 of the pirate signal   
    was_last_move_1 =  pirate_signal[5] == "T"
    current_move = None

    if percent_chance(75):
        current_move = move_1 if was_last_move_1 else move_2
    else:
        was_last_move_1 = not was_last_move_1
        current_move = move_2 if was_last_move_1 else move_1
    
    pirate_signal[5] = "T" if was_last_move_1 else "F"
    pirate.setSignal("".join(pirate_signal))
    return current_move

def explore_side_quadrant(pirate, primary_move, secondary_moves):
    sample = lambda collection: collection[randint(0, len(collection) - 1)]

    return primary_move if percent_chance(60) else sample(secondary_moves)