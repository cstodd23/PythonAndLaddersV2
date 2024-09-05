import os
import numpy as np
import game_logic
from game_settings import  GameSettings
import pygame
from spinner import Spinner


def spinner_test():
    pygame.init()
    clock = pygame.time.Clock()
    spinner = Spinner

    window = pygame.display.set_mode((GameSettings.WINDOW_SIZE_X, GameSettings.WINDOW_SIZE_Y))


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if display_board.buttons["ROLL"].is_clicked(event.pos):
                    pass

        display_board.draw_to_window(player_group)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
