import os
from time import sleep

import pygame

import Color
import settings
from Debug import Debug
from Event import Event
from Ship import Ship
from SpaceBattle import SpaceBattle
from System import System
from Warp import Warp
from src.components.Box import Box
from src.components.Window import Window
from src.components.text.TextBox import TextBox
from src.components.text.TextBoxList import TextBoxList


class ControlPanel(object):
    def __init__(self, main_window_width=800, main_window_height=600, main_white_space=50, side_window_width=350,
                 side_window_height=650, side_white_space=50, font=None, small_font=None):
        self.big_font_size = 24
        self.small_font_size = 16
        self.main_window = None
        self.main_width = main_window_width
        self.main_height = main_window_height
        self.console_height = 120
        self.side_window = None
        self.font = font
        self.small_font = small_font

        # keeps buttons from being pressed when they aren't supposed to
        self.window_lock = False

        # some events consants
        self.intro_event_file = os.path.join(settings.main_path, 'data', 'intro.eve')
        self.intro_event_id = 'INTRO_1'
        self.station = None

        self.window_dict = {'console': False,
                            'Messages': True,
                            'email': False,
                            'Ship': True,
                            'System': True,
                            'planet': False,
                            'Battle': False,
                            'Warp': True,
                            'Debug': True,
                            'Station': True}

        self.window_list = {}
        self.sidebar_list = {}

        for window in self.window_dict:
            self.window_list[window] = Window((main_white_space, main_white_space),
                                              (main_window_width, main_window_height-self.console_height),
                                              name=window)
            self.sidebar_list[window] = Window((main_white_space + main_window_width + side_white_space,
                                                side_white_space),
                                               (side_window_width, side_window_height),
                                               name=window,
                                               border_color=Color.d_gray)

        # console
        self.the_big_board = Box(pygame.Rect(0, 0, main_window_width, main_window_height-self.console_height),
                                 box_color=None, border_color=None, highlight_color=None, active_color=None)
        self.board_bottom = Box(pygame.Rect(main_white_space, main_white_space+main_window_height-self.console_height,
                                            main_window_width, self.console_height), box_color=Color.d_gray,
                                border_color=Color.gray, highlight_color=Color.gray, active_color=Color.gray,
                                border=3, name='Console-back')
        self.console = TextBoxList(pygame.Rect(main_white_space+10, main_white_space+main_window_height -
                                               self.console_height+10, main_window_width, self.console_height),
                                   name='Console', text_color=Color.white, text_outline=True, font=self.small_font,
                                   list_size=5, line_size=20)

        self.event = Event(panel=self, picture=self.the_big_board, text=self.console)

        self.window_list['console'].sprites.append(self.the_big_board)
        # self.window_list['console'].sprites.append(self.board_bottom)
        # self.window_list['console'].sprites.append(self.console)
        # main navigation buttons
        self.nav_button = {}
        y_offset = 0
        # self.big_font_size+4)/2*len(window)
        for (window, visible) in self.window_dict.items():
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
        self.system = None
        self.warp_to_system(x=6541, y=43322)

        self.screen_title = None
        self.switch_window('console')

        # battle screen
        self.space_battle = None
        '''
        self.space_battle = SpaceBattle(player_ship=self.ship, font=self.font, small_font=self.small_font,
                                        window_size=(main_window_width, main_window_height - self.console_height))
        self.window_list['Battle'].components.append(self.space_battle)
        self.sidebar_list['Battle'].components.append(self.space_battle.side_panel)
        '''

        # warp menu
        self.sidebar_list['Warp'].components.append(self.back_to_console)
        self.warp = Warp(self, font=self.font, small_font=self.small_font)
        self.sidebar_list['Warp'].components.append(self.warp)
        # self.window_list['Warp'].sprites.append(self.board_bottom)
        # self.window_list['Warp'].sprites.append(self.console)

        # debug
        self.debug_console = TextBoxList(pygame.Rect(10, main_window_height-300, main_window_width, 300),
                                         name='D_con', text_color=Color.white, text_outline=True, font=self.small_font,
                                         list_size=14, line_size=20)
        self.debug = Debug(self.debug_console, self, self.ship, self.font)

        self.window_list['Debug'].sprites.append(Box(pygame.Rect(5, main_window_height-310, main_window_width-10, 5),
                                                     box_color=Color.white, name='LINE'))
        self.window_list['Debug'].sprites.append(self.debug_console)
        self.sidebar_list['Debug'].components.append(self.debug)
        self.sidebar_list['Debug'].components.append(self.back_to_console)

    def load_event(self, event_file, event_name):
        self.event.read_event_file(event_file)
        self.event.run_event(event_name)

    def new_game(self, captain=None):
        self.ship.load(os.path.join(settings.main_path, 'data', 'start.shp'))
        if captain is not None:
            del self.ship.crew[:]
            self.ship.add_crew(captain)
        self.load_event(event_file=self.intro_event_file, event_name=self.intro_event_id)

    def warp_to_system(self, x, y):
        del self.window_list['System'].components[:]
        del self.sidebar_list['System'].components[:]
        self.station = None
        self.system = System(panel=self, font=self.font, small_font=self.small_font, x=x, y=y, add_station=True)
        self.window_list['System'].components.append(self.system.system_map)
        self.sidebar_list['System'].components.append(self.system)
        # self.system_map_index = len(self.window_list['System'].components)-1
        self.sidebar_list['System'].components.append(self.back_to_console)
        self.event.adhoc_event(picture=self.system.family_portrait(),
                               text='Warped to system: {0}'.format(self.system.name),
                               goto='console')

    def dock_with_station(self, station=None):
        if station:
            self.station = station
            self.event.adhoc_event(picture=self.station.image,
                                   text='You have docked with {0}'.format(self.station.name),
                                   goto='console')

    def start_space_battle(self, battle_params=None):
        del self.window_list["Battle"].components[:]
        del self.sidebar_list["Battle"].components[:]
        enemies = None
        if battle_params:
            if "enemies" in battle_params:
                enemies = battle_params["enemies"]
        self.space_battle = SpaceBattle(player_ship=self.ship, font=self.font, small_font=self.small_font,
                                        window_size=(self.main_width, self.main_height - self.console_height),
                                        enemies=enemies)

        self.window_list["Battle"].components.append(self.space_battle)
        self.sidebar_list["Battle"].components.append(self.space_battle.side_panel)
        self.switch_window(new_window="Battle")

    def switch_window(self, new_window):
        self.window_lock = True
        try:
            self.main_window = self.window_list[new_window]
            self.side_window = self.sidebar_list[new_window]
            sleep(0.1)
        except Exception as e:
            print("Exception: {0}".format(e))
            pass
        self.screen_title = self.main_window.name
        self.window_lock = False

    def always(self):
        self.main_window.always()

    def update(self, key, mouse):
        if not self.window_lock:
            self.main_window.update(key=key, mouse=mouse)
            self.side_window.update(key=key, mouse=mouse)

            if self.back_to_console.update(key=key, mouse=mouse, offset=self.side_window.position):
                self.switch_window('console')

            if self.screen_title == 'console':
                for button in self.nav_button:
                    if self.nav_button[button].update(key=key, mouse=mouse, offset=self.side_window.position):
                        if button == 'Station' and self.station is None:
                            self.event.adhoc_event(text='You are currently not docked at a station.')
                        else:
                            self.switch_window(button)

    def draw(self, screen):
        self.main_window.draw(screen)
        # always draw console probably
        self.board_bottom.draw(screen)
        self.console.draw(screen)
        self.side_window.draw(screen)
