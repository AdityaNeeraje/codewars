from scout_explore import scout_explore
from infiltrate import infiltrate

name = "trial_script"

def pirate_setup(pirate):
    if pirate.getSignal() == "":
        pirate.setSignal(" " * 50)

def ActPirate(pirate):
    pirate_setup(pirate)
    if pirate.getCurrentFrame() >= 250:
        return infiltrate(pirate)
    return scout_explore(pirate)
        
def ActTeam(team):
    pass