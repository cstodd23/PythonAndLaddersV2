import game_board
from button import Button
import pygame
from colors import GameColors


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

if __name__ == "__main__":
    test_button_functionality()
