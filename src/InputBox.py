import pygame
from TextBox import TextBox
from TextCursor import TextCursor


class InputBox(TextBox):
    def __init__(self, rect, box_color=None, border_color=None, message='', text_color=None, font=None,
                 text_limit=None):
        TextBox.__init__(self, rect, box_color, border_color, message, text_color, font)
        self.active = False
        self.text_limit = text_limit

    def check_click(self):
        if TextBox.check_click(self):
            self.active = True
        else:
            self.active = False

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
            elif len(self.message) < self.text_limit and 48 <= in_key <= 57:
                self.message += chr(in_key)
            return None
