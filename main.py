from engine.main import Game
import script, aayush, new_script, scriptblue, scriptred

if __name__ == "__main__":
    G = Game((40, 40), new_script, script)
    G.run_game()