import os
import pygame

import Color

from Pawn import Pawn
from TextBox import TextBox


class Debug(object):
    def __init__(self, debug_console, panel, ship, font):
        self.debug_console = debug_console
        self.panel = panel
        self.ship = ship
        self.font = font
        self.buttons = []

        self.add_crew = TextBox(pygame.Rect(20, 50, 200, 45), Color.d_gray, border_color=None,
                                highlight_color=Color.white, active_color=None, message='Add Crew',
                                text_color=Color.white, text_outline=True, font=self.font)
        self.buttons.append(self.add_crew)

        self.spam_console = TextBox(pygame.Rect(20, 100, 200, 45), Color.d_gray, highlight_color=Color.white,
                                    message='Spam Debug', text_color=Color.white, text_outline=True, font=self.font)
        self.buttons.append(self.spam_console)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def update(self, key, mouse, offset=(0, 0)):
        if self.add_crew.update(key, mouse, offset):
            self.ship.add_crew(Pawn(name='FooBar', age='Female', race='Compooter',
                                    bio='Stop all the downloadin!',
                                    profile=pygame.image.load(os.path.join('res', 'face', 'joe.png'))))
            self.debug_console.add_message('>> Added crew member ')
        if self.spam_console.update(key, mouse, offset):
            self.debug_console.add_message('>> BLAH BLAH BLAH')

