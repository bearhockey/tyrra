import pygame

import Color
from src.components.Box import Box

node_type = {
    "CLEAR": 0,
    "OBJECT": 1,
    }


class BattleNode(Box):
    def __init__(self, x, y, cell_size=8):
        self.cell_x = x
        self.cell_y = y
        self.offset = (0, 0)
        self.cell_size = cell_size
        self.zoom = 1
        Box.__init__(self, pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                     (0, 0, 0), (100, 100, 100))
        self.border = 1

        self.node_type = 0

    def set(self, x, y, zoom=None):
        self.offset = (x, y)
        if zoom:
            self.zoom = zoom

    def move(self, x, y, zoom=None):
        self.set(x + self.offset[0], y + self.offset[1], zoom)

    def update(self, key, mouse, offset=(0, 0)):
        if self.check_click(mouse, offset=offset):
            return True
        else:
            return False

    def draw(self, screen):
        self.box_color = Color.black
        zoomed_size = self.cell_size * self.zoom
        self.rect.x = self.cell_x * zoomed_size + self.offset[0]
        self.rect.y = self.cell_y * zoomed_size + self.offset[1]
        self.rect.width = zoomed_size
        self.rect.height = zoomed_size
        Box.draw(self, screen)
