import pygame
import numpy as np
from colors import GameColors
import math


class Spinner:
    def __init__(self,
                 rng_seed,
                 game_area: pygame.surface.Surface,
                 window,
                 spinner_surface,
                 center,
                 radius: int = 300,
                 min_spin: int = 1,
                 max_spin: int = 6
                 ):
        self.rng = self.rng = np.random.default_rng(rng_seed)
        self.min_spin = min_spin
        self.max_spin = max_spin
        self.radius = radius
        self.num_sections = self.max_spin - (min_spin - 1)
        self.game_area = game_area
        self.spinner_surface = spinner_surface
        self.spinner_surface_center = self.spinner_surface.get_rect().center
        self.spinner_arrow_surface = pygame.surface.Surface(self.spinner_surface.get_size())
        self.window = window
        self.center = center
        self.font_size = int(self.radius * 0.4)
        self.width = int(self.radius * 0.05)
        self.font = pygame.font.Font(None, self.font_size)

    def draw_spinner_base(self):
        pygame.draw.circle(
            self.spinner_surface, GameColors.GUNMETAL.value, self.spinner_surface_center, radius=self.radius)
        pygame.draw.circle(
            self.spinner_surface, GameColors.BLACK.value, self.spinner_surface_center, radius=self.radius - (self.width * 2), width=self.width)
        pygame.draw.circle(
            self.spinner_surface, GameColors.EBONY.value, self.spinner_surface_center, radius=self.radius - (self.width * 3), width=self.width)

        for section_num in range(self.num_sections):
            x, y = self.calculate_line_end_point(self.spinner_surface_center, self.radius-(self.width * 2) + (self.width * 0.5), self.num_sections, section_num)
            pygame.draw.line(self.spinner_surface, GameColors.BLACK.value, self.spinner_surface_center, (x, y), width=self.width)
            text = str(section_num + 1)
            text_surface = self.font.render(text, True, GameColors.SILVER.value)
            text_x, text_y = self.calculate_text_centers(self.spinner_surface_center, self.radius, self.num_sections, section_num)
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            self.spinner_surface.blit(text_surface, text_rect)

        pygame.draw.circle(self.spinner_surface,
                           GameColors.EBONY.value,
                           self.spinner_surface_center,
                           radius=self.radius - self.width,
                           width=self.width)

    def animate_spinner(self):
        pass



    def calculate_line_end_point(self, center, line_length, number_of_sections, section_number):
        radian_angle = (section_number / number_of_sections) * (2 * math.pi)
        x = center[0] + math.cos(radian_angle) * line_length
        y = center[1] + math.sin(radian_angle) * line_length
        return x, y

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

    def calculate_text_centers(self, center, radius, number_of_sections, section_number):

        radian_angle = ((section_number / number_of_sections) + (1 / (number_of_sections * 2))) * (2 * math.pi)

        x = center[0] + math.cos(radian_angle) * (radius * 0.6)
        y = center[1] + math.sin(radian_angle) * (radius * 0.6)
        return x, y

    def print_surface_centers(self):
        print(f'self.spinner_arrow_surface: {self.spinner_arrow_surface.get_rect()}')
        print(f'self.spinner_surface: {self.spinner_surface.get_rect()}')
        print(f'self.game_area: {self.game_area.get_rect()}')


