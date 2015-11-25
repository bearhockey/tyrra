import pygame

import Color

from Box import Box
from InputBox import InputBox
from Ship import ShipGrid
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

        self.window_list = [Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Blank'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Ship'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='System')]
        self.sidebar_list = [Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='Blank', border_color=Color.d_gray),
                             Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='Ship', border_color=Color.d_gray),
                             Window((main_white_space + main_window_width + side_white_space, side_white_space),
                                    (side_window_width, wide_window_height), name='System', border_color=Color.d_gray)]
        # ship grid construct
        self.window_list[1].components.append(ShipGrid(size_x=40, size_y=40))

        # system construct
        # self.system = System(x=454556, y=45645)
        self.system = System(x=6541, y=43322)
        self.system.generate()
        # self.system.system_map.rotate(40)
        self.window_list[2].components.append(self.system.system_map)
        self.system_map_index = len(self.window_list[2].components)-1

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
        self.sidebar_list[2].components.append(self.x_cord_box)
        self.sidebar_list[2].components.append(self.y_cord_box)
        self.sidebar_list[2].sprites.append(self.generate_button)
        self.sidebar_list[2].components.append(TextBox(pygame.Rect(50, 50, 50, 50), Color.d_gray, border_color=None,
                                                       highlight_color=Color.white, active_color=Color.blue))

        self.window_dict = {'blank': 0,
                            'ship': 1,
                            'system': 2}

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
            del self.system.stars[:]
            del self.system.planets[:]
            self.system.generate()
            self.window_list[2].components[self.system_map_index] = self.system.system_map

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
