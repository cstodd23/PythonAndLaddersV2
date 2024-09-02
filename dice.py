import numpy as np


class Dice:
    def __init__(self, rng_seed: int = None, min_roll: int = 1, max_roll: int = 6):
        self.min_roll = min_roll
        self.max_roll = max_roll
        self.rng = np.random.default_rng(rng_seed)

    def roll(self):
        return self.rng.integers(self.min_roll, self.max_roll, endpoint=True)