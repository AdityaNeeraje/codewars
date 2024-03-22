import random
import math


name = "sexy"


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
    nw = pirate.investigate_nw()
    ne = pirate.investigate_ne()
    sw = pirate.investigate_sw()
    se = pirate.investigate_se()
    if ("island" in up[0] or "island" in down[0]) and ("island" in left[0] or "island" in right[0]):
        return True
    else:
        return False
    
    
    # 1:up
    # 2:right
    # 3:down
    # 4:left

def ActPirate(pirate):
    _id=int(pirate.getID())
    x=int(pirate.getPosition()[0])
    y=int(pirate.getPosition()[1])
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    nw = pirate.investigate_nw()
    ne = pirate.investigate_ne()
    sw = pirate.investigate_sw()
    se = pirate.investigate_se()
    tp = pirate.trackPlayers()
    squad=_id%4
        
    # if island is not captured by us squad[2] will go to the island   

    # scouting captured island
    position = pirate.getPosition()
    if pirate.getTeamSignal()== '':
        team_sig="0,"+"x,"+"y,"+"0,"+"x,"+"y,"+"0,"+"x,"+"y,"+'0,'+'x,'+'y'
        pirate.setTeamSignal(team_sig)
        
    s = pirate.getTeamSignal()
    l = s.split(",")
#team signalling
    if(l[0]=='1' and tp[0]!="myCaptured"):
        if _id%7==0:
            moveTo(int(l[1]),int(l[2]),pirate)
    if(l[3]=='2' and tp[1]!="myCaptured"):
        if _id%7==0:
            moveTo(int(l[4]),int(l[5]),pirate)
    if(l[6]=='3' and tp[2]!="myCaptured"):
        if _id%7==0:
            moveTo(int(l[7]),int(l[8]),pirate)
        
    if (
        (up == "island1" and tp[0] != "myCaptured" and l[0]!=up[-1]) 
        or (up == "island2" and tp[1] != "myCaptured" and l[3]!=up[-1])
        or (up == "island3" and tp[2] != "myCaptured" and l[6]!=up[-1])
    ):
        if up[-1]=='1':
            l[0]=1
            l[1]=str(x)
            l[2]=str(y)
        if up[-1]=='2':
            l[3]=2
            l[4]=str(x)
            l[5]=str(y)
        if up[-1]=='3':
            l[6]=3
            l[7]=str(x)
            l[8]=str(y)
        l[9]=str(squad)
        l[10]=str(x)
        l[11]=str(y)
        sig=','.join(map(str,l))
        pirate.setTeamSignal(sig)
        return moveTo(x,y-1,pirate)
    if (
        (down == "island1" and tp[0] != "myCaptured" and l[0]!=down[-1])
        or (down == "island2" and tp[1] != "myCaptured" and l[3]!=down[-1])
        or (down == "island3" and tp[2] != "myCaptured" and l[6]!=down[-1])
    ):
        if down[-1]=='1':
            l[0]=1
            l[1]=str(x)
            l[2]=str(y)
        if down[-1]=='2':
            l[3]=2
            l[4]=str(x)
            l[5]=str(y)
        if down[-1]=='3':
            l[6]=3
            l[7]=str(x)
            l[8]=str(y)
        l[9]=str(squad)
        l[10]=str(x)
        l[11]=str(y)
        sig=','.join(map(str,l))
        pirate.setTeamSignal(sig)
        return moveTo(x,y+1,pirate)

    if (
        (left == "island1" and tp[0] != "myCaptured" and l[0]!=left[-1])
        or (left == "island2" and tp[1] != "myCaptured" and l[3]!=left[-1])
        or (left == "island3" and tp[2] != "myCaptured" and l[6]!=left[-1])
    ):
        if left[-1]=='1':
            l[0]=1
            l[1]=str(x)
            l[2]=str(y)
        if left[-1]=='2':
            l[3]=2
            l[4]=str(x)
            l[5]=str(y)
        if left[-1]=='3':
            l[6]=3
            l[7]=str(x)
            l[8]=str(y)
        l[9]=str(squad)
        l[10]=str(x)
        l[11]=str(y)
        sig=','.join(map(str,l))
        pirate.setTeamSignal(sig)
        return moveTo(x-1,y,pirate)

    if (
        (right == "island1" and tp[0] != "myCaptured" and l[0]!=right[-1])
        or (right == "island2" and tp[1] != "myCaptured" and l[3]!=right[-1])
        or (right == "island3" and tp[2] != "myCaptured" and l[6]!=right[-1])
    ):
        if right[-1]=='1':
            l[0]=1
            l[1]=str(x)
            l[2]=str(y)
        if right[-1]=='2':
            l[3]=2
            l[4]=str(x)
            l[5]=str(y)
        if right[-1]=='3':
            l[6]=3
            l[7]=str(x)
            l[8]=str(y)
        l[9]=str(squad)
        l[10]=str(x)
        l[11]=str(y)
        sig=','.join(map(str,l))
        pirate.setTeamSignal(sig)
        return moveTo(x+1,y,pirate)

    if (
        (nw == "island1" and tp[0] != "myCaptured" and l[0]!=nw[-1])
        or (nw == "island2" and tp[1] != "myCaptured" and l[3]!=nw[-1])
        or (nw == "island3" and tp[2] != "myCaptured" and l[6]!=nw[-1])
    ):
        if nw[-1]=='1':
            l[0]=1
            l[1]=str(x)
            l[2]=str(y)
        if nw[-1]=='2':
            l[3]=2
            l[4]=str(x)
            l[5]=str(y)
        if nw[-1]=='3':
            l[6]=3
            l[7]=str(x)
            l[8]=str(y)
        l[9]=str(squad)
        l[10]=str(x)
        l[11]=str(y)
        sig=','.join(map(str,l))
        pirate.setTeamSignal(sig)
        return moveTo(x-1,y-1,pirate)

    if (
        (se == "island1" and tp[0] != "myCaptured" and l[0]!=se[-1])
        or (se == "island2" and tp[1] != "myCaptured" and l[3]!=se[-1])
        or (se == "island3" and tp[2] != "myCaptured" and l[6]!=se[-1])
    ):
        if se[-1]=='1':
            l[0]=1
            l[1]=str(x)
            l[2]=str(y)
        if se[-1]=='2':
            l[3]=2
            l[4]=str(x)
            l[5]=str(y)
        if se[-1]=='3':
            l[6]=3
            l[7]=str(x)
            l[8]=str(y)
        l[9]=str(squad)
        l[10]=str(x)
        l[11]=str(y)
        sig=','.join(map(str,l))
        pirate.setTeamSignal(sig)
        return moveTo(x+1,y+1,pirate)

    if (
        (ne == "island1" and tp[0] != "myCaptured" and l[0]!=ne[-1])
        or (ne == "island2" and tp[1] != "myCaptured" and l[3]!=ne[-1])
        or (ne == "island3" and tp[2] != "myCaptured" and l[6]!=ne[-1])
    ):
        if ne[-1]=='1':
            l[0]=1
            l[1]=str(x)
            l[2]=str(y)
        if ne[-1]=='2':
            l[3]=2
            l[4]=str(x)
            l[5]=str(y)
        if ne[-1]=='3':
            l[6]=3
            l[7]=str(x)
            l[8]=str(y)
        l[9]=str(squad)
        l[10]=str(x)
        l[11]=str(y)
        sig=','.join(map(str,l))
        pirate.setTeamSignal(sig)
        return moveTo(x+1,y-1,pirate)

    if (
        (sw == "island1" and tp[0] != "myCaptured" and l[0]!=sw[-1])
        or (sw == "island2" and tp[1] != "myCaptured" and l[3]!=sw[-1])
        or (sw == "island3" and tp[2] != "myCaptured" and l[6]!=sw[-1])
    ):
        if sw[-1]=='1':
            l[0]=1
            l[1]=str(x)
            l[2]=str(y)
        if sw[-1]=='2':
            l[3]=2
            l[4]=str(x)
            l[5]=str(y)
        if sw[-1]=='3':
            l[6]=3
            l[7]=str(x)
            l[8]=str(y)
        l[9]=str(squad)
        l[10]=str(x)
        l[11]=str(y)
        sig=','.join(map(str,l))
        pirate.setTeamSignal(sig)
        return moveTo(x-1,y+1,pirate)
    
# some condition for pirates which are alloted for scouting
    if (checkIsland(pirate) and (_id%8==0 or _id%8==1 or _id%8==2)) or pirate.getSignal()=="scout":
        
        if position != IslandCenter(pirate,position):
            return moveTo(IslandCenter(pirate,position)[0],IslandCenter(pirate,position)[1],pirate)
        if (up==("island1" or "island2" or "island3") and pirate.investigate_up()[1]==("enemy" ) and pirate.getTotalGunpowder() >100 ):
            return 1
        if (down==("island1" or "island2" or "island3") and pirate.investigate_down()[1]==("enemy" ) and pirate.getTotalGunpowder() >100 ):
            return 3
        if (left==("island1" or "island2" or "island3") and pirate.investigate_left()[1]==("enemy" ) and pirate.getTotalGunpowder() >100 ):
            return 4
        if (right==("island1" or "island2" or "island3") and pirate.investigate_right()[1]==("enemy" ) and pirate.getTotalGunpowder() >100):
            return 2
        pirate.setSignal("scout")
        return circleAround(position[0],position[1],1,pirate)    
    

    if (up==("island1" or "island2" or "island3") and pirate.investigate_up()[1]==("enemy" ) and pirate.getTotalGunpowder() >100 and checkIsland(pirate)==True):
        return 1
    if (down==("island1" or "island2" or "island3") and pirate.investigate_down()[1]==("enemy" ) and pirate.getTotalGunpowder() >100 and checkIsland(pirate)==True):
        return 3
    if (left==("island1" or "island2" or "island3") and pirate.investigate_left()[1]==("enemy" ) and pirate.getTotalGunpowder() >100 and checkIsland(pirate)==True):
        return 4
    if (right==("island1" or "island2" or "island3") and pirate.investigate_right()[1]==("enemy" ) and pirate.getTotalGunpowder() >100 and checkIsland(pirate)==True):
        return 2



#teams

    if pirate.getSignal() == '':
        pirate.setSignal('988080')
    # if (squad == 2):
    #     return moveAway(x, y, pirate)
    # _id % 4 == 1 vertical                          1   2
    # _id % 4 == 0 horizontal                        4   3
    return Direction(pirate)


def ActTeam(team):
    l = team.trackPlayers()
    s = team.getTeamSignal()

    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)
    

def Direction(pirate):
    up = pirate.investigate_up()
    down = pirate.investigate_down()
    left = pirate.investigate_left()
    right = pirate.investigate_right()
    if up[0] == 'wall' and left[0] == 'wall':
        signal = pirate.getSignal()
        signal = '1' + signal[1:]
        pirate.setSignal(signal)  # 1   2
    elif up[0] == 'wall' and right[0] == 'wall':  # 4   3
        signal = pirate.getSignal()
        signal = '2' + signal[1:]
        pirate.setSignal(signal)
    elif down[0] == 'wall' and right[0] == 'wall':
        signal = pirate.getSignal()
        signal = '3' + signal[1:]
        pirate.setSignal(signal)
    elif down[0] == 'wall' and left[0] == 'wall':
        signal = pirate.getSignal()
        signal = '4' + signal[1:]
        pirate.setSignal(signal)
    elif up[0] == 'wall':
        signal = pirate.getSignal()
        if pirate.getSignal() == '4':
            signal = '2' + signal[1:]
        else:
            signal = '1' + signal[1:]
        pirate.setSignal(signal)
    elif down[0] == 'wall':
        signal = pirate.getSignal()
        if pirate.getSignal()[0] == '1':
            signal = '4' + signal[1:]
        else:
            signal = '3' + signal[1:]
        pirate.setSignal(signal)
    elif left[0] == 'wall':
        signal = pirate.getSignal()
        if pirate.getSignal() == '2':
            signal = '1' + signal[1:]
        else:
            signal = '4' + signal[1:]
        pirate.setSignal(signal)
    elif right[0] == 'wall':
        signal = pirate.getSignal()
        if pirate.getSignal() == '1':
            signal = '3' + signal[1:]
        else:
            signal = '2' + signal[1:]
        pirate.setSignal(signal)
    dir = pirate.getSignal()[0]
    # if int(pirate.getID()) % 4 == 0:
    #     if dir == '1':
    #         arr = [3, 3, 2, 2, 2, 2, 2, 2, 2, 2]
    #         return random.choice(arr)
    #     if dir == '2':
    #         arr = [3, 3, 4, 4, 4, 4, 4, 4, 4, 4]
    #         return random.choice(arr)
    #     if dir == '3':
    #         arr = [1, 1, 4, 4, 4, 4, 4, 4, 4, 4]
    #         return random.choice(arr)
    #     if dir == '4':
    #         arr = [1, 1, 2, 2, 2, 2, 2, 2, 2, 2]
    #         return random.choice(arr)
    # if int(pirate.getID()) % 4 == 1:
    #     if dir == '1':
    #         arr = [3, 3, 3, 3, 3, 3, 3, 3, 2, 2]
    #         return random.choice(arr)
    #     if dir == '2':
    #         arr = [3, 3, 3, 3, 3, 3, 3, 3, 4, 4]
    #         return random.choice(arr)
    #     if dir == '3':
    #         arr = [1, 1, 1, 1, 1, 1, 1, 1, 4, 4]
    #         return random.choice(arr)
    #     if dir == '4':
    #         arr = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2]
    #         return random.choice(arr)
    # else:
    if int(pirate.getID())%4 == 0 or int(pirate.getID())%4 == 1:
        if dir == '1':  
            arr = [3, 2]
            return random.choice(arr)
        if dir == '2':
            arr = [3, 4]
            return random.choice(arr)
        if dir == '3':
            arr = [1, 4]
            return random.choice(arr)
        if dir == '4':
            arr = [1, 2]
            return random.choice(arr)
    if int(pirate.getID())%4 == 2:
        if dir == '1':  
            arr = [2,2,2,2,3]
            print(random.choice(arr))
            return random.choice(arr)
        if dir == '2':
            arr = [3, 4,4,4,4]
            return random.choice(arr)
        if dir == '3':
            arr = [1, 4,4,4,4]
            return random.choice(arr)
        if dir == '4':
            arr = [1, 2,2,2,2]
            return random.choice(arr)
    if int(pirate.getID())%4 == 3:
        if dir == '1':  
            arr = [2,3,3,3,3]
            return random.choice(arr)
        if dir == '2':
            arr = [3, 3,3,4,3]
            return random.choice(arr)
        if dir == '3':
            arr = [1, 1,1,4,1]
            return random.choice(arr)
        if dir == '4':
            arr = [1, 1,1,2,1]
            return random.choice(arr)
        # return random.randint(1,4)

def IslandCenter(pirate,position):
    x = int(position[0])
    y = int(position[1])
    if (pirate.investigate_up()[0][0:-1] == 'island' and pirate.investigate_down()[0][0:-1] == 'island' and 
        pirate.investigate_left()[0][0:-1] == 'island' and pirate.investigate_right()[0][0:-1] == 'island'):
        return (x,y)
    if (pirate.investigate_up()[0][0:-1] == 'island' and pirate.investigate_right()[0][0:-1] == 'island' and
        pirate.investigate_down()[0][0:-1] == 'island'):
        return (x+1,y)
    if (pirate.investigate_up()[0][0:-1] == 'island' and pirate.investigate_left()[0][0:-1] == 'island' and
        pirate.investigate_down()[0][0:-1] == 'island'):
        return (x-1,y)
    if (pirate.investigate_right()[0][0:-1] == 'island' and pirate.investigate_left()[0][0:-1] == 'island' and
        pirate.investigate_down()[0][0:-1] == 'island'):
        return (x,y+1)
    if (pirate.investigate_right()[0][0:-1] == 'island' and pirate.investigate_left()[0][0:-1] == 'island' and
        pirate.investigate_up()[0][0:-1] == 'island'):
        return (x,y-1)
    if (pirate.investigate_right()[0][0:-1] == 'island' and pirate.investigate_up()[0][0:-1] == 'island'):
        return (x+1,y-1)
    if (pirate.investigate_right()[0][0:-1] == 'island' and pirate.investigate_down()[0][0:-1] == 'island'):
        return (x+1,y+1)
    if (pirate.investigate_left()[0][0:-1] == 'island' and pirate.investigate_down()[0][0:-1] == 'island'):
        return (x-1,y+1)
    if (pirate.investigate_left()[0][0:-1] == 'island' and pirate.investigate_up()[0][0:-1] == 'island'):
        return (x-1,y-1)
        
        
        
        
    #FUNCTION FOR NEAREST PIRATES
def nearest_pirates(x,y,team,pirate):
    x_=pirate.getPosition()[0]
    y_=pirate.getPosition()[1]
    number=team.getTotalPirates()
    for pirate in range(1,number+1):   
        x_=pirate.getPosition()[0]
        y_=pirate.getPosition()[1]
        if (abs(x-x_)>2 or abs(y-y_)>2):
            number=number-1   
                
    stringsig=pirate.getTeamSignal()+str(number)
    pirate.setTeamSignal(stringsig)




#FUNCTION
def scoutout(pirate,team):
    if pirate.getSignal()=="scout" and team.getTotalGunpowder()<300 and team.getTotalPirates()<20:
        pirate.setSignal("")
        
def scoutin(pirate,team):
    if pirate.getSignal()!="scout" and team.getTotalGunpowder()>600 and team.getTotalPirates()>45:
        pirate.setSignal("scout")