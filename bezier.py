import numpy as np
import math
from game_settings import GameSettings

from logger_setup import func_logger, logger
import os
import inspect

file_path = __file__
file_name = os.path.basename(file_path)


class Bezier:
    def __init__(self, distance_coefficient: float = 0.01):
        self.distance_coefficient = distance_coefficient
        self.t = 0
        self.step = 0.01
        self.p0 = None
        self.p1 = None
        self.p2 = None
        self.min_vector_length = GameSettings.SQUARE_SIZE
        self.max_vector_length = math.sqrt(GameSettings.WINDOW_SIZE_X**2 + GameSettings.WINDOW_SIZE_Y**2)

    def set_bezier_points_old(self, p0: tuple, p2: tuple):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        x1 = p0[0]
        x2 = p2[0]
        y1 = p0[1]
        y2 = p2[1]

        midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)

        # Got some MaGiC nUmBeRs here that I need to figure out

        vector = ((y2 - y1), (x2 - x1))
        length_normal_vector = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        ratio_scaled = (length_normal_vector - self.min_vector_length) / (self.max_vector_length - self.min_vector_length) * 0.05
        self.step = 0.06 - max(ratio_scaled, 0.01)

        if length_normal_vector == 0:
            p1 = midpoint
        else:
            height = 0.5 * length_normal_vector
            normal_vector = ((vector[0] / length_normal_vector), (vector[1] / length_normal_vector))
            p1 = ((midpoint[0] + (normal_vector[0] * height)), (midpoint[1] + (normal_vector[1] * height)))

        self.p0 = np.array(p0)
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)

    def set_bezier_points(self, p0: tuple, p2: tuple):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        x1 = p0[0]
        x2 = p2[0]
        y1 = p0[1]
        y2 = p2[1]

        midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)
        vector = ((y2 - y1), (x2 - x1))
        length_normal_vector = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        speed_scale = ((length_normal_vector - self.min_vector_length) /
                        (self.max_vector_length - self.min_vector_length) * 0.05)
        self.step = 0.06 - max(speed_scale, 0.01)

        try:
            theta = math.atan((y2 - y1) / (x2 - x1))
        except ZeroDivisionError:
            if y2 > y1:
                theta = math.pi / 2
            elif y2 < y1:
                theta = -math.pi / 2
            else:
                theta = 0
        height = GameSettings.SQUARE_SIZE

        p1x = midpoint[0] + (height * math.cos(theta + (math.pi / 2)))
        p1y = midpoint[1] + (height * math.sin(theta + (math.pi / 2)))

        self.p0 = np.array(p0)
        self.p1 = np.array((p1x, p1y))
        self.p2 = np.array(p2)

    def bezier_old(self):
        logger.info("Running in game loop, must not differ")
        new_loc = ((1-self.t)**2 * self.p0) + (2 * (1-self.t) * self.t * self.p1) + (self.t**2 * self.p2)
        return new_loc

    def bezier(self):
        logger.info("Running in game loop, must not differ")
        new_loc = ((1 - self.t) * ((1 - self.t) * self.p0 + self.t * self.p1)
                   + self.t * ((1 - self.t) * self.p1 + (self.t * self.p2))
                   )
        return new_loc
