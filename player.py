import math
import numpy as np
import os.path
import bezier

import pygame.sprite

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
        self.new_center = None
        self.square = 0
        self.moving = False
        self.bezier = bezier.Bezier()

    def print_info(self):
        print(f'Name {self.name}')
        print(f'Number {self.num}')
        print(f'Square {self.square}')

    def set_square(self, square: int):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.square = square

    def add_roll(self, roll: int):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.square += roll

    def get_square(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        return self.square

    def set_new_center(self, new_center):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        logger.info(f'Bezier Points at start of movement: ({self.bezier.p0}, {self.bezier.p1}, {self.bezier.p2}')
        logger.info(f'New Center: {new_center}, Current Center: {self.rect.center}')
        self.new_center = new_center
        self.bezier.set_bezier_points(self.rect.center, self.new_center)

    def update(self):
        logger.info("Running in game loop, must not differ")
        if self.rect.center != self.new_center and self.new_center is not None:
            self.moving = True
        else:
            self.moving = False
        if self.moving:
            self.bezier.t += self.bezier.step
            self.rect.center = self.bezier.bezier()
            if self.bezier.t > 1:
                self.bezier.t = 0
                self.moving = False
                self.rect.center = self.new_center
                # self.new_center = None

    @staticmethod
    def load_player_image(width, height):
        current_path = os.path.dirname(__file__)
        sprites_path = os.path.join(current_path, 'sprites')
        image_path = os.path.join(sprites_path, "computer.jpg")
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

