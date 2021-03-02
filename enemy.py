import pygame
import config
import math
from unit import Unit
from unit_move import UnitMove


class Enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start_position = [x, y]
        self.time_till_damage = 0
        self.look = []              # [center_x, center_y, radius]
        self.score = 0

    def move_to_position(self, move_to_position):
        position = self.get_position()

        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = move_to_position[0] - position[0], move_to_position[1] - position[1]
        dist = math.hypot(dx, dy)

        if dx < 0:
            self.set_direction(UnitMove.LEFT)
        else:
            self.set_direction(UnitMove.RIGHT)

        if dist > 1:
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            position[0] += dx * config.BAT_VELOCITY
            position[1] += dy * config.BAT_VELOCITY
            self.set_position(position[0], position[1])

    def contains_look(self, player):
        player_corners = player.get_hitbox_corners()
        enemy_look = self.get_look()
        player_center = [player_corners[0][0] + (player_corners[1][0] - player_corners[0][0])/2,
                         player_corners[0][1] + (player_corners[3][1] - player_corners[0][1])/2]
        dx = enemy_look[0] - player_center[0]
        dy = enemy_look[1] - player_center[1]
        if dx * dx + dy * dy <= enemy_look[2] * enemy_look[2]:
            return True
        return False

    def contains(self, player):
        player_hitbox = player.get_hitbox()
        enemy_hitbox = self.get_hitbox()
        time_till_damage = self.get_time_till_damage()
        if time_till_damage == 0:
            # Check player up left corner is in enemy hitbox
            if enemy_hitbox[0] <= player_hitbox[0] <= enemy_hitbox[0] + enemy_hitbox[2]:
                if enemy_hitbox[1] <= player_hitbox[1] <= enemy_hitbox[1] + enemy_hitbox[3]:
                    self.set_time_till_damage(time_till_damage + 1)
                    return True

            # Check player up right corner is in enemy hitbox
            if enemy_hitbox[0] <= player_hitbox[0] <= enemy_hitbox[0] + enemy_hitbox[2]:
                if enemy_hitbox[1] <= player_hitbox[1] + player_hitbox[3] <= enemy_hitbox[1] + enemy_hitbox[3]:
                    self.set_time_till_damage(time_till_damage + 1)
                    return True

            # Check player down right corner is in enemy hitbox
            if enemy_hitbox[0] <= player_hitbox[0] + player_hitbox[2] <= enemy_hitbox[0] + enemy_hitbox[2]:
                if enemy_hitbox[1] <= player_hitbox[1] + player_hitbox[3] <= enemy_hitbox[1] + enemy_hitbox[3]:
                    self.set_time_till_damage(time_till_damage + 1)
                    return True

            # Check player down left corner is in enemy hitbox
            if enemy_hitbox[0] <= player_hitbox[0] + player_hitbox[2] <= enemy_hitbox[0] + enemy_hitbox[2]:
                if enemy_hitbox[1] <= player_hitbox[1] <= enemy_hitbox[1] + enemy_hitbox[3]:
                    self.set_time_till_damage(time_till_damage + 1)
                    return True
        else:
            time_till_damage += 1
            if time_till_damage < config.TIME_TILL_DAMAGE:
                self.set_time_till_damage(time_till_damage + 1)
            else:
                self.set_time_till_damage(0)

        return False

    def render_look(self, screen, camera):
        look = self.get_look()
        pygame.draw.circle(screen, (0, 0, 255), [look[0] - camera[0], look[1] - camera[1]], look[2], 1)

    def set_look(self, hitbox):
        self.look = [hitbox[0] + hitbox[2] / 2, hitbox[1] + hitbox[3] / 2, config.RADIUS]

    def get_look(self):
        return self.look

    def get_start_position(self):
        return self.start_position

    def set_time_till_damage(self, time_till_damage):
        self.time_till_damage = time_till_damage

    def get_time_till_damage(self):
        return self.time_till_damage

    def move_directrion(self, dx, dy):
        pass

    def get_score(self):
        return self.score
