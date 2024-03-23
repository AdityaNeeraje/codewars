from utils.cipher import cipher

def updateIslandCord(pirate):
    up = pirate.investigate_up()[0]
    ne = pirate.investigate_ne()[0]
    nw = pirate.investigate_nw()[0]
    down = pirate.investigate_down()[0]
    se = pirate.investigate_se()[0]
    sw = pirate.investigate_sw()[0]
    right = pirate.investigate_right()[0]
    left = pirate.investigate_left()[0]
    x, y = pirate.getPosition()

    team_signal = pirate.getTeamSignal()

    if (up[:-1] == "island"):

        island_no = int(up[-1])

        if (up == ne and up == nw):
            island_x = x 
            island_y = y - 2
        elif (up == ne):
            island_x = x + 1
            island_y = y - 2
        else:
            island_x = x - 1
            island_y = y - 2
    
        if(team_signal[2*island_no-2] == " "):
            team_signal = team_signal[0:2*island_no-2] + cipher(island_x) + cipher(island_y) + team_signal[2*island_no:]

    elif (down[:-1] == "island"):

        island_no = int(down[-1])

        if (down == se and down == sw):
            island_x = x
            island_y = y + 2
        elif (down == se):
            island_x = x + 1
            island_y = y + 2
        else:
            island_x = x - 1
            island_y = y + 2

        if(team_signal[2*island_no-2] == " "):
            team_signal = team_signal[0:2*island_no-2] + cipher(island_x) + cipher(island_y) + team_signal[2*island_no:]

    elif (left[:-1] == "island"):

        island_no = int(left[-1])

        if (left == nw and left == sw):
            island_x = x - 2
            island_y = y
        elif (left == nw):
            island_x = x - 2
            island_y = y - 1
        else:
            island_x = x - 2
            island_y = y + 1

        if(team_signal[2*island_no-2] == " "):
            team_signal = team_signal[0:2*island_no-2] + cipher(island_x) + cipher(island_y) + team_signal[2*island_no:]

    elif (right[:-1] == "island"):

        island_no = int(right[-1])

        if(right == ne and right == se):
            island_x = x + 2
            island_y = y
        elif(right == ne):
            island_x = x + 2
            island_y = y - 1
        else:
            island_x = x + 2
            island_y = y + 1

        if(team_signal[2*island_no-2] == " "):
            team_signal = team_signal[0:2*island_no-2] + cipher(island_x) + cipher(island_y) + team_signal[2*island_no:]
    
    elif (ne[:-1] == "island"):

        island_no = int(ne[-1])

        island_x = x + 2
        island_y = y - 2

        if(team_signal[2*island_no-2] == " "):
            team_signal = team_signal[0:2*island_no-2] + cipher(island_x) + cipher(island_y) + team_signal[2*island_no:]

    elif (se[:-1] == "island"):

        island_no = int(se[-1])

        island_x = x + 2
        island_y = y + 2

        if(team_signal[2*island_no-2] == " "):
            team_signal = team_signal[0:2*island_no-2] + cipher(island_x) + cipher(island_y) + team_signal[2*island_no:]


    elif (nw[:-1] == "island"):

        island_no = int(nw[-1])

        island_x = x - 2
        island_y = y - 2

        if(team_signal[2*island_no-2] == " "):
            team_signal = team_signal[0:2*island_no-2] + cipher(island_x) + cipher(island_y) + team_signal[2*island_no:]

    elif (sw[:-1] == "island"):

        island_no = int(sw[-1])

        island_x = x - 2
        island_y = y + 2

        if(team_signal[2*island_no-2] == " "):
            team_signal = team_signal[0:2*island_no-2] + cipher(island_x) + cipher(island_y) + team_signal[2*island_no:]

    pirate.setTeamSignal(team_signal)