# import random
# import math

# name = "scriptblue"


# def moveTo(x, y, Pirate):
#     position = Pirate.getPosition()
#     if position[0] == x and position[1] == y:
#         return 0
#     if position[0] == x:
#         return (position[1] < y) * 2 + 1
#     if position[1] == y:
#         return (position[0] > x) * 2 + 2
#     if random.randint(1, 2) == 1:
#         return (position[0] > x) * 2 + 2
#     else:
#         return (position[1] < y) * 2 + 1

# pos = dict()

# def ActPirate(pirate):
#     up = pirate.investigate_up()[0]
#     down = pirate.investigate_down()[0]
#     left = pirate.investigate_left()[0]
#     right = pirate.investigate_right()[0]
#     x, y = pirate.getPosition()
#     pirate.setSignal("")
#     s = pirate.trackPlayers()
    
#     if (
#         (up == "island1" and s[0] != "myCaptured")
#         or (up == "island2" and s[1] != "myCaptured")
#         or (up == "island3" and s[2] != "myCaptured")
#     ):
#         s = up[-1] + str(x) + "," + str(y - 1)
#         pirate.setTeamSignal(s)

#     if (
#         (down == "island1" and s[0] != "myCaptured")
#         or (down == "island2" and s[1] != "myCaptured")
#         or (down == "island3" and s[2] != "myCaptured")
#     ):
#         s = down[-1] + str(x) + "," + str(y + 1)
#         pirate.setTeamSignal(s)

#     if (
#         (left == "island1" and s[0] != "myCaptured")
#         or (left == "island2" and s[1] != "myCaptured")
#         or (left == "island3" and s[2] != "myCaptured")
#     ):
#         s = left[-1] + str(x - 1) + "," + str(y)
#         pirate.setTeamSignal(s)

#     if (
#         (right == "island1" and s[0] != "myCaptured")
#         or (right == "island2" and s[1] != "myCaptured")
#         or (right == "island3" and s[2] != "myCaptured")
#     ):
#         s = right[-1] + str(x + 1) + "," + str(y)
#         pirate.setTeamSignal(s)
#     global pos
#     pos[pirate.getID()] = [x, y]
#     print(pos)
    
#     if pirate.getTeamSignal() != "":
#         s = pirate.getTeamSignal()
#         l = s.split(",")
#         x = int(l[0][1:])
#         y = int(l[1])
    
#         return moveTo(x, y, pirate)

#     else:
#         return random.randint(1, 4)


# def ActTeam(team):
#     l = team.trackPlayers()
#     s = team.getTeamSignal()

#     team.buildWalls(1)
#     team.buildWalls(2)
#     team.buildWalls(3)
#     # print(team.getTeamSignal())
#     # print(team.trackPlayers())
#     if s:
#         island_no = int(s[0])
#         signal = l[island_no - 1]
#         if signal == "myCaptured":
#             team.setTeamSignal("")

import random
import math

name = "scriptblue"


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


def moveAway(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return random.randint(1, 4)
    if random.randint(1, 2) == 1:
        return (position[0] < x) * 2 + 2
    else:
        return (position[1] > y) * 2 + 1

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
    
def checkIsland(pirate):
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    if (up[0:-1] == "island" or down[0:-1] == "island") and (left[0:-1] == "island" or right[0:-1] == "island"):
        return True
    else:
        return False


def setthem(pirate):
    s = pirate.GetCurretPosition()
    x = s[0]
    y = s[1]

b = 0

def checkIsland(pirate):
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    if (up[0:-1] == "island" or down[0:-1] == "island") and (left[0:-1] == "island" or right[0:-1] == "island"):
        return True
    else:
        return False

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

def checkfriends(pirate , quad ):
    sum = 0 
    up = pirate.investigate_up()[1]
    print(up)
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
    
    if( x == 0 and y == 0):
        return random.randint(1,4)
    
    if(sorted_dict[list(sorted_dict.keys())[3]] == 0 ):
        return random.randint(1,4)
    
    if(list(sorted_dict.keys())[0] == 'sw'):
        return moveTo(x-1 , y+1 , pirate)
    elif(list(sorted_dict.keys())[0] == 'se'):
        return moveTo(x+1 , y+1 , pirate)
    elif(list(sorted_dict.keys())[0] == 'ne'):
        return moveTo(x+1 , y-1 , pirate)
    elif(list(sorted_dict.keys())[0] == 'nw'):
        return moveTo(x-1 , y-1 , pirate)

def ActPirate(pirate):
    # global pirate_pos
    # pirate_pos[pirate.getID()] = pirate.getPosition()
    p = pirate.getDeployPoint()
    frame = pirate.getCurrentFrame()
    if(frame % 150 < 75 and frame < 2000):
        return moveTo(39-p[0], 39-p[1], pirate)
    elif(frame % 150 > 75 and frame < 2000):
        return moveTo(p[0], p[1], pirate)
    elif(frame < 2500):
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
    elif(frame <= 3000):
        up = pirate.investigate_up()[0]
        down = pirate.investigate_down()[0]
        left = pirate.investigate_left()[0]
        right = pirate.investigate_right()[0]
        x, y = pirate.getPosition()
        pirate.setSignal("")
        s = pirate.trackPlayers()
        
        if (
            (up == "island1" and s[0] != "myCaptured")
            or (up == "island2" and s[1] != "myCaptured")
            or (up == "island3" and s[2] != "myCaptured")
        ):
            s = up[-1] + str(x) + "," + str(y - 1)
            pirate.setTeamSignal(s)

        if (
            (down == "island1" and s[0] != "myCaptured")
            or (down == "island2" and s[1] != "myCaptured")
            or (down == "island3" and s[2] != "myCaptured")
        ):
            s = down[-1] + str(x) + "," + str(y + 1)
            pirate.setTeamSignal(s)

        if (
            (left == "island1" and s[0] != "myCaptured")
            or (left == "island2" and s[1] != "myCaptured")
            or (left == "island3" and s[2] != "myCaptured")
        ):
            s = left[-1] + str(x - 1) + "," + str(y)
            pirate.setTeamSignal(s)

        if (
            (right == "island1" and s[0] != "myCaptured")
            or (right == "island2" and s[1] != "myCaptured")
            or (right == "island3" and s[2] != "myCaptured")
        ):
            s = right[-1] + str(x + 1) + "," + str(y)
            pirate.setTeamSignal(s)

        
        if pirate.getTeamSignal() != "":
            s = pirate.getTeamSignal()
            l = s.split(",")
            x = int(l[0][1:])
            y = int(l[1])
        
            return moveTo(x, y, pirate)

        else:
            return spread(pirate)

def ActTeam(team):
    pass    