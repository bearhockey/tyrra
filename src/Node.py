import pygame


class Node(object):
    def __init__(self, x=0, y=0, elevation=0):
        self.x = x
        self.y = y
        self.elevation = elevation

    def add_elevation(self, value):
        self.elevation += value
        if self.elevation > 1.0:
            self.elevation = 1.0
        elif self.elevation < 0.0:
            self.elevation = 0.0

    def is_above(self, level):
        if self.elevation > level:
            return True
        else:
            return False

    def draw(self, screen, zoom=1, filters=None):
        height = int(self.elevation * 255)
        rect = pygame.Rect(self.x * zoom + 1, self.y * zoom + 1, zoom + 1, zoom + 1)
        r = height
        g = height
        b = height
        a = 255
        if filters:
            if 'water' in filters:
                b = min(height + (255 / 2), 255)
            if 'clouds' in filters:
                a = height
        # print("Color is {0}".format((r, g, b, a)))
        pygame.draw.rect(screen, (r, g, b, a), rect)

