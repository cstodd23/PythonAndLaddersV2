import game_board
from button import Button
from game_board_display import DisplayBoard
from game_board import GameBoard
from typing import Iterator
import pygame
from colors import GameColors
from logger_setup import func_logger, logger

ANIMATION_TIME = 10


def test_check_snakes_ladders():
    game = game_board.GameBoard()
    for i in range(100):
        mover_info = game.check_snakes_ladders(i)
        print(f'Checking Square: {i}, Mover Info Returned: {mover_info}')

def test_button_functionality():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()

    test_button = Button(
        rect=pygame.Rect(150, 100, 100, 50),
        color=GameColors.PRUSSIAN_BLUE,
        text='Test'
    )

    running = True
    is_blue = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if test_button.is_clicked(event.pos):
                    print(f"Button Clicked at {event.pos}")
                    is_blue = not is_blue
                    test_button.set_colors(GameColors.PRUSSIAN_BLUE if is_blue else GameColors.HOOKER_GREEN,
                                           GameColors.BLACK if is_blue else GameColors.WHITE_SMOKE)
        screen.fill(GameColors.BLACK.value)

        test_button.draw(screen)

        pygame.display.flip()

        clock.tick(60)
    pygame.quit()


def test_display_board():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((800, 800))  # Reduced window size for example

    display_board = DisplayBoard(10, 10, window)
    display_board.generate_board_squares()  # Generate the board squares

    display_board.draw_board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(GameColors.BLACK.value)
        display_board.draw_to_window()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


def square_animation_test():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1500, 1500))
    board = GameBoard()

    display_board = DisplayBoard(board, window)
    display_board.generate_board_squares()

    draw_generator = display_board.draw_board_animated()

    pygame.time.set_timer(pygame.USEREVENT, ANIMATION_TIME)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                try:
                    next(draw_generator)
                except:
                    pygame.time.set_timer(pygame.USEREVENT, 0)

        if not display_board.is_drawing_complete():
            display_board.draw_to_window()
            pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def square_mover_animation_test():
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((1500, 1500))
    board = GameBoard()

    display_board = DisplayBoard(board, window)
    display_board.generate_board_squares()

    combined_animation = chain_generators(
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
                try:
                    current_animation, is_complete = next(combined_animation)
                    if is_complete:
                        logger.info(f'{current_animation} animation completed')
                except StopIteration:
                    pygame.time.set_timer(pygame.USEREVENT, 0)

        display_board.draw_to_window()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def start_square_mover_animation_test():
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((1500, 1500))
    board = GameBoard()

    display_board = DisplayBoard(board, window)
    display_board.generate_start_squares()
    display_board.generate_board_squares()

    combined_animation = chain_generators(
        display_board.draw_start_animated(),
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
                try:
                    current_animation, is_complete = next(combined_animation)
                    if is_complete:
                        logger.info(f'{current_animation} animation completed')
                except StopIteration:
                    pygame.time.set_timer(pygame.USEREVENT, 0)

        display_board.draw_to_window()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def button_test():
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((1500, 1500))
    board = GameBoard()

    display_board = DisplayBoard(board, window)
    display_board.board_setup()

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
                try:
                    current_animation, is_complete = next(combined_animation)
                    if is_complete:
                        logger.info(f'{current_animation} animation completed')
                except StopIteration:
                    pygame.time.set_timer(pygame.USEREVENT, 0)

        display_board.draw_to_window()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def player_animation_test():
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((1500, 1500))
    board = GameBoard()
    display_board = DisplayBoard(board, window)

    display_board.board_setup()

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
                try:
                    current_animation, is_complete = next(combined_animation)
                    if is_complete:
                        logger.info(f'{current_animation} animation completed')
                except StopIteration:
                    pygame.time.set_timer(pygame.USEREVENT, 0)

            print(event)

        display_board.draw_to_window()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def chain_generators(*generators: Iterator[tuple[str, bool]]) -> Iterator[tuple[str, bool]]:
    logger.debug(f"Currently in chain_generators function")
    for gen in generators:
        yield from gen


if __name__ == "__main__":
    # test_display_board()
    # test_button_functionality()
    # square_animation_test()
    # square_mover_animation_test()
    # start_square_mover_animation_test()
    # start_animation()
    # button_test()
    player_animation_test()
