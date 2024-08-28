import pygame
import math
from colors import GameColors
from game_board import GameBoard
from typing import Iterator

from logger_setup import func_logger, logger
import os
import inspect

file_path = __file__
file_name = os.path.basename(file_path)


class DisplayBoard:
    def __init__(self,
                 game_board: GameBoard,
                 window: pygame.display,
                 border_squares: float = 1.5
                 ):
        self.game_board = game_board
        self.x_board = self.game_board.x_board
        self.y_board = self.game_board.y_board

        self.window = window
        self.window_width, self.window_height = window.get_size()
        self.game_area = pygame.Surface((self.window_width, self.window_height))

        self.border_squares = border_squares

        self.square_size = self.calculate_square_size()
        self.border_size = self.square_size * border_squares

        self.square_rects = {}
        self.square_colors = {}

        self.arrow_head_length = 30
        self.arrow_head_angle = 0.5

        self.ladder_color = GameColors.HOOKER_GREEN.value
        self.snake_color = GameColors.REDWOOD.value

        self.font = pygame.font.Font(None, 36)

        self.animate_squares_complete = False
        self.animate_ladders_complete = None
        self.animate_snakes_complete = None

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

    def draw_board_animated(self) -> Iterator[tuple[str, bool]]:
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
            yield "squares", False
        self.animate_squares_complete = True
        yield "squares", True

    def draw_ladders(self) -> Iterator[tuple[str, bool]]:
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        for ladder in self.game_board.ladders:
            start = self.square_rects[ladder[0]].center
            end = self.square_rects[ladder[1]].center
            arrow_width = self.get_arrow_width(ladder[0], ladder[1])
            pygame.draw.line(self.game_area,
                             self.ladder_color,
                             self.square_rects[ladder[0]].center,
                             self.square_rects[ladder[1]].center,
                             width=arrow_width)

            self.draw_arrow_head(start, end, self.game_area, self.ladder_color)
            self.draw_to_window()
            yield "ladders", False
        self.animate_ladders_complete = True
        yield "ladders", True

    def draw_snakes(self) -> Iterator[tuple[str, bool]]:
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        for snake in self.game_board.snakes:
            start = self.square_rects[snake[0]].center
            end = self.square_rects[snake[1]].center
            arrow_width = self.get_arrow_width(snake[0], snake[1])
            pygame.draw.line(self.game_area,
                             self.snake_color,
                             self.square_rects[snake[0]].center,
                             self.square_rects[snake[1]].center,
                             width=arrow_width)

            self.draw_arrow_head(start, end, self.game_area, self.snake_color)
            self.draw_to_window()
            yield "snakes", False
        self.animate_ladders_complete = True
        yield "snakes", True

    def draw_arrow_head(self, start, end, surface, color):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        angle = math.atan2(dy, dx)

        head_counter_clock_x = end[0] - (self.arrow_head_length * math.cos(angle + self.arrow_head_angle))
        head_counter_clock_y = end[1] - (self.arrow_head_length * math.sin(angle + self.arrow_head_angle))
        head_clockwise_x = end[0] - (self.arrow_head_length * math.cos(angle - self.arrow_head_angle))
        head_clockwise_y = end[1] - (self.arrow_head_length * math.sin(angle - self.arrow_head_angle))

        pygame.draw.polygon(surface,
                            color,
                            [(end[0], end[1]),
                             (head_counter_clock_x, head_counter_clock_y),
                             (head_clockwise_x, head_clockwise_y)])

    def get_arrow_width(self, start, end):
        width = abs(int(((end - start) / self.game_board.finish_line) * 10)) + 3
        logger.info(f'Start: {start}, End: {end}, Difference: {end - start}, Width: {width}')
        return width

    def is_drawing_complete(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        return self.drawing_complete

    def draw_to_window(self):
        self.window.blit(self.game_area, self.game_area.get_rect().topleft)

    def test_draw_board(self, col: int, row: int):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        logger.info(f'Left Square Coord: {col}')
        logger.info(f'Top Square Coord: {self.x_board - row - 1}')
        logger.info(f'Current col, row {col}, {row}')


