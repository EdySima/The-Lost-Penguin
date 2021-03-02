import pygame
import config
from game import Game
from game_state import GameState

pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

pygame.display.set_caption(config.TITLE)

clock = pygame.time.Clock()

game = Game(screen)

while game.game_state != GameState.ENDING:
    clock.tick(60)
    game.update()
    pygame.display.flip()

pygame.quit()
