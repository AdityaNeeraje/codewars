from engine.main import Game
import script, aayush, new_script, scriptblue, scriptred, vishwa
from sample_scripts import sample1, sample2, sample3

if __name__ == "__main__":
    G = Game((20, 20), new_script, vishwa)
    G.run_game()