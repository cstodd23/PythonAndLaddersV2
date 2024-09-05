import os
import numpy as np
import game_logic


if __name__ == '__main__':
    seeded_rng = np.random.default_rng(3711)

    game = game_logic.DisplayedGame(4, rng_seed=47)
    game.run_game()


'''
Bug List:
Starting animations are taking place but the entire board is drawn instantly

'''
