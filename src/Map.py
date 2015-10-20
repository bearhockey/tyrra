import pygame
import random

from Elevation import Elevation
from Node import Node


class Map(object):
    def __init__(self, width=20, height=10, rando=False, seed=None):
        random.seed(seed)
        # map data
        self.map = []
        for x in range(0, width):
            self.map.append([])
            for y in range(0, height):
                self.map[x].append(Node(x=x, y=y))

        self.sea_level = 0.1
        self.canvas = None

        # try out this
        x = random.randrange(1, width)
        y = random.randrange(1, height)
        print '{0}, {1} out of {2}, {3}'.format(x, y, width, height)
        Elevation.flat_land(self.map, self.sea_level)
        Elevation.build_land(self.map, x, y, 0.8, 0, 0.000001, 0.000001)

        # map layers
        self.drawing_layers = {
            'water': True,
            'ice': True,
            'biome': True,
            'coast': False,
            'temperature': False,
            'rainfall': False
        }

        self.create_map(width, height, zoom_level=2)

    def create_map(self, width, height, zoom_level=1):
        self.canvas = pygame.Surface(size=(width * zoom_level, height * zoom_level))
        for row in self.map:
            for node in row:
                node.draw(self.canvas, zoom=zoom_level)

    def draw(self, screen):
        if self.canvas:
            screen.blit(self.canvas, (0, 0))
