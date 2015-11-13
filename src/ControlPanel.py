import pygame

import Color

from Ship import ShipGrid
from System import System, SystemMap
from TextBox import TextBox
from Window import Window


class ControlPanel(object):
    def __init__(self, main_window_width=800, main_window_height=600, main_white_space=50):
        self.big_font_size = 24
        self.small_font_size = 16
        self.main_window = None
        self.font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)

        self.window_list = [Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Blank'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='Ship'),
                            Window((main_white_space, main_white_space), (main_window_width, main_window_height),
                                   name='System')]
        # ship grid construct
        self.window_list[1].components.append(ShipGrid(size_x=40, size_y=40))
        # system construct
        self.system = System(x=454556, y=45645)
        self.system.generate()
        self.window_list[2].components.append(self.system.system_map)

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
        else:
            try:
                self.main_window = self.window_list[new_window]
            except:
                pass
        self.screen_title.message = self.main_window.name

    def update(self, key, mouse):
        self.main_window.update(key=key, mouse=mouse)
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
        self.left_button.draw(screen)
        self.right_button.draw(screen)
        self.screen_title.draw(screen)
