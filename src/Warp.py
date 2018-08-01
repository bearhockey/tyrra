import pygame

import src.Color as Color
from src.components.text import Text
from src.components.text.InputBox import InputBox
from src.components.text.TextBox import TextBox


class Warp(object):
    def __init__(self, panel, font, small_font):
        self.panel = panel
        self.font = font
        self.small_font = small_font
        self.x_cord_box = InputBox(pygame.Rect(75, 200, 200, 30), box_color=Color.d_gray, border_color=Color.gray,
                                   highlight_color=Color.white, active_color=Color.gray, message='0',
                                   text_color=Color.white, font=self.font, text_limit=10,
                                   allowed_characters=range(48, 58))
        self.y_cord_box = InputBox(pygame.Rect(75, 250, 200, 30), box_color=Color.d_gray, border_color=Color.gray,
                                   highlight_color=Color.white, active_color=Color.gray, message='0',
                                   text_color=Color.white, font=self.font, text_limit=10,
                                   allowed_characters=range(48, 58))
        self.generate_button = TextBox(pygame.Rect(125, 300, 100, 50), (20, 150, 30), Color.gray,
                                       highlight_color=Color.white, active_color=Color.blue, message=u'\u304D',
                                       text_color=Color.white, font=self.font)

    def draw(self, screen):
        Text.draw_text(screen, self.font, 'Warp to System', Color.white, (105, 14))
        Text.draw_text(screen, self.font, 'X:', Color.white, (40, 200))
        Text.draw_text(screen, self.font, 'Y:', Color.white, (40, 250))
        self.x_cord_box.draw(screen)
        self.y_cord_box.draw(screen)
        self.generate_button.draw(screen)

    def update(self, key, mouse, offset=(0, 0)):
        self.x_cord_box.update(key, mouse, offset)
        self.y_cord_box.update(key, mouse, offset)

        # check for generate
        if self.generate_button.update(key, mouse, offset):
            if len(self.x_cord_box.message) != 0:
                x = int(self.x_cord_box.message)
            else:
                x = 0
            if len(self.y_cord_box.message) != 0:
                y = int(self.y_cord_box.message)
            else:
                y = 0
            self.panel.warp_to_system(x, y)
