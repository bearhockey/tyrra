import pygame
import random

import Color

from Map import Map
from Orbit import Orbit


class Planet(object):
    def __init__(self, index=0, seed=0, sun_position=(0, 0), radius=128, orbit=128, orbit_point=360, name='NULL'):
        random.seed(seed)
        self.radius = radius
        self.orbit = Orbit(position=sun_position, orbit=orbit, color=Color.gray)
        self.orbit_point = orbit_point
        self.name = name
        self.radius_mod = 10
        self.planet_index = index
        self.planet_seed = int(str(seed)+str(index))

        self.station = None

        # some stats
        # larger the planet, the more likely the atmosphere is thick
        self.atmosphere_density = round(self.radius / 255.0 * random.uniform(0.7, 1.0), 4)
        atmopshere_mod = self.atmosphere_density-0.5
        self.temperature = 1000-orbit
        self.temperature += int(self.temperature * atmopshere_mod)

        self.map = Map(width=300, height=200, rando=False, seed=self.planet_seed, zoom=2)

    def draw(self, screen):
        # pygame.draw.circle(screen, (255, 255, 255), position, self.radius / 10)
        # pygame.draw.circle(screen, (0, 0, 0), position, max(self.radius / 10, 5), 1)
        pygame.draw.circle(screen, Color.gray, self.orbit.get_point(self.orbit_point), self.radius / self.radius_mod)
        pygame.draw.circle(screen, Color.black, self.orbit.get_point(self.orbit_point),
                           max(self.radius / self.radius_mod, 5), 1)
