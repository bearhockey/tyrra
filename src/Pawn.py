import pygame
import os

import settings


class Pawn(object):
    def __init__(self, name=None, age=None, race=None, bio=None, profile=None, ship_skills=None, battle_skills=None):
        self.name = name or 'Buzz'
        self.age = age or 30
        self.race = race or 'Human'
        self.bio = bio or 'To just short of infinity, and then we head back, because fuck man, space is hard.'
        # portrait is 250x250
        try:
            print 'Getting portrait {0}'.format(os.path.join(settings.main_path, 'res', 'face', 'buzz.png'))
            self.portrait = profile or pygame.image.load(os.path.join(settings.main_path, 'res', 'face', 'buzz.png'))
        except Exception as e:
            print 'oh no: {0}'.format(e)

        self.health = 100
        self.ship_skills = ship_skills or {'Pilot': 0,
                                           'Guns': 0,
                                           'Engineer': 0,
                                           'Medic': 0,
                                           'Scientist': 0}
        self.battle_skills = battle_skills or {'Melee': 1,
                                               'Ranged': 1,
                                               'Defense': 1,
                                               'Intelligence': 1,
                                               'Speed': 1}
