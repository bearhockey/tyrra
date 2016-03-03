import os
import pygame


class Station(object):
    def __init__(self, name=None, image=None):
        self.name = name or 'Poop'
        try:
            self.image = image or pygame.image.load(os.path.join('res', 'station.png'))
        except:
            pass
