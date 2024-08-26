import pygame
from matplotlib import colors as mcolors

import inspect
from logger_setup import func_logger
from logger_setup import logger
import os

file_path = __file__
file_name = os.path.basename(file_path)


class Button:
    def __init__(self, rect, color, text, font, text_color=mcolors.CSS4_COLORS['black']):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color

    def draw(self, surface):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        print(f'Text Rect from Button Class: {text_rect}')
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False