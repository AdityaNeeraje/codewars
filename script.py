import random
import math

from pkg_resources import run_main

from engine import island, pirate

name = "script"

island_pos = {
    'island1': (0, 0),
    'island2': (0, 0),
    'island3': (0, 0)
}

gunpowder = 0
rum = 0
wood = 0

guards = {} # This has the id of every living guard as a key and their position and direction relative to island center as values.
colonists = {} # This has the id of every living colonist as a key and the coordinate of their island center as value
pirates = {} # This has the id of every living pirate as a key and the generating frame and coordinates as values
assassins = []
earlier_list_of_signals = []

# Our resources
gunPowder = 0
rum = 0
wood = 0


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
    return moveTo(guards[pirate][0], guards[pirate][1], pirate)

def ActColonist(x,y,pirate):
    up = pirate.investigate_up()[1]
    down = pirate.investigate_down()[1]
    left = pirate.investigate_left()[1]
    right = pirate.investigate_right()[1]
    ne = pirate.investigate_ne()[1]
    nw = pirate.investigate_nw()[1]
    se = pirate.investigate_se()[1]
    sw = pirate.investigate_sw()[1]
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
    # print(up[0:-1] == "", down, left, right, nw, ne, se, sw)
    # print(up[0], down[0], left[0], right[0], nw[0], ne[0], se[0], sw[0])
    # print(f'-{up[0]}--{down[0]}--{left[0]}--{right[0]}--{nw[0]}--{ne[0]}--{se[0]}--{sw[0]}-')
    # print(f'-{up[0][-1]}--{down[0][:-1]}--{left[0][-1]}--{right[0][-1]}--{nw[0][-1]}--{ne[0][-1]}--{se[0][-1]}--{sw[0][-1]}-')
    if nw[0][0:-1] == "island" and up[0][0:-1] == "blank" and left[0][0:-1] == "blank":
        # print('Hello!!!')
        island_pos[nw[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] - 2)
    if ne[0][0:-1] == "island" and up[0][0:-1] == "blank" and right[0][0:-1] == "blank":
        # print('Hello!!!')
        island_pos[ne[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] - 2)
    if se[0][0:-1] == "island" and down[0][0:-1] == "blank" and right[0][0:-1] == "blank":
        # print('Hello!!!')
        island_pos[se[0]] = (pirate.getPosition()[0] + 2, pirate.getPosition()[1] + 2)
    if sw[0][0:-1] == "island" and down[0][0:-1] == "blank" and left[0][0:-1] == "blank":
        # print('Hello!!!')
        island_pos[sw[0]] = (pirate.getPosition()[0] - 2, pirate.getPosition()[1] + 2)
    if up[0][0:-1] == "island" and nw[0][0:-1] == "island" and ne[0][0:-1] == "island":
        # print('Hello!!!')
        island_pos[up[0]] = (pirate.getPosition()[0], pirate.getPosition()[1]-2)
    if left[0][0:-1] == "island" and nw[0][0:-1] == "island" and sw[0][0:-1] == "island":
        # print('Hello!!!')
        island_pos[left[0]] = (pirate.getPosition()[0]-2, pirate.getPosition()[1])
    if down[0][0:-1] == "island" and sw[0][0:-1] == "island" and se[0][0:-1] == "island":
        # print('Hello!!!')
        island_pos[down[0]] = (pirate.getPosition()[0], pirate.getPosition()[1]+2)
    if right[0][0:-1] == "island" and ne[0][0:-1] == "island" and se[0][0:-1] == "island":
        # print('Hello!!!')
        island_pos[right[0]] = (pirate.getPosition()[0]+2, pirate.getPosition()[1])

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

# game_pos = 0
# 0: Game just started
# 1: One Island found
# 2: Second Island found
# 3: Island being captured

# Make an enum for the game state
class GameState:
    START = 0
    ONE_ISLAND = 1
    TWO_ISLANDS = 2
    CAPTURING = 3

current_game_state = GameState.START

def ColoniseIsland(pirate):
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

pirate_pos = dict()
pirate_goal = dict()
island_pos = dict()

# Get the closest n pirates to a given position
def closest_n_pirates(x, y, n, team):
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
    s = pirate.GetCurretPosition()
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
    global pirate_pos, assassins, gunpowder, rum, wood
    p = list(pirate.getDeployPoint())
    id = int(pirate.getID())
    pirate.setSignal(f"{id}")
    if pirate in assassins:
        print(f'Gunpowder: {gunPowder}')
        if gunPowder > 100 or id%2 == 1:
            print('I am ass')
            return moveTo(39-p[0], 39-p[1], pirate)
        else:
            return moveTo(38-p[0], 38-p[1], pirate)
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
    
    checkIsland(pirate=pirate)

    if pirate.getID() not in pirates:
        pirates[pirate.getID()] = [pirate.getCurrentFrame(), p[0], p[1]]
    frame = pirate.getCurrentFrame() - pirate.generatingFrame
    if (frame < 75):
        return moveTo(39-p[0], 39-p[1], pirate)
    if (frame%75 < 38 and frame%600 < 300 and frame < 1000):
        return moveTo(random.randint(17, 23), random.randint(17, 23), pirate)
    if(frame % 75 >= 38 and frame%600 < 300 and frame < 1000):
        if id%16 == 1:
            return moveTo(p[0], p[1], pirate)
        elif id%4 == 2:
            return moveTo(p[0], 39-p[1], pirate)
        elif id%4 == 3:
            return moveTo(39-p[0], p[1], pirate)
        else:
            return moveTo(39-p[0], 39-p[1], pirate)
    if(frame % 40 >= 20 and frame%600 >= 300 and frame < 1000):
        if id%8 == 1:
            return moveTo(random.randint(15,25), p[1], pirate)
        elif id%8 == 5:
            return moveTo(p[0], random.randint(15,25), pirate)
        elif id%4 == 2:
            return moveTo(39-p[0], random.randint(15,25), pirate)
        else:
            return moveTo(random.randint(15,25), 39-p[1], pirate)
    if (frame%40 < 20 and frame%600 >= 300 and frame < 1000):
        return moveTo(random.randint(17, 23), random.randint(17, 23), pirate)
    if (frame % 80 < 40 and 1000 <= frame < 2000):
        return moveTo(39-p[0], p[1], pirate)
    elif frame % 80 > 40 and 1000 <= frame < 2000:
        return moveTo(p[0], 39-p[1], pirate)
    else:
        up = pirate.investigate_up()
        down = pirate.investigate_down()
        left = pirate.investigate_left()
        right = pirate.investigate_right()
        x, y = pirate.getPosition()
        pirate.setSignal("")
        s = pirate.trackPlayers()
        
        if (
            (up == "island1" and s[0] != "myCaptured")
            or (up == "island2" and s[1] != "myCaptured")
            or (up == "island3" and s[2] != "myCaptured")
        ):
            s = up[-1] + str(x) + "," + str(y - 1)
            b += 1
            pirate.setSignal("mid")

        if (
            (down == "island1" and s[0] != "myCaptured")
            or (down == "island2" and s[1] != "myCaptured")
            or (down == "island3" and s[2] != "myCaptured")
        ):
            s = down[-1] + str(x) + "," + str(y + 1)
            b += 1
            pirate.setSignal("mid")

        if (
            (left == "island1" and s[0] != "myCaptured")
            or (left == "island2" and s[1] != "myCaptured")
            or (left == "island3" and s[2] != "myCaptured")
        ):
            s = left[-1] + str(x - 1) + "," + str(y)
            b += 1

            pirate.setSignal("mid")


        if (
            (right == "island1" and s[0] != "myCaptured")
            or (right == "island2" and s[1] != "myCaptured")
            or (right == "island3" and s[2] != "myCaptured")
        ):
            s = right[-1] + str(x + 1) + "," + str(y)
            b += 1
            pirate.setSignal("mid")


        if (
            (up == "island1" and s[0] == "myCaptured")
            or (up == "island2" and s[1] == "myCaptured")
            or (up == "island3" and s[2] == "myCaptured") 
        ):
            pirate.setSignal("mid")

        if (
            (right == "island1" and s[0] == "myCaptured")
            or (right == "island2" and s[1] == "myCaptured")
            or (right == "island3" and s[2] == "myCaptured") 
        ):
            # pirate.SetTeamSignal(s)
            pirate.setSignal("mid")

        if (
            (down == "island1" and s[0] == "myCaptured")
            or (down == "island2" and s[1] == "myCaptured")
            or (down == "island3" and s[2] == "myCaptured") 
        ):
            s = down[-1] + str(x) + "," + str(y + 1)
            pirate.setSignal("mid")


        if (
                (left == "island1" and s[0] == "myCaptured")
                or (left == "island2" and s[1] == "myCaptured")
                or (left == "island3" and s[2] == "myCaptured") 
            ):
                pirate.setSignal("mid")

        if (up == "friend"):
            if checkIsland(pirate) and b<= 4:
                pirate.setSignal("mid")
            else:
                s = up[-1] + str(x) + "," + str(y + 1)
                pirate.setSignal("move")
        
        if (down == "friend"):
            if checkIsland(pirate) and b<= 4:
                pirate.setSignal("mid")
            else:
                s = up[-1] + str(x) + "," + str(y - 1)
                pirate.setSignal("move")
        
        if (left == "friend"):
            if checkIsland(pirate) and b<= 4:
                pirate.setSignal("mid")
            else:
                s = up[-1] + str(x - 1) + "," + str(y)
                pirate.setSignal("move")
        
        if (right == "friend" ) :
            if checkIsland(pirate) and b<= 4:
                pirate.setSignal("mid")
            else:
                s = up[-1] + str(x + 1) + "," + str(y)
                pirate.setSignal("move")

        if (up != "friend" and up != "enemy" ):
            if checkIsland(pirate) and b<= 4:
                pirate.setSignal("mid")
            else:
                pirate.setSignal("random")
        
        if (down != "friend" and down != "enemy"):
            if checkIsland(pirate) and b<= 4:
                pirate.setSignal("mid")
            else:
                pirate.setSignal("random")
        
        if (left != "friend" and left != "enemy" ):
            if checkIsland(pirate) and b<= 4:
                pirate.setSignal("mid")
            else:
                pirate.setSignal("random")
        
        if (right != "friend" and right != "enemy"):
            if checkIsland(pirate) and b<= 4:
                pirate.setSignal("mid")
            else:
                pirate.setSignal("random")

        if pirate.getSignal() =="mid":
            return 0

        elif pirate.getSignal() == "move":
            s = pirate.getTeamSignal()
            l = s.split(",")
            x = int(l[0][1:])
            y = int(l[1])
            return moveTo(x, y, pirate)
        
        elif pirate.getSignal() == "random":
            return random.randint(1,4)

def ActTeam(team):
    global earlier_list_of_signals, assassins, gunPowder, wood, rum

    gunPowder = team.getTotalGunpowder()
    wood = team.getTotalWood()
    rum = team.getTotalRum()

    list_of_signals = team.getListOfSignals()
    new_pirates = [int(id) for id in list_of_signals if id not in earlier_list_of_signals]
    dead_pirates = [int(id) for id in earlier_list_of_signals if id not in list_of_signals]
    for id in dead_pirates:
        if id in assassins:
            assassins.remove(id)
    if len(assassins) < 5:
        assassins = closest_n_pirates(39-team.getDeployPoint()[0], 39-team.getDeployPoint()[1], 5, team)
    earlier_list_of_signals = list_of_signals.copy()
    # gunpowder = team.getTotalGunpowder()
    pass
