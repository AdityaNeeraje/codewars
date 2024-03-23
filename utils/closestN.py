from utils.cipher import cipher
from utils.decipher import decipher

def ClosestN(team, x, y, N):        #Returns list of decipher closest N pirates to a point. Need to cipher it if using for team signal

    x = int(x)
    y = int(y)
    distances = {}
    pirate_signals = team.getListOfSignals()

    for pirate_signal in pirate_signals:
        if len(pirate_signal) == 100:
            curr_x = decipher(pirate_signal[1])
            curr_y = decipher(pirate_signal[2])
            pirate_id = decipher(pirate_signal[0])
            distances[pirate_id] = abs(curr_x - x) + abs(curr_y - y)
    
    sorted_dist = dict(sorted(distances.items(), key=lambda item: item[1]))
    l = []

    for index in range(0,min(N,len(list(sorted_dist)))):
        l.append(list(sorted_dist)[index])

    return l