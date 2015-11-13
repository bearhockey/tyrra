import pygame

import Color

from Box import Box


class TextBox(Box):
    def __init__(self, rect, box_color=None, border_color=None, highlight_color=None, active_color=None, message='',
                 text_color=None, text_outline=True, font=None):
        Box.__init__(self, rect, box_color=box_color, border_color=border_color, highlight_color=highlight_color,
                     active_color=active_color)
        self.message = message
        self.text_color = text_color
        self.text_outline = text_outline
        self.font = font
        self.text_rect = pygame.Rect(self.rect.left + self.border * 2,
                                     self.rect.top + self.border * 2,
                                     self.rect.width - self.border * 4,
                                     self.rect.height - self.border * 4)

    def draw(self, screen):
        Box.draw(self, screen)
        if len(self.message) != 0:
            if self.text_outline:
                outline_rect = pygame.Rect(self.text_rect.left+2, self.text_rect.top+2, self.text_rect.width,
                                           self.text_rect.height)
                if self.text_color == Color.black:
                    screen.blit(self.font.render(self.message, True, Color.white), outline_rect)
                else:
                    screen.blit(self.font.render(self.message, True, Color.black), outline_rect)

            screen.blit(self.font.render(self.message, True, self.text_color), self.text_rect)
