import pygame

import src.const.Color as Color
from src.components.Box import Box


class Window(object):
    def __init__(self, position, size, name=None, border_color=Color.WHITE):
        self.name = name
        self.position = position
        self.canvas = pygame.Surface(size=size)
        self.border = Box(pygame.Rect(position[0], position[1], size[0], size[1]), box_color=None,
                          border_color=border_color, highlight_color=border_color, active_color=border_color)
        self.components = []
        self.sprites = []

    def always(self):
        elements = self.components + self.sprites
        for element in elements:
            always = getattr(element, 'always', None)
            if callable(always):
                element.always()

    def update(self, key, mouse, offset=None):
        if offset is None:
            offset = self.position
            # offset = (0, 0)
        if self.border.check_mouse_inside(mouse, (0, 0)):
            # print 'mouse inside {0}'.format(self.name)
            for component in self.components:
                update = getattr(component, 'update', None)
                if callable(update):
                    # print 'Update on {0}'.format(component)
                    component.update(key=key, mouse=mouse, offset=offset)

    def draw(self, screen):
        self.canvas.fill(Color.BLACK)
        for component in self.components:
            component.draw(self.canvas)
        for sprite in self.sprites:
            sprite.draw(self.canvas)
        screen.blit(self.canvas, self.position)
        self.border.draw(screen)
