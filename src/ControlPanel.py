import pygame

import Color

from Box import Box
from InputBox import InputBox
from Map import Map
from Ship import Ship, ShipGrid, ShipPreview
from System import System, SystemMap
from TextBox import TextBox
from Window import Window


class ControlPanel(object):
    def __init__(self, main_window_width=800, main_window_height=600, main_white_space=50, side_window_width=350,
                 wide_window_height=650, side_white_space=50):
        self.big_font_size = 24
        self.small_font_size = 16
        self.main_window = None
        self.side_window = None
        self.font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)
        self.small_font = pygame.font.Font(pygame.font.match_font('kaiti'), self.small_font_size)

        self.window_dict = {'blank': 0,
                            'thunderbird': 1,
                            'email': 2,
                            'ship-edit': 3,
                            'system': 4,
                            'planet': 5}

        self.window_list = [Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Blank'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Thunderbird'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Email'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Ship Edit'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='System'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Planet')]
        self.sidebar_list = [Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='Blank',
                                    border_color=Color.d_gray),
                             Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='Thunderbird',
                                    border_color=Color.d_gray),
                             Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='Email',
                                    border_color=Color.d_gray),
                             Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='Ship Edit',
                                    border_color=Color.d_gray),
                             Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='System',
                                    border_color=Color.d_gray),
                             Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='Planet',
                                    border_color=Color.d_gray)]
        # ship construct
        self.ship = Ship(size_x=40, size_y=40)
        self.window_list[self.window_dict['ship-edit']].components.append(self.ship.ship_grid)
        self.sidebar_list[self.window_dict['ship-edit']].components.append(self.ship)

        # system construct
        # self.system = System(x=454556, y=45645)
        self.system = System(x=6541, y=43322)
        self.system.generate()
        # window_list[2] is system map
        self.window_list[self.window_dict['system']].components.append(self.system.system_map)
        self.system_map_index = len(self.window_list[self.window_dict['system']].components)-1

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
        self.generate_system_list()

        # planet surface map
        self.generate_planet_map()

        # outside the windows (window control)
        self.left_button = TextBox(pygame.Rect(50, 665, 50, 30), Color.d_gray, border_color=None,
                                   highlight_color=Color.blue, active_color=None, message=' < ',
                                   text_color=Color.white, font=self.font)
        self.screen_title = TextBox(pygame.Rect(400, 665, 100, 30), box_color=None, border_color=None,
                                    highlight_color=None, active_color=None, message='',
                                    text_color=Color.white, font=self.font)
        self.right_button = TextBox(pygame.Rect(800, 665, 50, 30), Color.d_gray, border_color=None,
                                    highlight_color=Color.blue, active_color=None, message=' > ',
                                    text_color=Color.white, font=self.font)
        self.switch_window('blank')

    def generate_system_list(self):
        del self.sidebar_list[self.window_dict['system']].components[:]
        del self.sidebar_list[self.window_dict['system']].sprites[:]
        self.sidebar_list[self.window_dict['system']].components.append(self.x_cord_box)
        self.sidebar_list[self.window_dict['system']].components.append(self.y_cord_box)
        self.sidebar_list[self.window_dict['system']].sprites.append(self.generate_button)
        star_list = []
        y_off = 0
        for star in self.system.stars:
            star_list.append(TextBox(pygame.Rect(20, 50+y_off, 50, 50), star.convert_temperature_to_color(),
                                     border_color=None, highlight_color=Color.white, active_color=Color.blue))
            self.sidebar_list[self.window_dict['system']].components.append(TextBox(pygame.Rect(80, 60+y_off, 400, 50),
                                                                                    message=star.name,
                                                                                    text_color=Color.white,
                                                                                    text_outline=Color.black,
                                                                                    font=self.small_font))
            y_off += 60
            self.sidebar_list[self.window_dict['system']].components.append(star_list[-1])

        planet_list = []
        for planet in self.system.planets:
            planet_list.append(TextBox(pygame.Rect(25, 50+y_off, 40, 40), Color.white, border_color=None,
                                       highlight_color=Color.d_gray, active_color=Color.blue))
            self.sidebar_list[self.window_dict['system']].components.append(TextBox(pygame.Rect(80, 60+y_off, 400, 50),
                                                                                    message=planet.name,
                                                                                    text_color=Color.white,
                                                                                    text_outline=Color.black,
                                                                                    font=self.small_font))
            y_off += 50
            self.sidebar_list[self.window_dict['system']].components.append(planet_list[-1])

    def generate_planet_map(self):
        del self.window_list[self.window_dict['planet']].sprites[:]
        planet_map = Map(width=320, height=200, rando=False, seed=self.system.seed)
        self.window_list[self.window_dict['planet']].sprites.append(planet_map)

    def switch_window(self, new_window):
        if new_window in self.window_dict:
            self.main_window = self.window_list[self.window_dict[new_window]]
            self.side_window = self.sidebar_list[self.window_dict[new_window]]
        else:
            try:
                self.main_window = self.window_list[new_window]
                self.side_window = self.sidebar_list[new_window]
            except Exception as e:
                print e
                pass
        self.screen_title.message = self.main_window.name

    def always(self):
        self.main_window.always()

    def update(self, key, mouse):
        self.main_window.update(key=key, mouse=mouse)
        self.side_window.update(key=key, mouse=mouse)

        # check for generate
        if self.generate_button.update(key, mouse, offset=self.side_window.position):
            if len(self.x_cord_box.message) != 0:
                self.system.x = int(self.x_cord_box.message)
            else:
                self.system.x = 0
            if len(self.y_cord_box.message) != 0:
                self.system.y = int(self.y_cord_box.message)
            else:
                self.system.y = 0
            self.system.generate(clear=True)
            self.window_list[2].components[self.system_map_index] = self.system.system_map
            self.generate_system_list()
            self.generate_planet_map()

        if self.left_button.update(key=key, mouse=mouse):
            index = self.window_list.index(self.main_window)
            if index > 0:
                self.switch_window(index-1)
        if self.right_button.update(key=key, mouse=mouse):
            index = self.window_list.index(self.main_window)
            if index < len(self.window_dict)-1:
                self.switch_window(index+1)

    def draw(self, screen):
        self.main_window.draw(screen)
        self.side_window.draw(screen)
        self.left_button.draw(screen)
        self.right_button.draw(screen)
        self.screen_title.draw(screen)
