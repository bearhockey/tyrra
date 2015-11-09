import pygame

import Color

from Box import Box


class Window(object):
    def __init__(self, position, size):
        self.position = position
        self.canvas = pygame.Surface(size=size)
        self.border = Box(pygame.Rect(position[0], position[1], size[0], size[1]), box_color=None,
                          border_color=Color.white)
        self.components = []

    def update(self, mouse, key, offset=None):
        if offset is None:
            offset=self.position
        for component in self.components:
            update = getattr(component, 'update', None)
            if callable(update):
                update(mouse, key, offset)

    def draw(self, screen):
        self.canvas.fill(Color.black)
        for component in self.components:
            component.draw(self.canvas)
        screen.blit(self.canvas, self.position)
        self.border.draw(screen)
