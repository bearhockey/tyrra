import pygame

import src.Color
from src.components.Box import Box


class TextBox(Box):
    def __init__(self, rect, box_color=None, border_color=None, highlight_color=None, active_color=None, border=2,
                 name=None, message='', text_color=None, text_outline=True, font=None, highlight_box=True,
                 highlight_text=False):
        super(TextBox, self).__init__(rect, box_color=box_color, border_color=border_color,
                                      highlight_color=highlight_color, active_color=active_color, border=border,
                                      highlight_box=highlight_box, name=name)
        self.message = message
        self.text_color = text_color
        self.text_outline = text_outline
        self.font = font
        self.text_rect = pygame.Rect(self.rect.left + self.border * 2,
                                     self.rect.top + self.border * 2,
                                     self.rect.width - self.border * 4,
                                     self.rect.height - self.border * 4)
        self.highlight_text = highlight_text

    def translate_rect(self, left=None, top=None, width=None, height=None):
        if left:
            self.rect.left += left
            self.text_rect.left += left
        if top:
            self.rect.top += top
            self.text_rect.top += top
        if width:
            self.rect.width += width
            self.text_rect.width += width
        if height:
            self.rect.height += height
            self.text_rect.height += height

    def update(self, key, mouse, offset=(0, 0)):
        return Box.update(self, key, mouse, offset)

    def draw(self, screen):
        Box.draw(self, screen)
        text_color = self.text_color
        if self.highlight_text:
            if self.status == 'ACTIVE':
                text_color = self.border_color['ACTIVE']
            elif self.status == 'HIGHLIGHT':
                text_color = self.border_color['HIGHLIGHT']
        if len(self.message) != 0:
            if self.text_outline:
                outline_rect = pygame.Rect(self.text_rect.left+2, self.text_rect.top+2, self.text_rect.width,
                                           self.text_rect.height)
                if text_color == src.Color.black:
                    screen.blit(self.font.render(self.message, True, src.Color.white), outline_rect)
                else:
                    screen.blit(self.font.render(self.message, True, src.Color.black), outline_rect)

            screen.blit(self.font.render(self.message, True, text_color), self.text_rect)
