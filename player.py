import math
import numpy as np
import os.path
import bezier

import pygame.sprite
import warnings

import inspect
from logger_setup import logger, func_logger
import os

file_path = __file__
file_name = os.path.basename(file_path)



class Player(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, num: int, name: str):
        super().__init__()
        self.rect = rect
        self.num = num
        self.name = name
        self.image = self.load_player_image(rect.width, rect.height)
        self.square = 0
        self.next_square = None
        self.next_center = None
        self.snake_ladder_end_square = None
        self.snake_ladder_end_center = None
        self.moving = False
        self.bezier = bezier.Bezier()

    @staticmethod
    def load_player_image(width, height):
        current_path = os.path.dirname(__file__)
        sprites_path = os.path.join(current_path, 'sprites')
        image_path = os.path.join(sprites_path, "computer.jpg")
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

    def print_info(self):
        print(f'Name {self.name}')
        print(f'Number {self.num}')
        print(f'Square {self.square}')

    def get_square(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        return self.square

    def set_next_square(self, square: int):
        """
        :param square: The next square
        :type square: int
        :return: None

        This will either be called by the DisplayBoard, GameBoard, classes
        or by this player class once a snake/ladder base has been reached.
        """
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.next_square = square

    def set_next_center(self, next_center: tuple[float, float]):
        """
        :param next_center: The next location where this players center will be moved to.
        :type next_center: tuple[float, float]
        :return: None

        Updates the instance variable and sets the Bezier points needed for movement
        This will either be called by the DisplayBoard, GameBoard, classes
        or by this player class once a snake/ladder base has been reached.
        """
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        logger.info(f'New Center: {next_center}, Current Center: {self.rect.center}')
        self.next_center = next_center
        self.bezier.set_bezier_points(self.rect.center, self.next_center)
        logger.info(f'Bezier Points at start of movement: ({self.bezier.p0}, {self.bezier.p1}, {self.bezier.p2}')

    def set_snake_ladder_end_square(self, square):
        """
        :param square: int
        :return: None

        Should only be called by DisplayGame, and GameBoard objects
        """
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.snake_ladder_end_square = square

    def set_snake_ladder_end_center(self, center):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.snake_ladder_end_center = center

    # def reset(self):
    #     func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
    #     self.next_center = None
    #     self.next_square = None
    #     self.snake_ladder_end_square = None
    #     self.snake_ladder_end_center = None

    def update(self):
        logger.info("Running in game loop, must not differ")
        if self.rect.center != self.next_center and self.next_center is not None:
            self.moving = True
            self.square = self.next_square
        elif self.rect.center == self.next_center and self.snake_ladder_end_center:
            self.moving = True
            self.set_next_center(self.snake_ladder_end_center)
            self.set_next_square(self.snake_ladder_end_square)
            self.snake_ladder_end_center = None
            self.snake_ladder_end_square = None
        elif self.rect.center == self.next_center:
            self.moving = False
        else:
            warnings.warn(
                "Incorrect Center Status: current center does not match next_center and self.next_center is None"
            )
        if self.moving:
            self.bezier.t += self.bezier.step
            self.rect.center = self.bezier.bezier()
            if self.bezier.t > 1:
                self.bezier.t = 0
                self.rect.center = self.next_center
