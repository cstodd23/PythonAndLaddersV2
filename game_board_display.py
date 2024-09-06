import pygame
import math

import button
from colors import GameColors
from game_settings import GameSettings
from game_board import GameBoard
from button import Button

from typing import Iterator

from logger_setup import func_logger, logger
import os
import inspect

file_path = __file__
file_name = os.path.basename(file_path)


class GameBoardDisplay:
    def __init__(self,
                 game_board: GameBoard,
                 window: pygame.display,
                 num_players: int = 4,
                 border_squares: float = 1.5
                 ):
        self.game_board = game_board
        self.x_board = self.game_board.x_board
        self.y_board = self.game_board.y_board

        self.window = window
        self.window_width, self.window_height = window.get_size()
        self.game_area = pygame.Surface((self.window_width, self.window_height))
        self.snakes_ladders_area = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        self.player_area = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)

        self.num_players = num_players

        self.border_squares = border_squares
        self.calculate_square_size()

        # Need to change all the dimentions that can change with window size to reference the
        # GameSettings class, that way if they are updated, the game will scale.
        self.square_size = GameSettings.SQUARE_SIZE
        self.border_size = self.square_size * border_squares

        self.start_rects = {}
        self.start_colors = {}

        self.square_rects = {}
        self.square_colors = {}

        self.arrow_head_length = 30
        self.arrow_head_angle = 0.5

        self.font = pygame.font.Font(None, 36)

        self.controls_area = None
        self.buttons = None

    @staticmethod
    def pixelate(surface, pixel_size):
        # Get the dimensions of the original surface
        width = surface.get_width()
        height = surface.get_height()

        # Calculate the new dimensions
        new_width = width // pixel_size
        new_height = height // pixel_size

        # Create a new surface with reduced size
        small_surface = pygame.transform.scale(surface, (new_width, new_height))

        # Scale it back up to the original size
        pixelated = pygame.transform.scale(small_surface, (width, height))

        return pixelated

    def board_setup(self, button_info):
        self.generate_start_squares()
        self.generate_buttons(button_info)
        self.calculate_controls_area()
        self.generate_board_squares()

    def calculate_square_size(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        base_length = min(self.window_width, self.window_height)
        square_size = int(base_length / (min(self.x_board, self.y_board) + (self.border_squares * 2)))
        GameSettings.SQUARE_SIZE = square_size
        return square_size

    def generate_board_squares(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        for col in range(self.y_board):
            for row in range(self.x_board):
                square_rect = pygame.Rect((col * self.square_size) + self.border_size,
                                          ((self.x_board - row - 1) * self.square_size) + self.border_size,
                                          self.square_size,
                                          self.square_size
                                          )
                square_color = GameColors.WHITE_SMOKE.value if (row + col) % 2 == 0 else GameColors.SILVER.value

                square_number = self.get_square_number(row, col)

                self.square_rects[square_number] = square_rect
                self.square_colors[square_number] = square_color

    def generate_start_squares(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        for player_num in range(self.num_players):
            if player_num % 2 == 0:
                color = GameColors.WHITE_SMOKE.value
            else:
                color = GameColors.SILVER.value
            start_top, start_left = self.get_topleft_start_square(player_num)
            square = pygame.Rect(start_left,
                                 start_top,
                                 self.square_size,
                                 self.square_size)
            self.start_rects[player_num] = square
            self.start_colors[player_num] = color

    def get_topleft_start_square(self, num) -> tuple[float, float]:
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        top = self.border_size + (self.y_board * self.square_size) + ((self.border_size - self.square_size) / 2)
        left = self.border_size + (self.square_size * num)
        return top, left

    def get_square_number(self, row, col):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        if row % 2 == 0:
            square_number = (row * self.x_board) + col + 1
        else:
            square_number = (row * self.x_board) + 10 - col
        return square_number

    def draw_board_animated(self) -> Iterator[tuple[str, bool]]:
        # When I generate the square rects dictionary, it goes by col then row
        # I want to animate the board in order of squares, so I sorted the dictionary keys
        sorted_square_rects = sorted(self.square_rects.keys())
        for square_number in sorted_square_rects:
            pygame.draw.rect(self.game_area,
                             self.square_colors[square_number],
                             self.square_rects[square_number])
            text = self.font.render(str(square_number), True, GameColors.BLACK.value)
            text_rect = text.get_rect()
            text_rect.center = self.square_rects[square_number].center

            self.game_area.blit(text, text_rect)
            # self.draw_to_window()
            yield "squares", False
        yield "squares", True

    def update_board_square(self, square, color):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.square_colors[square] = color

    def draw_start_animated(self):
        for player_num in self.start_rects.keys():
            pygame.draw.rect(self.game_area,
                             self.start_colors[player_num],
                             self.start_rects[player_num])
            text = self.font.render("P" + (str(player_num + 1)), True, GameColors.BLACK.value)
            text_rect = text.get_rect()
            text_rect.center = self.start_rects[player_num].center

            self.game_area.blit(text, text_rect)

            yield "start", False
        yield "start", True

    def draw_ladders(self) -> Iterator[tuple[str, bool]]:
        for ladder in self.game_board.ladders:
            start = self.square_rects[ladder[0]].center
            end = self.square_rects[ladder[1]].center
            arrow_width = self.get_arrow_width(ladder[0], ladder[1])
            pygame.draw.line(self.snakes_ladders_area,
                             GameColors.OPAQUE_HOOKER_GREEN.value,
                             self.square_rects[ladder[0]].center,
                             self.square_rects[ladder[1]].center,
                             width=arrow_width)

            self.draw_arrow_head(start, end, self.snakes_ladders_area, GameColors.OPAQUE_HOOKER_GREEN.value)

            yield "ladders", False
        yield "ladders", True

    def draw_snakes(self) -> Iterator[tuple[str, bool]]:
        for snake in self.game_board.snakes:
            start = self.square_rects[snake[0]].center
            end = self.square_rects[snake[1]].center
            arrow_width = self.get_arrow_width(snake[0], snake[1])
            pygame.draw.line(self.snakes_ladders_area,
                             GameColors.OPAQUE_REDWOOD.value,
                             self.square_rects[snake[0]].center,
                             self.square_rects[snake[1]].center,
                             width=arrow_width)

            self.draw_arrow_head(start, end, self.snakes_ladders_area, GameColors.OPAQUE_REDWOOD.value)

            yield "snakes", False
        yield "snakes", True

    def draw_arrow_head(self, start, end, surface, color):
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
        return width

    def draw_board_instantly(self):
        self.game_area.fill((0, 0, 0, 0))
        self.snakes_ladders_area.fill((0, 0, 0, 0))
        list(self.draw_board_animated())
        list(self.draw_buttons())
        list(self.draw_start_animated())
        list(self.draw_ladders())
        list(self.draw_snakes())

    def calculate_controls_area(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        last_starting_square = list(self.start_rects.items())[-1][1]
        controls_rect = pygame.Rect(
            last_starting_square.right,
            last_starting_square.top,
            self.window_width - self.border_size - last_starting_square.right,
            last_starting_square.bottom - last_starting_square.top
        )
        self.controls_area = controls_rect

    def generate_buttons(self, buttons_info: tuple):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.calculate_controls_area()
        buttons = {}
        i = 0
        for button_info in buttons_info:
            button_rect = pygame.Rect(
                (self.controls_area.width * (0.125 + (i * 0.25))) + self.controls_area.x,
                (self.controls_area.height * 0.25) + self.controls_area.y,
                self.controls_area.width * 0.2,
                self.controls_area.height * 0.5
            )
            button = Button(button_rect, button_info[1], button_info[0])
            buttons[button_info[0]] = button
            i += 1
        self.buttons = buttons

    def draw_buttons(self):
        for butt in self.buttons.values():
            butt.draw(self.game_area)
            yield 'buttons', False
        yield 'buttons', True

    def draw_to_window(self, player_group):
        logger.info("Running in game loop, must not differ")
        self.player_area.fill((0, 0, 0, 0))
        player_group.draw(self.player_area)
        self.window.blit(self.game_area, self.game_area.get_rect().topleft)
        self.window.blit(self.snakes_ladders_area, self.snakes_ladders_area.get_rect().topleft)
        self.window.blit(self.player_area, self.player_area.get_rect().topleft)
        # window_copy = self.window.copy()
        # pixelated_window = self.pixelate(window_copy, 1.5)
        # self.window.blit(pixelated_window, (0,0))

