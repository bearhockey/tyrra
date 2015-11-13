import pygame
import random

import Color
import Maths
import Text

from InputBox import InputBox
from Satellite import Satellite
from Star import Star
from TextBox import TextBox


class System(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.name = 'Poop'
        self.short_name = 'Jerk'
        self.seed = 0

        self.stars = []
        self.planets = []

        self.star_orbit = 0

        self.big_font_size = 24
        self.small_font_size = 16
        self.font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), self.small_font_size)

        self.main_window = pygame.Rect(0, 0, 800, 600)

        # buttons
        self.generate_button = TextBox(pygame.Rect(650, 650, 100, 50), (20, 150, 30), Color.white,
                                       highlight_color=Color.white, active_color=Color.white, message=u'\u304D',
                                       text_color=Color.white, font=self.font)

        self.system_map = SystemMap(stars=self.stars, planets=self.planets, star_orbit=self.star_orbit,
                                    window_width=self.main_window.width, window_height=self.main_window.height)

    def generate(self):
        self.generate_seed()
        self.generate_name()
        self.generate_stars()
        self.generate_planets()

    def generate_planets(self):
        random.seed(self.seed)
        planet_num = 100
        while planet_num > 0:
            planet_num -= random.randrange(10, 100)
            self.planets.append(Satellite(radius=random.randint(1, 255)))

    def generate_seed(self):
        self.seed = float(0.5) * float(self.x + self.y) * float(self.x + self.y + 1) + self.y
        self.seed = int(self.seed)
        print 'Seed: {0}'.format(self.seed)

    def generate_stars(self):
        random.seed(self.seed)
        rand = random.randrange(0, 9)
        position = self.main_window.center
        radius = random.randint(1, 255)
        # star.draw_grid(screen, (center[0] + i, center[1] - center[1] / 3 + i))
        # i += star.radius / 4
        self.stars.append(Star(position=position,
                               radius=radius,
                               luminosity=random.randint(1, 255),
                               temperature=random.randint(1, 255)))
        if rand > 6:
            self.star_orbit += radius/2
            position = (position[0]+radius/2, position[1]+radius/2)
            radius = random.randint(1, 255)
            self.stars.append(Star(position=position,
                                   radius=radius,
                                   luminosity=random.randint(1, 255),
                                   temperature=random.randint(1, 255)))
            self.star_orbit += radius/2
        if rand > 9:
            self.stars.append(Star(radius=random.randint(1, 255),
                                   luminosity=random.randint(1, 255),
                                   temperature=random.randint(1, 255)))

        sorted(self.stars, key=lambda star: star.radius, reverse=True)
        star_designations = ['Major', 'Minor', 'Augmented', 'Diminished']
        for sun in self.stars:
            sun.name = '{0} {1}'.format(self.short_name, star_designations.pop(0))
        self.system_map.star_orbit = self.star_orbit

    def generate_name(self):
        lookup = ['Aleph', 'Alpha', 'Antares', 'Beta', 'Bootes', 'Barum', 'Ceres', 'Charion', 'Chardibus', 'Chalupa',
                  'Delta', 'Darion', 'Doolan', 'Echo', 'Eres', 'Eribus', 'Encephalus', 'Ender', 'Foxtrot', 'Famicom',
                  'Gamma', 'Gregorio', 'Grace', 'Gaea', 'Gaia', 'Howzer', 'Hera', 'Hosio', 'Ignus', 'Io', 'Ionus',
                  'Ibus', 'Jax', 'Jova', 'Jolo', 'Keras', 'Kodia', 'Li', 'Libra', 'Lol', 'Orphius', 'Orchid',
                  'Odyssus', 'Persephone', 'Pax', 'Qualude', 'Qi', 'Ra', 'Rez', 'Radium', 'Tia', 'Tori', 'Uso', 'Ura',
                  'Varia', 'Verit', 'Wex', 'Woolio', 'X', 'Yota', 'Yttrius', 'Zoe', 'Zee', 'Zae', 'Zeebs']
        base = len(lookup)  # Base whatever.
        name = []
        num = self.seed + pow(2, 16)
        while num > 0:
            digit = num%base
            num = num//base
            name.append(lookup[digit])

        string = u""
        string += u"{0} supercluster.  ".format(name.pop())
        string += u"{0} group.  ".format(name.pop())
        string += u"{0} system.  ".format(name.pop())
        self.short_name = u"-".join(name)
        string += self.short_name
        self.name = string

    def draw(self, screen):
        self.draw_gui(screen)

    def draw_gui(self, screen):
        self.main_window.draw(screen)
        # cords
        Text.draw_text(screen, self.font, 'X:', Color.white, (50, 650))
        Text.draw_text(screen, self.font, 'Y:', Color.white, (350, 650))

        self.generate_button.draw(screen)

        Text.draw_text(screen, self.font, self.name, Color.white, (20, 20))
        text_offset = 0
        for star in self.stars:
            text_offset = self.stars.index(star) * 100
            Text.draw_text(screen, self.small_font, '{0}'.format(star.name), Color.white, (900, 50 + text_offset))
            Text.draw_text(screen, self.small_font, 'Temperature: {0}K'.format(star.get_temperature()), Color.white,
                           (900, 70 + text_offset))
            Text.draw_text(screen, self.small_font, 'Size: {0}'.format(star.get_size()), Color.white,
                           (900, 90 + text_offset))
            Text.draw_text(screen, self.small_font, 'Luminosity: {0}'.format(star.get_luminosity()), Color.white,
                           (900, 110 + text_offset))
        for planet in self.planets:
            Text.draw_text(screen, self.small_font, 'Planets: {0}'.format(len(self.planets)), Color.white,
                           (900, 350 + text_offset))

    def update(self, key, mouse, offset=(0, 0)):
        if mouse[1]:
            self.x_box.check_click()
            self.y_box.check_click()
            if self.generate_button.check_click():
                if len(self.x_box.message) != 0:
                    self.x = int(self.x_box.message)
                if len(self.y_box.message) != 0:
                    self.y = int(self.y_box.message)
                del self.stars[:]
                del self.planets[:]
                self.generate()
        if key:
            self.x_box.poll(key)
            self.y_box.poll(key)


class SystemMap(object):
    def __init__(self, stars, planets, star_orbit, window_width=200, window_height=100):
        self.main_window = pygame.Rect(0, 0, window_width, window_height)
        self.big_font_size = 24
        self.small_font_size = 16
        self.font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), self.small_font_size)

        self.stars = stars
        self.planets = planets
        self.star_orbit = star_orbit

        box_width = self.font.size('12345678900')[0]
        self.x_box = InputBox(pygame.Rect(800-box_width*2, 570, box_width, 30), (10, 10, 10), Color.white,
                              highlight_color=Color.white, active_color=Color.white, message='0',
                              text_color=Color.white, font=self.font, text_limit=10, allowed_characters=range(48, 57))
        self.y_box = InputBox(pygame.Rect(800-box_width, 570, box_width, 30), (10, 10, 10), Color.white,
                              highlight_color=Color.white, active_color=Color.white, message='0',
                              text_color=Color.white, font=self.font, text_limit=10, allowed_characters=range(48, 57))

        self.mouse_box = TextBox(pygame.Rect(0, 0, 200, 30), box_color=None,border_color=None, highlight_color=None,
                                 active_color=None, message='Poop', text_color=Color.white, font=self.small_font)

    def draw_stars(self, screen):
        '''
        i = 0
        for star in self.stars:
            center = self.main_window.center
            star.draw_grid(screen, (center[0] + i, center[1] - center[1] / 3 + i))
            i += star.radius / 4
            '''
        for star in self.stars:
            star.draw_grid(screen, position=star.position)
        # orbit
        if self.star_orbit > 0:
            elipse_box = pygame.Rect(self.main_window.center[0]-self.star_orbit/2,
                                     self.main_window.center[1]-self.star_orbit/4,
                                     self.star_orbit,
                                     self.star_orbit/2)
            pygame.draw.ellipse(screen, Color.white, elipse_box, 2)

    def draw_planets(self, screen):
        i = 0
        for planet in self.planets:
            i += planet.radius / 10
            center = self.main_window.center
            planet.draw(screen, (center[0], center[1] + i))
            i += planet.radius / 10 + 5

    def update(self, key, mouse, offset=(0, 0)):
        mouse_position = pygame.mouse.get_pos()
        hover = False
        for star in self.stars:
            star_position = (star.position[0] + offset[0], star.position[1] + offset[1])
            if Maths.Maths.collide_circle(point=mouse_position, circle_center=star_position,
                                          circle_radius=star.radius/2):
                self.mouse_box.message = star.name
                hover = True
                break
        if hover:
            self.mouse_box.text_rect.left = mouse_position[0]
            self.mouse_box.text_rect.top = mouse_position[1]
        else:
            self.mouse_box.message = ''

    def draw(self, screen):
        screen.fill(Color.black)
        self.draw_stars(screen)
        # self.draw_planets(screen)
        self.x_box.draw(screen)
        self.y_box.draw(screen)
        self.mouse_box.draw(screen)
