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

        self.sea_level = 0.5

        # try out this
        Elevation.build_land(self.map, 10, 10, 0.1, 0.02, 0.02)

        # map layers
        self.drawing_layers = {
            'water': True,
            'ice': True,
            'biome': True,
            'coast': False,
            'temperature': False,
            'rainfall': False
            }

    def draw(self, screen, zoom=1):
        for row in self.map:
            for node in row:
                node.draw(screen, zoom=zoom)
