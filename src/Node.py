import pygame


class Node(object):
    def __init__(self, x=0, y=0, elevation=0):
        self.x = x
        self.y = y
        self.elevation = elevation

    def draw(self, screen, zoom=1):
        height = self.elevation*255
        rect = pygame.Rect(self.x * zoom, self.y * zoom, zoom, zoom)
        pygame.draw.rect(screen, (height, height, height), rect)
