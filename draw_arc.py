import pygame
from math import atan2, pi

class Arc:

    def __init__(self, color, center, radius, start_angle, stop_angle, width=1):
        self.color = color
        self.x = center[0]
        self.y = center[1]
        self.rect = [self.x - 3*radius/4, self.y - radius, 3*radius/2,  radius*2]
        self.radius = radius
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.width = width

    def draw(self, canvas):
        pygame.draw.arc(canvas, self.color, self.rect, self.start_angle, self.stop_angle, self.width)
        pygame.draw.line(canvas, self.color, [self.x, self.y], [self.x, self.y - self.radius])
        pygame.draw.line(canvas, self.color, [self.x, self.y], [self.x, self.y + self.radius])

    def contains(self, x, y, canvas):

        dx = x - self.x
        dy = y - self.y
        print("dx,dy ", dx, dy)
        print("x,y ", x, y)
        print("self.x, self.y ", self.x, self.y)
        pygame.draw.line(canvas, (0, 0, 0), [self.x, self.y], [x, y])
        greater_than_outside_radius = dx*dx + dy*dy >= self.radius * self.radius

        less_than_inside_radius = dx*dx + dy*dy <= (self.radius - self.width) * (self.radius - self.width)

        if greater_than_outside_radius or less_than_inside_radius:
            return False

        rads = atan2(-dy, dx)
        print("rads ", rads)
        if rads < 0:
            rads = 2 * pi + rads

        return self.start_angle <= rads <= self.stop_angle
