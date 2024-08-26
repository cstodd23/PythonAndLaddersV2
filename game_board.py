import numpy as np
import inspect
from logger_setup import func_logger, logger
import os

file_path = __file__
file_name = os.path.basename(file_path)


class GameBoard:
    def __init__(self,
                 x_board: int = 10,
                 y_board: int = 10,
                 snake_amount: int = 10,
                 snake_end_min: int = 1,
                 ladder_amount: int = 10,
                 ladder_start_min: int = 5,
                 rng_seed: int = None):

        self.x_board = x_board
        self.y_board = y_board
        self.snake_amount = snake_amount
        self.snake_end_min = snake_end_min
        self.ladder_amount = ladder_amount
        self.ladder_start_min = ladder_start_min

        self.rng_seed = rng_seed
        self.rng = np.random.default_rng(self.rng_seed) if self.rng_seed is not None else np.random.default_rng()

        self.snakes = []
        self.ladders = []
        self.square_count = self.x_board * self.y_board
        self.finish_line = self.square_count

        self.snake_start_max = self.square_count - 1
        self.ladder_end_max = self.square_count - 1

        self.generate_snakes()
        self.generate_ladders()

    def generate_snakes(self, min_length: int = 3):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        while len(self.snakes) < self.snake_amount:
            snake_start = self.rng.integers(self.snake_end_min + min_length + 1, self.snake_start_max)
            snake_end = self.rng.integers(self.snake_end_min, snake_start - min_length)
            if not self.check_duplicates((snake_start, snake_end)):
                self.snakes.append((snake_start, snake_end))
                logger.info(f"Generated Snake from {snake_start} to {snake_end}")

    def generate_ladders(self, min_length: int = 3):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        while len(self.ladders) < self.ladder_amount:
            ladder_start = self.rng.integers(self.ladder_start_min, self.ladder_end_max - min_length - 1)
            ladder_end = self.rng.integers(ladder_start + min_length, self.ladder_end_max)
            if not self.check_duplicates((ladder_start, ladder_end)):
                self.ladders.append((ladder_start, ladder_end))
                logger.info(f'Generated Ladder from {ladder_start} to {ladder_end}')

    def check_duplicates(self, numbers_to_check: tuple):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        if self.snakes:
            for segment in self.snakes:
                if any(num in numbers_to_check for num in segment):
                    return True
        if self.ladders:
            for segment in self.ladders:
                if any(num in numbers_to_check for num in segment):
                    return True
        return False

    def check_snakes_ladders(self, square: int):
        """
        Parameters:
        Square (int): Square to be checked for starting a snake or ladder

        Returns:
        tuple: (mover_type, mover_length, start, end)
        """
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        mover_info = (None, None, None, None)
        if self.snakes:
            matching_snake = next((snake for snake in self.snakes if snake[0] == square), None)
            if matching_snake:
                start, end = matching_snake
                mover_type = 'Snake'
                mover_length = end - start
                mover_info = (mover_type, mover_length, start, end)
        if self.ladders:
            matching_ladder = next((ladder for ladder in self.ladders if ladder[0] == square), None)
            if matching_ladder:
                start, end = matching_ladder
                mover_type = 'Snake'
                mover_length = end - start
                mover_info = (mover_type, mover_length, start, end)
        return mover_info

    def debug_snakes_ladders(self):
        for snake in self.snakes:
            logger.info(f'Snake Start: {snake[0]}, Snake End: {snake[1]}')
        logger.info(f'End of Snakes, Total Snakes: {len(self.snakes)}')

        for ladder in self.ladders:
            logger.info(f'Ladder Start: {ladder[0]}, Ladder End: {ladder[1]}')
        logger.info(f'End of Ladders, Total Ladders: {len(self.ladders)}')
