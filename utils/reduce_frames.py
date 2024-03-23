def reduceFrames(team, island_no):
    team_signal = team.getTeamSignal()
    team_signal = team_signal[:5 + island_no] + chr(ord(team_signal[5 + island_no]) - 1) + team_signal[6 + island_no:]
    team.setTeamSignal(team_signal)