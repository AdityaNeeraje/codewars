# CONCEPT OF PHASE:
# Any pirate who is on an island should constantly traverse all the cells of the island
# To do so, the motion of the pirate is divided into 12 phases
# In each move, the pirate makes the move that his phase number dictates
# The moves are as follows:
# [0]      [1]      [2]
# [5/11]   [4/10]   [3/9]
# [6]      [7]      [8]
# (Phase 11 moves towards the 0 cell and hence the loop completes)
# Also, there is a limit of atmost 3 people on an island

# PIRATE SIGNAL SYNTAX:
# If the pirate is on an island, the signal is "i" followed by the phase number
# The phase number is a number from 0 to 11 and is SEPARATED BY A ','

def get_phase(pirate):
    signal = pirate.getSignal()
    if signal and signal[0] == "i":
        return int(signal.split(",")[1])
    on_upper_edge = not pirate.investigate_up()[0].startswith("island")
    on_lower_edge = not pirate.investigate_down()[0].startswith("island")
    on_left_edge = not pirate.investigate_left()[0].startswith("island")
    on_right_edge = not pirate.investigate_right()[0].startswith("island")
    if on_upper_edge:
        if on_left_edge:
            return 0
        if on_right_edge:
            return 2
        return 1
    if on_lower_edge:
        if on_left_edge:
            return 6
        if on_right_edge:
            return 8
        return 7
    if on_left_edge:
        return 5
    if on_right_edge:
        return 3
    return 4
    

def defend_island(pirate):
    phase = get_phase(pirate)
    pirate.setSignal("i," + str((phase + 1) % 12))
    if phase in (8, 11):
        return 1
    if phase in (0, 1, 6, 7):
        return 2
    if phase in (2, 5):
        return 3
    return 4
