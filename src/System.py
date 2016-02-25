import pygame
import random

import Color
import Maths
import Text

from Orbit import Orbit
from InputBox import InputBox
from Satellite import Satellite
from Star import Star
from TextBox import TextBox


class System(object):
    def __init__(self, font, small_font, x=0, y=0, generate=True):
        self.x = x
        self.y = y
        self.name = 'Poop'
        self.short_name = 'Jerk'
        self.seed = 0

        self.stars = []
        self.planets = []

        self.big_font_size = 24
        self.small_font_size = 16
        self.font = font
        self.small_font = small_font

        self.main_window = pygame.Rect(0, 0, 800, 600)
        self.star_orbit = Orbit(self.main_window.center, orbit=0, color=Color.d_gray, outline=2)

        self.system_map = None

        self.roman = {1: 'I',
                      2: 'II',
                      3: 'III',
                      4: 'IV',
                      5: 'V',
                      6: 'VI',
                      7: 'VII',
                      8: 'VIII',
                      9: 'IX'}

        self.star_buttons = []
        self.planet_buttons = []

        if generate:
            self.generate(clear=True)

    def generate(self, clear=True):
        if clear:
            del self.stars[:]
            del self.planets[:]
        self.generate_seed()
        self.generate_name()
        self.generate_stars()
        self.generate_planets()

        self.system_map = SystemMap(self.font, self.small_font, stars=self.stars, planets=self.planets,
                                    star_orbit=self.star_orbit, window_width=self.main_window.width,
                                    window_height=self.main_window.height)
        self.generate_system_list()

    def generate_planets(self):
        random.seed(self.seed)
        center = self.main_window.center
        star_sum = self.star_orbit.orbit
        for star in self.stars:
            star_sum += star.radius/2
        planet_num = 200
        planet_count = 1
        while planet_num > 100:
            planet_num -= random.randrange(10, 50)
            print 'planet num is {0}'.format(planet_num)
            planet_name = '{0} {1}'.format(self.short_name, self.roman[planet_count])
            self.planets.append(Satellite(sun_position=center,
                                          radius=random.randint(1, 255),
                                          orbit=planet_num+star_sum,
                                          name=planet_name))
            planet_count += 1
        orbit_position = 360/len(self.planets)
        i = 1
        for planet in self.planets:
            planet.orbit_point = orbit_position*i
            i += 1

    def generate_seed(self):
        self.seed = float(0.5) * float(self.x + self.y) * float(self.x + self.y + 1) + self.y
        self.seed = int(self.seed)
        print 'Seed: {0}'.format(self.seed)

    def generate_stars(self):
        random.seed(self.seed)
        rand = random.randrange(0, 9)
        position = self.main_window.center
        orbit = 0
        radius = random.randint(1, 255)

        self.stars.append(Star(position=position,
                               radius=radius,
                               luminosity=random.randint(1, 255),
                               temperature=random.randint(1, 255)))
        if rand > 6:
            orbit += radius/2
            position = (position[0]+radius/2, position[1]+radius/2)
            radius = random.randint(1, 255)
            self.stars.append(Star(position=position,
                                   radius=radius,
                                   luminosity=random.randint(1, 255),
                                   temperature=random.randint(1, 255)))
            orbit += radius/2
        if rand > 9:
            self.stars.append(Star(radius=random.randint(1, 255),
                                   luminosity=random.randint(1, 255),
                                   temperature=random.randint(1, 255)))

        self.stars = sorted(self.stars, key=lambda star: star.radius, reverse=True)
        star_designations = ['Major', 'Minor', 'Augmented', 'Diminished']
        orbit_position = 360/len(self.stars)
        self.star_orbit.set_orbit(orbit)
        i = 1
        for sun in self.stars:
            sun.name = '{0} {1}'.format(self.short_name, star_designations.pop(0))
            sun.orbit_point = orbit_position*i
            sun.orbit = self.star_orbit
            i += 1

    def generate_name(self):
        lookup_a = ['A', 'Ba', 'Ca', 'Da', 'Fa', 'Ga', 'Ha', 'Ja', 'Ka', 'La', 'Ma', 'Na', 'Pa', 'Qua', 'Ra', 'Sa',
                    'Ta', 'Va', 'Wa', 'Xa', 'Ya', 'Za']
        lookup_e = ['E', 'BE', 'CE', 'DE', 'FE', 'GE', 'HE', 'JE', 'KE', 'LE', 'ME', 'NE', 'PE', 'QUE', 'RE', 'SE',
                    'TE', 'VE', 'WE', 'XE', 'YE', 'ZE']
        lookup_i = ['I', 'BI', 'CI', 'DI', 'FI', 'GI', 'HI', 'JI', 'KI', 'LI', 'MI', 'NI', 'PI', 'QUI', 'RI', 'SI',
                    'TI', 'VI', 'WI', 'XI', 'YI', 'ZI']
        # lookup_x = [u'\u3042', u'\u3044', u'\u3046', u'\u3048', u'\u304A', u'\u304B', u'\u304C', u'\u304D', u'\u304E']
        '''
        lookup_x = [u'\u3042', u'\u3044', u'\u3046', u'\u3048', u'\u304A', u'\u304B', u'\u304C', u'\u304D', u'\u304E',
                    u'\u304F', u'\u3050', u'\u3051', u'\u3052', u'\u3053', u'\u3054', u'\u3055', u'\u3056', u'\u3057',
                    u'\u3058', u'\u3059', u'\u305A', u'\u305B', u'\u305C', u'\u305D', u'\u305E', u'\u305F', u'\u3060',
                    u'\u3061', u'\u3062', u'\u3063', u'\u3064', u'\u3065', u'\u3066', u'\u3067', u'\u3068', u'\u3069']
        '''
        lookup = lookup_a + lookup_e + lookup_i
        '''
        lookup = ['Aleph', 'Alpha', 'Antares', 'Beta', 'Bootes', 'Barum', 'Ceres', 'Charion', 'Chardibus', 'Chalupa',
                  'Delta', 'Darion', 'Doolan', 'Echo', 'Eres', 'Eribus', 'Encephalus', 'Ender', 'Foxtrot', 'Famicom',
                  'Gamma', 'Gregorio', 'Grace', 'Gaea', 'Gaia', 'Howzer', 'Hera', 'Hosio', 'Ignus', 'Io', 'Ionus',
                  'Ibus', 'Jax', 'Jova', 'Jolo', 'Keras', 'Kodia', 'Li', 'Libra', 'Lol', 'Orphius', 'Orchid',
                  'Odyssus', 'Persephone', 'Pax', 'Qualude', 'Qi', 'Ra', 'Rez', 'Radium', 'Tia', 'Tori', 'Uso', 'Ura',
                  'Varia', 'Verit', 'Wex', 'Woolio', 'X', 'Yota', 'Yttrius', 'Zoe', 'Zee', 'Zae', 'Zeebs']
        '''
        base = len(lookup)  # Base whatever.
        name = []
        num = self.seed + pow(2, 25)
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

    def generate_system_list(self):
        star_list = []
        y_off = 0
        for star in self.stars:
            star_list.append(TextBox(pygame.Rect(20, 50+y_off, 50, 50), star.convert_temperature_to_color(),
                                     border_color=None, highlight_color=Color.white, active_color=Color.blue))
            self.star_buttons.append(TextBox(pygame.Rect(80, 60+y_off, 400, 50),
                                             message=star.name,
                                             highlight_color=Color.gray, active_color=Color.blue,
                                             text_color=Color.white, text_outline=True,
                                             font=self.small_font, highlight_text=True,highlight_box=False))

            y_off += 60
            self.star_buttons.append(star_list[-1])

        planet_list = []
        y_off += 40
        for planet in self.planets:
            planet_list.append(TextBox(pygame.Rect(25, 50+y_off, 40, 40), Color.white, border_color=None,
                                       highlight_color=Color.d_gray, active_color=Color.blue))
            self.planet_buttons.append(TextBox(pygame.Rect(80, 60+y_off, 400, 50),
                                               message=planet.name,
                                               highlight_color=Color.gray, active_color=Color.blue,
                                               text_color=Color.white, text_outline=True,
                                               font=self.small_font, highlight_text=True, highlight_box=False))
            y_off += 50
            self.planet_buttons.append(planet_list[-1])

    def draw(self, screen):
        self.draw_body_list(screen)

    def draw_body_list(self, screen):
        # system side-bar
        for star in self.star_buttons:
            star.draw(screen)
        for planet in self.planet_buttons:
            planet.draw(screen)
        '''
        self.x_cord_box = InputBox(pygame.Rect(25, 600, 150, 30), box_color=Color.d_gray, border_color=Color.gray,
                                   highlight_color=Color.white, active_color=Color.gray, message='0',
                                   text_color=Color.white, font=self.font, text_limit=10,
                                   allowed_characters=range(48, 57))
        self.y_cord_box = InputBox(pygame.Rect(175, 600, 150, 30), box_color=Color.d_gray, border_color=Color.gray,
                                   highlight_color=Color.white, active_color=Color.gray, message='0',
                                   text_color=Color.white, font=self.font, text_limit=10,
                                   allowed_characters=range(48, 57))
        self.generate_button = TextBox(pygame.Rect(125, 550, 100, 50), (20, 150, 30), Color.gray,
                                       highlight_color=Color.white, active_color=Color.blue, message=u'\u304D',
                                       text_color=Color.white, font=self.font)
        '''

    def draw_gui(self, screen):
        self.main_window.draw(screen)
        # cords
        # Text.draw_text(screen, self.font, 'X:', Color.white, (200, 400))
        # Text.draw_text(screen, self.font, 'Y:', Color.white, (350, 650))

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
        for star in self.star_buttons:
            star.update(key, mouse, offset)
        for planet in self.planet_buttons:
            planet.update(key, mouse, offset)
        '''
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
        '''


class SystemMap(object):
    def __init__(self, font, small_font, stars, planets, star_orbit, window_width=200, window_height=100):
        self.main_window = pygame.Rect(0, 0, window_width, window_height)
        self.big_font_size = 24
        self.small_font_size = 16
        self.font = font
        self.small_font = small_font

        self.scrolling = False
        self.starting_mouse_pos = 0

        self.stars = stars
        self.planets = planets
        self.star_orbit = star_orbit

        box_width = self.font.size('12345678900')[0]
        self.x_box = InputBox(pygame.Rect(800-box_width*2, 570, box_width, 30), (10, 10, 10), Color.white,
                              highlight_color=Color.blue, active_color=Color.white, message='0',
                              text_color=Color.white, font=self.font, text_limit=10, allowed_characters=range(48, 57))
        self.y_box = InputBox(pygame.Rect(800-box_width, 570, box_width, 30), (10, 10, 10), Color.white,
                              highlight_color=Color.blue, active_color=Color.white, message='0',
                              text_color=Color.white, font=self.font, text_limit=10, allowed_characters=range(48, 57))

        self.mouse_box = TextBox(pygame.Rect(0, 0, 200, 30), box_color=None,border_color=None, highlight_color=None,
                                 active_color=None, message='Poop', text_color=Color.white, font=self.small_font)

    def draw_bodies(self, screen):
        # orbits
        if self.star_orbit.orbit > 0:
            self.star_orbit.draw(screen)
        if len(self.planets) > 0:
            for planet in self.planets:
                planet.orbit.draw(screen)
        # combine lists and then draw them
        bodies = self.stars + self.planets
        bodies = sorted(bodies, key=lambda y: y.orbit.get_point(y.orbit_point)[1], reverse=False)
        for body in bodies:
            body.draw(screen)

    def rotate(self, amount):
        bodies = self.stars + self.planets
        for body in bodies:
            body.orbit_point += amount/10
            if body.orbit_point > 360:
                body.orbit_point -= 360
            if body.orbit_point < 1:
                body.orbit_point += 360

    def always(self):
        self.rotate(10)

    def update(self, key, mouse, offset=(0, 0)):
        mouse_position = pygame.mouse.get_pos()
        hover = False
        bodies = self.stars + self.planets
        for body in reversed(bodies):
            '''
            if self.star_orbit.orbit > 0:
                star_position = (self.star_orbit.get_point(body.orbit_point)[0] + offset[0],
                                 self.star_orbit.get_point(body.orbit_point)[1] + offset[1])
            else:
                star_position = (body.position[0] + offset[0], body.position[1] + offset[1])
            '''
            body_position = body.orbit.get_point(body.orbit_point)
            if Maths.Maths.collide_circle(point=mouse_position, circle_center=body_position,
                                          circle_radius=body.radius/body.radius_mod):
                self.mouse_box.message = body.name
                hover = True
                break
        if hover:
            self.mouse_box.text_rect.left = mouse_position[0]
            self.mouse_box.text_rect.top = mouse_position[1]
        else:
            self.mouse_box.message = ''

        '''
        # disabling manual rotation until we figure we need it
        if mouse is not None:
            if mouse[3]:
                if not self.scrolling:
                    self.starting_mouse_pos = pygame.mouse.get_pos()
                self.scrolling = True
                new_pos_x = pygame.mouse.get_pos()[0] - self.starting_mouse_pos[0]
                self.rotate(new_pos_x/10)
                # self.scrolling = False
            else:
                self.scrolling = False
        else:
            self.scrolling = False
        '''

    def draw(self, screen):
        screen.fill(Color.black)
        # self.draw_stars(screen)
        # self.draw_planets(screen)
        self.draw_bodies(screen)
        # self.x_box.draw(screen)
        # self.y_box.draw(screen)
        # self.mouse_box.draw(screen)
