import random
import math
import signal

from engine import island, pirate

name = "script"

# Into the team signal
island_pos = {
    'island1': (0, 0),
    'island2': (0, 0),
    'island3': (0, 0)
}

pirates_on_islands = 0

deploy_guards = {} # This has the id of every living guard as a key and their position and direction relative to island center as values.
colonists = {} # This has the id of every living colonist as a key and the coordinate of their island center as value
pirates = {} # This has the id of every living pirate as a key and the generating frame and coordinates as values
assassins = []
earlier_list_of_signals = []
possible_positions = {id: {} for id in range(78)} # subtract frame from the current frame to get the id number (maybe +1)
reached_end = False
destination_visits = [(x, y) for x in range(40) for y in range(40)]
random.shuffle(destination_visits)
destination_visits = {
    pos: 0 for pos in destination_visits
}
destinations_for_actors = {}

# Our resources
gunPowder = 0
rum = 0
wood = 0

# pirate_pos = dict()
pirate_goal = dict()
island_pos = dict()

def sig_decode(signal:str):
    dec_data = dict()
    # Encode string to bytes
    byte_data = signal.encode('utf-8')
    # Convert bytes to binary string
    binary_str = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_str
    pass

def ActAsGuard(x, y, pirate, dir_island):
    up = pirate.investigate_up()[1]
    down = pirate.investigate_down()[1]
    left = pirate.investigate_left()[1]
    right = pirate.investigate_right()[1]
    ne = pirate.investigate_ne()[1]
    nw = pirate.investigate_nw()[1]
    se = pirate.investigate_se()[1]
    sw = pirate.investigate_sw()[1]
    # pirate.setSignal(pirate.getSignal()[0] + str(x) + "," + str(y))
    if (dir_island=='up'):
        if (up == 'enemy'):
            return moveTo(x, y-1, pirate)
        elif (ne == 'enemy' or nw == 'enemy'):
            return moveTo(x, y-1, pirate)
        if (left == 'enemy'):
            return moveTo(x-1, y, pirate)
        elif (right == 'enemy'):
            return moveTo(x+1, y, pirate)
        elif (down == 'enemy'):
            return moveTo(x, y+1, pirate)
        elif (sw == 'enemy'):
            return moveTo(x-1, y, pirate)
        elif (se == 'enemy'):
            return moveTo(x+1, y, pirate)
    if (dir_island=='down'):
        if (down == 'enemy'):
            return moveTo(x, y+1, pirate)
        elif (se == 'enemy' or sw == 'enemy'):
            return moveTo(x, y+1, pirate)
        if (left == 'enemy'):
            return moveTo(x-1, y, pirate)
        elif (right == 'enemy'):
            return moveTo(x+1, y, pirate)
        elif (up == 'enemy'):
            return moveTo(x, y-1, pirate)
        elif (nw == 'enemy'):
            return moveTo(x-1, y, pirate)
        elif (ne == 'enemy'):
            return moveTo(x+1, y, pirate)
    if (dir_island=='left'):
        if (left == 'enemy'):
            return moveTo(x-1, y, pirate)
        elif (nw == 'enemy' or sw == 'enemy'):
            return moveTo(x-1, y, pirate)
        elif (right == 'enemy'):
            return moveTo(x+1, y, pirate)
        elif (down == 'enemy'):
            return moveTo(x, y+1, pirate)
        elif (up == 'enemy'):
            return moveTo(x, y-1, pirate)
        elif (ne == 'enemy'):
            return moveTo(x, y-1, pirate)
        elif (se == 'enemy'):
            return moveTo(x, y+1, pirate)
    if (dir_island=='right'):
        if (right == 'enemy'):
            return moveTo(x+1, y, pirate)
        elif (ne == 'enemy' or se == 'enemy'):
            return moveTo(x+1, y, pirate)
        if (left == 'enemy'):
            return moveTo(x-1, y, pirate)
        elif (down == 'enemy'):
            return moveTo(x, y+1, pirate)
        elif (up == 'enemy'):
            return moveTo(x, y-1, pirate)
        elif (nw == 'enemy'):
            return moveTo(x, y-1, pirate)
        elif (sw == 'enemy'):
            return moveTo(x, y+1, pirate)
    return moveTo(x, y, pirate)

# Move a pirate to a given position
def moveTo(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if random.randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1

# Move a pirate away from a given position
def moveAway(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return random.randint(1, 4)
    if random.randint(1, 2) == 1:
        return (position[0] < x) * 2 + 2
    else:
        return (position[1] > y) * 2 + 1

# Move a pirate in a circle around a given position
def circleAround(x, y, radius, Pirate, initial="abc", clockwise=True):
    position = Pirate.getPosition()
    rx = position[0]
    ry = position[1]
    pos = [[x + i, y + radius] for i in range(-1 * radius, radius + 1)]
    pos.extend([[x + radius, y + i] for i in range(radius - 1, -1 * radius - 1, -1)])
    pos.extend([[x + i, y - radius] for i in range(radius - 1, -1 * radius - 1, -1)])
    pos.extend([[x - radius, y + i] for i in range(-1 * radius + 1, radius)])
    if [rx, ry] not in pos:
        if initial != "abc":
            return moveTo(initial[0], initial[1], Pirate)
        if rx in [x + i for i in range(-1 * radius, radius + 1)] and ry in [
            y + i for i in range(-1 * radius, radius + 1)
        ]:
            return moveAway(x, y, Pirate)
        else:
            return moveTo(x, y, Pirate)
    else:
        index = pos.index([rx, ry]) 
        return moveTo(
            pos[(index + (clockwise * 2) - 1) % len(pos)][0],
            pos[(index + (clockwise * 2) - 1) % len(pos)][1],
            Pirate,
        )

# Check if a pirate is next to an island
def checkIsland(pirate):
    global island_pos
    if 'island1' not in island_pos:
        island_pos['island1'] = (0, 0)
    if 'island2' not in island_pos:
        island_pos['island2'] = (0, 0)
    if 'island3' not in island_pos:
        island_pos['island3'] = (0, 0)
    # print(island_pos)
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    if island_pos['island1'] != (0, 0) and island_pos['island2'] != (0, 0) and island_pos['island3'] != (0, 0):
        if (up[0:-1] == "island" or down[0:-1] == "island") and (left[0:-1] == "island" or right[0:-1] == "island"):
            return True
        else:
            return False

    nw = pirate.investigate_nw()
    ne = pirate.investigate_ne()
    se = pirate.investigate_se()
    sw = pirate.investigate_sw()

    if nw[0][0:-1] == "island" and up[0] == "blank" and left[0] == "blank":
        # print('Hello!!!')
        island_pos[nw[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] - 2)
    if ne[0][0:-1] == "island" and up[0] == "blank" and right[0] == "blank":
        # print('Hello!!!')
        island_pos[ne[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] - 2)
    if se[0][0:-1] == "island" and down[0] == "blank" and right[0] == "blank":
        # print('Hello!!!')
        island_pos[se[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] + 2)
    if sw[0][0:-1] == "island" and down[0] == "blank" and left[0] == "blank":
        # print('Hello!!!')
        island_pos[sw[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] + 2)
    if up[0][0:-1] == "island" and nw[0][0:-1] == "island" and ne[0][0:-1] == "island" and right[0] == "blank" and left[0] == "blank":
        # print('Hello!!!')
        island_pos[up[0]] = (pirate.getPosition()[0], pirate.getPosition()[1] - 2)
    if left[0][0:-1] == "island" and nw[0][0:-1] == "island" and sw[0][0:-1] == "island" and up[0] == "blank" and down[0] == "blank":
        # print('Hello!!!')
        island_pos[left[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1])
    if down[0][0:-1] == "island" and sw[0][0:-1] == "island" and se[0][0:-1] == "island" and right[0] == "blank" and left[0] == "blank":
        # print('Hello!!!')
        island_pos[down[0]] = (pirate.getPosition()[0], pirate.getPosition()[1] + 2)
    if right[0][0:-1] == "island" and ne[0][0:-1] == "island" and se[0][0:-1] == "island" and up[0] == "blank" and down[0] == "blank":
        # print('Hello!!!')
        island_pos[right[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1])
    if up[0][:-1] == "island" and nw[0][:-1] == "island" and ne[0] == "blank" and left[0] == "blank" and right[0] == "blank":
        island_pos[up[0]] = (pirate.getPosition()[0] - 1, pirate.getPosition()[1] - 2)
    if up[0][:-1] == "island" and ne[0][:-1] == "island" and nw[0] == "blank" and right[0] == "blank" and left[0] == "blank":
        island_pos[up[0]] = (pirate.getPosition()[0] + 1, pirate.getPosition()[1] - 2)
    if left[0][:-1] == "island" and nw[0][:-1] == "island" and sw[0] == "blank" and up[0] == "blank" and down[0] == "blank":
        island_pos[left[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] - 1)
    if left[0][:-1] == "island" and sw[0][:-1] == "island" and nw[0] == "blank" and up[0] == "blank" and down[0] == "blank":
        island_pos[left[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] + 1)
    if down[0][:-1] == "island" and sw[0][:-1] == "island" and se[0] == "blank" and left[0] == "blank" and right[0] == "blank":
        island_pos[down[0]] = (pirate.getPosition()[0] - 1, pirate.getPosition()[1] + 2)
    if down[0][:-1] == "island" and se[0][:-1] == "island" and sw[0] == "blank" and left[0] == "blank" and right[0] == "blank":
        island_pos[down[0]] = (pirate.getPosition()[0] + 1, pirate.getPosition()[1] + 2)
    if right[0][:-1] == "island" and ne[0][:-1] == "island" and se[0] == "blank" and up[0] == "blank" and down[0] == "blank":
        island_pos[right[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] - 1)
    if right[0][:-1] == "island" and se[0][:-1] == "island" and ne[0] == "blank" and up[0] == "blank" and down[0] == "blank":
        island_pos[right[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] + 1)\

    # if ne[0:-1] == "island" and up[0:-1] == "blank" and right[0:-1] == "blank":
    #     print('Hello!!!')
    #     island_pos[ne[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] - 2)
    # if se[0:-1] == "island" and down[0:-1] == "blank" and right[0:-1] == "blank":
    #     print('Hello!!!')
    #     island_pos[se[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] + 2)
    # if sw[0:-1] == "island" and down[0:-1] == "blank" and left[0:-1] == "blank":
    #     print('Hello!!!')
    #     island_pos[sw[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] + 2)
    # if up[0:-1] == "island" and nw[0:-1] == "island" and ne[0:-1] == "island":
    #     print('Hello!!!')
    #     island_pos[up[0]] = (pirate.getPosition()[0], pirate.getPosition()[1]-2)
    # if left[0:-1] == "island" and nw[0:-1] == "island" and sw[0:-1] == "island":
    #     print('Hello!!!')
    #     island_pos[left[0]] = (pirate.getPosition()[0]-2, pirate.getPosition()[1])
    # if down[0:-1] == "island" and sw[0:-1] == "island" and se[0:-1] == "island":
    #     print('Hello!!!')
    #     island_pos[down[0]] = (pirate.getPosition()[0], pirate.getPosition()[1]+2)
    # if right[0:-1] == "island" and ne[0:-1] == "island" and se[0:-1] == "island":
    #     print('Hello!!!')
    #     island_pos[right[0]] = (pirate.getPosition()[0]+2, pirate.getPosition()[1])
    # print(island_pos)


    if (up[0:-1] == "island" or down[0:-1] == "island") and (left[0:-1] == "island" or right[0:-1] == "island"):
        return True
    else:
        return False

def ActColonist(pirate):
    global pirate_pos, island_pos, colonists
    id = int(pirate.getID())
    for island in colonists:
        if id in colonists[island]:
            if colonists[island][0] == id:
                return moveTo(island_pos[island][0], island_pos[island][1], pirate)
            elif colonists[island][1] == id:
                return circleAround(island_pos[island][0], island_pos[island][1], 1, pirate, (island_pos[island][0] + 1, island_pos[island][1] + 1))
            else:
                return circleAround(island_pos[island][0], island_pos[island][1], 1, pirate, (island_pos[island][0] - 1, island_pos[island][1] - 1))
    pass

def update_game_state(team):
    global current_game_state
    captured_count = sum(1 for status in team.trackPlayers() if status == "myCaptured")
    capturing_count = sum(1 for status in team.trackPlayers() if status == "myCapturing")
    
    if captured_count == 1:
        current_game_state = GameState.ONE_ISLAND
    elif captured_count == 2:
        current_game_state = GameState.TWO_ISLANDS
    elif capturing_count > 0:
        current_game_state = GameState.CAPTURING
    else:
        current_game_state = GameState.START

def check_game_state():
    global current_game_state
    return current_game_state

# Get the closest n pirates to a given position
def closest_n_pirates(x, y, n, pirate_pos):
    # pirates = pirate_pos.keys()
    # pirates.sort(key=lambda p: abs(p.getPosition()[0] - x) + abs(p.getPosition()[1] - y))
    pirates = {k: v for k, v in sorted(pirate_pos.items(), key=lambda item: abs(item[1][0] - x) + abs(item[1][1] - y))}
    return list(pirates.keys())[:n]

def checkfriends(pirate , quad ):
    sum = 0 
    up = pirate.investigate_up()[1]
    # print(up)
    down = pirate.investigate_down()[1]
    left = pirate.investigate_left()[1]
    right = pirate.investigate_right()[1]
    ne = pirate.investigate_ne()[1]
    nw = pirate.investigate_nw()[1]
    se = pirate.investigate_se()[1]
    sw = pirate.investigate_sw()[1]
    
    if(quad=='ne'):
        if(up == 'friend'):
            sum +=1 
        if(ne== 'friend'):
            sum +=1 
        if(right == 'friend'):
            sum +=1 
    if(quad=='se'):
        if(down == 'friend'):
            sum +=1 
        if(right== 'friend'):
            sum +=1 
        if(se == 'friend'):
            sum +=1 
    if(quad=='sw'):
        if(down == 'friend'):
            sum +=1 
        if(sw== 'friend'): 
            sum +=1 
        if(left == 'friend'):
            sum +=1 
    if(quad=='nw'):
        if(up == 'friend'):
            sum +=1 
        if(nw == 'friend'):
            sum +=1 
        if(left == 'friend'):
            sum +=1 

    return sum

def ActGuard(x,y,pirate,dir):
    up = pirate.investigate_up()[1]
    down = pirate.investigate_down()[1]
    left = pirate.investigate_left()[1]
    right = pirate.investigate_right()[1]
    ne = pirate.investigate_ne()[1]
    nw = pirate.investigate_nw()[1]
    se = pirate.investigate_se()[1]
    sw = pirate.investigate_sw()[1]
    if dir == 'up':
        if up == 'enemy':
            return moveTo(x, y-1, pirate)
        elif ne == 'enemy' or nw == 'enemy':
            return moveTo(x, y-1, pirate)
        if left == 'enemy':
            return moveTo(x-1, y, pirate)
        elif right == 'enemy':
            return moveTo(x+1, y, pirate)
        elif down == 'enemy':
            return moveTo(x, y+1, pirate)
        elif sw == 'enemy':
            return moveTo(x-1, y, pirate)
        elif se == 'enemy':
            return moveTo(x+1, y, pirate)
    if dir == 'left':
        if left == 'enemy':
            return moveTo(x-1, y, pirate)
        elif nw == 'enemy' or sw == 'enemy':
            return moveTo(x-1, y, pirate)
        if up == 'enemy':
            return moveTo(x, y-1, pirate)
        elif down == 'enemy':
            return moveTo(x, y+1, pirate)
        elif right == 'enemy':
            return moveTo(x+1, y, pirate)
        elif ne == 'enemy':
            return moveTo(x, y-1, pirate)
        elif se == 'enemy':
            return moveTo(x, y+1, pirate)
    if dir == 'down':
        if down == 'enemy':
            return moveTo(x, y+1, pirate)
        elif se == 'enemy' or sw == 'enemy':
            return moveTo(x, y+1, pirate)
        if left == 'enemy':
            return moveTo(x-1, y, pirate)
        elif right == 'enemy':
            return moveTo(x+1, y, pirate)
        elif up == 'enemy':
            return moveTo(x, y-1, pirate)
        elif nw == 'enemy':
            return moveTo(x-1, y, pirate)
        elif ne == 'enemy':
            return moveTo(x+1, y, pirate)
    if dir == 'right':
        if right == 'enemy':
            return moveTo(x+1, y, pirate)
        elif ne == 'enemy' or se == 'enemy':
            return moveTo(x+1, y, pirate)
        if left == 'enemy':
            return moveTo(x-1, y, pirate)
        elif down == 'enemy':
            return moveTo(x, y+1, pirate)
        elif up == 'enemy':
            return moveTo(x, y-1, pirate)
        elif nw == 'enemy':
            return moveTo(x-1, y, pirate)
        elif sw == 'enemy':
            return moveTo(x, y+1, pirate)
    return moveTo(x, y, pirate)

def spread(pirate):
    sw = checkfriends(pirate ,'sw' )
    se = checkfriends(pirate ,'se' )
    ne = checkfriends(pirate ,'ne' )
    nw = checkfriends(pirate ,'nw' )
   
    my_dict = {'sw': sw, 'se': se, 'ne': ne, 'nw': nw}
    sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1]))

    x, y = pirate.getPosition()
    
    if( x == 0 , y == 0):
        return random.randint(1,4)
    
    if(sorted_dict[list(sorted_dict())[3]] == 0 ):
        return random.randint(1,4)
    
    if(list(sorted_dict())[0] == 'sw'):
        return moveTo(x-1 , y+1 , pirate)
    elif(list(sorted_dict())[0] == 'se'):
        return moveTo(x+1 , y+1 , pirate)
    elif(list(sorted_dict())[0] == 'ne'):
        return moveTo(x+1 , y-1 , pirate)
    elif(list(sorted_dict())[0] == 'nw'):
        return moveTo(x-1 , y-1 , pirate)

def setthem(pirate):
    s = pirate.GetCurrentPosition()
    x = s[0]
    y = s[1]

b = 0

def positionInIsland(pirate):
    up = pirate.investige_up()
    down = pirate.investige_down()
    right = pirate.investige_right()
    left = pirate.investige_left()
    x, y = pirate.getPosition()
    if up[0:-1] == "island" and down[0:-1] == "island" and right[0:-1] == "island" and left[0:-1] == "island":
        return "centre"   
    if up[0:-1] != "island" and right[0:-1] == "island" and left[0:-1] != "island" and down[0:-1] == "island":
        return "topleft"
    if up[0:-1] != "island" and right[0:-1] != "island" and left[0:-1] == "island" and down[0:-1] == "island":
        return "topright"
    if up[0:-1] == "island" and right[0:-1] != "island" and left[0:-1] == "island" and down[0:-1] != "island":
        return "bottomright"
    if up[0:-1] == "island" and right[0:-1] == "island" and left[0:-1] != "island" and down[0:-1] != "island":
        return "bottomleft"
    if up[0:-1] == "island" and down[0:-1] == "island" and left[0:-1] == "island" and right[0:-1] != "island":
        return "middleright"
    if up[0:-1] == "island" and down[0:-1] == "island" and left[0:-1] != "island" and right[0:-1] == "island":
        return "middleleft"
    if up[0:-1] != "island" and down[0:-1] == "island" and left[0:-1] == "island" and right[0:-1] == "island":
        return "topmiddle"
    if up[0:-1] == "island" and down[0:-1] != "island" and left[0:-1] == "island" and right[0:-1] == "island":
        return "bottommiddle"

def ActPirate(pirate):
    global assassins, gunPowder, rum, wood, possible_positions, destinations_for_actors, destination_visits
    p = list(pirate.getDeployPoint())
    id = int(pirate.getID())
    pirate.setSignal(f"{id},{pirate.getPosition()[0]},{pirate.getPosition()[1]}")
    dimensionX = pirate.getDimensionX()
    dimensionY = pirate.getDimensionY()
    if pirate.getID() not in pirates:
       pirates[pirate.getID()] = [pirate.getCurrentFrame(), p[0], p[1]]
    frame = pirate.getCurrentFrame() - pirates[str(id)][0]
    curr_frame = pirate.getCurrentFrame()
    if id in assassins:
        if id == assassins[0]: #Instead, let actteam return the string a1 for the first assassin
            # print(dimensionX-p[0], dimensionY-1-p[1], pirate.getPosition())
            return moveTo(dimensionX-1-p[0], dimensionY-2-p[1], pirate)
        elif id == assassins[1]: #Instead, let actteam return the string a2 for the second assassin
            return moveTo(dimensionX-2-p[0], dimensionY-1-p[1], pirate)
        elif gunPowder > 100 or id%2 == 1:
            return moveTo(dimensionY-1-p[0], dimensionX-1-p[1], pirate)
        else:
            return moveTo(dimensionX-2-p[0], dimensionY-2-p[1], pirate)

    for island in colonists:
        if id in colonists[island]:
            # print(f'Acting colonist {id} on {island}')
            # print(f'Colonists: {colonists}')
            # print(island_pos)
            return ActColonist(pirate)
    # if id in :
    #     print(f'Acting colonist')
    #     print(f'Colonists: {colonists}')
    #     # print(f'Ghosts: {}')
    #     return ActColonist(pirate)
    
    if id in deploy_guards:
        return ActGuard(deploy_guards[id][0], deploy_guards[id][1], pirate, deploy_guards[id][2])
    
    checkIsland(pirate=pirate)

    if not reached_end and possible_positions:
        index = abs(pirate.getPosition()[0]-pirate.getDeployPoint()[0]) + abs(pirate.getPosition()[1]-pirate.getDeployPoint()[1])
        # print(index, possible_positions[index])
        # If position is x, y and start is start_x, start_y, then possible_positions x-start_x + y - start_y is needed
        if pirate.getDeployPoint()[0] != pirate.getDeployPoint()[1]:
            if id%3 == 0:
                some_dict = dict(sorted({key: value for key, value in \
                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], random.random())))
            elif id%3 == 1:
                some_dict = dict(sorted({key: value for key, value in \
                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
            elif id%3 == 2:
                some_dict = dict(sorted({key: value for key, value in \
                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], -x[0][1])))
        else:
            if id%3 == 0:
                some_dict = dict(sorted({key: value for key, value in \
                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], random.random())))
            elif id %3 == 1:
                some_dict = dict(sorted({key: value for key, value in \
                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
            elif id%3 == 2:
                some_dict = dict(sorted({key: value for key, value in \
                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][1]))
            )
        choice = list(some_dict.keys())[0]
        possible_positions[index][choice] += 1
        return moveTo(choice[0], choice[1], pirate)
        
    if id%10 == 1:
        if p[0] == 0 and p[1] == 0:
            p[1] = 8
        elif p[0] == 0 and p[1] == 39:
            p[0] = 8
        elif p[0] == 39 and p[1] == 39:
            p[1] = 31
        elif p[0] == 39 and p[1] == 0:
            p[0] = 31
    if id%10 == 2:
        if p[0] == 0 and p[1] == 0:
            p[1] = 16
        elif p[0] == 0 and p[1] == 39:
            p[0] = 16
        elif p[0] == 39 and p[1] == 39:
            p[1] = 23
        elif p[0] == 39 and p[1] == 0:
            p[0] = 23
    if id%10 == 3:
        if p[0] == 0 and p[1] == 0:
            p[1] = 24
        elif p[0] == 0 and p[1] == 39:
            p[0] = 24
        elif p[0] == 39 and p[1] == 39:
            p[1] = 15
        elif p[0] == 39 and p[1] == 0:
            p[0] = 15
    if id%10 == 4:
        if p[0] == 0 and p[1] == 0:
            p[1] = 32
        elif p[0] == 0 and p[1] == 39:
            p[0] = 32
        elif p[0] == 39 and p[1] == 39:
            p[1] = 7
        elif p[0] == 39 and p[1] == 0:
            p[0] = 7
    if id%10 == 5:
            if p[0] == 0 and p[1] == 0:
                p[0] = 8
            elif p[0] == 0 and p[1] == 39:
                p[1] = 31
            elif p[0] == 39 and p[1] == 39:
                p[0] = 31
            elif p[0] == 39 and p[1] == 0:
                p[1] = 8
    if id%10 == 6:
        if p[0] == 0 and p[1] == 0:
            p[0] = 16
        elif p[0] == 0 and p[1] == 39:
            p[1] = 23
        elif p[0] == 39 and p[1] == 39:
            p[0] = 23
        elif p[0] == 39 and p[1] == 0:
            p[1] = 16
    if id%10 == 7:
        if p[0] == 0 and p[1] == 0:
            p[0] = 24
        elif p[0] == 0 and p[1] == 39:
            p[1] = 15
        elif p[0] == 39 and p[1] == 39:
            p[0] = 15
        elif p[0] == 39 and p[1] == 0:
            p[1] = 24   
    if id%10 == 8:
        if p[0] == 0 and p[1] == 0:
            p[0] = 32
        elif p[0] == 0 and p[1] == 39:
            p[1] = 7
        elif p[0] == 39 and p[1] == 39:
            p[0] = 7
        elif p[0] == 39 and p[1] == 0:
            p[1] = 32    
            

    if frame > 600:
        # print("HERE")
        p = pirate.getDeployPoint()
    # if (frame < 75):
    #     return moveTo(39-p[0], 39-p[1], pirate)
    # if (frame%234 < 182 and frame%26 != 0 and frame < 2000):
    #     if destinations_for_actors.get(id) is not None:
    #         return moveTo(destinations_for_actors[id][0], destinations_for_actors[id][1], pirate)
    #     else:
    #         destination_probabilities = dict(sorted(destination_visits.items(), key=lambda x: x[1]))
    #         destinations = list(destination_probabilities.keys())
    #         # print (abs(destinations[0][0] - 24)+abs(destinations[0][1]- 24))
    #         # while abs(destinations[-1][0] - pirate.getPosition()[0]) + abs(destinations[-1][1] - pirate.getPosition()[1]) < 30:
    #         #     destinations.pop()
    #         if (pirate.getPosition()[0] < 20 and pirate.getPosition()[1] < 20):
    #             destinations_for_actors[id] = (random.randint(0,19), random.randint(0,19))
    #         elif (pirate.getPosition()[0] >= 20 and pirate.getPosition()[1] > 20):
    #             destinations_for_actors[id] = (random.randint(20,39), random.randint(20,39))
    #         elif (pirate.getPosition()[0] < 20 and pirate.getPosition()[1] > 20):
    #             destinations_for_actors[id] = (random.randint(0,39), random.randint(20,39))
    #         else:
    #             destinations_for_actors[id] = (random.randint(20,39), random.randint(0,19))
    #         # destinations_for_actors[id] = (random.randint(0,36), random.randint(0,36))
    #         print(destinations_for_actors[id])
    #         destination_visits[destinations_for_actors[id]] += 1
    #         # print(True)
    #         return moveTo(destinations_for_actors[id][0], destinations_for_actors[id][1], pirate)
    # if (frame%26 == 0 and frame < 2000):
    #     destinations_for_actors = {}
    #     try:
    #         if max(destination_visits.values()) > 0 and frame%52 == 0:
    #             destinations_to_visit = [(x, y) for x in range(40) for y in range(40)]
    #             random.shuffle(destinations_to_visit)
    #             destination_visits = {
    #                 pos: 0 for pos in destinations_to_visit
    #             }
    #     except:
    #         pass
    # if(frame % 234 >= 182 and frame < 2000):
    #     # print(False)
    # # if (frame%600 < 300 and frame < 1000):
    #     width = 2
    #     if id%16 == 1:
    #         return moveTo(random.randint(max(0,p[0]-width),min(p[0]+width,39)), random.randint(max(0,p[1]-width),min(p[1]+width,39)), pirate)
    #     elif id%4 == 2:
    #         return moveTo(random.randint(max(0,p[0]-width),min(p[0]+width,39)), random.randint(max(0,39-p[1]-width),min(39-p[1]+width,39)), pirate)
    #     elif id%4 == 3:
    #         return moveTo(random.randint(max(0,39-p[0]-width),min(39-p[0]+width,39)), random.randint(max(0,p[1]-width),min(p[1]+width,39)), pirate)
    #     else:
    #         return moveTo(random.randint(max(0,39-p[0]-width),min(39-p[0]+width,39)), random.randint(max(0,39-p[1]-width),min(39-p[1]+width,39)), pirate)
    if(frame % (dimensionX+dimensionY) >= (dimensionX+dimensionY)//2 and frame%300 >= (dimensionX+dimensionY-2) and frame < 1500):
        if id%8 == 1:
            return moveTo(random.randint(dimensionX//2-5,dimensionX//2+5), random.randint(max(0,p[1]-4), min(dimensionY-1,p[1]+4)), pirate)
        elif id%8 == 5:
            return moveTo(random.randint(max(0, p[0]-4), min(dimensionX-1, p[0]+4)), random.randint(dimensionY//2-5,dimensionY//2+5), pirate)
        elif id%4 == 2:
            return moveTo(dimensionX-1-random.randint(max(0, p[0]-4), min(dimensionX-1, p[0]+4)), random.randint(dimensionY//2-5,dimensionY//2+5), pirate)
        else:
            return moveTo(random.randint(dimensionX//2-5,dimensionX//2+5), dimensionY-1-random.randint(max(0,p[1]-4), min(dimensionY-1,p[1]+4)), pirate)
    if (frame%(dimensionX+dimensionY) < (dimensionX+dimensionY)//2 and frame%300 >= (dimensionX+dimensionY-2) and frame < 1500):
        if id%16 == 1:
            return moveTo(random.randint(max(0, p[0]-4), min(dimensionX-1, p[0]+4)), random.randint(max(0,p[1]-4), min(dimensionY-1,p[1]+4)), pirate)
        if id%4 == 2:
            return moveTo(dimensionX-1-random.randint(max(0, p[0]-4), min(dimensionX-1, p[0]+4)), random.randint(max(0,p[1]-4), min(dimensionY-1,p[1]+4)), pirate)
        if id%4 == 3:
            return moveTo(random.randint(max(0, p[0]-4), min(dimensionX-1, p[0]+4)), dimensionY-1-random.randint(max(0,p[1]-4), min(dimensionY-1,p[1]+4)), pirate)
        else:
            return moveTo(dimensionX-1-random.randint(max(0, p[0]-4), min(dimensionX-1, p[0]+4)), dimensionY-1-random.randint(max(0,p[1]-4), min(dimensionY-1,p[1]+4)), pirate)
        # return moveTo(random.randint(17, 23), random.randint(17, 23), pirate)
    if (frame % 80 < 40 and 500 <= frame < 2000):
        return moveTo(39-p[0], p[1], pirate)
    elif frame % 80 > 40 and 500 <= frame < 2000:
        return moveTo(p[0], 39-p[1], pirate)
    else:
        # print("HERE3")
        up = pirate.investigate_up()
        down = pirate.investigate_down()
        left = pirate.investigate_left()
        right = pirate.investigate_right()
        x, y = pirate.getPosition()
        return moveAway(x, y, pirate)
        # pirate.setSignal("")
        # s = pirate.trackPlayers()
        
        # if (
        #     (up == "island1" and s[0] != "myCaptured")
        #     or (up == "island2" and s[1] != "myCaptured")
        #     or (up == "island3" and s[2] != "myCaptured")
        # ):
        #     s = up[-1] + str(x) + "," + str(y - 1)
        #     b += 1
        #     pirate.setSignal("mid")

        # if (
        #     (down == "island1" and s[0] != "myCaptured")
        #     or (down == "island2" and s[1] != "myCaptured")
        #     or (down == "island3" and s[2] != "myCaptured")
        # ):
        #     s = down[-1] + str(x) + "," + str(y + 1)
        #     b += 1
        #     pirate.setSignal("mid")

        # if (
        #     (left == "island1" and s[0] != "myCaptured")
        #     or (left == "island2" and s[1] != "myCaptured")
        #     or (left == "island3" and s[2] != "myCaptured")
        # ):
        #     s = left[-1] + str(x - 1) + "," + str(y)
        #     b += 1

        #     pirate.setSignal("mid")


        # if (
        #     (right == "island1" and s[0] != "myCaptured")
        #     or (right == "island2" and s[1] != "myCaptured")
        #     or (right == "island3" and s[2] != "myCaptured")
        # ):
        #     s = right[-1] + str(x + 1) + "," + str(y)
        #     b += 1
        #     pirate.setSignal("mid")


        # if (
        #     (up == "island1" and s[0] == "myCaptured")
        #     or (up == "island2" and s[1] == "myCaptured")
        #     or (up == "island3" and s[2] == "myCaptured") 
        # ):
        #     pirate.setSignal("mid")

        # if (
        #     (right == "island1" and s[0] == "myCaptured")
        #     or (right == "island2" and s[1] == "myCaptured")
        #     or (right == "island3" and s[2] == "myCaptured") 
        # ):
        #     # pirate.SetTeamSignal(s)
        #     pirate.setSignal("mid")

        # if (
        #     (down == "island1" and s[0] == "myCaptured")
        #     or (down == "island2" and s[1] == "myCaptured")
        #     or (down == "island3" and s[2] == "myCaptured") 
        # ):
        #     s = down[-1] + str(x) + "," + str(y + 1)
        #     pirate.setSignal("mid")


        # if (
        #         (left == "island1" and s[0] == "myCaptured")
        #         or (left == "island2" and s[1] == "myCaptured")
        #         or (left == "island3" and s[2] == "myCaptured") 
        #     ):
        #         pirate.setSignal("mid")

        # if (up == "friend"):
        #     if checkIsland(pirate) and b<= 4:
        #         pirate.setSignal("mid")
        #     else:
        #         s = up[-1] + str(x) + "," + str(y + 1)
        #         pirate.setSignal("move")
        
        # if (down == "friend"):
        #     if checkIsland(pirate) and b<= 4:
        #         pirate.setSignal("mid")
        #     else:
        #         s = up[-1] + str(x) + "," + str(y - 1)
        #         pirate.setSignal("move")
        
        # if (left == "friend"):
        #     if checkIsland(pirate) and b<= 4:
        #         pirate.setSignal("mid")
        #     else:
        #         s = up[-1] + str(x - 1) + "," + str(y)
        #         pirate.setSignal("move")
        
        # if (right == "friend" ) :
        #     if checkIsland(pirate) and b<= 4:
        #         pirate.setSignal("mid")
        #     else:
        #         s = up[-1] + str(x + 1) + "," + str(y)
        #         pirate.setSignal("move")

        # if (up != "friend" and up != "enemy" ):
        #     if checkIsland(pirate) and b<= 4:
        #         pirate.setSignal("mid")
        #     else:
        #         pirate.setSignal("random")
        
        # if (down != "friend" and down != "enemy"):
        #     if checkIsland(pirate) and b<= 4:
        #         pirate.setSignal("mid")
        #     else:
        #         pirate.setSignal("random")
        
        # if (left != "friend" and left != "enemy" ):
        #     if checkIsland(pirate) and b<= 4:
        #         pirate.setSignal("mid")
        #     else:
        #         pirate.setSignal("random")
        
        # if (right != "friend" and right != "enemy"):
        #     if checkIsland(pirate) and b<= 4:
        #         pirate.setSignal("mid")
        #     else:
        #         pirate.setSignal("random")

        # if pirate.getSignal() =="mid":
        #     return 0

        # elif pirate.getSignal() == "move":
        #     s = pirate.getTeamSignal()
        #     l = s.split(",")
        #     x = int(l[0][1:])
        #     y = int(l[1])
        #     return moveTo(x, y, pirate)
        
        # elif pirate.getSignal() == "random":
        #     return random.randint(1,4)

def ActTeam(team):
    global earlier_list_of_signals, assassins, gunPowder, wood, rum, possible_positions, reached_end, deploy_guards
    dimensionX = team.getDimensionX()
    dimensionY = team.getDimensionY()
    if not reached_end:
        start_x, start_y = team.getDeployPoint()
        # for i in range(team.getCurrentFrame(),1,-1):
        #     # positions_i_want = [(x, y) for x in range(40) for y in range(40) if abs(start_x - x) + abs(start_y - y) == i]
        #     possible_positions[i-1] = possible_positions[i-2].copy()
        possible_positions[team.getCurrentFrame()-1] = {(x, y): 0 for x in range(dimensionX) for y in range(dimensionY) if abs(start_x - x) + abs(start_y - y) == team.getCurrentFrame()}
        # positions_i_want = [(x, y) for x in range(39,-1,-1) for y in range(39,-1,-1) if abs(start_x-x) + abs(start_y-y) == team.getCurrentFrame()]
        # if start_x == 39 and start_y == 39:
        #     positions_i_want = [(x, y) for x in range(39,-1,-1) for y in range(39,-1,-1) if abs(start_x-x) + abs(start_y-y) == team.getCurrentFrame()]
        # if start_x == 0 and start_y == 0:
        #     positions_i_want = [(x, y) for x in range(40) for y in range(40) if abs(start_x-x) + abs(start_y-y) == team.getCurrentFrame()]
        # if start_x == 0 and start_y == 39:
        #     positions_i_want = [(x, y) for x in range(0, 40) for y in range(39, -1, -1) if abs(start_x-x) + abs(start_y-y) == team.getCurrentFrame()]
        # if start_x == 39 and start_y == 0:
        #     positions_i_want = [(x, y) for x in range(39, -1, -1) for y in range(40) if abs(start_x-x) + abs(start_y-y) == team.getCurrentFrame()]
        # # random.shuffle(positions_i_want)
        # # if (team.getCurrentFrame() % 2 == 0):
        # #     positions_i_want.reverse()
        # possible_positions = {key: 0 for key in positions_i_want}
        if (dimensionX-1-start_x, dimensionY-1-start_y) in possible_positions[team.getCurrentFrame()-1]:
            reached_end = True
    
    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)

    gunPowder = team.getTotalGunpowder()
    wood = team.getTotalWood()
    rum = team.getTotalRum()
    if 'island1' not in island_pos:
        island_pos['island1'] = (0, 0)
    if 'island2' not in island_pos:
        island_pos['island2'] = (0, 0)
    if 'island3' not in island_pos:
        island_pos['island3'] = (0, 0)

    pirate_pos = dict()

    pirate_signals = team.getListOfSignals()
    for signal in pirate_signals:
        if signal.count(',') != 2:
            continue
        print(signal)
        pirate_id, x, y = signal.split(',')
        pirate_pos[int(pirate_id)] = (int(x), int(y))

    pirates_on_islands = 0
    for island in island_pos:
        if island_pos[island] != (0, 0):
            for pirate in pirate_pos:
                print(pirate_pos[pirate])
                # if pirate_pos[pirate][0] <= island_pos[0] + 1 and pirate_pos[0] >= island_pos[0] - 1 and pirate_pos[1] <= island_pos[1] + 1 and pirate_pos[1] >= island_pos[1] - 1:
                if pirate_pos[pirate][0] <= island_pos[island][0] + 1 and pirate_pos[pirate][0] >= island_pos[island][0] - 1 and pirate_pos[pirate][1] <= island_pos[island][1] + 1 and pirate_pos[pirate][1] >= island_pos[island][1] - 1:
                    pirates_on_islands += 1
    print(f'Pirates on islands: {pirates_on_islands}')
    print(island_pos)
    print(colonists)

    start_x, start_y = team.getDeployPoint()
    list_of_signals = [x.split(',')[0] for x in team.getListOfSignals()]
    new_pirates = [int(id) for id in list_of_signals if id not in earlier_list_of_signals]
    dead_pirates = [int(id) for id in earlier_list_of_signals if id not in list_of_signals] 
    for id in dead_pirates:
        if id in assassins:
            assassins.remove(id)
        if id in deploy_guards:
            del deploy_guards[id]
        if id in pirate_pos:
            del pirate_pos[id]
        for key in colonists:
            if id in colonists[key]:
                colonists[key].remove(id)
    for i in range(1, 4):
        if island_pos[f'island{i}'] != (0, 0):
            colonists[f'island{i}'] = closest_n_pirates(island_pos[f'island{i}'][0], island_pos[f'island{i}'][1], 3, pirate_pos)
            if len(colonists[f'island{i}']) < 3:
                if len(new_pirates) == 0:
                    break
                colonists[f'island{i}'].append(new_pirates.pop(0))


    if len(assassins) < 6 and len(list_of_signals) >= 5:
        assassins = closest_n_pirates(dimensionX-1-start_x, dimensionY-1-start_y, 5, pirate_pos)
    if team.getCurrentFrame() > dimensionX and len(deploy_guards) < 2 and len(list_of_signals) >= 2:
        # print(closest_n_pirates(1*(start_x==0) + 38*(start_x==39), start_y, 1, team))
        # print(closest_n_pirates(start_x, 1*(start_y==0)+38*(start_y==39), 2, team)[1:])
        deploy_guards = {pirate: [start_x, start_y, 'blank'] for pirate in closest_n_pirates(1*(start_x==0) + 38*(start_x==39), start_y, 1, pirate_pos) + closest_n_pirates(start_x, 1*(start_y==0)+38*(start_y==39), 2, pirate_pos)[1:]}    
        deployed_guards = list(deploy_guards.keys())
        if len(deployed_guards) < 2:
            closest_to_home = closest_n_pirates(start_x, 1*(start_y==0)+(dimensionY-2)*(start_y==(dimensionY-1)), 1, pirate_pos)
            index = 0
        while len(deploy_guards) < 2:
            deploy_guards[closest_to_home[index]] = [start_x, start_y, 'blank']
            index += 1
            deployed_guards = list(deploy_guards.keys())
        if start_x == 0 and start_y == 0:
            deploy_guards[deployed_guards[0]][0] = 1
            deploy_guards[deployed_guards[0]][1] = 0
            deploy_guards[deployed_guards[0]][2] = 'left'
            deploy_guards[deployed_guards[1]][0] = 0
            deploy_guards[deployed_guards[1]][1] = 1
            deploy_guards[deployed_guards[1]][2] = 'down'
        if start_x == dimensionX-1 and start_y == 0:
            deploy_guards[deployed_guards[0]][0] = dimensionX-2
            deploy_guards[deployed_guards[0]][1] = 0
            deploy_guards[deployed_guards[0]][2] = 'right'
            deploy_guards[deployed_guards[1]][0] = dimensionX-1
            deploy_guards[deployed_guards[1]][1] = 1
            deploy_guards[deployed_guards[1]][2] = 'down'
        if start_x == 0 and start_y == dimensionY-1:
            deploy_guards[deployed_guards[0]][0] = 1
            deploy_guards[deployed_guards[0]][1] = dimensionY-1
            deploy_guards[deployed_guards[0]][2] = 'left'
            deploy_guards[deployed_guards[1]][0] = 0
            deploy_guards[deployed_guards[1]][1] = dimensionY-2
            deploy_guards[deployed_guards[1]][2] = 'up'
        if start_x == dimensionX-1 and start_y == dimensionY-1:
            deploy_guards[deployed_guards[0]][0] = dimensionX-2
            deploy_guards[deployed_guards[0]][1] = dimensionY-1
            deploy_guards[deployed_guards[0]][2] = 'right'
            deploy_guards[deployed_guards[1]][0] = dimensionX-1
            deploy_guards[deployed_guards[1]][1] = dimensionY-2
            deploy_guards[deployed_guards[1]][2] = 'up'
    earlier_list_of_signals = list_of_signals.copy()
    # gunPowder = team.getTotalGunpowder()
    pass
