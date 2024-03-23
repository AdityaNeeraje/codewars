from random import randint
import math
from utils.island_identification import updateIslandCord
from utils.pirate_initialization import intitializePirate
from utils.team_initialization_and_update import intitializeTeam
from utils.decipher import decipher
from utils.cipher import cipher
from final_script import get_quadrant
from utils.closestN import ClosestN


name = "attack1"

def moveTo(x , y , Pirate):
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
    
def id_of_close_5(team):
    team_signal = team.getTeamSignal()
    a, b = team.getDeployPoint()
    X = team.getDimensionX()
    Y = team.getDimensionY()
    for i in range(0, 5, 2):                                # i = 0, 2, 4
        island_x = decipher(team_signal[i])
        island_y = decipher(team_signal[i + 1])
        if(team_signal[i] != " " and abs(island_x - a) < X/2 and abs(island_y - b) < Y/2):
            pirate_list = ClosestN(team, island_x, island_y, min(team.getTotalPirates(), 5))
            team_signal = team_signal[:70] + cipher(pirate_list) + team_signal[75:]
            team.setTeamSignal(team_signal)
            

def Attack_1st_Island(pirate, i):
    team_signal = pirate.getTeamSignal()
    island_x = decipher(team_signal[i])             # r8 ?
    island_y = decipher(team_signal[i + 1])
    
    island_status = pirate.trackPlayers()
    x, y = pirate.getPosition()
    pirate_signal = pirate.getSignal()
    pirateID = decipher(pirate_signal[0])

    if(island_status[i/2] == '' and abs(x - island_x) < 3 and abs(y - island_y) < 3):
        # flag this pirate.
        time_counter = 0
        team_signal = team_signal[:69] + cipher(time_counter) + team_signal[70:]
        pirate.setTeamSignal(team_signal)

        return moveTo(island_x, island_y, pirate)
        
    elif(island_status[i/2] == 'myCapturing'):
        time_counter = decipher(team_signal[69]) + 1
        team_signal = team_signal[:69] + time_counter + team_signal[70:]
        pirate.setTeamSignal(team_signal)

        if(x == island_x and y == island_y):
            return randint(1, 4)
        elif(abs(x - island_x) < 2 and abs(y - island_y) < 2):
            return moveTo(island_x, island_y, pirate)
        elif( 85 > time_counter > 30 or 170 > time_counter > 115 ):
            quadrant = get_quadrant(pirate, island_x, island_y)
            
            for j in range(70, 75):
                if(decipher(pirate.getSignal()[j]) == pirateID):
                    if(quadrant == 1):
                        my_dict = { 0: (-1, 1) , 1: (-1, 0), 2: (0, 1), 3: (-1, -1), 4: (1, 1) }
                        return moveTo(island_x + my_dict[j - 70][0], island_y + my_dict[j - 70][1], pirate)
                    if(quadrant == 2):
                        my_dict = { 0: (1, 1) , 1: (1, 0), 2: (0, 1), 3: (1, -1), 4: (-1, 1) }
                        return moveTo(island_x + my_dict[j - 70][0], island_y + my_dict[j - 70][1], pirate)
                    if(quadrant == 3):
                        my_dict = { 0: (1, -1) , 1: (1, 0), 2: (0, -1), 3: (1, 1), 4: (-1, -1) }
                        return moveTo(island_x + my_dict[j - 70][0], island_y + my_dict[j - 70][1], pirate)
                    if(quadrant == 4):
                        my_dict = { 0: (-1, -1) , 1: (-1, 0), 2: (0, -1), 3: (-1, 1), 4: (1, -1) }
                        return moveTo(island_x + my_dict[j - 70][0], island_y + my_dict[j - 70][1], pirate)
                    


    else:
        return None
    


def attack_check(pirate):
    updateIslandCord(pirate)                    # updates island coordiantes in team signal
    team_signal = pirate.getTeamSignal()

    a, b = pirate.getDeployPoint()
    X = pirate.getDimensionX()
    Y = pirate.getDimensionY()

    for i in range(0, 5, 2):                                # i = 0, 2, 4
        island_x = decipher(team_signal[i])
        island_y = decipher(team_signal[i + 1])
        if(team_signal[i] != " " and abs(island_x - a) < X/2 and abs(island_y - b) < Y/2 ):
                return Attack_1st_Island(pirate, i)                           # home island

    return None


def ActPirate(pirate):
    intitializePirate(pirate)
    # scout and explore

    attack_check(pirate)


def ActTeam(team):
    intitializeTeam(team)

    id_of_close_5(team)

    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)