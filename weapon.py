import pygame
import config
from unit_move import UnitMove


class Weapon:
    def __init__(self, player):
        positon = player.get_position()
        self.position = [positon[0] + config.WEAPON_OFFSET_LEFT[0], positon[1] + config.WEAPON_OFFSET_LEFT[1]]
        self.hitbox = []
        self.hitbox_corners = []
        self.set_hitbox(self.position, [0, 0], config.WEAPON_SCALE)
        self.damage = 2
        self.direction = UnitMove.LEFT
        self.sprite = None
        self.set_sprite('sword')
        self.start_angle = 30
        self.angle = self.start_angle
        self.origin = []
        self.rend_origin = []
        self.swing_sound = []
        self.load_sound_effect()
        self.count_swing = 0

    def load_sound_effect(self):
        for i in range(3):
            self.swing_sound.append(pygame.mixer.Sound('resources/sound_effect/sword' + str(i) + '.wav'))

    def play_swing(self, volume):
        self.swing_sound[self.count_swing].set_volume(volume)
        self.swing_sound[self.count_swing].play()
        self.count_swing += 1
        if self.count_swing == 3:
            self.count_swing = 0

    def rotate(self, render_position, angle):

        pivot = pygame.math.Vector2(config.WEAPON_SCALE[0] / 2, -config.WEAPON_SCALE[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        box = [pygame.math.Vector2(p) for p in [(0, 0), (config.WEAPON_SCALE[0], 0),
                                                (config.WEAPON_SCALE[0], -config.WEAPON_SCALE[1]),
                                                (0, -config.WEAPON_SCALE[1])]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        rend_origin = (render_position[0] + min_box[0] - pivot_move[0], render_position[1] - max_box[1] + pivot_move[1])
        origin = (self.position[0] + min_box[0] - pivot_move[0], self.position[1] - max_box[1] + pivot_move[1])
        self.rend_origin = rend_origin
        self.origin = origin
        rotated_image = pygame.transform.rotate(self.sprite, angle)
        image_box = rotated_image.get_rect()
        self.hitbox = [origin[0], origin[1], image_box[2], image_box[3]]
        return rotated_image

    def render(self, screen, camera, grid, is_attacking):
        position = self.get_position()
        render_position = [position[0] - camera[0], position[1] - camera[1]]
        if is_attacking:
            angle = self.angle
            rotated_image = self.rotate(render_position, angle)
            screen.blit(rotated_image, self.rend_origin)
            if self.direction == UnitMove.LEFT or self.direction == UnitMove.DOWN:
                if self.angle < self.start_angle + config.MAX_SWING:
                    self.angle = angle + config.SPEED_ATTACK
                else:
                    self.angle = self.start_angle
            if self.direction == UnitMove.RIGHT or self.direction == UnitMove.UP:
                if self.angle > self.start_angle - config.MAX_SWING:
                    self.angle = angle - config.SPEED_ATTACK
                else:
                    self.angle = self.start_angle
            if grid:
                hitbox = self.hitbox
                hitbox = [hitbox[0] - camera[0], hitbox[1] - camera[1], hitbox[2], hitbox[3]]
                pygame.draw.rect(screen, config.HITBOX_COLOR, hitbox, 1)
        else:
            self.angle = self.start_angle
            self.rotate(render_position, self.start_angle)

    def set_weapon(self, direction, position):
        if direction != UnitMove.NONE:
            self.direction = direction
            if direction == UnitMove.RIGHT:
                self.position[0] = position[0] + config.WEAPON_OFFSET_RIGHT[0]
                self.position[1] = position[1] + config.WEAPON_OFFSET_RIGHT[1]
                self.start_angle = config.START_ANGLE_RIGHT
            if direction == UnitMove.LEFT:
                self.position[0] = position[0] + config.WEAPON_OFFSET_LEFT[0]
                self.position[1] = position[1] + config.WEAPON_OFFSET_LEFT[1]
                self.start_angle = config.START_ANGLE_LEFT
            if direction == UnitMove.UP:
                self.position[0] = position[0] + config.WEAPON_OFFSET_UP[0]
                self.position[1] = position[1] + config.WEAPON_OFFSET_UP[1]
                self.start_angle = config.START_ANGLE_UP
            if direction == UnitMove.DOWN:
                self.position[0] = position[0] + config.WEAPON_OFFSET_DOWN[0]
                self.position[1] = position[1] + config.WEAPON_OFFSET_DOWN[1]
                self.start_angle = config.START_ANGLE_DOWN

    def get_position(self):
        return self.position

    def get_hitbox(self):
        return self.hitbox

    def set_hitbox(self, position, hitbox_offset, hitbox_dimension):
        self.hitbox = pygame.Rect(position[0] + hitbox_offset[0], position[1] + hitbox_offset[1],
                                  hitbox_dimension[0], hitbox_dimension[1])

    def set_hitbox_corners(self, up_left, up_right, down_right, down_left):
        self.hitbox_corners = [up_left, up_right, down_right, down_left]

    def get_hitbox_corners(self):
        return self.hitbox_corners

    def set_damage(self, damage):
        self.damage = damage

    def get_damage(self):
        return self.damage

    def set_sprite(self, file_name):
        self.sprite = pygame.transform.scale(pygame.image.load('resources/weapons/' + file_name + '.png'),
                                             config.WEAPON_SCALE)

    def get_sprite(self):
        return self.sprite
