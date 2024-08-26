import pygame
from enum import Enum
import game_board

# Logger Imports and Setup
from logger_setup import func_logger, logger
import inspect
import os

file_path = __file__
file_name = os.path.basename(file_path)


class EventSystem:
    def __init__(self):
        self.listeners = {}

    def register_listener(self, event_name, listener):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def emit(self, event_name, data=None):
        logger.info(f'Emitting Event: {event_name}')
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(data)
        else:
            logger.info(f'No Listeners for event: {event_name}')

    def remove_listener(self, event_name, listener):
        if event_name in self.listeners:
            self.listeners[event_name].remove(listener)


class GameEvents:
    ROLL = 'roll'
    SKIP_ROLL = 'skip_roll'
    KEEP_ROLL = 'keep_roll'


class GameState(Enum):
    READY_TO_ROLL = 1
    ROLL_MADE = 2


class DisplayedGame:
    def __init__(self, rng_seed: int = None, fps: int = 60):
        pygame.init()
        pygame.font.init()

        self.event_system = EventSystem()
        self.game_events = GameEvents()
        self.current_state = GameState.READY_TO_ROLL

        self.rng_seed = rng_seed

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.running = True

        # TEST VARIABLES
        self.test_screen = pygame.display.set_mode((1000, 1000))
        self.roll_button = pygame.Rect(100, 450, 150, 50)
        self.skip_roll_button = pygame.Rect(300, 450, 150, 50)
        self.keep_roll_button = pygame.Rect(500, 450, 150, 50)

    def setup_game(self):
        self.event_system.register_listener(self.game_events.ROLL, self.on_roll)
        self.event_system.register_listener(self.game_events.SKIP_ROLL, self.on_skip_roll)
        self.event_system.register_listener(self.game_events.KEEP_ROLL, self.on_keep_roll)


    def run_game(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.setup_game()
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(self.fps)
        finally:
            self.cleanup()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        if self.current_state == GameState.READY_TO_ROLL:
            if self.roll_button.collidepoint(pos):
                self.event_system.emit(self.game_events.ROLL)
                self.current_state = GameState.ROLL_MADE
        elif self.current_state == GameState.ROLL_MADE:
            if self.skip_roll_button.collidepoint(pos):
                self.event_system.emit(self.game_events.SKIP_ROLL)
                self.current_state = GameState.READY_TO_ROLL
            elif self.keep_roll_button.collidepoint(pos):
                self.event_system.emit(self.game_events.KEEP_ROLL)
                self.current_state = GameState.READY_TO_ROLL

    def update(self):
        pass

    def draw(self):
        self.test_screen.fill((0, 0, 0))

        pygame.draw.rect(self.test_screen, (0, 255, 0), self.roll_button)
        pygame.draw.rect(self.test_screen, (255, 0, 0), self.skip_roll_button)
        pygame.draw.rect(self.test_screen, (0, 0, 255), self.keep_roll_button)
        pygame.display.flip()

    def on_roll(self, data):
        print("Roll Button Clicked!")

    def on_skip_roll(self, data):
        print("Skip Roll Button Clicked!")

    def on_keep_roll(self, data):
        print("Keep Roll Button Clicked!")

    def cleanup(self):
        pygame.quit()

    def quit_game(self):
        self.running = False

