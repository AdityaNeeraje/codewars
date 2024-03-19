from engine.main import Game
import sys
import script, aayush, new_script, scriptblue, scriptred, vishwa
from sample_scripts import sample1, sample2, sample3

if __name__ == "__main__":
    x = int(sys.argv[1])
    G = Game((x, x), script, vishwa)
    G.run_game()