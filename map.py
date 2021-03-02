import math
import pygame
import config
import tile_images


class Map:
    def __init__(self, file_name):
        self.background_map = []
        self.load_background_map(file_name)
        self.camera = [0.0, 0.0]

    def load_background_map(self, file_name):
        with open('resources/maps/' + file_name + '.txt') as file:
            for line in file.readlines():
                start = 0
                map_line = []
                for i in range(0, len(line)):
                    if line[i] == ' ' or line[i] == '\n':
                        map_line.append(line[start:i])
                        start = i+1
                self.background_map.append(map_line)

    def is_valid_position(self, x, y):
        background_map = self.get_background_map()
        if 'W' in background_map[y][x] or 'C' in background_map[y][x]:
            return False
        return True

    def render_map(self, screen, player):
        self.position_camera(player)
        y = 0
        for line in self.background_map:
            x = 0
            for tile in line:
                image = tile_images.tile_map_images[tile]
                image = pygame.transform.scale(image, (config.TILESIZE, config.TILESIZE))
                screen.blit(image, (x - int(self.camera[0]), y - int(self.camera[1])))
                x += config.TILESIZE
            y += config.TILESIZE

    def position_camera(self, player):
        max_x_pos = len(self.background_map[0]) * config.TILESIZE - config.WIDTH/2
        max_y_pos = len(self.background_map) * config.TILESIZE - config.HEIGHT/2

        pos = player.get_position()
        if max_x_pos > pos[0] > config.WIDTH/2:
            self.camera[0] += (pos[0] - self.camera[0] - config.WIDTH / 2) / config.CAMERA_SMOOTH
        elif pos[0] < config.WIDTH/2:
            if self.camera[0] > config.EPSILON:
                self.camera[0] = self.camera[0] / config.CAMERA_BOUNDARIES_SMOOTH
            else:
                self.camera[0] = 0
        else:
            if self.camera[0] < max_x_pos - config.WIDTH / 2:
                self.camera[0] += config.CAMERA_SMOOTH / config.REDUCE / config.CAMERA_BOUNDARIES_SMOOTH
            else:
                self.camera[0] = max_x_pos - config.WIDTH / 2

        if max_y_pos > pos[1] > config.HEIGHT/2:
            self.camera[1] += (pos[1] - self.camera[1] - config.HEIGHT / 2) / config.CAMERA_SMOOTH
        elif pos[1] < config.HEIGHT/2:
            if self.camera[1] > config.EPSILON:
                self.camera[1] = self.camera[1] / config.CAMERA_BOUNDARIES_SMOOTH
            else:
                self.camera[1] = 0
        else:
            if self.camera[1] < max_y_pos - config.HEIGHT/2:
                self.camera[1] += config.CAMERA_SMOOTH/config.REDUCE/config.CAMERA_BOUNDARIES_SMOOTH
            else:
                self.camera[1] = max_y_pos - config.HEIGHT/2

    def get_background_map(self):
        return self.background_map

    def get_height_map(self):
        return len(self.background_map)

    def get_width_map(self):
        return len(self.background_map[0])

    def get_tile_back_map(self, i, j):
        return self.background_map[i][j]

    def get_camera(self):
        return self.camera

    def set_background_map(self, background_map):
        self.background_map = background_map
