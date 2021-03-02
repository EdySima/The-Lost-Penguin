import pygame
import config
from unit_move import UnitMove
from unit import Unit


class Player(Unit):

    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.player_tiles = []
        self.hitbox_corners = []        # [up_left, up_right, down_right, down_left]
        self.life_srpites = []
        self.set_hitbox(self.position, config.PENGUIN_HITBOX_OFFSET, config.PENGUIN_HITBOX)
        self.load_life_sprites()
        self.load_sound_effect()

    def load_life_sprites(self):
        life = []
        for i in range(3):
            life.append(pygame.transform.scale(pygame.image.load('resources/player_lifes/life{}.png'.format(i)),
                                               (config.SCALE, config.SCALE)))
        self.set_life_sprites(life)

    def load_sound_effect(self):
        self.penguin_hit = pygame.mixer.Sound('resources/sound_effect/penguin_hit.wav')

    def play_hit_sound(self, volume):
        self.penguin_hit.set_volume(volume)
        self.penguin_hit.play()

    def calculate_hitbox_corners(self):
        hitbox = self.get_hitbox()
        hitbox_corners = [[hitbox[0], hitbox[1]], [hitbox[0] + hitbox[2], hitbox[1]],
                          [hitbox[0] + hitbox[2], hitbox[1] + hitbox[3]], [hitbox[0], hitbox[1] + hitbox[3]]]
        self.set_hitbox_corners(hitbox_corners)

    def update_position(self, direction, player_tiles):
        self.set_is_still(True)
        self.validate_position(self.direction, player_tiles)
        position = self.get_position()

        if direction != UnitMove.NONE:
            self.set_is_still(False)
            self.set_direction(direction)
            if direction == UnitMove.UP:
                self.set_position(position[0], position[1] - self.get_velocity())
            if direction == UnitMove.DOWN:
                self.set_position(position[0], position[1] + self.get_velocity())
            if direction == UnitMove.LEFT:
                self.set_position(position[0] - self.get_velocity(), position[1])
            if direction == UnitMove.RIGHT:
                self.set_position(position[0] + self.get_velocity(), position[1])

            self.set_hitbox(self.position, config.PENGUIN_HITBOX_OFFSET, config.PENGUIN_HITBOX)

    def validate_position(self, direction, player_tiles):
        position = self.get_position()

        if ('C' in player_tiles[0] or 'C' in player_tiles[1]) and direction == UnitMove.UP:
            self.set_position(position[0], position[1] + self.get_velocity())
        if ('C' in player_tiles[2] or 'C' in player_tiles[3]) and direction == UnitMove.DOWN:
            self.set_position(position[0], position[1] - self.get_velocity())
        if ('C' in player_tiles[0] or 'C' in player_tiles[3]) and direction == UnitMove.LEFT:
            self.set_position(position[0] + self.get_velocity(), position[1])
        if ('C' in player_tiles[1] or 'C' in player_tiles[2]) and direction == UnitMove.RIGHT:
            self.set_position(position[0] - self.get_velocity(), position[1])

        if ('E' in player_tiles[2] or 'E' in player_tiles[3]) and direction == UnitMove.UP:
            self.set_position(position[0], position[1] + self.get_velocity())
        if ('E' in player_tiles[2] or 'E' in player_tiles[3]) and direction == UnitMove.DOWN:
            self.set_position(position[0], position[1] - self.get_velocity())

        self.set_hitbox(self.position, config.PENGUIN_HITBOX_OFFSET, config.PENGUIN_HITBOX)

    def render(self, screen, camera, grid):
        walk_count = self.get_walk_count()
        player_position = self.get_position()
        is_still = self.get_is_still()
        direction = self.get_direction()
        walk_animation = self.get_walk_animation()

        if walk_count >= config.WALK_COUNT_MAX:
            walk_count = 0
        render_position = [player_position[0] - camera[0], player_position[1] - camera[1]]

        if is_still:
            if direction == UnitMove.RIGHT or direction == UnitMove.NONE:
                screen.blit(walk_animation[1][0], render_position)
            elif direction == UnitMove.LEFT:
                screen.blit(walk_animation[3][0], render_position)
            elif direction == UnitMove.UP:
                screen.blit(walk_animation[0][0], render_position)
            elif direction == UnitMove.DOWN:
                screen.blit(walk_animation[2][0], render_position)
        else:
            if direction == UnitMove.UP:
                screen.blit(walk_animation[0][walk_count//config.WALK_SPEED], render_position)
            elif direction == UnitMove.DOWN:
                screen.blit(walk_animation[2][walk_count//config.WALK_SPEED], render_position)
            elif direction == UnitMove.LEFT:
                screen.blit(walk_animation[3][walk_count//config.WALK_SPEED], render_position)
            elif direction == UnitMove.RIGHT:
                screen.blit(walk_animation[1][walk_count//config.WALK_SPEED], render_position)
            self.set_walk_count(walk_count + 1)

        if grid:
            self.render_hitboxes(screen, camera)

    def render_hitboxes(self, screen, camera):
        hitbox = self.get_hitbox()
        hitbox = [hitbox[0] - camera[0], hitbox[1] - camera[1], hitbox[2], hitbox[3]]
        pygame.draw.rect(screen, config.HITBOX_COLOR, hitbox, 1)

    def render_lifes(self, screen):
        lifes = self.get_lifes()
        life_sprites = self.get_life_sprites()
        i = 0
        while i < lifes//2:
            screen.blit(life_sprites[0], [(config.LIFE_POSITION[0] + config.LIFE_SCALE) * i, config.LIFE_POSITION[0]])
            i += 1

        if lifes % 2 == 1:
            screen.blit(life_sprites[1], [(config.LIFE_POSITION[0] + config.LIFE_SCALE) * i, config.LIFE_POSITION[0]])
            i += 1

        while i < config.PENGUIN_MAX_LIFE // 2:
            screen.blit(life_sprites[2], [(config.LIFE_POSITION[0] + config.LIFE_SCALE) * i, config.LIFE_POSITION[0]])
            i += 1

    def set_hitbox(self, position, hitbox_offset, hitbox_dimension):
        self.hitbox = (position[0] + hitbox_offset[0], position[1] + hitbox_offset[1],
                       hitbox_dimension[0], hitbox_dimension[1])
        self.calculate_hitbox_corners()

    def set_hitbox_corners(self, hitbox_corners):
        self.hitbox_corners = hitbox_corners

    def get_hitbox_corners(self):
        return self.hitbox_corners

    def set_life_sprites(self, life_sprites):
        self.life_srpites = life_sprites

    def get_life_sprites(self):
        return self.life_srpites
