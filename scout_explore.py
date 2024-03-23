from explore_quadrant import explore_main_quadrant, explore_side_quadrant

def scout_explore(pirate):
    # "North" is 1, "East" is 2, "South" is 3, "West" is 4
    x_dimension = pirate.getDimensionX()
    y_dimension = pirate.getDimensionY()
    x, y = pirate.getPosition()
    pirate_signal = list(pirate.getSignal())

    # whether home quadrant is explored or not is stored in index 6 of the pirate signal
    is_home_explored = pirate_signal[6] == "T"

    # print(pirate_signal)

    if is_home_explored:
        # Index 7 contains the quadrant being explored
        # Index 8 contains the direction being explored
        # Index 12 stores T if rebound is activated
        quadrant_exploring = int(pirate_signal[7])
        is_exploring_X = pirate_signal[8] == "T"
        if quadrant_exploring == 1:
            if is_exploring_X:
                if x == x_dimension - 1:
                    pirate_signal[12] = "T"
                    pirate.setSignal("".join(pirate_signal))
                # if x == 0:
                if x == x_dimension//2:
                    pirate_signal[12] = " "
                    pirate.setSignal("".join(pirate_signal))
                if pirate_signal[12] == "T":
                    return explore_side_quadrant(pirate, 4, [1, 3])
                return explore_side_quadrant(pirate, 2, [1, 3])

            if y == 0:
                pirate_signal[12] = "T"
                pirate.setSignal("".join(pirate_signal))
            # if y == y_dimension - 1:
            if y == y_dimension//2:
                pirate_signal[12] = " "
                pirate.setSignal("".join(pirate_signal))
            if pirate_signal[12] == "T":
                return explore_side_quadrant(pirate, 3, [2, 4])
            return explore_side_quadrant(pirate, 1, [2, 4])
        
        if quadrant_exploring == 2:
            if is_exploring_X:
                if x == 0:
                    pirate_signal[12] = "T"
                    pirate.setSignal("".join(pirate_signal))
                # if x == x_dimension - 1:
                if x == x_dimension//2:
                    pirate_signal[12] = " "
                    pirate.setSignal("".join(pirate_signal))
                if pirate_signal[12] == "T":
                    return explore_side_quadrant(pirate, 2, [1, 3])
                return explore_side_quadrant(pirate, 4, [1, 3])
        
            if y == 0:
                pirate_signal[12] = "T"
                pirate.setSignal("".join(pirate_signal))
            # if y == y_dimension - 1:
            if y == y_dimension//2:
                pirate_signal[12] = " "
                pirate.setSignal("".join(pirate_signal))
            if pirate_signal[12] == "T":
                return explore_side_quadrant(pirate, 3, [2, 4])
            return explore_side_quadrant(pirate, 1, [2, 4])
        
        if quadrant_exploring == 3:
            if is_exploring_X:
                if x == 0 :
                    pirate_signal[12] = "T"
                    pirate.setSignal("".join(pirate_signal))
                # if x == x_dimension - 1:
                if x == x_dimension//2:
                    pirate_signal[12] = " "
                    pirate.setSignal("".join(pirate_signal))
                if pirate_signal[12] == "T":
                    return explore_side_quadrant(pirate, 2, [1, 3])
                return explore_side_quadrant(pirate, 4, [1, 3])

            if y == y_dimension - 1:
                pirate_signal[12] = "T"
                pirate.setSignal("".join(pirate_signal))
            # if y == 0:
            if y == y_dimension//2:
                pirate_signal[12] = " "
                pirate.setSignal("".join(pirate_signal))
            if pirate_signal[12] == "T":
                return explore_side_quadrant(pirate, 1, [2, 4])
            return explore_side_quadrant(pirate, 3, [2, 4])
            
        if is_exploring_X:
            if x == x_dimension - 1 :
                pirate_signal[12] = "T"
                pirate.setSignal("".join(pirate_signal))
            # if x == 0:
            if x == x_dimension//2:
                pirate_signal[12] = " "
                pirate.setSignal("".join(pirate_signal))
            if pirate_signal[12] == "T":
                return explore_side_quadrant(pirate, 4, [1, 3])
            return explore_side_quadrant(pirate, 2, [1, 3])
                    
        if y == y_dimension - 1:
            pirate_signal[12] = "T"
            pirate.setSignal("".join(pirate_signal))
        # if y == 0:
        if y == y_dimension//2:
            pirate_signal[12] = " "
            pirate.setSignal("".join(pirate_signal))
        if pirate_signal[12] == "T":
            return explore_side_quadrant(pirate, 1, [2, 4])
        return explore_side_quadrant(pirate, 3, [2, 4])    

    # if the pirate has just completed home quadrant, switch to side quadrant exploration
    if x == x_dimension // 2 or y == y_dimension // 2:
        is_home_explored = True
        quadrant_exploring = None
        is_exploring_X = None
        current_move = None

        # determine which quadrant is the home quadrant
        deploy_x, deploy_y = pirate.getDeployPoint()
        
        def get_home_quadrant():
            if deploy_x < x_dimension / 2:
                if deploy_y < y_dimension / 2:
                    return 2
                return 3
            if deploy_y < y_dimension / 2:
                return 1
            return 4
        
        home_quadrant = get_home_quadrant()

        # TODO: Condense this
        if x == x_dimension // 2:
            if home_quadrant == 1:
                # gotta explore quadrant 4
                current_move = explore_side_quadrant(pirate, 3, [2, 4])
                quadrant_exploring = 2
                is_exploring_X = True
            elif home_quadrant == 2:
                # gotta explore quadrant 3
                current_move = explore_side_quadrant(pirate, 3, [2, 4])
                quadrant_exploring = 1
                is_exploring_X = True
            elif home_quadrant == 3:
                # gotta explore quadrant 2
                current_move = explore_side_quadrant(pirate, 1, [2, 4])
                quadrant_exploring = 4
                is_exploring_X = True
            else:
                # gotta explore quadrant 1
                current_move = explore_side_quadrant(pirate, 1, [2, 4])
                quadrant_exploring = 3
                is_exploring_X = True
        else:
            if home_quadrant == 1:
                # gotta explore quadrant 2
                current_move = explore_side_quadrant(pirate, 4, [1, 3])
                quadrant_exploring = 4
                is_exploring_X = False
            elif home_quadrant == 2:
                # gotta explore quadrant 1
                current_move = explore_side_quadrant(pirate, 2, [1, 3])
                quadrant_exploring = 3
                is_exploring_X = False
            elif home_quadrant == 3:
                # gotta explore quadrant 4
                current_move = explore_side_quadrant(pirate, 2, [1, 3])
                quadrant_exploring = 2
                is_exploring_X = False
            else:
                # gotta explore quadrant 3
                current_move = explore_side_quadrant(pirate, 4, [1, 3])
                quadrant_exploring = 1
                is_exploring_X = False

        # Index 7 contains the quadrant being explored
        # Index 8 contains the direction being explored
        pirate_signal[6] = "T"
        pirate_signal[7] = str(quadrant_exploring)
        pirate_signal[8] = "T" if is_exploring_X else "F"
        pirate.setSignal("".join(pirate_signal))
        return current_move
    
    # otherwise, explore the home quadrant
    if x < x_dimension / 2 and y < y_dimension / 2:
        return explore_main_quadrant(pirate, 2, 3)
    elif x < x_dimension / 2 and y > y_dimension / 2:
        return explore_main_quadrant(pirate, 2, 1)
    elif x > x_dimension / 2 and y < y_dimension / 2:
        return explore_main_quadrant(pirate, 4, 3)
    elif x > x_dimension / 2 and y > y_dimension / 2:
        return explore_main_quadrant(pirate, 4, 1)
    
    # OLD SCRIPT:
    # if x < x_dimension / 2:
    #     if y < y_dimension / 2:
    #         return explore_main_quadrant(pirate, 2, 3)
        
    #     return explore_main_quadrant(pirate, 2, 1)
    
    # if y < y_dimension / 2:
    #     return explore_main_quadrant(pirate, 4, 3)
    
    # return explore_main_quadrant(pirate, 4, 1)
