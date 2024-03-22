import random

name = "ByteMeBaby"





def moveTo(x , y , Pirate):
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
    
def moveStraight(direction, pirate):
    if direction == "n":
        return 1
    if direction == "s":
        return 3
    if direction == "e":
        return 2
    if direction == "w":
        return 4

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


def collectResourceX(pirate, lambda_):
    x, y = pirate.getPosition()
    xD, yD = pirate.getDeployPoint()
    xD += lambda_
    yD += lambda_
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    x, y = pirate.getPosition()
    pirate.setSignal("")
    s = pirate.trackPlayers()
    thirty9 = pirate.getDimensionX()-1

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

    # First quadrant deploy point
    if (xD < 20 and yD < 20):
        if (((y - yD) % 6)) < 3:
            if x != thirty9: return moveStraight('e', pirate)
            else: return moveStraight('s', pirate)
        else:
            if x != 0: return moveStraight('w', pirate)
            else: return moveStraight('s', pirate)

    # Second quadrant deploy point
    elif (xD >= 20 and yD < 20):
        if (((y - yD) % 6)) < 3:
            if x != 0: return moveStraight('w', pirate)
            else: return moveStraight('s', pirate)
        else:
            if x != thirty9: return moveStraight('e', pirate)
            else: return moveStraight('s', pirate)

    # Third quadrant deploy point
    elif (xD >= 20 and yD >= 20):
        if (((y - yD) % 6)) < 3:
            if x != 0: return moveStraight('w', pirate)
            else: return moveStraight('n', pirate)
        else:
            if x != thirty9: return moveStraight('e', pirate)
            else: return moveStraight('n', pirate)

    # Fourth quadrant deploy point
    elif (xD < 20 and yD >= 20):
        if (((y - yD) % 6)) < 3:
            if x != thirty9: return moveStraight('e', pirate)
            else: return moveStraight('n', pirate)
        else:
            if x != 0: return moveStraight('w', pirate)
            else: return moveStraight('n', pirate)

def collectResourceY(pirate, lambda_):
    x, y = pirate.getPosition()
    xD, yD = pirate.getDeployPoint()
    xD += lambda_
    yD += lambda_
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]

    x, y = pirate.getPosition()
    pirate.setSignal("")
    s = pirate.trackPlayers()
    thirty9 = pirate.getDimensionX()-1


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

    # First quadrant deploy point
    if (xD < 20 and yD < 20):
        if (x - xD) % 6 < 3:
            if y != thirty9: return moveStraight('s', pirate)
            else: return moveStraight('e', pirate)
        else:
            if y != 0: return moveStraight('n', pirate)
            else: return moveStraight('e', pirate)

    # Second quadrant deploy point
    elif (xD >= 20 and yD < 20):
        if (x - xD) % 6 < 3:
            if y != thirty9: return moveStraight('s', pirate)
            else: return moveStraight('w', pirate)
        else:
            if y != 0: return moveStraight('n', pirate)
            else: return moveStraight('w', pirate)

    # Third quadrant deploy point
    elif (xD >= 20 and yD >= 20):
        if (x - xD) % 6 < 3:
            if y != 0: return moveStraight('n', pirate)
            else: return moveStraight('w', pirate)
        else:
            if y != thirty9: return moveStraight('s', pirate)
            else: return moveStraight('w', pirate)

    # Fourth quadrant deploy point
    elif (xD < 20 and yD >= 20):
        if (x - xD) % 6 < 3:
            if y != 0: return moveStraight('n', pirate)
            else: return moveStraight('e', pirate)
        else:
            if y != thirty9: return moveStraight('s', pirate)
            else: return moveStraight('e', pirate)

def moveToRow(pirate, lambda_):
    x, y = pirate.getPosition()
    thirty9 = pirate.getDimensionX()-1

    # Calculate the nearest row
    r_up = y - y % 3 + lambda_
    if r_up < y:
        r_up += 3

    r_down = y - y % 3 + lambda_
    if r_down > y:
        r_down -= 3

    # Choose the nearest row
    r = r_up if abs(r_up - y) < abs(r_down - y) else r_down

    # Move the pirate towards the target row
    if y < r and y < thirty9:  # Ensure the pirate doesn't move out of bounds
        return moveStraight('s', pirate)
    elif y > r and y > 0:  # Ensure the pirate doesn't move out of bounds
        return moveStraight('n', pirate)
    else:
        # If the pirate is already on the target row, do nothing
        return 0  

def moveToCol(pirate, lambda_):
    x, y = pirate.getPosition()
    thirty9 = pirate.getDimensionX()-1

    # Calculate the nearest column
    c_right = x - x % 3 + lambda_
    if c_right < x:
        c_right += 3

    c_left = x - x % 3 + lambda_
    if c_left > x:
        c_left -= 3

    # Choose the nearest column
    c = c_right if abs(c_right - x) < abs(c_left - x) else c_left

    # Move the pirate towards the target column
    if x < c and x < thirty9:  # Ensure the pirate doesn't move out of bounds
        return moveStraight('e', pirate)
    elif x > c and x > 0:  # Ensure the pirate doesn't move out of bounds
        return moveStraight('w', pirate)
    else:
        # If the pirate is already on the target column, do nothing
        return 0

def notCenterorCorner(pirate):
    x,y = pirate.getPosition()
    if (x>15 and x<25) and (y>15 and y<25):
        movexory = random.randint(0,1)
        if movexory == 0:
            if (x-20 > 0):
                return 2
            else: 
                return 4
        else:
            if (y-20 > 0):
                return 3
            else: 
                return 1
    elif (x<10 and y<10):
        movexory = random.randint(0,1)
        if movexory == 0:
            return 2
        else:
            return 3
    elif (x>30 and y<10):
        movexory = random.randint(0,1)
        if movexory == 0:
            return 4
        else:
            return 3
    elif (x>30 and y>30):
        movexory = random.randint(0,1)
        if movexory == 0:
            return 1
        else:
            return 4
    elif (x<10 and y>30):
        movexory = random.randint(0,1)
        if movexory == 0:
            return 1
        else:
            return 2
    else:
        return random.randint(1,4)


def diag (pirate):
    time = pirate.getCurrentFrame()
    xd=int(pirate.getDeployPoint()[0])
    yd=int(pirate.getDeployPoint()[1])
    
    xz = int(pirate.getDimensionX())
    yz = int(pirate.getDimensionY())
    x=int(pirate.getPosition()[0])
    y=int(pirate.getPosition()[1])
    print(x,y)
    print((xz-xd-1), yz-yd-1)
    if (time %300 < 150):
        return moveTo((xz-xd-1), yz-yd-1, pirate)
    else:
        return moveTo(xd, yd, pirate)
    


def howtomove(pirate):
    x, y = pirate.getPosition()
    z = random.randint(1,10)
    if z==1 :
        return random.randint(1,4)
    if z > 1:
        return diag(pirate)


def how2move(pirate):
    x, y = pirate.getPosition()
    z = random.randint(1,9)
    if z < 7 :
        return random.randint(1,4)
    if z > 6:
        return notCenterorCorner(pirate)


def ActPirate(pirate):
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    x, y = pirate.getPosition()
    pirate.setSignal("")
    s = pirate.trackPlayers()
    time = pirate.getCurrentFrame()
    id = int(pirate.getID())
    squad=id%25


    x,y = pirate.getPosition() 

    if (pirate.getCurrentFrame() == 2):
        if (squad == 1):    return moveToRow(pirate,0)
        if (squad == 2):    return moveToRow(pirate,1)
        if (squad == 3):    return moveToRow(pirate,2)

        if (squad == 4):    return moveToCol(pirate,1)
        if (squad == 5):    return moveToCol(pirate,2)
        if (squad == 6):    return moveToCol(pirate,0)

    if (pirate.getCurrentFrame() >= 3 and pirate.getCurrentFrame()<500):
        if (squad == 1):    return collectResourceX(pirate, 0)
        if (squad == 2):    return collectResourceX(pirate, 1)
        if (squad == 3):    return collectResourceX(pirate, 2)

        if (squad == 4):    return collectResourceY(pirate, 1)
        if (squad == 5):    return collectResourceY(pirate, 2)
        if (squad == 6):    return collectResourceY(pirate, 0)
    elif (pirate.getCurrentFrame() >= 3 and pirate.getCurrentFrame()>=500):
        if (squad == 1):    return random.randint(1,4)
        if (squad == 2):    return random.randint(1,4)
        if (squad == 3):    return random.randint(1,4)

        if (squad == 4):    return random.randint(1,4)
        if (squad == 5):    return random.randint(1,4)
        if (squad == 6):    return random.randint(1,4)
    
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



    if pirate.getTeamSignal() != "" and time>300:
        s = pirate.getTeamSignal()
        l = s.split(",")
        x = int(l[0][1:])
        y = int(l[1])
        goornot = random.randint(0,1)
        if goornot < 1 :
            return moveTo(x, y, pirate)
        else: 
            return howtomove(pirate)
    else:
        return howtomove(pirate)

def ActTeam(team):
    l = team.trackPlayers()
    s = team.getTeamSignal()


    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)

    if s:
        island_no = int(s[0])
        signal = l[island_no - 1]
        if signal == "myCaptured":
            team.setTeamSignal("")