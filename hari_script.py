from random import randint

from utils.pirate_movements import moveTo, moveAway
# from utils.defend_island import defend_island

# TEAM SIGNAL FORMAT:
# "x1y1x2y2x3y3abcdef"
# x1, y1, x2, y2, x3, y3 are the coordinates of the islands. 
# If not known, they are "  " (2 spaces).
# If they are a single digit, they are followed by a space. (IMPORTANT)
# a: should be "1" if island 1 is to be attacked and " " if not.
# b: should be "2" if island 2 is to be attacked and " " if not.
# c: should be "3" if island 3 is to be attacked and " " if not.
# d: should be "1" if island 1 is to be defended and " " if not.
# e: should be "2" if island 2 is to be defended and " " if not.
# f: should be "3" if island 3 is to be defended and " " if not.

# PIRATE SIGNAL FORMAT:
# "S" - Scout
# "Ax" - Attacker for island x (x = 1, 2, 3)
# "Dx" - Defender for island x (x = 1, 2, 3)
# "P" - Passive Scout

# TODO: POINTS TO REVIEW:
# -> Movement of the attacker on an island
# -> Splitting (or not) of defenders when two islands are attacked at the same time
# -> Movement (or not) of defenders when an island is attacked (inside/outside, etc.)
# -> Percentage chance of scout becoming attacker vs. passive scout when an attack command is given
# -> Movement of the scout (always away from the deploy point, or different origin?)
# -> WHEN DOES A PASSIVE SCOUT TURN BACK TO SCOUT?
# -> Implement defender movement function defender_move(pirate)
# -> Implement attacke movement function attacker_move(pirate)

name = "hari_script"

def scout_move(pirate):
    deploy_x, deploy_y = pirate.getDeployPoint()
    pirate_x, pirate_y = pirate.getPosition()
    # if in the same quadrant as the deploy point, move away
    # else, move randomly
    is_deploy_left = deploy_x < 20
    is_deploy_top = deploy_y < 20
    is_pirate_left = pirate_x < 20
    is_pirate_top = pirate_y < 20
    if is_deploy_left == is_pirate_left and is_deploy_top == is_pirate_top:
        return moveAway(deploy_x, deploy_y, pirate)
    return randint(1, 4)

def defender_move(pirate): # TODO: IMPLEMENT DEFENDER MOVEMENT
    # TEMPORARY MEASURE: This is a naive approach where the defender just moves to the island
    # Actual implementation: The defender follows the exact same path as the previous defender (as discussed)
    island_number = int(pirate.getSignal()[1])
    # island 1's coords are stored in indices 0,1 and 2,3
    # island 2's coords are stored in indices 4,5 and 6,7
    # island 3's coords are stored in indices 8,9 and 10,11
    island_x = int(pirate.getTeamSignal()[island_number * 4 - 4:island_number * 4 - 2])
    island_y = int(pirate.getTeamSignal()[island_number * 4 - 2:island_number * 4])
    return moveTo(island_x, island_y, pirate)

# def attacker_move(pirate): TODO: IMPLEMENT ATTACKER MOVEMENT

def ActPirate(pirate):

    deploy_x, deploy_y = pirate.getDeployPoint()

    def store_island_coords(team_signal, current_location):
        island_number = int(current_location[-1])
        island_x, island_y = pirate.getPosition()

        # island 1's coords are stored in indices 0,1 and 2,3
        # island 2's coords are stored in indices 4,5 and 6,7
        # island 3's coords are stored in indices 8,9 and 10,11
        
        def stringify(num):
            num = str(num)
            if len(num) == 1:
                return num + " "
            return num
        
        def update(arr, index, value):
            arr[index] = value[0]
            arr[index + 1] = value[1]

        update(team_signal, island_number * 4 - 4, stringify(island_x))
        update(team_signal, island_number * 4 - 2, stringify(island_y))


    # newly created pirates are set to Scout by default
    if pirate.getSignal() == "":
        pirate.setSignal("S")
    
    pirate_signal = pirate.getSignal()
    team_signal = list(pirate.getTeamSignal())
    track = pirate.trackPlayers()

    if pirate_signal == "S":
        current_location = pirate.investigate_current()[0]

        # the scout first checks if he is on an island which is either neutral or enemy
        # if it is, he becomes of type Attacker
        if current_location.startswith("island") and track[int(current_location[-1]) - 1] != "myCaptured":
            island_number = int(current_location[-1])
            pirate_signal = f"A{island_number}"
            pirate.setSignal(pirate_signal)
            
            # store this island's location in the team signal
            store_island_coords(team_signal, current_location)
            
            # store "attack this island" on the team signal if not already done
            # 12, 13 and 14 are the indices of attack commands for islands 1, 2 and 3 respectively in the team signal
            team_signal[island_number + 11] = str(island_number)
            
            # convert the list back to string and update the team signal
            pirate.setTeamSignal("".join(team_signal))

            # TODO: attacker should not just stay on one spot, but should move around the island
            return 0 # temporary measure
        
        # next, the scout checks whether or not to become a defender
        # CURRENT IMPLEMENTATION:
        # If 1 island needs to be defended, 10% of the scouts become defenders.
        # If 2 islands need to be defended, 5% become defenders of each island.
        
        to_defend = [None, team_signal[15] != " ", team_signal[16] != " ", team_signal[17] != " "]

        def respond_to_defend(island_number_1, island_number_2=None):
            if island_number_2 is None:
                if not to_defend[island_number_1]:
                    return False
                
                if randint(1, 100) <= 10:
                    pirate_signal = f"D{island_number_1}"
                else:
                    pirate_signal = "P"
                
                return True
            
            if not to_defend[island_number_1] and not to_defend[island_number_2]:
                return False
            
            discriminator = randint(1, 100)
            
            if discriminator <= 5:
                pirate_signal = f"D{island_number_1}"
            elif discriminator <= 10:
                pirate_signal = f"D{island_number_2}"
            else:
                pirate_signal = "P"
            return True
        
        if respond_to_defend(1, 2) or respond_to_defend(1, 3) or respond_to_defend(2, 3) or respond_to_defend(1) or respond_to_defend(2) or respond_to_defend(3):
            pirate.setSignal(pirate_signal)
            if pirate_signal[0] == "D":
                # TODO: IMPLEMENT DEFENDER MOVEMENT
                # return defender_move(pirate)
                return 0 # temporary measure
            return scout_move(pirate)
                
        # next, the scout checks whether there is an attack command on the team signal
        # if there is, he has the chance to become Attacker
        # 12, 13 and 14 are the indices of attack commands for islands 1, 2 and 3 respectively in the team signal

        to_attack = [None, team_signal[12] != " ", team_signal[13] != " ", team_signal[14] != " "]

        def respond_to_attack(island_number_1, island_number_2=None, island_number_3=None):
            if island_number_2 is None:
                if not to_attack[island_number_1]:
                    return False
                
                if randint(1, 100) <= 50:
                    pirate_signal = f"A{island_number_1}"
                else:
                    pirate_signal = "P"
                
                return True
            
            if island_number_3 is None:
                if not to_attack[island_number_1] and not to_attack[island_number_2]:
                    return False
                
                discriminator = randint(1, 100)
                
                if discriminator <= 45:
                    pirate_signal = f"A{island_number_1}"
                elif discriminator <= 90:
                    pirate_signal = f"A{island_number_2}"
                else:
                    pirate_signal = "P"
                
                return True
            
            if not to_attack[island_number_1] and not to_attack[island_number_2] and not to_attack[island_number_3]:
                return False
            
            discriminator = randint(1, 100)
            
            if discriminator <= 33:
                pirate_signal = f"A{island_number_1}"
            elif discriminator <= 66:
                pirate_signal = f"A{island_number_2}"
            elif discriminator <= 99:
                pirate_signal = f"A{island_number_3}"
            else:
                pirate_signal = "P"
            
            return True
        
        if respond_to_attack(1, 2, 3) or respond_to_attack(1, 2) or respond_to_attack(1, 3) or respond_to_attack(2, 3) or respond_to_attack(1) or respond_to_attack(2) or respond_to_attack(3):
            pirate.setSignal(pirate_signal)
            if pirate_signal[0] == "A":
                # TODO: movement of attacker: Write this function
                # attacker_move()
                return 0 # temporary measure
            return scout_move(pirate)
        
        # if none of the above conditions are met, the scout explores
        return scout_move(pirate)
    
    elif pirate_signal[0] == "A":
        island_number = int(pirate_signal[1])
        # if not known before, this island's location should be stored in the team signal
        # island 1's coords are stored in indices 0,1 and 2,3
        # island 2's coords are stored in indices 4,5 and 6,7
        # island 3's coords are stored in indices 8,9 and 10,11
        if(team_signal[island_number * 4 - 4] == " "):
            current_location = pirate.investigate_current()[0]
            store_island_coords(team_signal, current_location)
        
        # check whether the island has been captured yet
        # if it has, the attacker becomes a scout
        if track[island_number - 1] == "myCaptured":
            pirate_signal = "S"
            pirate.setSignal(pirate_signal)
            return scout_move(pirate)
        
        # set in the team signal to attack the current island
        team_signal[island_number + 11] = str(island_number)

        # convert the list back to string and update the team signal
        pirate.setTeamSignal("".join(team_signal))

        # TODO: movement of attacker: Write this function
        # attacker_move()
        return 0 # temporary measure
    
    elif pirate_signal[0] == "D":
        island_to_defend = int(pirate_signal[1])
        # checking whether the island has been successfully defended
        # if so, no longer a need to defend the island
        if track[island_to_defend - 1] == "myCaptured" and track[island_to_defend + 2] != "oppCapturing":
            pirate_signal = "S"
            pirate.setSignal(pirate_signal)
            return scout_move(pirate)
        
        # else, the defender should take the exact same route as previous defenders
        # this logic needs to be implemented in the move_defender function
        return defender_move(pirate)
    
    # we now know that the pirate is a passive scout (P)
    # TODO: review when the passive scout should turn back to scout
    # TEMPOARY MEASURE: The passive scout becomes a scout after sensing no attack/defend signals
    # This is very naive and not a good approach
    if team_signal[12:15] == "   " and team_signal[15:18] == "   ":
        pirate_signal = "S"
        pirate.setSignal(pirate_signal)
    
    return scout_move(pirate)
    

def ActTeam(team):
    team.setTeamSignal(" " * 18)
    pass