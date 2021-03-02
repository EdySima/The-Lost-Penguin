import pygame
import config
from enemy import Enemy
from unit_move import UnitMove


class Bat(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.load_walk_sprites()
        self.damage = config.BAT_DAMAGE
        self.render_animation = self.get_walk_animation()
        self.set_hitbox(self.position, config.BAT_HITBOX_OFFSET, config.BAT_HITBOX)
        self.set_look(self.get_hitbox())
        self.score = config.BAT_SCORE
        self.hit_sound = None
        self.load_sound_effect()

    def load_sound_effect(self):
        self.hit_sound = pygame.mixer.Sound('resources/sound_effect/bat.wav')

    def play_hit_sound(self, volume):
        self.hit_sound.set_volume(volume)
        self.hit_sound.play()

    def load_walk_sprites(self):
        right = []
        left = []
        walk_animation = []
        for i in range(5):
            left.append(pygame.transform.scale(pygame.image.load('resources/units/bat/B_W_L{}.png'.format(i)),
                                               (config.BAT_SCALE, config.BAT_SCALE)))
            right.append(pygame.transform.scale(pygame.image.load('resources/units/bat/B_W_R{}.png'.format(i)),
                                                (config.BAT_SCALE, config.BAT_SCALE)))
        walk_animation.extend([left, right])
        self.set_walk_animation(walk_animation)

    def load_attack_sprites(self):
        right = []
        left = []
        attack_animation = []
        for i in range(5):
            left.append(pygame.transform.scale(pygame.image.load('resources/units/bat/B_A_L{}.png'.format(i)),
                                               (config.BAT_SCALE, config.BAT_SCALE)))
            right.append(pygame.transform.scale(pygame.image.load('resources/units/bat/B_A_R{}.png'.format(i)),
                                                (config.BAT_SCALE, config.BAT_SCALE)))
        attack_animation.extend([left, right])
        self.set_attack_animation(attack_animation)

    def set_look(self, hitbox):
        self.look = [hitbox[0] + hitbox[2] / 2, hitbox[1] + hitbox[3] / 2, config.BAT_RADIUS]

    def render(self, screen, camera, grid):
        walk_count = self.get_walk_count()
        position = self.get_position()
        direction = self.get_direction()
        render_animation = self.get_walk_animation()

        if walk_count >= config.ENEMY_WALK_COUNT_MAX:
            walk_count = 0
        render_position = [position[0] - camera[0], position[1] - camera[1]]

        if direction == UnitMove.LEFT:
            screen.blit(render_animation[0][walk_count // config.ENEMY_WALK_SPEED], render_position)
        if direction == UnitMove.RIGHT:
            screen.blit(render_animation[1][walk_count // config.ENEMY_WALK_SPEED], render_position)
        self.set_walk_count(walk_count + 1)
        self.set_look(self.get_hitbox())
        hitbox = self.get_hitbox()
        hitbox = [hitbox[0] - camera[0], hitbox[1] - camera[1], hitbox[2], hitbox[3]]
        self.set_hitbox(position, config.BAT_HITBOX_OFFSET, config.BAT_HITBOX)

        if grid:
            self.render_look(screen, camera)
            pygame.draw.rect(screen, config.HITBOX_COLOR, hitbox, 1)

    def set_render_animation(self, render_animation):
        self.render_animation = render_animation

    def get_render_animation(self):
        return self.render_animation
