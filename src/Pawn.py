import pygame
import os


class Pawn(object):
    def __init__(self, name=None, age=None, race=None, bio=None, profile=None):
        self.name = name or 'Buzz'
        self.age = age or 30
        self.race = race or 'Human'
        self.bio = bio or 'To just short of infinity, and then we head back, because fuck man, space is hard.'
        try:
            self.portrait = profile or pygame.image.load(os.path.join('res', 'buzz.png'))
        except:
            pass

        self.health = 100
        self.ship_skills = {'pilot': 0,
                            'guns': 0,
                            'engineer': 0,
                            'medic': 0,
                            'scientist': 0}
        self.battle_skills = {'melee': 0,
                              'ranged': 0,
                              'defense': 0,
                              'speed': 0}
