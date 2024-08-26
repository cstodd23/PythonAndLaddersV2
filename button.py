import pygame
from matplotlib import colors as mcolors
from colors import GameColors, lighten_color

import inspect
from logger_setup import func_logger
from logger_setup import logger
import os

file_path = __file__
file_name = os.path.basename(file_path)


class Button:
    def __init__(self,
                 rect: pygame.Rect,
                 color: GameColors,
                 text: str,
                 font_size: int = 24,
                 text_color: GameColors = GameColors.BLACK):
        self.rect = rect
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, self.text_color.value)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface) -> None:
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        pygame.draw.rect(screen, self.color.value, self.rect)

        border_color = lighten_color(self.color)
        pygame.draw.rect(screen, border_color, self.rect, 4)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        return self.rect.collidepoint(pos)

    def set_text(self, new_text: str) -> None:
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color.value)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def set_colors(self, button_color: GameColors, text_color: GameColors = GameColors.BLACK) -> None:
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.color = button_color
        self.text_color = text_color
        self.text_surface = self.font.render(self.text, True, self.text_color.value)