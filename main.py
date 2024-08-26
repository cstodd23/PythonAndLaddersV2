import os
import numpy as np
import game_logic

if __name__ == '__main__':
    seeded_rng = np.random.default_rng(3711)

    game = game_logic.DisplayedGame()
    game.run_game()
