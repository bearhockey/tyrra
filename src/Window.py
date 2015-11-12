import pygame

import Color

from Box import Box


class Window(object):
    def __init__(self, position, size, name=None):
        self.name = name
        self.position = position
        self.canvas = pygame.Surface(size=size)
        self.border = Box(pygame.Rect(position[0], position[1], size[0], size[1]), box_color=None,
                          border_color=Color.white, highlight_color=Color.white, active_color=Color.white)
        self.components = []

    def update(self, key, mouse, offset=None):
        if offset is None:
            offset = self.position
        if self.border.check_mouse_inside(mouse, offset):
            for component in self.components:
                update = getattr(component, 'update', None)
                if callable(update):
                    update(key=key, mouse=mouse, offset=offset)

    def draw(self, screen):
        self.canvas.fill(Color.black)
        for component in self.components:
            component.draw(self.canvas)
        screen.blit(self.canvas, self.position)
        self.border.draw(screen)
