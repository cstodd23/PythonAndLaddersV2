from button import Button
from game_board_display import DisplayBoard
from game_board import GameBoard
from dice import Dice
from game_settings import GameSettings

from typing import Iterator
import pygame
from colors import GameColors
import player
from logger_setup import func_logger, logger

ANIMATION_TIME = 10


class GameState:
    def __init__(self):
        self.roll_clickable = False
        self.interaction_clickable = False
        self.board_setup_animation_completed = False
        self.dice_value = None


def player_animation_test():
    pygame.init()
    clock = pygame.time.Clock()
    game_state = GameState()

    window = pygame.display.set_mode((GameSettings.WINDOW_SIZE_X, GameSettings.WINDOW_SIZE_Y))
    board = GameBoard()
    display_board = DisplayBoard(board, window)
    display_board.board_setup()

    dice = Dice()
    player1_rect = display_board.start_rects[1].scale_by(0.75)
    player1 = player.Player(player1_rect, 1, "Juan")
    player_group = pygame.sprite.Group(player1)


    # Comment out all other animations if you want to just test a single animation
    combined_animation = chain_generators(
        display_board.draw_start_animated(),
        display_board.draw_buttons(),
        display_board.draw_board_animated(),
        display_board.draw_ladders(),
        display_board.draw_snakes()
    )

    pygame.time.set_timer(pygame.USEREVENT, ANIMATION_TIME)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                handle_user_event(game_state, combined_animation)
            elif event.type == pygame.MOUSEBUTTONUP and game_state.roll_clickable:
                if display_board.buttons["ROLL"].is_clicked(event.pos):
                    logger.info(f'ROLL BUTTON CILCKED')
                    logger.info('~' * 80)
                    game_state.dice_value = dice.roll()
                    logger.info(f'Dice Rolled: {game_state.dice_value}')
                    player1.add_roll(game_state.dice_value)
                    player1.set_new_center(display_board.square_rects[player1.get_square()].center)
        if player1.moving:
            game_state.roll_clickable = False
            game_state.interaction_clickable = False
        else:
            game_state.roll_clickable = True
            game_state.interaction_clickable = True

        display_board.draw_to_window(player_group)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def handle_user_event(game_state: GameState, combined_animation: Iterator[tuple[str, bool]]):
    if not game_state.board_setup_animation_completed:
        try:
            current_animation, is_complete = next(combined_animation)
            if is_complete:
                logger.info(f"{current_animation} animation completed")
        except StopIteration:
            game_state.board_setup_animation_completed = True
            game_state.roll_clickable = True
            logger.info('Board setup completed')



def chain_generators(*generators: Iterator[tuple[str, bool]]) -> Iterator[tuple[str, bool]]:
    logger.debug(f"Currently in chain_generators function")
    for gen in generators:
        yield from gen


if __name__ == "__main__":
    player_animation_test()
