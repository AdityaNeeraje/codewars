from utils.decipher import decipher

def NoOfPiratesAssembled(x ,y, team):             # Counts the numbers of pirates at a point

    x = int(x)
    y = int(y)

    cnt=0
    pirate_signals = team.getListOfSignals()

    for pirate_signal in pirate_signals:
        curr_x = decipher(pirate_signal[1])
        curr_y = decipher(pirate_signal[2])
        if curr_x == x and curr_y == y:
            cnt += 1
            
    return cnt