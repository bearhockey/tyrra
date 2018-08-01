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
        self.portrait_path = profile or os.path.join(settings.main_path, 'res', 'face', 'buzz.png')
        try:
            self.portrait = pygame.image.load(self.portrait_path)
        except Exception as e:
            print('oh no: {0}'.format(e))
            self.portrait = None

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

    def get_data(self):
        return {"NAME": self.name,
                "AGE": self.age,
                "RACE": self.race,
                "BIO": self.bio,
                "PICTURE": self.portrait_path,
                "HEALTH": self.health,
                "SKILLS": self.ship_skills,
                "STATS": self.battle_skills}
