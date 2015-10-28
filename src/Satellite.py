import pygame


class Satellite(object):
    def __init__(self, radius=128):
        self.radius = radius

    def draw(self, screen, position):
        pygame.draw.circle(screen, (255, 255, 255), position, self.radius / 10)
        pygame.draw.circle(screen, (0, 0, 0), position, max(self.radius / 10, 5), 1)
