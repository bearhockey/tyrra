import pygame

import Color

from Box import Box
from ShipNode import ShipNode


class Ship(object):
    def __init__(self, size_x=16, size_y=16):
        self.ship_window = self.main_window = Box(pygame.Rect(20, 50, 800, 600), (0, 0, 0), Color.white)

        self.name = 'Tyrra'

        self.big_font_size = 24
        self.small_font_size = 16
        self.font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)

        self.cell_size = 4
        self.grid = []
        for x in range(0, size_x):
            self.grid.append([])
            for y in range(0, size_y):
                self.grid[x].append(ShipNode(x, y))

        self.mass_set(25, 55, 4)

    def mass_move(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.move(x, y, zoom)

    def mass_set(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.set(x, y, zoom)

    def update(self, key, mouse):
        if key:
            if key == pygame.K_LEFT:
                self.mass_move(-8, 0)
            elif key == pygame.K_RIGHT:
                self.mass_move(8, 0)
            if key == pygame.K_UP:
                self.mass_move(0, -8)
            elif key == pygame.K_DOWN:
                self.mass_move(0, 8)
        if mouse:
            for row in self.grid:
                for node in row:
                    if node.update(mouse):
                        break

    def draw(self, screen):
        self.ship_window.draw(screen)
        for row in self.grid:
            for node in row:
                node.draw(screen)
