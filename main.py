from engine.main import Game
import script, aayush, new_script, scriptblue, scriptred, vishwa, scriptdestroy, balaji
from sample_scripts import sample1, sample2, sample3

if __name__ == "__main__":
    G = Game((32, 32), scriptdestroy, script)
    G.run_game()