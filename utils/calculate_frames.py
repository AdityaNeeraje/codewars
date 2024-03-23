from utils.cipher import cipher
from utils.decipher import decipher

def calculateFrames(team, no_of_pirates_defending, island_no):
    pirate_signals = team.getListOfSignals()
    team_signal = team.getTeamSignal()
    island_x = decipher(team_signal[2*island_no - 2])
    island_y = decipher(team_signal[2*island_no - 1])

    for pirate_signal in pirate_signals:
        if pirate_signal[0] == team_signal[10*island_no + no_of_pirates_defending - 1]:
            curr_x = decipher(pirate_signal[1])
            curr_y = decipher(pirate_signal[2])
            time_frames_reqd = abs(curr_x - max(island_x-6,1)) + abs(curr_y - island_y)
            team_signal = team_signal[:5 + island_no] + cipher(time_frames_reqd) + team_signal[6 + island_no:]
            team.setTeamSignal(team_signal)
            break