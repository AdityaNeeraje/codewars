from utils.cipher import cipher

def intitializeTeam(team):
    team_signal = team.getTeamSignal()
    no_of_pirates = int(team.getTotalPirates())

    if team_signal == "":               # Intitialization
        team_signal = " "*9 + cipher(no_of_pirates) + " "*90
        team.setTeamSignal(team_signal)
    
    team_signal = team_signal[:9] + cipher(no_of_pirates) + team_signal[10:]        #Updating no of pirates
    team.setTeamSignal(team_signal)