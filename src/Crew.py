class Crew(object):
    def __init__(self):
        self.name = 'Drew'
        self.portrait = None

        self.health = 100
        self.ship_skills = {'pilot': 0,
                            'guns': 0,
                            'engineer': 0,
                            'medic': 0,
                            'scientist': 0}
        self.battle_skills = {'attack': 0,
                              'defense': 0,
                              'speed': 0}
