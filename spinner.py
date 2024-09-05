import pygame
import numpy as np
from colors import GameColors


class Spinner:
    def __init__(self,
                 rng_seed,
                 game_area: pygame.surface.Surface,
                 min_spin: int = 1,
                 max_spin: int = 6
                 ):
        self.rng = self.rng = np.random.default_rng(rng_seed)
        self.min_spin = min_spin
        self.max_spin = max_spin
        self.game_area = game_area

    def draw_spinner(self):
        pygame.draw.circle(self.game_area, GameColors.GUNMETAL.value)



