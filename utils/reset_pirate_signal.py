from utils.decipher import decipher

def resetPirateSignal(pirate):
    pirate_signal = pirate.getSignal()

    if pirate_signal[3] == pirate_signal[1]:            # Reset target location if target reached
        pirate_signal = pirate_signal[:3] + " " + pirate_signal[4:]
    if pirate_signal[4] == pirate_signal[2]:
        pirate_signal = pirate_signal[:4] + " " + pirate_signal[5:]
    pirate.setSignal(pirate_signal)