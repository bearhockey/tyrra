import math
import random

import pygame

import Color
from Orbit import Orbit
from Planet import Planet
from Star import Star
from Station import Station
from src.components.text import Text
from src.components.text.TextBox import TextBox


class System(object):
    def __init__(self, panel, font, small_font, x=0, y=0, generate=True, add_station=False):
        self.panel = panel

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

        self.main_window = pygame.Rect(0, 0, self.panel.main_width, self.panel.main_height)
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

        self.system_button = TextBox(pygame.Rect(20, 60, 300, 30), message=self.short_name, box_color=Color.l_gray,
                                     highlight_color=Color.gray, active_color=Color.blue, text_color=Color.black,
                                     text_outline=True, font=self.small_font, highlight_text=False, highlight_box=True)
        self.station_dock_button = TextBox(pygame.Rect(20, 460, 300, 30), message='DOCK', box_color=Color.d_gray,
                                           highlight_color=Color.white, active_color=Color.blue, text_color=Color.white,
                                           text_outline=True, font=self.small_font,
                                           highlight_text=False, highlight_box=True)
        self.star_buttons = []
        self.planet_buttons = []

        if generate:
            self.generate(clear=True, add_station=add_station)

        self.current_body = None

    def generate(self, clear=True, add_station=False):
        if clear:
            del self.stars[:]
            del self.planets[:]
        self.generate_seed()
        self.generate_name()
        self.generate_stars()
        self.generate_planets()

        if add_station:
            random.seed(self.seed)
            random.choice(self.planets).station = Station()

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
            self.planets.append(Planet(index=planet_count,
                                       seed=self.seed,
                                       sun_position=center,
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
            digit = num % base
            num /= base
            name.append(lookup[digit])

        string = u""
        string += u"{0} supercluster.  ".format(name.pop())
        string += u"{0} group.  ".format(name.pop())
        string += u"{0} system.  ".format(name.pop())
        self.short_name = u"-".join(name)
        string += self.short_name
        self.name = string

    def generate_system_list(self):

        self.system_button.message = '{0} System'.format(self.short_name)
        star_list = []
        y_off = 60
        for star in self.stars:
            star_list.append(TextBox(pygame.Rect(20, 50+y_off, 50, 50), star.convert_temperature_to_color(),
                                     border_color=None, highlight_color=Color.white, active_color=Color.blue))
            self.star_buttons.append(TextBox(pygame.Rect(80, 60+y_off, 400, 50),
                                             message=star.name,
                                             highlight_color=Color.gray, active_color=Color.blue,
                                             text_color=Color.white, text_outline=True,
                                             font=self.small_font, highlight_text=True, highlight_box=False))

            y_off += 60
            self.star_buttons.append(star_list[-1])

        planet_list = []
        y_off += 40
        for planet in self.planets:
            if planet.station:
                color = Color.d_gray
            else:
                color = Color.white
            planet_list.append(TextBox(pygame.Rect(25, 50+y_off, 40, 40), color, border_color=None,
                                       highlight_color=Color.d_gray, active_color=Color.blue))
            self.planet_buttons.append(TextBox(pygame.Rect(80, 60+y_off, 400, 50),
                                               message=planet.name,
                                               highlight_color=Color.gray, active_color=Color.blue,
                                               text_color=Color.white, text_outline=True,
                                               font=self.small_font, highlight_text=True, highlight_box=False))
            y_off += 50
            self.planet_buttons.append(planet_list[-1])

    def draw(self, screen):
        self.system_button.draw(screen)
        if self.current_body is not None:
            self.draw_body_detail(screen)
        else:
            self.draw_body_list(screen)

    def draw_body_list(self, screen):
        # system side-bar
        for star in self.star_buttons:
            star.draw(screen)
        for planet in self.planet_buttons:
            planet.draw(screen)

    def draw_body_detail(self, screen):
        body = self.current_body
        Text.draw_text(screen, self.font, body.name, Color.white, (25, 100))
        if type(body) is Star:
            Text.draw_text(screen, self.small_font, 'Temperature:', Color.white, (20, 200))
            Text.draw_text(screen, self.small_font, str(body.get_temperature()), Color.white, (150, 200))
            #
            Text.draw_text(screen, self.small_font, 'Size:', Color.white, (20, 230))
            Text.draw_text(screen, self.small_font, str(body.get_size()), Color.white, (150, 230))
            #
            Text.draw_text(screen, self.small_font, 'Luminosity:', Color.white, (20, 260))
            Text.draw_text(screen, self.small_font, str(body.get_luminosity()), Color.white, (150, 260))
        elif type(body) is Planet:
            Text.draw_text(screen, self.small_font, 'I is planet', Color.green, (25, 200))
            Text.draw_text(screen, self.small_font, "Atmosphere is {0}".format(body.atmosphere_density),
                           Color.blue, (25, 240))
            Text.draw_text(screen, self.small_font, "Temperature is {0}K".format(body.temperature),
                           Color.red, (25, 280))
            if body.temperature > 373:
                water = "BOILED"
            elif body.temperature < 273:
                water = "FROZEN"
            else:
                water = "LIFE"
            Text.draw_text(screen, self.small_font, water, Color.green, (25, 320))
            if body.station is not None:
                Text.draw_text(screen, self.small_font, 'Station {0} is online'.format(body.station.name),
                               Color.blue, (25, 350))
                self.station_dock_button.draw(screen)
        else:
            Text.draw_text(screen, self.small_font, 'What am I?', Color.white, (25, 200))

    def draw_gui(self, screen):
        Text.draw_text(screen, self.font, self.name, Color.white, (20, 20))
        text_offset = 0
        for star in self.stars:
            text_offset = self.stars.index(star) * 100
            Text.draw_text(screen, self.small_font, '{0}'.format(star.name), Color.white, (900, 50 + text_offset))

        for _ in self.planets:
            Text.draw_text(screen, self.small_font, 'Planets: {0}'.format(len(self.planets)), Color.white,
                           (900, 350 + text_offset))

    def update(self, key, mouse, offset=(0, 0)):
        if self.system_button.update(key, mouse, offset):
            self.current_body = None
            self.system_map.planet_focus = 0
        if self.current_body is None:
            self.update_body_list(key, mouse, offset)
        elif type(self.current_body) is Planet:
            if self.current_body.station:
                if self.station_dock_button.update(key, mouse, offset):
                    self.panel.dock_with_station(self.current_body.station)

    def update_body_list(self, key, mouse, offset=(0, 0)):
        for star in self.star_buttons:
            if star.update(key, mouse, offset):
                self.current_body = self.get_body_by_name(self.stars, star.message)
        for planet in self.planet_buttons:
            if planet.update(key, mouse, offset):
                self.current_body = self.get_body_by_name(self.planets, planet.message)
                self.system_map.planet_focus = self.current_body.planet_index

    @staticmethod
    def get_body_by_name(body_list, name):
        for body in body_list:
            if name == body.name:
                return body

    # prototype thing
    def family_portrait(self):
        # random star background
        random.seed(self.seed)
        canvas = pygame.Surface((self.panel.main_width, self.panel.main_height))
        canvas.fill(color=Color.black)
        x = 0
        while x < self.panel.main_width:
            y = 0
            while y < self.panel.main_height:
                val = random.random()*255
                if val > 254.5:
                    i = random.randrange(50, 255)
                    color = pygame.Color(i, i, i)
                    pygame.draw.circle(canvas, color, (x, y), int(math.log10(random.randrange(1, 1000))))
                    # canvas.set_at((x, y), pygame.Color(int(val), int(val), int(val), 255))
                y += 1
            x += 1

        # draw parent stars
        center_x = self.panel.main_width/2 + random.randrange(-100, 100)
        center_y = self.panel.main_height/2 + random.randrange(-100, 100)
        for star in self.stars:
            center = center_x+random.randrange(0, 100), center_y+random.randrange(0, 100)
            width = int(star.get_size())*2
            alpha_mod = 255/(width+1)
            while width > 0:
                r, g, b = star.convert_temperature_to_color()
                a = 255-(width*alpha_mod)
                # r -= width*10
                # print 'colors: {0} {1} {2} {3} @ {4}'.format(r, b, g, a, width)
                # color = pygame.Color(r, g, b, a)
                pygame.draw.circle(canvas, (r, g, b, a), center, width)
                width -= 1
            # lens flares?
            f = 0
            while f < random.randrange(5, 7):
                pygame.draw.line(canvas, star.convert_temperature_to_color(), center,
                                 (center_x+random.randrange(-50, 50), center_y+random.randrange(-50, 50)))
                f += 1
        return canvas


class SystemMap(object):
    def __init__(self, font, small_font, stars, planets, star_orbit, window_width=200, window_height=100):
        self.main_window = pygame.Rect(0, 0, window_width, window_height)
        self.center_x = window_width/2
        self.center_y = window_height/2
        self.big_font_size = 24
        self.small_font_size = 16
        self.font = font
        self.small_font = small_font

        self.scrolling = False
        self.starting_mouse_pos = 0

        self.stars = stars
        self.planets = planets
        self.star_orbit = star_orbit

        self.planet_focus = 0

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
        pass

    def draw(self, screen):
        screen.fill(Color.black)
        # self.draw_stars(screen)
        # self.draw_planets(screen)
        if self.planet_focus > 0:
            self.planets[self.planet_focus-1].map.draw(screen)
        else:
            self.draw_bodies(screen)
        # self.x_box.draw(screen)
        # self.y_box.draw(screen)
        # self.mouse_box.draw(screen)
