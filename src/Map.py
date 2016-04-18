import pygame
import random

from Elevation import Elevation
from Node import Node


class Map(object):
    def __init__(self, width=20, height=10, rando=False, seed=None, zoom=1, temperature=0):
        random.seed(seed)
        # map data
        self.width = width
        self.height = height
        self.zoom = zoom

        self.map = []
        self.clouds = []
        for x in range(0, width):
            self.map.append([])
            self.clouds.append([])
            for y in range(0, height):
                self.map[x].append(Node(x=x, y=y))
                self.clouds[x].append(Node(x=x, y=y))

        self.sea_level = 0.5
        self.canvas = None

        # some weird generation constants for now
        self.gen_depth = 0.02
        self.render_limit = 0.01

        self.x_offset = 0
        self.y_offset = 0

        Elevation.rando_card(self.map, scale=100.0, octaves=4, seed=random.randint(-65536, 65536))
        Elevation.land_ceiling(self.map, 0.7)

        Elevation.rando_card(self.clouds, scale=200.0, octaves=2, seed=random.randint(-65536, 65536))

        # map layers
        self.drawing_layers = {
            'water': True,
            'ice': True,
            'biome': True,
            'clouds': False,
            'coast': False,
            'temperature': False,
            'rainfall': False
        }

        if temperature > 373:
            self.drawing_layers['water'] = False
            self.drawing_layers['ice'] = False
        if temperature < 273:
            self.drawing_layers['water'] = False

        if self.drawing_layers['water']:
            Elevation.amplify(self.map, base=0.0, ceiling=self.sea_level, factor=2.0, direction='negative')

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
        if self.drawing_layers['clouds']:
            for row in self.clouds:
                for node in row:
                    node.draw(self.canvas, zoom=zoom_level, filters=['clouds'])

    def draw(self, screen):
        if self.canvas:
            screen.blit(self.canvas, (self.x_offset, self.y_offset))

    def draw_at_offset(self, screen, x_offset, y_offset):
        if self.canvas:
            screen.blit(self.canvas, (x_offset, y_offset))
