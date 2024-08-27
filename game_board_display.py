import pygame
import math
from colors import GameColors

from logger_setup import func_logger, logger
import os
import inspect

file_path = __file__
file_name = os.path.basename(file_path)


class DisplayBoard:
    def __init__(self,
                 x_board: int,
                 y_board: int,
                 window: pygame.display,
                 border_squares: float = 1.5
                 ):
        self.x_board = x_board
        self.y_board = y_board

        self.window = window
        self.window_width, self.window_height = window.get_size()
        self.game_area = pygame.Surface((self.window_width, self.window_height))

        self.border_squares = border_squares

        self.square_size = self.calculate_square_size()
        self.border_size = self.square_size * border_squares

        self.square_rects = {}
        self.square_colors = {}

        self.font = pygame.font.Font(None, 36)
        self.drawing_complete = False

    def calculate_square_size(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        base_length = min(self.window_width, self.window_height)
        square_size = int(base_length / (min(self.x_board, self.y_board) + (self.border_squares * 2)))
        return square_size

    def generate_board_squares(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        for col in range(self.y_board):
            for row in range(self.x_board):
                # self.test_draw_board(col, row)
                square_rect = pygame.Rect((col * self.square_size) + self.border_size,
                                          ((self.x_board - row - 1) * self.square_size) + self.border_size,
                                          self.square_size,
                                          self.square_size
                                          )
                square_color = GameColors.WHITE_SMOKE if (row + col) % 2 == 0 else GameColors.SILVER

                square_number = self.get_square_number(row, col)

                self.square_rects[square_number] = square_rect
                self.square_colors[square_number] = square_color

    def get_square_number(self, row, col):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        if row % 2 == 0:
            square_number = (row * self.x_board) + col + 1
        else:
            square_number = (row * self.x_board) + 10 - col
        return square_number

    def draw_board_animated(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.game_area.fill(GameColors.BLACK.value)
        self.drawing_complete = False

        # When I generate the square rects dictionary, it goes by col then row
        # I want to animate the board in order of squares, so I sorted the dictionary keys
        sorted_square_rects = sorted(self.square_rects.keys())
        for square_number in sorted_square_rects:
            pygame.draw.rect(self.game_area,
                             self.square_colors[square_number].value,
                             self.square_rects[square_number])
            text = self.font.render(str(square_number), True, GameColors.BLACK.value)
            text_rect = text.get_rect()
            text_rect.center = self.square_rects[square_number].center

            self.game_area.blit(text, text_rect)
            self.draw_to_window()
            yield

        self.drawing_complete = True

    def draw_board(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        for square_number in self.square_rects.keys():
            pygame.draw.rect(self.game_area,
                             self.square_colors[square_number].value,
                             self.square_rects[square_number])
            text = self.font.render(str(square_number), True, GameColors.BLACK.value)
            text_rect = text.get_rect()
            text_rect.center = self.square_rects[square_number].center

            self.game_area.blit(text, text_rect)
            pygame.display.flip()


    def is_drawing_complete(self):
        return self.drawing_complete

    def draw_snakes(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        pass

    def draw_to_window(self):
        self.window.blit(self.game_area, self.game_area.get_rect().topleft)

    def test_draw_board(self, col: int, row: int):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        logger.info(f'Left Square Coord: {col}')
        logger.info(f'Top Square Coord: {self.x_board - row - 1}')
        logger.info(f'Current col, row {col}, {row}')


