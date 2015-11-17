import pygame

import Color

from Orbit import Orbit


class Satellite(object):
    def __init__(self, sun_position=(0, 0), radius=128, orbit=128, orbit_point=360):
        self.radius = radius
        self.orbit = Orbit(position=sun_position, orbit=orbit, color=Color.gray)
        self.orbit_point = orbit_point

    def draw(self, screen):
        # pygame.draw.circle(screen, (255, 255, 255), position, self.radius / 10)
        # pygame.draw.circle(screen, (0, 0, 0), position, max(self.radius / 10, 5), 1)
        pygame.draw.circle(screen, Color.white, self.orbit.get_point(self.orbit_point), self.radius / 10)
        pygame.draw.circle(screen, Color.black, self.orbit.get_point(self.orbit_point), max(self.radius / 10, 5), 1)

