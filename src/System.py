import pygame
import random

from Box import Box
from Button import Button
from InputBox import InputBox
from Star import Star


class System(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.name = 'Poop'
        self.seed = 0

        self.stars = []
        self.white = (255, 255, 255)

        self.big_font_size = 24
        self.small_font_size = 16
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.big_font_size)
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), self.small_font_size)

        # main screen turn on
        self.main_window = Box(pygame.Rect(20, 50, 800, 600), (0, 0, 0), self.white)
        # input boxes
        box_width = self.font.size('12345678900')[0]
        self.x_box = InputBox(pygame.Rect(100, 660, box_width, 30), (10, 10, 10), self.white, '0', self.white,
                              self.font, 10)
        self.y_box = InputBox(pygame.Rect(400, 660, box_width, 30), (10, 10, 10), self.white, '0', self.white,
                              self.font, 10)
        # buttons
        self.generate_button = Button(pygame.Rect(650, 650, 100, 50), (20, 150, 30), self.white, 'GENERATE',
                                      self.white, self.small_font)

    def generate_stars(self):
        self.seed = -self.x * self.y
        random.seed(self.seed)
        rand = random.randrange(0, 9)
        self.stars.append(Star(radius=random.randint(1, 255),
                               luminosity=random.randint(1, 255),
                               temperature=random.randint(1, 255)))
        if rand > 6:
            self.stars.append(Star(radius=random.randint(1, 255),
                                   luminosity=random.randint(1, 255),
                                   temperature=random.randint(1, 255)))
        if rand > 9:
            self.stars.append(Star(radius=random.randint(1, 255),
                                   luminosity=random.randint(1, 255),
                                   temperature=random.randint(1, 255)))

        sorted(self.stars, key=lambda star: star.radius)

    def generate_name(self):
        self.seed = -self.x * self.y
        lookup = ['Aleph', 'Alpha', 'Antares', 'Beta', 'Bootes', 'Barum', 'Ceres', 'Charion', 'Chardibus', 'Chalupa',
                  'Delta', 'Darion', 'Doolan', 'Echo', 'Eres', 'Eribus', 'Encephalus', 'Ender', 'Foxtrot', 'Famicom',
                  'Gamma', 'Gregorio', 'Grace', 'Gaea', 'Gaia', 'Howzer', 'Hera', 'Hosio', 'Ignus', 'Io', 'Ionus',
                  'Ibus', 'Jax', 'Jovia', 'Jolo', 'Keras', 'Kodia', 'Li', 'Libra', 'Lol', 'Orphius', 'Orchid',
                  'Odyssus', 'Persephone', 'Pax', 'Qualude', 'Qi', 'Ra', 'Rez', 'Radium', 'Tia', 'Tori', 'Uso', 'Ura',
                  'Varia', 'Verit', 'Wex', 'Woolio', 'X', 'Yota', 'Yttrius', 'Zoe', 'Zee', 'Zae', 'Zeebs']
        base = len(lookup) # Base whatever.
        name = list()
        num = self.seed
        while num > 0:
            digit = num%base
            num = num//base
            name.append(lookup[digit])
        string = ""
        string += "{0} supercluster.  ".format(name.pop())
        string += "{0} group.  ".format(name.pop())
        string += "{0} system.  ".format(name.pop())
        string += "-".join(name)
        self.name = string
        # return string

    def draw(self, screen):
        self.draw_gui(screen)
        self.draw_stars(screen)

    def draw_text(self, screen, font, text, color, position):
        screen.blit(font.render(text, True, color), pygame.Rect(position[0], position[1], 200, 50))

    def draw_stars(self, screen):
        i = 100
        for star in self.stars:
            i += star.radius
            star.draw_grid(screen, (i, 200))
            i += star.radius

    def draw_gui(self, screen):
        self.main_window.draw(screen)
        # cords
        self.draw_text(screen, self.font, 'X:', self.white, (50, 650))
        self.draw_text(screen, self.font, 'Y:', self.white, (350, 650))
        self.x_box.draw(screen)
        self.y_box.draw(screen)
        self.generate_button.draw(screen)

        self.draw_text(screen, self.font, self.name, self.white, (20, 20))
        star_designations = ['Major', 'Minor', 'Augmented', 'Diminished']
        for star in self.stars:
            text_offset = self.stars.index(star) * 100
            self.draw_text(screen, self.small_font, '<NAME> {0}'.format(star_designations.pop(0)), self.white,
                           (900, 50 + text_offset))
            self.draw_text(screen, self.small_font, 'Temperature: {0}K'.format(star.get_temperature()), self.white,
                           (900, 70 + text_offset))
            self.draw_text(screen, self.small_font, 'Size: {0}'.format(star.get_size()), self.white,
                           (900, 90 + text_offset))
            self.draw_text(screen, self.small_font, 'Luminosity: {0}'.format(star.get_luminosity()), self.white,
                           (900, 110 + text_offset))

    def update(self, key, mouse):
        if mouse[1]:
            self.x_box.check_click()
            self.y_box.check_click()
            if self.generate_button.check_click():
                if len(self.x_box.message) != 0:
                    self.x = int(self.x_box.message)
                if len(self.y_box.message) != 0:
                    self.y = int(self.y_box.message)
                del self.stars[:]
                self.generate_stars()
                self.generate_name()
        if key:
            self.x_box.poll(key)
            self.y_box.poll(key)
