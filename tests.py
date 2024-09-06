import os
import numpy as np
import game_logic
from game_settings import  GameSettings
import pygame
from spinner import Spinner


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


def spinner_test():
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((GameSettings.WINDOW_SIZE_X, GameSettings.WINDOW_SIZE_Y))
    game_area = pygame.surface.Surface((GameSettings.WINDOW_SIZE_X, GameSettings.WINDOW_SIZE_Y))
    radius = 300
    spinner_rect = pygame.rect.Rect((0,
                                     0,
                                     radius * 2,
                                     radius * 2))
    spinner_surface = pygame.surface.Surface(spinner_rect.size)
    spinner = Spinner(5, game_area, window, spinner_surface, game_area.get_rect().center, radius=radius)
    spinner.draw_spinner_base()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                # if display_board.buttons["ROLL"].is_clicked(event.pos):
                pass

        spinner.print_surface_centers()
        game_area.blit(spinner_surface, spinner_rect.center)
        window.blit(game_area, game_area.get_rect().topleft)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

spinner_test()
