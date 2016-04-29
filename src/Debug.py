import os

import pygame

import Color
import settings
from Pawn import Pawn
from src.components.text.TextBox import TextBox


class Debug(object):
    def __init__(self, debug_console, panel, ship, font):
        self.debug_console = debug_console
        self.panel = panel
        self.event = self.panel.event
        self.ship = ship
        self.font = font
        self.buttons = []

        self.add_crew = TextBox(pygame.Rect(20, 50, 250, 45), Color.d_gray, border_color=None,
                                highlight_color=Color.white, active_color=None, message='Add Crew',
                                text_color=Color.white, text_outline=True, font=self.font)
        self.buttons.append(self.add_crew)

        self.spam_console = TextBox(pygame.Rect(20, 100, 250, 45), Color.d_gray, highlight_color=Color.white,
                                    message='Spam Debug', text_color=Color.white, text_outline=True, font=self.font)
        self.buttons.append(self.spam_console)

        self.damage_shield = TextBox(pygame.Rect(20, 150, 250, 45), Color.d_gray, highlight_color=Color.white,
                                     message='Damage Ship Shields', text_color=Color.white, text_outline=True,
                                     font=self.font)
        self.buttons.append(self.damage_shield)

        self.enter_battle = TextBox(pygame.Rect(20, 200, 250, 45), Color.d_gray, highlight_color=Color.white,
                                    message="Enter Battle", text_color=Color.white, text_outline=True,
                                    font=self.font)
        self.buttons.append(self.enter_battle)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def update(self, key, mouse, offset=(0, 0)):
        if self.add_crew.update(key, mouse, offset):
            self.ship.add_crew(Pawn(name='FooBar', age='Female', race='Compooter',
                                    bio='Stop all the downloadin!',
                                    profile=(os.path.join(settings.main_path, 'res', 'face', 'joe.png'))))
            self.debug_console.add_message('>> Added crew member ')

        if self.spam_console.update(key, mouse, offset):
            self.debug_console.add_message('>> BLAH BLAH BLAH')

        if self.damage_shield.update(key, mouse, offset):
            self.ship.current_shield -= 10
            self.debug_console.add_message('>> Ship shield depleted by 10 to {0}'.format(self.ship.current_shield))

        if self.enter_battle.update(key, mouse, offset):
            self.event.adhoc_event(battle={"Bad": "guy", "enemies": [{"ship_file": "data/enemy_1.txt"},
                                                                     {"ship_file": "data/enemy_1.txt"}]})
