import pygame

import Color
from src.components.text.TextBox import TextBox


class EmailClient(object):
    def __init__(self):
        self.emails = []


class Email(object):
    def __init__(self, screen_width, screen_height, subject=None, message=None, font=None, small_font=None):
        self.big_font_size = 24
        self.small_font_size = 16
        self.large_font = font
        self.small_font = small_font
        if not self.large_font:
            self.large_font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)
        if not self.small_font:
            self.large_font = pygame.font.Font(pygame.font.match_font('kaiti'), self.small_font_size)

        self.subject = subject
        self.message = message
        self.body_width = screen_width
        self.body_height = screen_height
        self.email_screen = pygame.Surface(size=(self.body_width, self.body_height))

        self.subject_box = TextBox(pygame.Rect(10, 10, 10, 50), box_color=Color.blue, border_color=Color.gray,
                                   highlight_color=Color.white, active_color=Color.gray, text_color=Color.white,
                                   text_outline=Color.white, font=self.large_font)
        self.message_box = TextBox(pygame.Rect(10, 40, 10, 50), text_color=Color.white,
                                   text_outline=Color.white, font=self.small_font)
        if self.subject:
            self.subject_box.message = self.subject
        else:
            self.subject_box.message = 'FW: Get big peen now!'

        if self.message:
            self.message_box.message = self.message
        else:
            self.message_box.message = 'FW: Get big peen now!'

    def draw(self, screen):
        self.email_screen.fill(Color.d_blue)
        self.subject_box.draw(self.email_screen)
        self.message_box.draw(self.email_screen)
        screen.blit(self.email_screen, (0, 0))
