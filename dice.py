import numpy as np
from logger_setup import func_logger, logger
import inspect
import os

file_path = __file__
file_name = os.path.basename(file_path)


class Dice:
    def __init__(self, rng_seed: int = None, min_roll: int = 1, max_roll: int = 6):
        self.min_roll = min_roll
        self.max_roll = max_roll
        self.rng = np.random.default_rng(rng_seed)

    def roll(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        return self.rng.integers(self.min_roll, self.max_roll, endpoint=True)