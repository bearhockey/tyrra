import pygame
import random

from Elevation import Elevation
from Node import Node


class Map(object):
    def __init__(self, width=20, height=10, rando=False, seed=None):
        random.seed(seed)
        # map data
        self.width = width
        self.height = height
        self.zoom = 1

        self.map = []
        for x in range(0, width):
            self.map.append([])
            for y in range(0, height):
                self.map[x].append(Node(x=x, y=y))

        self.sea_level = 0.5
        self.canvas = None

        self.x_offset = 0
        self.y_offset = 0

        Elevation.flat_land(self.map, self.sea_level)
        # build 3 things
        for _ in range(0, 3):
            x = random.randrange(1, width)
            y = random.randrange(1, height)
            print '{0}, {1} out of {2}, {3}'.format(x, y, width, height)
            Elevation.build_land(self.map, x, y, 0.5, 0.4, 0.004, 0.002)
        x = random.randrange(1, width)
        y = random.randrange(1, height)
        # Elevation.build_land(self.map, x, y, -0.1, 0, 0.004, 0.002)
        Elevation.land_ceiling(self.map, 0.65)

        # map layers
        self.drawing_layers = {
            'water': True,
            'ice': True,
            'biome': True,
            'coast': False,
            'temperature': False,
            'rainfall': False
        }

        self.create_map(zoom_level=self.zoom)

    def create_map(self, zoom_level=1):
        self.canvas = pygame.Surface(size=(self.width * zoom_level, self.height * zoom_level))
        for row in self.map:
            for node in row:
                node.draw(self.canvas, zoom=zoom_level)

    def draw(self, screen):
        if self.canvas:
            screen.blit(self.canvas, (self.x_offset, self.y_offset))
