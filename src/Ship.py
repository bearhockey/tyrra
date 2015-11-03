import pygame

import Color

from Box import Box
from ShipNode import ShipNode


class Ship(object):
    def __init__(self, size_x=16, size_y=16):
        self.ship_window = self.main_window = Box(pygame.Rect(20, 50, 800, 600), (0, 0, 0), Color.white)

        self.cell_size = 4
        self.grid = []
        for x in range(0, size_x):
            self.grid.append([])
            for y in range(0, size_y):
                self.grid[x].append(ShipNode(x, y))

        self.mass_move(25, 55, 4)

    def mass_move(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.move(x, y, zoom)

    def update(self, key, mouse):
        if mouse[1]:
            for row in self.grid:
                for node in row:
                    node.update()

    def draw(self, screen):
        self.ship_window.draw(screen)
        for row in self.grid:
            for node in row:
                node.draw(screen)
