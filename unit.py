from unit_move import UnitMove


class Unit:
    def __init__(self, x, y):
        self.position = [x, y]
        self.is_still = True
        self.hitbox = []
        self.velocity = 0
        self.lifes = 0
        self.damage = 0
        self.direction = UnitMove.LEFT
        self.walk_count = 0
        self.walk_animation = []
        self.attack_animation = []
        self.death_animation = []
        self.hit_animation = []

    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def get_position(self):
        return self.position

    def get_hitbox(self):
        return self.hitbox

    def set_hitbox(self, position, hitbox_offset, hitbox_dimension):
        self.hitbox = [position[0] + hitbox_offset[0], position[1] + hitbox_offset[1],
                       hitbox_dimension[0], hitbox_dimension[1]]

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_is_still(self):
        return self.is_still

    def set_is_still(self, is_still):
        self.is_still = is_still

    def set_walk_count(self, walk_count):
        self.walk_count = walk_count

    def get_walk_count(self):
        return self.walk_count

    def set_velocity(self, velocity):
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity

    def set_lifes(self, lifes):
        self.lifes = lifes

    def get_lifes(self):
        return self.lifes

    def set_damage(self, damage):
        self.damage = damage

    def get_damage(self):
        return self.damage

    def set_death_animation(self, death_animation):
        self.death_animation = death_animation

    def get_death_animation(self):
        return self.death_animation

    def set_walk_animation(self, walk_animation):
        self.walk_animation = walk_animation

    def get_walk_animation(self):
        return self.walk_animation

    def set_attack_animation(self, attack_animation):
        self.attack_animation = attack_animation

    def get_attack_animation(self):
        return self.attack_animation

    def set_hit_animation(self, hit_animation):
        self.hit_animation = hit_animation

    def get_hit_animation(self):
        return self.hit_animation
