from enum import Enum


class GameState(Enum):
    NONE = 0
    RUNNING = 1
    PLAYER_DEAD = 2
    MAIN_MENU = 3
    OPTION = 4
    ENDING = 5
