import pygame
from TextBox import TextBox
from TextCursor import TextCursor


class InputBox(TextBox):
    def __init__(self, rect, box_color=None, border_color=None, highlight_color=None, active_color=None, message='',
                 text_color=None, font=None, text_limit=None, allowed_characters=None):
        TextBox.__init__(self, rect, box_color=box_color, border_color=border_color, highlight_color=highlight_color,
                         active_color=active_color, message=message, text_color=text_color, font=font)
        self.active = False
        self.text_limit = text_limit
        self.allowed_characters = allowed_characters

    def draw(self, screen):
        TextBox.draw(self, screen)
        if self.active:
            TextCursor.draw(screen, (self.rect.left + self.font.size(self.message)[0], self.rect.top), self.font)

    def poll(self, in_key):
        if self.active:
            if in_key == pygame.K_BACKSPACE:
                self.message = self.message[0:-1]
            elif in_key == pygame.K_RETURN:
                return self.message
            elif len(self.message) < self.text_limit:
                if not self.allowed_characters or in_key in self.allowed_characters:
                    self.message += chr(in_key)
            return None
