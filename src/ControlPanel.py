import pygame

import Color

from Box import Box
from Debug import Debug
from Event import Event
from InputBox import InputBox
from Map import Map
from Ship import Ship
from SpaceBattle import SpaceBattle
from System import System
from TextBox import TextBox
from TextBoxList import TextBoxList
from Window import Window


class ControlPanel(object):
    def __init__(self, main_window_width=800, main_window_height=600, main_white_space=50, side_window_width=350,
                 side_window_height=650, side_white_space=50, font=None, small_font=None):
        self.big_font_size = 24
        self.small_font_size = 16
        self.main_window = None
        self.side_window = None
        self.font = font
        self.small_font = small_font
        # self.font = font or pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)
        # self.small_font = small_font or pygame.font.Font(pygame.font.match_font('kaiti'), self.small_font_size)

        # some events consants
        self.intro_event_file = 'data/intro.eve'
        self.intro_event_id = 'INTRO_1'

        self.window_dict = {'console': False,
                            'Messages': True,
                            'email': False,
                            'Ship': True,
                            'System': True,
                            'planet': False,
                            'Battle': True,
                            'Debug': True}

        self.window_list = {}
        self.sidebar_list = {}

        for window in self.window_dict:
            self.window_list[window] = Window((main_white_space, main_white_space),
                                              (main_window_width, main_window_height),
                                              name=window)
            self.sidebar_list[window] = Window((main_white_space + main_window_width + side_white_space,
                                                side_white_space),
                                               (side_window_width, side_window_height),
                                               name=window,
                                               border_color=Color.d_gray)

        # console
        self.the_big_board = Box(pygame.Rect(0, 0, main_window_width, main_window_height-120), box_color=None,
                                 border_color=None, highlight_color=None, active_color=None)
        self.board_bottom = Box(pygame.Rect(0, main_window_height-120, main_window_width, 120), box_color=Color.d_gray,
                                border_color=Color.gray, highlight_color=Color.gray, active_color=Color.gray,
                                border=3, name='Console-back')
        self.console = TextBoxList(pygame.Rect(10, main_window_height-110, main_window_width, 120),
                                   name='Console', text_color=Color.white, text_outline=True, font=self.small_font,
                                   list_size=5, line_size=20)

        self.event = Event(picture=self.the_big_board, text=self.console)

        self.window_list['console'].sprites.append(self.the_big_board)
        self.window_list['console'].sprites.append(self.board_bottom)
        self.window_list['console'].sprites.append(self.console)
        # main navigation buttons
        self.nav_button = {}
        y_offset = 0
        # self.big_font_size+4)/2*len(window)
        for window, visible in self.window_dict.iteritems():
            if visible:
                self.nav_button[window] = TextBox(pygame.Rect(20, 50+y_offset, 200, 45),
                                                  Color.d_gray, border_color=None, highlight_color=Color.white,
                                                  active_color=None, message=window, text_color=Color.white,
                                                  text_outline=True, font=self.font)
                y_offset += 55

        for button in self.nav_button:
            self.sidebar_list['console'].components.append(self.nav_button[button])

        self.back_to_console = TextBox(pygame.Rect(10, 10, 50, 30), Color.d_gray, border_color=None,
                                       highlight_color=Color.blue, active_color=None, message='< <',
                                       text_color=Color.white, font=self.font)

        # email  client  construct
        # self.email = EmailClient()
        self.sidebar_list['Messages'].components.append(self.back_to_console)

        # ship construct
        self.ship = Ship(size_x=40, size_y=40)
        self.window_list['Ship'].components.append(self.ship.main_screen)
        self.sidebar_list['Ship'].components.append(self.ship)
        self.sidebar_list['Ship'].components.append(self.back_to_console)

        # system construct
        # self.system = System(x=454556, y=45645)
        self.system = System(self.font, self.small_font, x=6541, y=43322)
        self.system.generate()
        self.window_list['System'].components.append(self.system.system_map)
        self.system_map_index = len(self.window_list['System'].components)-1

        # system side-bar
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

        self.screen_title = None
        self.switch_window('console')

        # battle screen
        self.space_battle = SpaceBattle(player_ship=self.ship, font=self.font, small_font=self.small_font)
        self.window_list['Battle'].components.append(self.space_battle)
        self.sidebar_list['Battle'].components.append(self.space_battle.side_panel)

        # debug
        self.debug_console = TextBoxList(pygame.Rect(10, main_window_height-300, main_window_width, 300),
                                         name='D_con', text_color=Color.white, text_outline=True, font=self.small_font,
                                         list_size=14, line_size=20)
        self.debug = Debug(self.debug_console, self, self.ship, self.font)

        self.window_list['Debug'].sprites.append(Box(pygame.Rect(5, main_window_height-310, main_window_width-10, 5),
                                                     box_color=Color.white, name='LINE'))
        self.window_list['Debug'].sprites.append(self.debug_console)
        self.sidebar_list['Debug'].components.append(self.debug)

    def load_event(self, event_file, event_name):
        self.event.read_event_file(event_file)
        self.event.run_event(event_name)

    def new_game(self):
        self.ship.load('data/start.shp')
        self.load_event(event_file=self.intro_event_file, event_name=self.intro_event_id)

    def generate_system_list(self):
        del self.sidebar_list['System'].components[:]
        del self.sidebar_list['System'].sprites[:]
        self.sidebar_list['System'].components.append(self.back_to_console)
        self.sidebar_list['System'].components.append(self.x_cord_box)
        self.sidebar_list['System'].components.append(self.y_cord_box)
        self.sidebar_list['System'].sprites.append(self.generate_button)
        star_list = []
        y_off = 0
        for star in self.system.stars:
            star_list.append(TextBox(pygame.Rect(20, 50+y_off, 50, 50), star.convert_temperature_to_color(),
                                     border_color=None, highlight_color=Color.white, active_color=Color.blue))
            self.sidebar_list['System'].components.append(TextBox(pygame.Rect(80, 60+y_off, 400, 50),
                                                                  message=star.name,
                                                                  text_color=Color.white,
                                                                  text_outline=True,
                                                                  font=self.small_font))
            y_off += 60
            self.sidebar_list['System'].components.append(star_list[-1])

        planet_list = []
        for planet in self.system.planets:
            planet_list.append(TextBox(pygame.Rect(25, 50+y_off, 40, 40), Color.white, border_color=None,
                                       highlight_color=Color.d_gray, active_color=Color.blue))
            self.sidebar_list['System'].components.append(TextBox(pygame.Rect(80, 60+y_off, 400, 50),
                                                                  message=planet.name,
                                                                  text_color=Color.white,
                                                                  text_outline=True,
                                                                  font=self.small_font))
            y_off += 50
            self.sidebar_list['System'].components.append(planet_list[-1])

    def generate_planet_map(self):
        del self.window_list['planet'].sprites[:]
        planet_map = Map(width=320, height=200, rando=False, seed=self.system.seed)
        self.window_list['planet'].sprites.append(planet_map)

    def switch_window(self, new_window):
        try:
            self.main_window = self.window_list[new_window]
            self.side_window = self.sidebar_list[new_window]
        except Exception as e:
            print e
            pass
        self.screen_title = self.main_window.name

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
            self.window_list['System'].components[self.system_map_index] = self.system.system_map
            self.generate_system_list()
            self.generate_planet_map()

        if self.back_to_console.update(key=key, mouse=mouse, offset=self.side_window.position):
            self.switch_window('console')

        if self.screen_title == 'console':
            for button in self.nav_button:
                if self.nav_button[button].update(key=key, mouse=mouse, offset=self.side_window.position):
                    self.switch_window(button)
            # debug console message
            # self.console.message =  >> Your current attack is: {0}".format(self.ship.ship_grid.get_stats()[0])

    def draw(self, screen):
        self.main_window.draw(screen)
        self.side_window.draw(screen)
