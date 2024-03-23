from random import randint

name = "final_scipt"

def get_quadrant(pirate, x, y):
    dimension_x = pirate.getDimensionX()
    dimension_y = pirate.getDimensionY()
    if x < dimension_x / 2:
        if y < dimension_y / 2:
            return 2
        return 3
    if y < dimension_y / 2:
        return 1
    return 4

def get_opposite_quadrant(quadrant):
    if quadrant == 1:
        return 3
    if quadrant == 2:
        return 4
    if quadrant == 3:
        return 1
    return 2

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

def scout_explore(pirate):
    # "North" is 1, "East" is 2, "South" is 3, "West" is 4
    x_dimension = pirate.getDimensionX()
    y_dimension = pirate.getDimensionY()
    x, y = pirate.getPosition()
    pirate_signal = list(pirate.getSignal())

    # whether home quadrant is explored or not is stored in index 6 of the pirate signal
    is_home_explored = pirate_signal[6] == "T"

    if is_home_explored:
        # Index 7 contains the quadrant being explored
        # Index 8 contains the direction being explored
        # Index 12 stores T if rebound is activated
        quadrant_exploring = int(pirate_signal[7])
        is_exploring_X = pirate_signal[8] == "T"
        if quadrant_exploring == 1:
            if is_exploring_X:
                if x == x_dimension - 1:
                    pirate_signal[12] = "T"
                    pirate.setSignal("".join(pirate_signal))
                # if x == 0:
                if x == x_dimension//2:
                    pirate_signal[12] = " "
                    pirate.setSignal("".join(pirate_signal))
                if pirate_signal[12] == "T":
                    return explore_side_quadrant(pirate, 4, [1, 3])
                return explore_side_quadrant(pirate, 2, [1, 3])

            if y == 0:
                pirate_signal[12] = "T"
                pirate.setSignal("".join(pirate_signal))
            # if y == y_dimension - 1:
            if y == y_dimension//2:
                pirate_signal[12] = " "
                pirate.setSignal("".join(pirate_signal))
            if pirate_signal[12] == "T":
                return explore_side_quadrant(pirate, 3, [2, 4])
            return explore_side_quadrant(pirate, 1, [2, 4])
        
        if quadrant_exploring == 2:
            if is_exploring_X:
                if x == 0:
                    pirate_signal[12] = "T"
                    pirate.setSignal("".join(pirate_signal))
                # if x == x_dimension - 1:
                if x == x_dimension//2:
                    pirate_signal[12] = " "
                    pirate.setSignal("".join(pirate_signal))
                if pirate_signal[12] == "T":
                    return explore_side_quadrant(pirate, 2, [1, 3])
                return explore_side_quadrant(pirate, 4, [1, 3])
        
            if y == 0:
                pirate_signal[12] = "T"
                pirate.setSignal("".join(pirate_signal))
            # if y == y_dimension - 1:
            if y == y_dimension//2:
                pirate_signal[12] = " "
                pirate.setSignal("".join(pirate_signal))
            if pirate_signal[12] == "T":
                return explore_side_quadrant(pirate, 3, [2, 4])
            return explore_side_quadrant(pirate, 1, [2, 4])
        
        if quadrant_exploring == 3:
            if is_exploring_X:
                if x == 0 :
                    pirate_signal[12] = "T"
                    pirate.setSignal("".join(pirate_signal))
                # if x == x_dimension - 1:
                if x == x_dimension//2:
                    pirate_signal[12] = " "
                    pirate.setSignal("".join(pirate_signal))
                if pirate_signal[12] == "T":
                    return explore_side_quadrant(pirate, 2, [1, 3])
                return explore_side_quadrant(pirate, 4, [1, 3])

            if y == y_dimension - 1:
                pirate_signal[12] = "T"
                pirate.setSignal("".join(pirate_signal))
            # if y == 0:
            if y == y_dimension//2:
                pirate_signal[12] = " "
                pirate.setSignal("".join(pirate_signal))
            if pirate_signal[12] == "T":
                return explore_side_quadrant(pirate, 1, [2, 4])
            return explore_side_quadrant(pirate, 3, [2, 4])
            
        if is_exploring_X:
            if x == x_dimension - 1 :
                pirate_signal[12] = "T"
                pirate.setSignal("".join(pirate_signal))
            # if x == 0:
            if x == x_dimension//2:
                pirate_signal[12] = " "
                pirate.setSignal("".join(pirate_signal))
            if pirate_signal[12] == "T":
                return explore_side_quadrant(pirate, 4, [1, 3])
            return explore_side_quadrant(pirate, 2, [1, 3])
                    
        if y == y_dimension - 1:
            pirate_signal[12] = "T"
            pirate.setSignal("".join(pirate_signal))
        # if y == 0:
        if y == y_dimension//2:
            pirate_signal[12] = " "
            pirate.setSignal("".join(pirate_signal))
        if pirate_signal[12] == "T":
            return explore_side_quadrant(pirate, 1, [2, 4])
        return explore_side_quadrant(pirate, 3, [2, 4])    

    # if the pirate has just completed home quadrant, switch to side quadrant exploration
    if x == x_dimension // 2 or y == y_dimension // 2:
        is_home_explored = True
        quadrant_exploring = None
        is_exploring_X = None
        current_move = None

        # determine which quadrant is the home quadrant
        deploy_x, deploy_y = pirate.getDeployPoint()
        
        def get_home_quadrant():
            if deploy_x < x_dimension / 2:
                if deploy_y < y_dimension / 2:
                    return 2
                return 3
            if deploy_y < y_dimension / 2:
                return 1
            return 4
        
        home_quadrant = get_home_quadrant()

        # TODO: Condense this
        if x == x_dimension // 2:
            if home_quadrant == 1:
                # gotta explore quadrant 4
                current_move = explore_side_quadrant(pirate, 3, [2, 4])
                quadrant_exploring = 2
                is_exploring_X = True
            elif home_quadrant == 2:
                # gotta explore quadrant 3
                current_move = explore_side_quadrant(pirate, 3, [2, 4])
                quadrant_exploring = 1
                is_exploring_X = True
            elif home_quadrant == 3:
                # gotta explore quadrant 2
                current_move = explore_side_quadrant(pirate, 1, [2, 4])
                quadrant_exploring = 4
                is_exploring_X = True
            else:
                # gotta explore quadrant 1
                current_move = explore_side_quadrant(pirate, 1, [2, 4])
                quadrant_exploring = 3
                is_exploring_X = True
        else:
            if home_quadrant == 1:
                # gotta explore quadrant 2
                current_move = explore_side_quadrant(pirate, 4, [1, 3])
                quadrant_exploring = 4
                is_exploring_X = False
            elif home_quadrant == 2:
                # gotta explore quadrant 1
                current_move = explore_side_quadrant(pirate, 2, [1, 3])
                quadrant_exploring = 3
                is_exploring_X = False
            elif home_quadrant == 3:
                # gotta explore quadrant 4
                current_move = explore_side_quadrant(pirate, 2, [1, 3])
                quadrant_exploring = 2
                is_exploring_X = False
            else:
                # gotta explore quadrant 3
                current_move = explore_side_quadrant(pirate, 4, [1, 3])
                quadrant_exploring = 1
                is_exploring_X = False

        # Index 7 contains the quadrant being explored
        # Index 8 contains the direction being explored
        pirate_signal[6] = "T"
        pirate_signal[7] = str(quadrant_exploring)
        pirate_signal[8] = "T" if is_exploring_X else "F"
        pirate.setSignal("".join(pirate_signal))
        return current_move
    
    # otherwise, explore the home quadrant
    if x < x_dimension / 2 and y < y_dimension / 2:
        return explore_main_quadrant(pirate, 2, 3)
    elif x < x_dimension / 2 and y > y_dimension / 2:
        return explore_main_quadrant(pirate, 2, 1)
    elif x > x_dimension / 2 and y < y_dimension / 2:
        return explore_main_quadrant(pirate, 4, 3)
    elif x > x_dimension / 2 and y > y_dimension / 2:
        return explore_main_quadrant(pirate, 4, 1)

def infiltrate(pirate):
    pirate_signal = list(pirate.getSignal())
    deploy_x, deploy_y = pirate.getDeployPoint()

    home_quadrant = get_quadrant(pirate, deploy_x, deploy_y)
    opponent_quadrant = get_opposite_quadrant(home_quadrant)
    
    if pirate_signal[7] == " ":
        pirate_signal[7] = str(home_quadrant)
    
    quadrant = int(pirate_signal[7])
    
    if quadrant == home_quadrant or quadrant == opponent_quadrant:
        return None
    
    def goto_edge(current_quadrant, target_quadrant):
        if current_quadrant == 1:
            if target_quadrant == 2:
                if pirate.investigate_up()[0] == "wall":
                    return None
                return 1
            # target_quadrant == 4
            if pirate.investigate_right()[0] == "wall":
                return None
            return 2
        if current_quadrant == 2:
            if target_quadrant == 1:
                if pirate.investigate_up()[0] == "wall":
                    return None
                return 1
            # target_quadrant == 3
            if pirate.investigate_left()[0] == "wall":
                return None
            return 4
        if current_quadrant == 3:
            if target_quadrant == 2:
                if pirate.investigate_left()[0] == "wall":
                    return None
                return 4
            # target_quadrant == 4
            if pirate.investigate_down()[0] == "wall":
                return None
            return 3
        # current_quadrant == 4
        if target_quadrant == 1:
            if pirate.investigate_right()[0] == "wall":
                return None
            return 2
        # target_quadrant == 3
        if pirate.investigate_down()[0] == "wall":
            return None
        return 3

    def goto_enemy_spawn(current_quadrant, opponent_quadrant):
        if opponent_quadrant == 1:
            if pirate.investigate_up()[0] == "wall" and pirate.investigate_right()[0] == "wall":
                return None
        if opponent_quadrant == 2:
            if pirate.investigate_up()[0] == "wall" and pirate.investigate_left()[0] == "wall":
                return None
        if opponent_quadrant == 3:
            if pirate.investigate_down()[0] == "wall" and pirate.investigate_left()[0] == "wall":
                return None
        # opponent_quadrant == 4
        if pirate.investigate_down()[0] == "wall" and pirate.investigate_right()[0] == "wall":
            return None
                
        if current_quadrant == 1:
            if opponent_quadrant == 2:
                return 4
            # opponent_quadrant == 4
            return 3
        if current_quadrant == 2:
            if opponent_quadrant == 1:
                return 2
            # opponent_quadrant == 3
            return 3
        if current_quadrant == 3:
            if opponent_quadrant == 2:
                return 1
            # opponent_quadrant == 4
            return 2
        # current_quadrant == 4
        if opponent_quadrant == 1:
            return 1
        # opponent_quadrant == 3
        return 4


    def find_enemy_island(opponent_quadrant):
        if opponent_quadrant == 1:
            return explore_main_quadrant(pirate, 3, 4)
        if opponent_quadrant == 2:
            return explore_main_quadrant(pirate, 2, 3)
        if opponent_quadrant == 3:
            return explore_main_quadrant(pirate, 1, 2)
        # opponent_quadrant == 4
        return explore_main_quadrant(pirate, 1, 4)
    
    has_infiltrated = pirate_signal[14] == "T"

    if not has_infiltrated:
        temp = goto_edge(quadrant, opponent_quadrant)
        if temp is not None:
            return temp
        
        temp = goto_enemy_spawn(quadrant, opponent_quadrant)
        if temp is not None:
            return temp
        
        has_infiltrated = True
        pirate_signal[14] = "T"
        pirate.setSignal("".join(pirate_signal))
    
    return find_enemy_island(opponent_quadrant)

def cipher(l):
    s = ""
    if type(l) is list:
        for item in l:
            if item != " ":
                s += chr(int(item) + 63)
            else:
                s += " "
        return s
    else:
        if l != " ":
            return chr(int(l) + 63)
        else:
            return " "

def decipher(s):
    if len(s) > 1:
        l = []
        for ch in s:
            if ch == " ":
                l.append(" ")
            else:
                l.append(ord(ch) - 63)
        return l
    else:
        if s != " ":
            return ord(s) - 63
        else:
            return " "

def moveTo(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1

def reduceFrames(team, island_no):
    team_signal = team.getTeamSignal()
    team_signal = team_signal[:5 + island_no] + chr(ord(team_signal[5 + island_no]) - 1) + team_signal[6 + island_no:]
    team.setTeamSignal(team_signal)

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

def resetPirateSignal(pirate):
    pirate_signal = pirate.getSignal()

    if pirate_signal[3] == pirate_signal[1]:            # Reset target location if target reached
        pirate_signal = pirate_signal[:3] + " " + pirate_signal[4:]
    if pirate_signal[4] == pirate_signal[2]:
        pirate_signal = pirate_signal[:4] + " " + pirate_signal[5:]
    pirate.setSignal(pirate_signal)

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

def intitializePirate(pirate):
    pirate_signal  = pirate.getSignal()
    if pirate_signal == "":                         # Initialization
        pirate_signal = cipher(int(pirate.getID())) + cipher(pirate.getPosition()[0]) + cipher(pirate.getPosition()[1]) + " "*97
        pirate.setSignal(pirate_signal)
    else:
        pirate_signal = pirate_signal[:1] + cipher(pirate.getPosition()[0]) + cipher(pirate.getPosition()[1]) + pirate_signal[3:]
    pirate.setSignal(pirate_signal)

def intitializeTeam(team):
    team_signal = team.getTeamSignal()
    no_of_pirates = int(team.getTotalPirates())

    if team_signal == "":               # Intitialization
        team_signal = " "*9 + cipher(no_of_pirates) + " "*90
        team.setTeamSignal(team_signal)
    
    team_signal = team_signal[:9] + cipher(no_of_pirates) + team_signal[10:]        #Updating no of pirates
    team.setTeamSignal(team_signal)

def gradualDefensePirate(pirate):
    
    # updateIslandCord(pirate)        # updates island coordiantes in team signal
    x, y = pirate.getPosition()
    team_signal = pirate.getTeamSignal()
    status = pirate.trackPlayers()
    no_of_pirates = decipher(team_signal[9])
    resetPirateSignal(pirate)

    for island_no in range(1,4):        #First loop to put a serpoint some tiles away and add it to team signal
        if status[island_no + 2] == "oppCapturing" and status[island_no - 1] == "myCaptured" and team_signal[5 + island_no] != " " and decipher(team_signal[5 + island_no]) > 0:
            for index in range(0,max(min(10,no_of_pirates//10),min(no_of_pirates,3))):
                if(team_signal[island_no*10+index] == cipher(int(pirate.getID()))):
                    island_x = decipher(team_signal[2*island_no-2])
                    island_y = decipher(team_signal[2*island_no-1])
                    pirate_signal = pirate.getSignal()
                    pirate_signal = pirate_signal[:3] + cipher(max(island_x-6,1)) + cipher(island_y) + pirate_signal[5:]
                    pirate_signal = pirate_signal[0] + cipher(x) + cipher(y) + pirate_signal[3:]
                    pirate.setSignal(pirate_signal)
                    return moveTo(decipher(pirate_signal[3]), decipher(pirate_signal[4]), pirate)

    for island_no in range(1,4):        #Once checkpoint reached push all pirates to interior of island
        if status[island_no+2] == "oppCapturing" and status[island_no - 1] == "myCaptured" and team_signal[5 + island_no] != " " and decipher(team_signal[5 + island_no]) <= 0:
            for index in range(0,max(min(10,no_of_pirates//10),min(no_of_pirates,3))):
                if(team_signal[island_no*10+index] == cipher(int(pirate.getID()))):
                    island_x = decipher(team_signal[2*island_no-2])
                    island_y = decipher(team_signal[2*island_no-1])
                    pirate_signal = pirate.getSignal()
                    pirate_signal = pirate_signal[:3] + cipher(island_x) + cipher(island_y) + pirate_signal[5:]
                    pirate_signal = pirate_signal[0] + cipher(x) + cipher(y) + pirate_signal[3:]
                    pirate.setSignal(pirate_signal)
                    return moveTo(decipher(pirate_signal[3]), decipher(pirate_signal[4]), pirate)

    return None

def gradualDefenseTeam(team):
    team_signal = team.getTeamSignal()
    no_of_pirates = int(team.getTotalPirates())
    for island_no in range(1,4):                # Updating closest 10 using closestN (wrt to assembly point)
        if team_signal[2*island_no - 2] != " " and team_signal[2*island_no - 1] != " ":
            island_x = decipher(team_signal[2*island_no - 2])
            island_y = decipher(team_signal[2*island_no - 1])
            assembly_x = max(island_x - 6, 1)
            assembly_y = island_y
            l = ClosestN(team, assembly_x, assembly_y, min(no_of_pirates,10))
            while len(l) != 10:
                l.append(" ")
            team_signal = team_signal[0:10*island_no] + cipher(l) + team_signal[10*(island_no + 1):]
            team.setTeamSignal(team_signal)

    team_signal = team.getTeamSignal()
    status = team.trackPlayers()

    for island_no in range(1,4):            # Reducing frames so that defense entry is coordinated
        if status[island_no + 2] == "oppCapturing" and team_signal[5 + island_no] != " ":
            reduceFrames(team, island_no)              #Reduces frames required to reach assembly point by 1 

    for island_no in range(1,4):            # if Opp capturing calculating frames to assemble at common defense point
        if team_signal[2*island_no - 2] != " " and status[2 + island_no] == "oppCapturing" and status[island_no - 1] == "myCaptured" and team_signal[5 + island_no] == " ":
            island_x = decipher(team_signal[2*island_no - 2])
            island_y = decipher(team_signal[2*island_no - 1])
            pirates_defending = max(min(10,no_of_pirates//10),min(no_of_pirates,3))
            calculateFrames(team, pirates_defending, island_no)

    team_signal = team.getTeamSignal()

    for island_no in range(1,4):        # Reset signal if island is defended successfully or if all pirates have died which is remaining
            if team_signal[5 + island_no] != " " and (status[2 + island_no] != "oppCapturing" or decipher(team_signal[5 + island_no]) == -60):
                team_signal = team_signal[:5 + island_no] + " " + team_signal[6 + island_no:]
                team.setTeamSignal(team_signal) 
        
def ActPirate(pirate):
    intitializePirate(pirate)
    updateIslandCord(pirate)

    # check for sahil's L-shape capture function (capturing home island)

    # check for rolling guard (capturing second island)
    
    # check for monk (defending captured islands)
    
    # check for gradual defense (defending islands whose monk has been killed)
    gradual_defense_move = gradualDefensePirate(pirate)
    if gradual_defense_move is not None:
        return gradual_defense_move

    # check for infiltrate (capturing third island if second island is oppCaptured)
    infiltrate_move = infiltrate(pirate)
    if infiltrate_move is not None:
        return infiltrate_move
    
    # check for exploration (in all other cases)
    return scout_explore(pirate)

        
def ActTeam(team):
    intitializeTeam(team)
    gradualDefenseTeam(team)

    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)