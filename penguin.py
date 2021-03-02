import pygame
import config
from player import Player


class Penguin(Player):

    __instnce = None

    def __new__(cls, x_pos, y_pos):
        if cls.__instnce is None:
            cls.__instnce = super().__new__(cls)
        return cls.__instnce

    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.velocity = config.PENGUIN_VELOCITY
        self.load_walk_sprites()
        self.lifes = config.PENGUIN_MAX_LIFE

    def load_walk_sprites(self):
        up = []
        right = []
        down = []
        left = []
        walk_animation = []
        for i in range(5):
            up.append(pygame.transform.scale(pygame.image.load('resources/units/penguin/P_W_U{}.png'.format(i)),
                                             (config.SCALE, config.SCALE)))
            right.append(pygame.transform.scale(pygame.image.load('resources/units/penguin/P_W_R{}.png'.format(i)),
                                                (config.SCALE, config.SCALE)))
            down.append(pygame.transform.scale(pygame.image.load('resources/units/penguin/P_W_D{}.png'.format(i)),
                                               (config.SCALE, config.SCALE)))
            left.append(pygame.transform.scale(pygame.image.load('resources/units/penguin/P_W_L{}.png'.format(i)),
                                               (config.SCALE, config.SCALE)))
        walk_animation.extend([up, right, down, left])
        self.set_walk_animation(walk_animation)
