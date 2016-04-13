from math import pow, sqrt, tan, pi
import pygame


class Ellipse(object):
    def __init__(self, position=(0, 0), x_radius=1, y_radius=1):
        self.position = position
        self.x_radius = x_radius
        self.y_radius = y_radius

    def get_point(self, angle):
        if angle == 0:
            angle = 360
        rad = angle*(pi/180)
        try:
            x = (self.x_radius * self.y_radius) / sqrt(pow(self.y_radius, 2) + pow(self.x_radius, 2)*(pow(tan(rad), 2)))
        except Exception as e:
            # print e
            x = 0
        try:
            y = (self.x_radius * self.y_radius) / sqrt(pow(self.x_radius, 2) + pow(self.y_radius, 2)/pow(tan(rad), 2))
        except Exception as e:
            # print e
            y = 0

        if 90 < angle < 270:
            x = -x
        if 180 < angle < 360:
            y = -y
        return int(x)+self.position[0], int(y)+self.position[1]

    def draw(self, screen, color=None, outline=2):
        box = pygame.Rect(self.position[0] - self.x_radius, self.position[1] - self.y_radius,
                          self.x_radius * 2, self.y_radius * 2)
        if color is None:
            color = (0, 0, 0)
        pygame.draw.ellipse(screen, color, box, outline)
