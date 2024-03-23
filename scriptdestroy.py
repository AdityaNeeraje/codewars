import random
import math

name = "Babbar Sher"


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


def checkIsland(pirate):
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    if (up[0:-1] == "island" or down[0:-1] == "island") and (
        left[0:-1] == "island" or right[0:-1] == "island"
    ):
        if up[0:-1] == "island":
            return up
        if down[0:-1] == "island":
            return down
        if right[0:-1] == "island":
            return right
        if left[0:-1] == "island":
            return left
    else:
        return False


def MoveX(pirate, y_coordi, x_end):
    if pirate.getPosition()[1] != y_coordi:
        return moveTo(pirate.getPosition()[0], y_coordi, pirate)
    else:
        return moveTo(x_end, y_coordi, pirate)


def MoveY(pirate, x_coordi, y_end):
    if pirate.getPosition()[0] != x_coordi:
        return moveTo(x_coordi, pirate.getPosition()[1], pirate)
    else:
        return moveTo(x_coordi, y_end, pirate)


def Sweep(x_start, y_start, pirate, dimX, dimY, n):
    if n % 2 == 0 and n <= dimY:
        if n <= dimY // 2:
            if (x_start, y_start) == (0, 0):
                return MoveX(pirate, (dimY / 2) - n + 1, dimX - 1)
            if (x_start, y_start) == (dimX - 1, 0):
                return MoveX(pirate, (dimY / 2) - n + 1, 0)
            if (x_start, y_start) == (0, dimY - 1):
                return MoveX(pirate, (dimY / 2) + n - 2, dimX - 1)
            if (x_start, y_start) == (dimX - 1, dimY - 1):
                return MoveX(pirate, (dimY / 2) + n - 2, 0)
        else:
            if (x_start, y_start) == (0, 0):
                return MoveX(pirate, (dimY) - n, dimX - 1)
            if (x_start, y_start) == (dimX - 1, 0):
                return MoveX(pirate, (dimY) - n, 0)
            if (x_start, y_start) == (0, dimY - 1):
                return MoveX(pirate, n - 1, dimX - 1)
            if (x_start, y_start) == (dimX - 1, dimY - 1):
                return MoveX(pirate, n - 1, 0)
    if n % 2 == 1 and n <= dimX:
        if n <= dimX // 2:
            if (x_start, y_start) == (0, 0):
                return MoveY(pirate, (dimX / 2) - n, dimY - 1)
            if (x_start, y_start) == (dimX - 1, 0):
                return MoveY(pirate, (dimX / 2) + n - 1, dimY - 1)
            if (x_start, y_start) == (0, dimY - 1):
                return MoveY(pirate, (dimX / 2) - n, 0)
            if (x_start, y_start) == (dimX - 1, dimY - 1):
                return MoveY(pirate, (dimX / 2) + n - 1, 0)
        else:
            if (x_start, y_start) == (0, 0):
                return MoveY(pirate, dimX - n - 1, dimY - 1)
            if (x_start, y_start) == (dimX - 1, 0):
                return MoveY(pirate, n, dimY - 1)
            if (x_start, y_start) == (0, dimY - 1):
                return MoveY(pirate, dimX - n - 1, 0)
            if (x_start, y_start) == (dimX - 1, dimY - 1):
                return MoveY(pirate, n, 0)


def Attack(x_start, y_start, pirate, dimX, dimY, n, x_end, y_end):
    if n % 2 == 0 and n <= dimY // 2:
        if y_start == 0:
            if pirate.getPosition()[1] == dimY - n + 1:
                return MoveX(pirate, dimY - n + 1, x_start)
            else:
                return MoveY(pirate, x_end, dimY - n + 1)
        else:
            if pirate.getPosition()[1] == n - 2:
                return MoveX(pirate, n - 2, x_start)
            else:
                return MoveY(pirate, x_end, n - 2)
    elif n % 2 == 0 and n > dimY // 2 and n <= dimY:
        if y_start == 0:
            if pirate.getPosition()[1] == 3 * dimY // 2 - n:
                return MoveX(pirate, 3 * dimY // 2 - n, x_start)
            else:
                return MoveY(pirate, x_end, 3 * dimY // 2 - n)
        else:
            if pirate.getPosition()[1] == n - dimY // 2 - 1:
                return MoveX(pirate, n - dimY // 2 - 1, x_start)
            else:
                return MoveY(pirate, x_end, n - dimY // 2 - 1)
    if n % 2 == 1 and n <= dimX // 2:
        if x_start == 0:
            if pirate.getPosition()[0] == dimX - n:
                return MoveY(pirate, dimX - n, y_start)
            else:
                return MoveX(pirate, y_end, dimX - n)
        else:
            if pirate.getPosition()[0] == n - 1:
                return MoveY(pirate, n - 1, y_start)
            else:
                return MoveX(pirate, y_end, n - 1)
    elif n % 2 == 1 and n > dimX // 2 and n <= dimX:
        if x_start == 0:
            if pirate.getPosition()[0] == dimX - n - 1 + (dimX // 2):
                return MoveY(pirate, dimX - n - 1 + (dimX // 2), y_start)
            else:
                return MoveX(pirate, y_end, dimX - n - 1 + (dimX // 2))
        else:
            if pirate.getPosition()[0] == n - dimX // 2:
                return MoveY(pirate, n - dimX // 2, y_start)
            else:
                return MoveX(pirate, y_end, n - dimX // 2)


def ActPirate(pirate):
    # print(len(pirate.getTeamSignal().split(" ")))
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    x, y = pirate.getPosition()
    s = pirate.trackPlayers()
    x_start, y_start = pirate.getDeployPoint()
    dimX = int(pirate.getDimensionX())
    dimY = int(pirate.getDimensionY())
    n = int(pirate.getID())
    for i in [0, dimX - 1]:
        if i != x_start:
            x_end = i
    for i in [0, dimY - 1]:
        if i != y_start:
            y_end = i
    if (
        (up == "island1" and s[0] != "myCaptured")
        or (up == "island2" and s[1] != "myCaptured")
        or (up == "island3" and s[2] != "myCaptured")
    ):
        if pirate.getTeamSignal() == "":
            sig = up[-1] + "," + str(x) + "," + str(y - 1) + ",0"
            pirate.setTeamSignal(sig)
        elif (
            len(pirate.getTeamSignal().split(" ")) == 1
            and up[-1] != pirate.getTeamSignal()[0]
        ):
            team_assigned = pirate.getTeamSignal()[-1]
            team_to_be_assigned = "1" if team_assigned == "0" else "0"
            sig = up[-1] + "," + str(x) + "," + str(y - 1) + "," + team_to_be_assigned
            s = pirate.getTeamSignal()
            pirate.setTeamSignal(s + " " + sig)

    if (
        (down == "island1" and s[0] != "myCaptured")
        or (down == "island2" and s[1] != "myCaptured")
        or (down == "island3" and s[2] != "myCaptured")
    ):
        if pirate.getTeamSignal() == "":
            sig = down[-1] + "," + str(x) + "," + str(y + 1) + ",0"
            pirate.setTeamSignal(sig)
        elif (
            len(pirate.getTeamSignal().split(" ")) == 1
            and down[-1] != pirate.getTeamSignal()[0]
        ):
            team_assigned = pirate.getTeamSignal()[-1]
            team_to_be_assigned = "1" if team_assigned == "0" else "0"
            sig = down[-1] + "," + str(x) + "," + str(y + 1) + "," + team_to_be_assigned
            s = pirate.getTeamSignal()
            pirate.setTeamSignal(s + " " + sig)

    if (
        (left == "island1" and s[0] != "myCaptured")
        or (left == "island2" and s[1] != "myCaptured")
        or (left == "island3" and s[2] != "myCaptured")
    ):
        if pirate.getTeamSignal() == "":
            sig = left[-1] + "," + str(x - 1) + "," + str(y) + ",0"
            pirate.setTeamSignal(sig)
        elif (
            len(pirate.getTeamSignal().split(" ")) == 1
            and left[-1] != pirate.getTeamSignal()[0]
        ):
            team_assigned = pirate.getTeamSignal()[-1]
            team_to_be_assigned = "1" if team_assigned == "0" else "0"
            sig = left[-1] + "," + str(x - 1) + "," + str(y) + "," + team_to_be_assigned
            s = pirate.getTeamSignal()
            pirate.setTeamSignal(s + " " + sig)

    if (
        (right == "island1" and s[0] != "myCaptured")
        or (right == "island2" and s[1] != "myCaptured")
        or (right == "island3" and s[2] != "myCaptured")
    ):
        if pirate.getTeamSignal() == "":
            sig = right[-1] + "," + str(x + 1) + "," + str(y) + ",0"
            pirate.setTeamSignal(sig)
        elif (
            len(pirate.getTeamSignal().split(" ")) == 1
            and right[-1] != pirate.getTeamSignal()[0]
        ):
            team_assigned = pirate.getTeamSignal()[-1]
            team_to_be_assigned = "1" if team_assigned == "0" else "0"
            sig = (
                right[-1] + "," + str(x + 1) + "," + str(y) + "," + team_to_be_assigned
            )
            s = pirate.getTeamSignal()
            pirate.setTeamSignal(s + " " + sig)
    if n % 2 == 0 and n <= dimY:
        if (pirate.getSignal() != "1") and (
            (pirate.getPosition()[0] != dimX - 1 and x_start == 0)
            or (pirate.getPosition()[0] != 0 and x_start == dimX - 1)
        ):
            if (pirate.getPosition()[0] == dimX - 2 and x_start == 0) or (
                pirate.getPosition()[0] == 1 and x_start == dimX - 1
            ):
                pirate.setSignal("1")
            return Sweep(x_start, y_start, pirate, dimX, dimY, n)
        else:
            if (pirate.getPosition()[0] == 1 and x_start == 0) or (
                pirate.getPosition()[0] == dimX - 2 and x_start == dimX - 1
            ):
                pirate.setSignal("")
            return Attack(x_start, y_start, pirate, dimX, dimY, n, x_end, y_end)
    if n % 2 == 1 and n <= dimX:
        if (pirate.getSignal() != "1") and (
            (pirate.getPosition()[1] != dimY - 1 and y_start == 0)
            or (pirate.getPosition()[1] != 0 and y_start == dimY - 1)
        ):
            if (pirate.getPosition()[1] == dimY - 2 and y_start == 0) or (
                pirate.getPosition()[1] == 1 and y_start == dimY - 1
            ):
                pirate.setSignal("1")
            return Sweep(x_start, y_start, pirate, dimX, dimY, n)
        else:
            if (pirate.getPosition()[1] == 1 and y_start == 0) or (
                pirate.getPosition()[1] == dimY - 2 and y_start == dimY - 1
            ):
                pirate.setSignal("")
            return Attack(x_start, y_start, pirate, dimX, dimY, n, x_end, y_end)
    if pirate.getTeamSignal() != "":
        s = pirate.getTeamSignal()
        List = s.split(" ")
        for i in List:
            List2 = i.split(",")
            x = int(List2[1])
            y = int(List2[2])
            if n % 2 == int(i[-1]):
                return moveTo(x, y, pirate)
    # return random.randint(1,4)


def ActTeam(team):
    l = team.trackPlayers()
    s = team.getTeamSignal()

    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)
    # print(s)
    # print(team.getTeamSignal())
    # print(team.trackPlayers())
    if s:
        L = s.split(" ")
        for i in L:
            # print(i[0])
            island_no = int(i[0])
            signal = l[island_no - 1]
            if signal == "myCaptured":
                L.remove(i)
                # print(L)
                if L != []:
                    team.setTeamSignal(L[0])
                else:
                    team.setTeamSignal("")
