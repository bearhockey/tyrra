import pygame
import os

import Color
import settings

from Box import Box
from TextBox import TextBox


class Title(object):
    def __init__(self, font, screen_width=800, screen_height=600):
        self.font = font
        title_image = pygame.image.load(os.path.join(settings.main_path, 'res', 'tyrra_title.png'))
        pygame.mixer.music.load(os.path.join(settings.main_path, 'res', 'tyrra_bit.ogg'))
        self.title_image = Box(rect=pygame.Rect(10, 10, screen_width-20, screen_height-20), border_color=Color.white,
                               highlight_color=Color.white, active_color=Color.white, border=4, image=title_image)
        self.new_game = TextBox(rect=pygame.Rect(screen_width/2-40, screen_height/2+20, 120, 30),
                                highlight_color=Color.gray, active_color=Color.blue, name='new', message='New Game',
                                text_color=Color.white, text_outline=True, font=font, highlight_text=True,
                                highlight_box=False)
        self.load_game = TextBox(rect=pygame.Rect(screen_width/2-40, screen_height/2+60, 120, 30),
                                 highlight_color=Color.gray, active_color=Color.blue, name='load', message='Load Game',
                                 text_color=Color.white, text_outline=True, font=font, highlight_text=True,
                                 highlight_box=False)
        self.options = TextBox(rect=pygame.Rect(screen_width/2-40, screen_height/2+100, 100, 30),
                               highlight_color=Color.gray, active_color=Color.blue, name='options', message='Options',
                               text_color=Color.white, text_outline=True, font=font, highlight_text=True,
                               highlight_box=False)
        self.quit = TextBox(rect=pygame.Rect(screen_width/2-40, screen_height/2+140, 80, 30),
                            highlight_color=Color.gray, active_color=Color.blue, name='quit', message='Quit',
                            text_color=Color.white, text_outline=True, font=font, highlight_text=True,
                            highlight_box=False)
        self.buttons = [self.new_game, self.load_game, self.options, self.quit]

    @staticmethod
    def play_title_music():
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    @staticmethod
    def stop_title_music():
        pygame.mixer.music.fadeout(500)

    def update(self, key, mouse):
        for button in self.buttons:
            if button.update(key=key, mouse=mouse):
                return button.name

    def draw(self, screen):
        self.title_image.draw(screen)
        self.new_game.draw(screen)
        self.load_game.draw(screen)
        self.options.draw(screen)
        self.quit.draw(screen)
