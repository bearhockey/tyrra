import pygame
import random

from Elevation import Elevation
from Node import Node


class Map(object):
    def __init__(self, width=20, height=10, rando=False, seed=None, zoom=1):
        random.seed(seed)
        # map data
        self.width = width
        self.height = height
        self.zoom = zoom

        self.map = []
        for x in range(0, width):
            self.map.append([])
            for y in range(0, height):
                self.map[x].append(Node(x=x, y=y))

        self.sea_level = 0.5
        self.canvas = None

        # some weird generation constants for now
        self.gen_depth = 0.02
        self.render_limit = 0.01

        self.x_offset = 0
        self.y_offset = 0

        Elevation.rando_card(self.map, octaves=16, seed=random.randint(-65536, 65536))
        Elevation.land_ceiling(self.map, 0.6)
        Elevation.amplify(self.map, self.sea_level, 0.5)

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
                filters = []
                if self.drawing_layers['water']:
                    if not node.is_above(self.sea_level):
                        filters.append('water')
                node.draw(self.canvas, zoom=zoom_level, filters=filters)

    def draw(self, screen):
        if self.canvas:
            screen.blit(self.canvas, (self.x_offset, self.y_offset))
