from explore_quadrant import explore_main_quadrant

def infiltrate(pirate):
    pirate_signal = list(pirate.getSignal())
    deploy_x, deploy_y = pirate.getDeployPoint()

    def get_quadrant(x, y):
        dimension_x = pirate.getDimensionX()
        dimension_y = pirate.getDimensionY()
        if x < dimension_x / 2:
            if y < dimension_y / 2:
                return 2
            return 3
        if y < dimension_y / 2:
            return 1
        return 4
    
    def get_opposite_quadrant(quadrant):
        if quadrant == 1:
            return 3
        if quadrant == 2:
            return 4
        if quadrant == 3:
            return 1
        return 2
    
    home_quadrant = get_quadrant(deploy_x, deploy_y)
    opponent_quadrant = get_opposite_quadrant(home_quadrant)
    
    if pirate_signal[7] == " ":
        pirate_signal[7] = str(home_quadrant)
    
    quadrant = int(pirate_signal[7])
    
    if quadrant == home_quadrant or quadrant == opponent_quadrant:
        return None
    
    def goto_edge(current_quadrant, target_quadrant):
        if current_quadrant == 1:
            if target_quadrant == 2:
                if pirate.investigate_up()[0] == "wall":
                    return None
                return 1
            # target_quadrant == 4
            if pirate.investigate_right()[0] == "wall":
                return None
            return 2
        if current_quadrant == 2:
            if target_quadrant == 1:
                if pirate.investigate_up()[0] == "wall":
                    return None
                return 1
            # target_quadrant == 3
            if pirate.investigate_left()[0] == "wall":
                return None
            return 4
        if current_quadrant == 3:
            if target_quadrant == 2:
                if pirate.investigate_left()[0] == "wall":
                    return None
                return 4
            # target_quadrant == 4
            if pirate.investigate_down()[0] == "wall":
                return None
            return 3
        # current_quadrant == 4
        if target_quadrant == 1:
            if pirate.investigate_right()[0] == "wall":
                return None
            return 2
        # target_quadrant == 3
        if pirate.investigate_down()[0] == "wall":
            return None
        return 3

    def goto_enemy_spawn(current_quadrant, opponent_quadrant):
        if opponent_quadrant == 1:
            if pirate.investigate_up()[0] == "wall" and pirate.investigate_right()[0] == "wall":
                return None
        if opponent_quadrant == 2:
            if pirate.investigate_up()[0] == "wall" and pirate.investigate_left()[0] == "wall":
                return None
        if opponent_quadrant == 3:
            if pirate.investigate_down()[0] == "wall" and pirate.investigate_left()[0] == "wall":
                return None
        # opponent_quadrant == 4
        if pirate.investigate_down()[0] == "wall" and pirate.investigate_right()[0] == "wall":
            return None
                
        if current_quadrant == 1:
            if opponent_quadrant == 2:
                return 4
            # opponent_quadrant == 4
            return 3
        if current_quadrant == 2:
            if opponent_quadrant == 1:
                return 2
            # opponent_quadrant == 3
            return 3
        if current_quadrant == 3:
            if opponent_quadrant == 2:
                return 1
            # opponent_quadrant == 4
            return 2
        # current_quadrant == 4
        if opponent_quadrant == 1:
            return 1
        # opponent_quadrant == 3
        return 4


    def find_enemy_island(opponent_quadrant):
        if opponent_quadrant == 1:
            return explore_main_quadrant(pirate, 3, 4)
        if opponent_quadrant == 2:
            return explore_main_quadrant(pirate, 2, 3)
        if opponent_quadrant == 3:
            return explore_main_quadrant(pirate, 1, 2)
        # opponent_quadrant == 4
        return explore_main_quadrant(pirate, 1, 4)
    
    has_infiltrated = pirate_signal[14] == "T"

    if not has_infiltrated:
        temp = goto_edge(quadrant, opponent_quadrant)
        if temp is not None:
            return temp
        
        temp = goto_enemy_spawn(quadrant, opponent_quadrant)
        if temp is not None:
            return temp
        
        has_infiltrated = True
        pirate_signal[14] = "T"
        pirate.setSignal("".join(pirate_signal))
    
    return find_enemy_island(opponent_quadrant)