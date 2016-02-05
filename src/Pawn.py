import pygame
import os


class Pawn(object):
    def __init__(self):
        self.name = 'Buzz'
        self.portrait = None
        try:
            self.portrait = pygame.image.load(os.path.join('..', 'res', 'buzz.png'))
        except:
            pass

        self.health = 100
        self.ship_skills = {'pilot': 0,
                            'guns': 0,
                            'engineer': 0,
                            'medic': 0,
                            'scientist': 0}
        self.battle_skills = {'attack': 0,
                              'defense': 0,
                              'speed': 0}
