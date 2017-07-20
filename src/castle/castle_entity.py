import pygame


class CastleEntity(object):
    def __init__(self, image=None):
        self.image = image
        if image is None:
            self.image = pygame.Surface((50, 50))
            self.image.fill((128, 128, 128), pygame.Rect(10, 10, 30, 30))
