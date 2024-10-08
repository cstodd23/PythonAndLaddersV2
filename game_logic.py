import pygame
from enum import Enum
from typing import Iterator
import warnings

from game_board_display import GameBoardDisplay
from game_board import GameBoard
from dice import Dice
from game_settings import GameSettings
from player import Player
# from button import Button
from colors import GameColors


# Logger Imports and Setup
from logger_setup import func_logger, logger
import inspect
import os

file_path = __file__
file_name = os.path.basename(file_path)


class GameEvents:
    ROLL = 'roll'
    SKIP_ROLL = 'skip_roll'
    KEEP_ROLL = 'keep_roll'


class GamePhase(Enum):
    BOARD_CREATION = 1
    ANIMATING = 2
    READY_TO_ROLL = 3
    MOVER_CHOICE = 4
    ROLL_MADE = 5


class TurnTracker:
    def __init__(self, num_players):
        self.num_players = num_players
        self.current_player = 1
        self.current_turn = 1

    def next_turn(self):
        self.current_player = self.current_turn % self.num_players + 1
        self.current_turn += 1

    def get_current_player(self):
        return self.current_player

    def get_current_turn(self):
        return self.current_turn


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


class DisplayedGame:
    def __init__(self, num_players: int, rng_seed: int = None, fps: int = 60):
        pygame.init()
        pygame.time.set_timer(pygame.USEREVENT, GameSettings.ANIMATION_TIME)
        self.rng_seed = rng_seed

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.num_players = num_players
        self.button_info = (
            ("ROLL", GameColors.ENGLISH_VIOLET),
            ("SKIP ROLL", GameColors.PRUSSIAN_BLUE),
            ("KEEP ROLL", GameColors.EBONY))
        self.player_info = ((1, 'Juan'), (2, 'Jude'), (3, 'Tree'), (4, 'Boris'))
        # self.players = {}

        self.event_system = EventSystem()
        self.game_events = GameEvents()
        self.turn_tracker = TurnTracker(self.num_players)
        self.current_state = GamePhase.BOARD_CREATION
        self.dice = Dice(rng_seed=self.rng_seed)


        # Need to add a loading in pre-made boards feature to the GameBoard
        self.game_board = GameBoard(rng_seed=self.rng_seed)
        self.window = pygame.display.set_mode((GameSettings.WINDOW_SIZE_X, GameSettings.WINDOW_SIZE_Y))
        self.game_board_display = GameBoardDisplay(self.game_board, self.window)
        self.game_board_display.board_setup(self.button_info)

        self.combined_animation = self.chain_generators(
            self.game_board_display.draw_start_animated(),
            self.game_board_display.draw_buttons(),
            self.game_board_display.draw_board_animated(),
            self.game_board_display.draw_ladders(),
            self.game_board_display.draw_snakes()
        )

        self.player_group = pygame.sprite.Group()
        self.setup_players()

        self.next_square = None
        self.mover_info = None

        self.running = True

        # TEST VARIABLES
        # self.test_screen = pygame.display.set_mode((1000, 1000))
        # self.roll_button = pygame.Rect(100, 450, 150, 50)
        # self.skip_roll_button = pygame.Rect(300, 450, 150, 50)
        # self.keep_roll_button = pygame.Rect(500, 450, 150, 50)

    @staticmethod
    def chain_generators(*generators: Iterator[tuple[str, bool]]) -> Iterator[tuple[str, bool]]:
        for gen in generators:
            yield from gen

    def setup_game(self):
        self.event_system.register_listener(self.game_events.ROLL, self.on_roll)
        self.event_system.register_listener(self.game_events.SKIP_ROLL, self.on_skip_roll)
        self.event_system.register_listener(self.game_events.KEEP_ROLL, self.on_keep_roll)

    def setup_players(self):
        for num_player in range(self.num_players):
            player = Player(
                self.game_board_display.start_rects[num_player].scale_by(0.75),
                self.player_info[num_player][0],
                self.player_info[num_player][1]
            )
            self.player_group.add(player)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_state != GamePhase.BOARD_CREATION:
                    self.handle_mouse_click(event.pos)
            elif event.type == pygame.USEREVENT:
                self.handle_user_event()

    def handle_mouse_click(self, pos):
        if any(player.moving for player in self.player_group):
            self.current_state = GamePhase.ANIMATING
        elif self.current_state != GamePhase.MOVER_CHOICE:
            self.current_state = GamePhase.READY_TO_ROLL
        if self.current_state == GamePhase.READY_TO_ROLL:
            if self.game_board_display.buttons["ROLL"].collidepoint(pos):
                self.event_system.emit(self.game_events.ROLL)

        elif self.current_state == GamePhase.MOVER_CHOICE:
            if self.game_board_display.buttons["SKIP ROLL"].collidepoint(pos):
                self.event_system.emit(self.game_events.SKIP_ROLL)
            elif self.game_board_display.buttons["KEEP ROLL"].collidepoint(pos):
                self.event_system.emit(self.game_events.KEEP_ROLL)

    def handle_user_event(self):
        if self.current_state == GamePhase.BOARD_CREATION:
            try:
                current_animation, is_complete = next(self.combined_animation)
                if is_complete:
                    logger.info(f"{current_animation} animation completed")
            except StopIteration:
                self.current_state = GamePhase.READY_TO_ROLL
                logger.info('Board setup completed')

    def update(self):
        self.player_group.update()

    def draw(self):
        self.game_board_display.draw_board_instantly()
        self.game_board_display.draw_to_window(self.player_group)
        pygame.display.flip()

    def on_roll(self, data):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        logger.info("Roll Button Clicked!")
        player = self.get_player(self.turn_tracker.get_current_player())
        roll = self.dice.roll()
        self.next_square = roll + player.square
        logger.info(f'Roll: {roll}, Next Square: {self.next_square}')
        self.mover_info = self.game_board.check_snakes_ladders(self.next_square)
        if self.mover_info['type']:
            logger.info(f"Landed on a {self.mover_info['type']} at {self.mover_info['start']}")
            self.current_state = GamePhase.MOVER_CHOICE
            self.game_board_display.update_board_square(self.next_square, GameColors.ENGLISH_VIOLET.value)
            # Generate Ghost Sprite or Change colors of squares it will land on

        else:
            player.set_next_square(self.next_square)
            player.set_next_center(self.game_board_display.square_rects[self.next_square].center)

            self.end_turn()

    def on_skip_roll(self, data):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        logger.info("Skip Roll Button Clicked!")
        self.game_board_display.update_board_square(self.next_square, self.game_board_display.square_colors[self.next_square - 2])
        # remove the highlighted square
        self.end_turn()

    def on_keep_roll(self, data):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        logger.info("Keep Roll Button Clicked!")
        self.game_board_display.update_board_square(self.next_square, self.game_board_display.square_colors[self.next_square - 2])
        player = self.get_player(self.turn_tracker.get_current_player())
        player.set_next_square(self.next_square)
        player.set_next_center(self.game_board_display.square_rects[self.next_square].center)
        player.set_snake_ladder_end_square(self.mover_info['end'])
        player.set_snake_ladder_end_center(self.game_board_display.square_rects[self.mover_info['end']].center)

        self.end_turn()
        # I believe that the end turn logic needs to be contained in the player at this point....
        # Probably need to change the on skip roll and on roll functions to match.

    def end_turn(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.next_square = None
        self.mover_info = None
        self.current_state = GamePhase.ANIMATING
        self.turn_tracker.next_turn()

    def cleanup(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        pygame.quit()

    def quit_game(self):
        func_logger(file_name, self.__class__.__name__, inspect.currentframe().f_code.co_name)
        self.running = False

    def get_player(self, player_num: int):
        for sprite in self.player_group:
            if getattr(sprite, 'num') == player_num:
                return sprite
        return None

