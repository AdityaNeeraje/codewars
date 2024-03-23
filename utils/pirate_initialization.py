from utils.cipher import cipher

def intitializePirate(pirate):
    pirate_signal  = pirate.getSignal()
    if pirate_signal == "":                         # Initialization
        pirate_signal = cipher(int(pirate.getID())) + " "*99
        pirate.setSignal(pirate_signal)