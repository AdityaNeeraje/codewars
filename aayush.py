import random
import math

name = "aayush"


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
    if (up[0:-1] == "island" or down[0:-1] == "island") and (
        left[0:-1] == "island" or right[0:-1] == "island"
    ):
        return True
    else:
        return False


rad = 24
dec = True
zerostay = 0
radvac = list(range(0, 20))
radvac2 = list(range(3, 21))
flags = [(-1, -1), (-1, -1), (-1, -1)]
goingto = [False, False, False]


def ActPirate(pirate):
    global flags
    if pirate.investigate_nw()[0][:-1] == "island":
        flags[int(pirate.investigate_nw()[0][-1]) - 1] = (
            pirate.getPosition()[0] - 1,
            pirate.getPosition()[1] - 1,
        )
    elif pirate.investigate_up()[0][:-1] == "island":
        flags[int(pirate.investigate_up()[0][-1]) - 1] = (
            pirate.getPosition()[0],
            pirate.getPosition()[1] - 1,
        )
    elif pirate.investigate_ne()[0][:-1] == "island":
        flags[int(pirate.investigate_ne()[0][-1]) - 1] = (
            pirate.getPosition()[0] + 1,
            pirate.getPosition()[1] - 1,
        )
    elif pirate.investigate_left()[0][:-1] == "island":
        flags[int(pirate.investigate_left()[0][-1]) - 1] = (
            pirate.getPosition()[0] - 1,
            pirate.getPosition()[1],
        )
    elif pirate.investigate_current()[0][:-1] == "island":
        flags[int(pirate.investigate_current()[0][-1]) - 1] = (
            pirate.getPosition()[0],
            pirate.getPosition()[1],
        )
    elif pirate.investigate_right()[0][:-1] == "island":
        flags[int(pirate.investigate_right()[0][-1]) - 1] = (
            pirate.getPosition()[0] + 1,
            pirate.getPosition()[1],
        )
    elif pirate.investigate_sw()[0][:-1] == "island":
        flags[int(pirate.investigate_sw()[0][-1]) - 1] = (
            pirate.getPosition()[0] - 1,
            pirate.getPosition()[1] + 1,
        )
    elif pirate.investigate_down()[0][:-1] == "island":
        flags[int(pirate.investigate_down()[0][-1]) - 1] = (
            pirate.getPosition()[0],
            pirate.getPosition()[1] + 1,
        )
    elif pirate.investigate_se()[0][:-1] == "island":
        flags[int(pirate.investigate_se()[0][-1]) - 1] = (
            pirate.getPosition()[0] + 1,
            pirate.getPosition()[1] + 1,
        )
    return ActPirate2(pirate)


def ActPirate2(pirate):
    global goingto, flags
    global radvac, radvac2
    if flags[0] != (-1, -1) and not goingto[0]:
        goingto[0] = True
        pirate.setSignal("g0")
        return moveTo(flags[0][0], flags[0][1], pirate)
    elif flags[1] != (-1, -1) and not goingto[1]:
        goingto[1] = True
        pirate.setSignal("g1")
        return moveTo(flags[1][0], flags[1][1], pirate)
    elif flags[2] != (-1, -1) and not goingto[2]:
        goingto[2] = True
        pirate.setSignal("g2")
        return moveTo(flags[2][0], flags[2][1], pirate)
    if pirate.getSignal() == "":
        if len(radvac):
            rad = radvac.pop(0)
            pirate.setSignal(f"{rad}")
            return circleAround(20, 20, rad, pirate)
        elif len(radvac2):
            rad = radvac2.pop(0)
            pirate.setSignal(f"{rad}")
            return circleAround(20, 20, rad, pirate)
        else:
            rad = random.randint(10, 20)
            pirate.setSignal(f"{rad}")
            return circleAround(20, 20, rad, pirate)
    elif pirate.getSignal()[0] == "g":
        islandidx = int(pirate.getSignal()[1])
        return moveTo(flags[islandidx][0], flags[islandidx][1], pirate)
    return circleAround(20, 20, int(pirate.getSignal()), pirate)


def ActPirate1(pirate):
    # complete this function
    # position = pirate.getPosition()
    global dec
    global rad
    global zerostay
    if pirate.getCurrentFrame() % 30 == 0:
        if dec:
            rad -= 1
        else:
            rad += 1
        if rad < 0:
            rad = 0
            zerostay += 1
            if zerostay > 5:
                rad = 1
                zerostay = 0
                dec = False
        if rad > 24:
            rad = 24
            dec = True
    return circleAround(20, 20, rad, pirate)


def ActTeam(team):
    ActTeam2(team)
    pass


def ActTeam2(team):
    # complete this function
    # check for islands
    global radvac, radvac2
    global flags, goingto
    locto = [False, False, False]
    locvac = list(range(0, 20))
    locvac2 = list(range(3, 21))
    for piratesig in team.getListOfSignals():
        if piratesig != "":
            if piratesig[0] == "g":
                islandidx = int(piratesig[1])
                goingto[islandidx] = True
            else:
                if int(piratesig) in locvac:
                    locvac.remove(int(piratesig))
                elif int(piratesig) in locvac2:
                    locvac2.remove(int(piratesig))
    radvac = locvac
    radvac2 = locvac2
    goingto = locto
