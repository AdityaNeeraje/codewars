import random
import math
import copy

from numpy import sign

from engine import island, pirate

name = "script"

# island_pos = {
#     'island1': (0, 0),
#     'island2': (0, 0),
#     'island3': (0, 0)
# }

signals = {}
# deploy_guards = {} # This has the id of every living guard as a key and their position and direction relative to island center as values.
# colonists = {} # This has the id of every living colonist as a key and the coordinate of their island center as value
# assassins = []
# earlier_list_of_signals = []
possible_positions = {id: {} for id in range(78)} # subtract frame from the current frame to get the id number (maybe +1)
# reached_end = False

def encode_direction(direction):
    match(direction):
        case "blank":
            return 0
        case "up":
            return 1
        case "down":
            return 2
        case "left":
            return 3
        case "right":
            return 4
        
def decode_direction(direction):
    match(direction):
        case 0:
            return "blank"
        case 1:
            return "up"
        case 2:
            return "down"
        case 3:
            return "left"
        case 4:
            return "right"
    

def decode_signal(signal):
    signal_data = {
        'island_pos': {
            'island1': (0, 0),
            'island2': (0, 0),
            'island3': (0, 0)
        },
        'colonists': {
            'island1': [],
            'island2': [],
            'island3': []
        },
        'assassins': [],
        'reached_end': False,
    }
    
    #Island Positions...
    signal_data['island_pos']['island1'] = (ord(signal[0]) // (2**12), (ord(signal[0]) % (2**12)) // (2**6))
    signal_data['island_pos']['island2'] = ((ord(signal[0]) % (2**12)) % (2**6) // (2**0), (ord(signal[1]) // (2**12)))
    signal_data['island_pos']['island3'] = ((ord(signal[1]) % (2**12)) // (2**6), (ord(signal[1]) % (2**12)) % (2**6) // (2**0))

    #Colonists...
    signal_data['colonists']['island1'] = [int(ord(signal[2]) // (2**9)), int(ord(signal[2]) % (2**9) // (2**0)), int(ord(signal[3]) // (2**9))]
    signal_data['colonists']['island2'] = [int(ord(signal[3]) % (2**9) // (2**0)), int(ord(signal[4]) // (2**9)), int(ord(signal[4]) % (2**9) // (2**0))]
    signal_data['colonists']['island3'] = [int(ord(signal[5]) // (2**9)), int(ord(signal[5]) % (2**9) // (2**0)), int(ord(signal[6]) // (2**9))]

    #Assassins...
    signal_data['assassins'] = [int(ord(signal[7]) // (2**9)), int(ord(signal[7]) % (2**9) // (2**0)), int(ord(signal[8]) // (2**9))]

    #Reached End...
    signal_data['reached_end'] = bool(ord(signal[8]))

    return signal_data

def encode_signal(signal_data):
    signal = ""
    for island in signal_data['colonists']:
        if len(signal_data['colonists'][island]) < 3:
            while len(signal_data['colonists'][island]) < 3:
                signal_data['colonists'][island].append(511)
    # print(signal_data)

    signal += chr((2**12)*signal_data['island_pos']['island1'][0] + (2**6)*signal_data['island_pos']['island1'][1] + (2**0)*signal_data['island_pos']['island2'][0])
    signal += chr((2**12)*signal_data['island_pos']['island2'][1] + (2**6)*signal_data['island_pos']['island3'][0] + (2**0)*signal_data['island_pos']['island3'][1])
    
    signal += chr((2**9)*int(signal_data['colonists']['island1'][0]) + (2**0)*int(signal_data['colonists']['island1'][1]))
    signal += chr((2**9)*int(signal_data['colonists']['island1'][2]) + (2**0)*int(signal_data['colonists']['island2'][0]))
    signal += chr((2**9)*int(signal_data['colonists']['island2'][1]) + (2**0)*int(signal_data['colonists']['island2'][2]))
    signal += chr((2**9)*int(signal_data['colonists']['island3'][0]) + (2**0)*int(signal_data['colonists']['island3'][1]))
    signal += chr((2**9)*int(signal_data['colonists']['island3'][2]))

    signal += chr((2**9)*int(signal_data['assassins'][0]) + (2**0)*int(signal_data['assassins'][1]))
    signal += chr((2**9)*int(signal_data['assassins'][2]))

    signal += chr(int(signal_data['reached_end']))
        
    # print(signal)
    return signal

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
def checkIsland(pirate, island_pos):
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    nw = pirate.investigate_nw()
    ne = pirate.investigate_ne()
    se = pirate.investigate_se()
    sw = pirate.investigate_sw()

    if island_pos['island1'] != (0, 0) and island_pos['island2'] != (0, 0) and island_pos['island3'] != (0, 0):
        return island_pos

    if nw[0][0:-1] == "island" and up[0] == "blank" and left[0] == "blank":
        island_pos[nw[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] - 2)
    if ne[0][0:-1] == "island" and up[0] == "blank" and right[0] == "blank":
        island_pos[ne[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] - 2)
    if se[0][0:-1] == "island" and down[0] == "blank" and right[0] == "blank":
        island_pos[se[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] + 2)
    if sw[0][0:-1] == "island" and down[0] == "blank" and left[0] == "blank":
        island_pos[sw[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] + 2)
    if up[0][0:-1] == "island" and nw[0][0:-1] == "island" and ne[0][0:-1] == "island" and right[0] == "blank" and left[0] == "blank":
        island_pos[up[0]] = (pirate.getPosition()[0], pirate.getPosition()[1] - 2)
    if left[0][0:-1] == "island" and nw[0][0:-1] == "island" and sw[0][0:-1] == "island" and up[0] == "blank" and down[0] == "blank":
        island_pos[left[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1])
    if down[0][0:-1] == "island" and sw[0][0:-1] == "island" and se[0][0:-1] == "island" and right[0] == "blank" and left[0] == "blank":
        island_pos[down[0]] = (pirate.getPosition()[0], pirate.getPosition()[1] + 2)
    if right[0][0:-1] == "island" and ne[0][0:-1] == "island" and se[0][0:-1] == "island" and up[0] == "blank" and down[0] == "blank":
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
        island_pos[right[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] + 1)
    
    return island_pos

def ActColonist(pirate, island_pos, colonists):
    id = int(pirate.getID())
    for island in colonists:
        # print(f'Acting colonist {id} on {island}')
        if id in colonists[island]:
            position_of_first_colonist = positionInIsland(pirate)
            # centre, topleft, topright, bottomright, bottomleft, middleright, middleleft, topmiddle, bottommiddle
            investigation_result = ""
            if position_of_first_colonist == 'topleft':
                investigation_result = pirate.investigate_se()
            elif position_of_first_colonist == 'topright':
                investigation_result = pirate.investigate_sw()
            elif position_of_first_colonist == 'bottomright':
                investigation_result = pirate.investigate_nw()
            elif position_of_first_colonist == 'bottomleft':
                investigation_result = pirate.investigate_ne()
            elif position_of_first_colonist == 'bottommiddle':
                investigation_result = pirate.investigate_top()
            elif position_of_first_colonist == 'topmiddle':
                investigation_result = pirate.investigate_down()
            elif position_of_first_colonist == 'middleright':
                investigation_result = pirate.investigate_left()
            elif position_of_first_colonist == 'middleleft':
                investigation_result = pirate.investigate_right()
            if investigation_result == "enemy":
                return moveTo(island_pos[island][0], island_pos[island][1], pirate)
            try:
                if colonists[island][0] == id:
                    return circleAround(island_pos[island][0], island_pos[island][1], 1, pirate, (island_pos[island][0] + 1, island_pos[island][1] + 1), (pirate.getCurrentFrame() % 16 < 8))
            except:
                pass
            try:
                if colonists[island][1] == id:
                    return circleAround(island_pos[island][0], island_pos[island][1], 1, pirate, (island_pos[island][0] + 1, island_pos[island][1] + 1), (pirate.getCurrentFrame() % 16 >= 8))
            except:
                pass
            try:
                if colonists[island][2] == id:
                    return circleAround(island_pos[island][0], island_pos[island][1], 1, pirate, (island_pos[island][0] - 1, island_pos[island][1] + 1), (pirate.getCurrentFrame() % 16 < 8))
            except:
                pass
    pass

# pirate_pos = dict()
# pirate_goal = dict()
# island_pos = dict()

# Get the closest n pirates to a given position
def closest_n_pirates(x, y, n, pirate_pos):
    pirates = {k: v for k, v in sorted(pirate_pos.items(), key=lambda item: abs(item[1][0] - x) + abs(item[1][1] - y))}
    closest_pirates = list(pirates.keys())[:n] # Get the first n pirates from the sorted list
    # print(list(pirates.keys()), closest_pirates)
    return closest_pirates

def checkfriends(pirate, quad):
    sum = 0 
    up = pirate.investigate_up()[1]
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

def ActGuard(x, y, pirate, dir):
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
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    right = pirate.investigate_right()
    left = pirate.investigate_left()
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
    global gunpowder, rum, wood, possible_positions, destinations_for_actors, destination_visits, pirates, reached_end
    
    gunPowder = pirate.getTotalGunpowder()
    rum = pirate.getTotalRum()
    wood = pirate.getTotalWood()
    signal_data = decode_signal(pirate.getTeamSignal())

    island_pos = signal_data['island_pos']
    colonists = signal_data['colonists']
    assassins = signal_data['assassins']
    # print(assassins, colonists)

    dimensionX = pirate.getDimensionX()
    dimensionY = pirate.getDimensionY()
    gunpowder = pirate.getTotalGunpowder()
    rum = pirate.getTotalRum()
    wood = pirate.getTotalWood()
    p = list(pirate.getDeployPoint())
    x, y = pirate.getPosition()
    id = int(pirate.getID())
    # print(id, x, y, assassins)
    # print('Ass', assassins)
    if pirate.getSignal().count(',') == 0:
        pirate.setSignal(f"{id},{pirate.getPosition()[0]},{pirate.getPosition()[1]},{pirate.getCurrentFrame()}")
        init_frame = pirate.getCurrentFrame()
    else:
        _, __x, __y, init_frame = pirate.getSignal().strip().split(',')
        pirate.setSignal(f"{id},{pirate.getPosition()[0]},{pirate.getPosition()[1]},{init_frame}")    
    
    frame = pirate.getCurrentFrame() - int(init_frame)
    curr_frame = pirate.getCurrentFrame()
    if curr_frame > (dimensionX*dimensionY)/3:
        pass
    # print(pirate.getCurrentFrame()
    #  and pirate.getCurrentFrame() < (dimensionX*dimensionY)/3
    # print(assassins)
    if id in assassins and pirate.getCurrentFrame() > 1:
        # print(id, assassins)
        # print('nirav', id, assassins)
        if id == assassins[1]: #Instead, let actteam return the string a1 for the first assassin
            # print(dimensionX-1-p[0], dimensionY-2-p[1], pirate.getPosition())
            # print('haha0', x, y, dimensionX-1-abs(p[0]-1), dimensionY-1-p[1])
            return moveTo(dimensionX-1-abs(p[0]-1), dimensionY-1-p[1], pirate)
        elif id == assassins[2]: #Instead, let actteam return the string a2 for the second assassin
            # print(dimensionX-1-p[0], dimensionY-1-abs(p[1]-1), pirate.getPosition())
            # print('haha1', x, y, dimensionX-1-p[0], dimensionY-1-abs(p[1]-1))
            return moveTo(dimensionX-1-p[0], dimensionY-1-abs(p[1]-1), pirate)
        elif gunpowder > 100 or id%2 == 0:  # Use the "gunpowder" variable
            # print('haha2', dimensionX-1-abs(p[0]-1), dimensionY-1-abs(p[1]-1))
            return moveTo(dimensionX-1-abs(p[0]-1), dimensionY-1-abs(p[1]-1), pirate)
        else:
            return moveTo(dimensionX-1-p[0], dimensionY-1-p[1], pirate)

    if pirate.getCurrentFrame() > 100:
        for island in colonists:
            if id in colonists[island]:
                return ActColonist(pirate, island_pos, colonists)
    
    # if id in deploy_guards:
    #     return ActGuard(deploy_guards[id][0], deploy_guards[id][1], pirate, deploy_guards[id][2])
    
    island_pos = checkIsland(pirate=pirate, island_pos=island_pos)
    signal_data['island_pos'] = island_pos
    pirate.setTeamSignal(encode_signal(signal_data))
    
    x, y = pirate.getPosition()
    start_x, start_y = pirate.getDeployPoint()
    id_mod_dim = (id//2)%(dimensionX)
    if curr_frame < dimensionY+dimensionX+18 and frame < dimensionY+dimensionX-2:
        if id%2 == 0:
            if abs(x-start_x) < id_mod_dim and abs(y-start_y) == 0:
                return moveTo(abs(id_mod_dim-start_x), start_y, pirate)
            if abs(x-start_x) == id_mod_dim and abs(y-start_y) < id_mod_dim:
                return moveTo(abs(id_mod_dim-start_x),abs(id_mod_dim-start_y), pirate)
            if abs(x-start_x) != dimensionX-1-id_mod_dim and abs(y-start_y) == id_mod_dim:
                # print("DEST", abs(dimensionX-1-id_mod_dim-start_x),abs(id_mod_dim-start_y))
                return moveTo(abs(dimensionX-1-id_mod_dim-start_x),abs(id_mod_dim-start_y), pirate)
            if abs(x-start_x) == dimensionX-1-id_mod_dim and abs(y-start_y) != dimensionY-1-id_mod_dim:
                return moveTo(abs(dimensionX-1-id_mod_dim-start_x),abs(dimensionY-1-id_mod_dim-start_y), pirate)
            if abs(x-start_x) < dimensionX-1 and abs(y-start_y) == dimensionY-1-id_mod_dim:
                return moveTo(abs(dimensionX-1-start_x),abs(dimensionY-1-id_mod_dim-start_y), pirate)
            # if abs(x-start_x) == dimensionX-1 and abs(y-start_y) < dimensionY-1:
            #     return moveTo(abs(dimensionX-1-start_x),abs(dimensionY-1-start_y), pirate)
        else:
            if abs(x-start_x) == 0 and abs(y-start_y) < id_mod_dim:
                return moveTo(start_x, abs(id_mod_dim-start_y), pirate)
            if abs(x-start_x) < id_mod_dim and abs(y-start_y) == id_mod_dim:
                return moveTo(abs(id_mod_dim-start_x),abs(id_mod_dim-start_y), pirate)
            if abs(x-start_x) == id_mod_dim and abs(y-start_y) != dimensionY-1-id_mod_dim:
                # print("DEST", abs(id_mod_dim-start_x),abs(dimensionY-1-id_mod_dim-start_y))
                return moveTo(abs(id_mod_dim-start_x),abs(dimensionY-1-id_mod_dim-start_y), pirate)
            if abs(x-start_x) != dimensionX-1-id_mod_dim and abs(y-start_y) == dimensionY-1-id_mod_dim:
                return moveTo(abs(dimensionX-1-id_mod_dim-start_x),abs(dimensionY-1-id_mod_dim-start_y), pirate)
            if abs(x-start_x) == dimensionX-1-id_mod_dim and abs(y-start_y) != dimensionY-1:
                return moveTo(abs(dimensionX-1-id_mod_dim-start_x),abs(dimensionY-1-start_y), pirate)
            # if abs(x-start_x) < dimensionX-1 and abs(y-start_y) == dimensionY-1:
            #     return moveTo(abs(dimensionX-1-start_x),abs(dimensionY-1-start_y), pirate)
    # if not reached_end and possible_positions:
    #     index = abs(pirate.getPosition()[0]-pirate.getDeployPoint()[0]) + abs(pirate.getPosition()[1]-pirate.getDeployPoint()[1])
    #     # print(index, possible_positions[index])
    #     # If position is x, y and start is start_x, start_y, then possible_positions x-start_x + y - start_y is needed
    #     if pirate.getDeployPoint()[0] != pirate.getDeployPoint()[1]:
    #         if id%2 == 0:
    #             some_dict = dict(sorted({key: value for key, value in \
    #                                                      possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], random.random())))
    #         else:
    #             if random.randint(0,8) != 0:
    #                 if id%4 == 1:
    #                     some_dict = dict(sorted({key: value for key, value in \
    #                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
    #                 else:
    #                     some_dict = dict(sorted({key: value for key, value in \
    #                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], -x[0][1])))
    #             else:
    #                 if id%4 == 1:
    #                     some_dict = dict(sorted({key: value for key, value in \
    #                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], -x[0][1])))
    #                 else:
    #                     some_dict = dict(sorted({key: value for key, value in \
    #                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
    #         # elif id%4 == 3:
    #         #     some_dict = dict(sorted({key: value for key, value in \
    #         #                                              possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], -x[0][1])))
    #     else:
    #         if id%2 == 0:
    #             some_dict = dict(sorted({key: value for key, value in \
    #                                                      possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], random.random())))
    #         else:
    #             if random.randint(0,8) != 0:
    #                 if id%4 == 1:
    #                     some_dict = dict(sorted({key: value for key, value in \
    #                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
    #                 else:
    #                     some_dict = dict(sorted({key: value for key, value in \
    #                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][1])))
    #             else:
    #                 if id%4 == 1:
    #                     some_dict = dict(sorted({key: value for key, value in \
    #                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][1])))
    #                 else:
    #                     some_dict = dict(sorted({key: value for key, value in \
    #                                                         possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
    #         # elif id%4 == 1:
    #         #     some_dict = dict(sorted({key: value for key, value in \
    #         #                                              possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
    #         # elif id%4 == 3:
    #         #     some_dict = dict(sorted({key: value for key, value in \
    #         #                                              possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][1]))
    #         # )
    #
    #     # if pirate.getDeployPoint()[0] != pirate.getDeployPoint()[1]:
    #     #     if frame%(id%6 + 2) == 0:
    #     #         some_dict = dict(sorted({key: value for key, value in \
    #     #                                                  possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], (x[0][0]+1))))
    #     #     else:
    #     #         some_dict = dict(sorted({key: value for key, value in \
    #     #                                                  possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], (dimensionX-x[0][1]))))
    #     #     # elif id%3 == 1:
    #     #     #     some_dict = dict(sorted({key: value for key, value in \
    #     #     #                                              possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
    #     #     # elif id%3 == 2:
    #     #     #     some_dict = dict(sorted({key: value for key, value in \
    #     #     #                                              possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], -x[0][1])))
    #     # else:
    #     #     if frame%(id%6 + 2) == 0:
    #     #         some_dict = dict(sorted({key: value for key, value in \
    #     #                                                  possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], (x[0][0]+1))))
    #     #     else:
    #     #         some_dict = dict(sorted({key: value for key, value in \
    #     #                                                  possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], (x[0][1]+1))))
    #     #     # elif id %3 == 1:
    #     #     #     some_dict = dict(sorted({key: value for key, value in \
    #     #     #                                              possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][0])))
    #     #     # elif id%3 == 2:
    #     #     #     some_dict = dict(sorted({key: value for key, value in \
    #     #     #                                              possible_positions[index].items() if abs(key[0]-pirate.getPosition()[0]) + abs(key[1] - pirate.getPosition()[1]) == 1}.items(), key=lambda x: (x[1], x[0][1]))
    #     #     # )
    #     choice = list(some_dict.keys())[0]
    #     possible_positions[index][choice] += 1
    #     return moveTo(choice[0], choice[1], pirate)
        
    if id%10 == 1:
        if p[0] == 0 and p[1] == 0:
            p[1] = dimensionY//5
        elif p[0] == 0 and p[1] == 39:
            p[0] = dimensionX//5
        elif p[0] == dimensionX - 1 and p[1] == dimensionY - 1:
            p[1] = dimensionY - 1 - dimensionY//5
        elif p[0] == dimensionX - 1 and p[1] == 0:
            p[0] = dimensionX - 1 - dimensionX//5
    if id%10 == 2:
        if p[0] == 0 and p[1] == 0:
            p[1] = 2*dimensionY//5
        elif p[0] == 0 and p[1] == dimensionY - 1:
            p[0] = 2*dimensionX//5
        elif p[0] == dimensionX - 1 and p[1] == dimensionY - 1:
            p[1] = dimensionY - 1 - 2*dimensionY//5
        elif p[0] == dimensionX - 1 and p[1] == 0:
            p[0] = dimensionX - 1 - 2*dimensionX//5
    if id%10 == 3:
        if p[0] == 0 and p[1] == 0:
            p[1] = 3*dimensionY//5
        elif p[0] == 0 and p[1] == dimensionY - 1:
            p[0] = 3*dimensionX//5
        elif p[0] == dimensionX - 1 and p[1] == dimensionY - 1:
            p[1] = dimensionY - 1 - 3*dimensionY//5
        elif p[0] == dimensionX - 1 and p[1] == 0:
            p[0] = dimensionX - 1 - 3*dimensionX//5
    if id%10 == 4:
        if p[0] == 0 and p[1] == 0:
            p[1] = 4*dimensionY//5
        elif p[0] == 0 and p[1] == dimensionY - 1:
            p[0] = 4*dimensionX//5
        elif p[0] == dimensionX - 1 and p[1] == dimensionY - 1:
            p[1] = dimensionY - 1 - 4*dimensionY//5
        elif p[0] == dimensionX - 1 and p[1] == 0:
            p[0] = dimensionX - 1 - 4*dimensionX//5
    if id%10 == 5:
            if p[0] == 0 and p[1] == 0:
                p[0] = dimensionX//5
            elif p[0] == 0 and p[1] == dimensionY - 1:
                p[1] = dimensionY - 1 - dimensionY//5
            elif p[0] == dimensionX - 1 and p[1] == dimensionY - 1:
                p[0] = dimensionX - 1 - dimensionX//5
            elif p[0] == dimensionX - 1 and p[1] == 0:
                p[1] = dimensionY//5
    if id%10 == 6:
        if p[0] == 0 and p[1] == 0:
            p[0] = 2*dimensionX//5
        elif p[0] == 0 and p[1] == dimensionY - 1:
            p[1] = dimensionY - 1 - 2*dimensionY//5
        elif p[0] == dimensionX - 1 and p[1] == dimensionY - 1:
            p[0] = dimensionX - 1 - 2*dimensionX//5
        elif p[0] == dimensionX - 1 and p[1] == 0:
            p[1] = 2*dimensionY//5
    if id%10 == 7:
        if p[0] == 0 and p[1] == 0:
            p[0] = 3*dimensionX//5
        elif p[0] == 0 and p[1] == dimensionY - 1:
            p[1] = dimensionY - 1 - 3*dimensionY//5
        elif p[0] == dimensionX - 1 and p[1] == dimensionY - 1:
            p[0] = dimensionX - 1 - 3*dimensionX//5
        elif p[0] == dimensionX - 1 and p[1] == 0:
            p[1] = 3*dimensionY//5
    if id%10 == 8:
        if p[0] == 0 and p[1] == 0:
            p[0] = 4*dimensionX//5
        elif p[0] == 0 and p[1] == dimensionY - 1:
            p[1] = dimensionY - 1 - 4*dimensionY//5
        elif p[0] == dimensionX - 1 and p[1] == dimensionY - 1:
            p[0] = dimensionX - 1 - 4*dimensionX//5
        elif p[0] == dimensionX - 1 and p[1] == 0:
            p[1] = 4*dimensionY//5
            
    if signals.get(id) is None:
        signals[id] = ""
    # x,y = pirate.getPosition()
    strp = signals[id]
    if(strp != ''):
        try:
            xchange =int(strp[0])-2
            ychange = int(strp[1])-2
        except:
            xchange=1
            ychange=1
    else:
        xchange=1
        ychange=1
    if x == pirate.getDimensionX()-1:
        xchange = -1
        strp = str(xchange+2)+str(ychange+2)
        signals[id] = strp
        # print(strp)
        # print("rchd end")
    elif x == 0:
        xchange = 1
        strp = str(xchange+2)+str(ychange+2)
        signals[id] = strp
    if y == 0:
        ychange = 1
        strp = str(xchange+2)+str(ychange+2)
        signals[id] = strp
    elif y == pirate.getDimensionY()-1:
        ychange = -1
        strp = str(xchange+2)+str(ychange+2)
        signals[id] = strp
    return moveTo(x+xchange,y+ychange,pirate)


def ActTeam(team):
    global earlier_list_of_signals, gunPowder, wood, rum, possible_positions, reached_end
    data = {
        16: 22,
        20: 35,
        24: 45,
        28: 60,
        32: 70,
        36: 75,
        40: 90,
        44: 115,
        48: 130,
        52: 130,
        56: 140,
        60: 140,
        64: 160
    }
    # print(team.getTeamSignal())
    if team.getCurrentFrame() == 1:
        signal_data = {
            'island_pos': {
                'island1': (0, 0),
                'island2': (0, 0),
                'island3': (0, 0)
            },
            'colonists': {
                'island1': [2**9-1, 2**9-1, 2**9-1],
                'island2': [2**9-1, 2**9-1, 2**9-1],
                'island3': [2**9-1, 2**9-1, 2**9-1]
            },
            'assassins': [2**9-1, 2**9-1, 2**9-1],
            'reached_end': False,
        }
    else:
        signal_data = decode_signal(team.getTeamSignal())

    signal = encode_signal(signal_data)

    dimensionX = team.getDimensionX()
    dimensionY = team.getDimensionY()

    team.setTeamSignal(signal)
    
    pirate_pos = dict()

    pirate_signals = team.getListOfSignals()
    for signal in pirate_signals:
        if signal.count(',') != 3:
            continue
        pirate_id, x, y, init_frame = signal.split(',')
        pirate_pos[int(pirate_id)] = (int(x), int(y), int(init_frame))

    island_pos = signal_data['island_pos']
    colonists = signal_data['colonists']
    assassins = signal_data['assassins']
    reached_end = signal_data['reached_end']
    # print(team.getCurrentFrame(), "ASSASSINS", assassins)
    if team.getCurrentFrame() != 1:
        # print('START', assassins)
        # print(dimensionX-1-team.getDeployPoint()[0], dimensionY-1-team.getDeployPoint()[1], pirate_pos)
        assassins = closest_n_pirates(dimensionX-1-team.getDeployPoint()[0], dimensionY-1-team.getDeployPoint()[1], 3, pirate_pos=pirate_pos)
        # print(team.getCurrentFrame(), "ASSASSINS", assassins)

    # if not reached_end:
    #     start_x, start_y = team.getDeployPoint()
    #
    #     possible_positions[team.getCurrentFrame()-1] = {(x, y): 0 for x in range(dimensionX) for y in range(dimensionY) if abs(start_x - x) + abs(start_y - y) == team.getCurrentFrame()}
    #     curr_positions = list(pirate_pos.values())
    #     # print(curr_positions)
    #     for i in range(team.getCurrentFrame()-1):
    #         possible_positions[i-1] = {(x,y): curr_positions.count((x,y)) for x in range(dimensionX) for y in range(dimensionY) if abs(start_x-x) + abs(start_y-y) == i}
    #     if (dimensionX-1-start_x, dimensionY-1-start_y) in possible_positions[team.getCurrentFrame()-1]:
    #         signal_data['reached_end'] = True
    
    if team.getCurrentFrame() >= dimensionX+dimensionX+18:
        team.buildWalls(1)
        team.buildWalls(2)
        team.buildWalls(3)

    gunPowder = team.getTotalGunpowder()
    wood = team.getTotalWood()
    rum = team.getTotalRum()

    start_x, start_y = team.getDeployPoint()
    list_of_signals = [int(sig.split(",")[0].strip()) for sig in team.getListOfSignals() if sig.split(",")[0].isnumeric()]
    # print(earlier_list_of_signals)
    # print(list_of_signals)
    # new_pirates = [int(id) for id in list_of_signals if id not in earlier_list_of_signals]
    # dead_pirates = [int(id) for id in earlier_list_of_signals if id not in list_of_signals] 
    # print("NEW", new_pirates)
    # print("NEW", dead_pirates)
    for key in colonists:
        ids_to_remove = []
        for id in colonists[key]:
            if id not in list_of_signals:
                ids_to_remove.append(id)
        for id in ids_to_remove:
            colonists[key].remove(id)

    # legacy code relying on earlier_list_of_signals
    # for id in dead_pirates:
    #     if id in assassins:
    #         assassins.pop(assassins.index(id))
    #         print("here1")
    #     # if id in deploy_guards:
    #     #     del deploy_guards[id]
    #     if id in pirate_pos:
    #         print("here2")
    #         del pirate_pos[id]
    #     for key in colonists:
    #         if id in colonists[key]:
    #             print(f"here3{id}")
    #             colonists[key].remove(id)

    # print('here')
    for i in range(1, 4):
        if island_pos[f'island{i}'] != (0, 0) and team.getCurrentFrame() > 1:
            colonists[f'island{i}'] = closest_n_pirates(island_pos[f'island{i}'][0], island_pos[f'island{i}'][1], 3, pirate_pos=pirate_pos)
            # while len(colonists[f'island{i}']) < 3:
            #     if len(new_pirates) == 0:
            #         break
            #     colonists[f'island{i}'].append(new_pirates.pop(0))
    # print('here2')
    if len(list_of_signals) < 15:
        for key in colonists:
            try:
                colonists[key][1] = 511
                colonists[key][2] = 511
            except:
                pass

    # print('here3')
    if len(assassins) <= 3 and len(list_of_signals) >= 3 and team.getCurrentFrame() > 1:
        # print("REPLENISHING")
        assassins = closest_n_pirates(dimensionX-1-start_x, dimensionY-1-start_y, 3, pirate_pos=pirate_pos)
        # print('A', assassins)
    if len(pirate_pos.keys()) <= 20 or team.getCurrentFrame() > data[dimensionX]:
        assassins = [511, 511, 511]
    # print('here4')
    # if team.getCurrentFrame() > dimensionX and len(deploy_guards) < 2 and len(list_of_signals) >= 2:
    #     deploy_guards = {pirate: [start_x, start_y, 'blank'] for pirate in closest_n_pirates(1*(start_x==0) + 38*(start_x==39), start_y, 1, pirate_pos=pirate_pos) + closest_n_pirates(start_x, 1*(start_y==0)+38*(start_y==39), 2, pirate_pos=pirate_pos)[1:]}    
    #     deployed_guards = list(deploy_guards.keys())
    #     if len(deployed_guards) < 2:
    #         closest_to_home = closest_n_pirates(start_x, 1*(start_y==0)+(dimensionY-2)*(start_y==(dimensionY-1)), min(5, len(list_of_signals)), pirate_pos=pirate_pos)
    #         index = 0
    #     while len(deploy_guards) < 2 and index < len(closest_to_home):
    #         deploy_guards[closest_to_home[index]] = [start_x, start_y, 'blank']
    #         index += 1
    #         deployed_guards = list(deploy_guards.keys())
    #     if start_x == 0 and start_y == 0 and 1 < len(deployed_guards):
    #         # print("Guards", deployed_guards[0], deployed_guards[1])
    #         deploy_guards[deployed_guards[0]][0] = 1
    #         deploy_guards[deployed_guards[0]][1] = 0
    #         deploy_guards[deployed_guards[0]][2] = 'left'
    #         deploy_guards[deployed_guards[1]][0] = 0
    #         deploy_guards[deployed_guards[1]][1] = 1
    #         deploy_guards[deployed_guards[1]][2] = 'down'
    #     if start_x == dimensionX-1 and start_y == 0 and 1 < len(deployed_guards):
    #         # print("Guards", deployed_guards[0], deployed_guards[1])
    #         deploy_guards[deployed_guards[0]][0] = dimensionX-2
    #         deploy_guards[deployed_guards[0]][1] = 0
    #         deploy_guards[deployed_guards[0]][2] = 'right'
    #         deploy_guards[deployed_guards[1]][0] = dimensionX-1
    #         deploy_guards[deployed_guards[1]][1] = 1
    #         deploy_guards[deployed_guards[1]][2] = 'down'
    #     if start_x == 0 and start_y == dimensionY-1 and 1 < len(deployed_guards):
    #         # print("Guards", deployed_guards[0], deployed_guards[1])
    #         deploy_guards[deployed_guards[0]][0] = 1
    #         deploy_guards[deployed_guards[0]][1] = dimensionY-1
    #         deploy_guards[deployed_guards[0]][2] = 'left'
    #         deploy_guards[deployed_guards[1]][0] = 0
    #         deploy_guards[deployed_guards[1]][1] = dimensionY-2
    #         deploy_guards[deployed_guards[1]][2] = 'up'
    #     if start_x == dimensionX-1 and start_y == dimensionY-1 and 1 < len(deployed_guards):
    #         # print("Guards", deployed_guards[0], deployed_guards[1])
    #         deploy_guards[deployed_guards[0]][0] = dimensionX-2
    #         deploy_guards[deployed_guards[0]][1] = dimensionY-1
    #         deploy_guards[deployed_guards[0]][2] = 'right'
    #         deploy_guards[deployed_guards[1]][0] = dimensionX-1
    #         deploy_guards[deployed_guards[1]][1] = dimensionY-2
    #         deploy_guards[deployed_guards[1]][2] = 'up'
    earlier_list_of_signals = list_of_signals
    signal_data['assassins'] = assassins
    signal = encode_signal(signal_data)
    team.setTeamSignal(signal)
