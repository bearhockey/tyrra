import pygame
from Box import Box
from TextCursor import TextCursor


class InputBox(Box):
    def __init__(self, rect, box_color=None, border_color=None, message='', text_color=None, font=None):
        Box.__init__(self, rect, box_color, border_color)
        self.active = False
        self.message = message
        self.text_color = text_color
        self.font = font

    def check_click(self):
        if Box.check_click(self):
            self.active = True
        else:
            self.active = False

    def draw(self, screen):
        Box.draw(self, screen)
        if len(self.message) != 0:
            screen.blit(self.font.render(self.message, True, self.text_color), self.rect)
        if self.active:
            TextCursor.draw(screen, (self.rect.left + self.font.size(self.message)[0], self.rect.top), self.font)

    def poll(self, in_key):
        if self.active:
            if in_key == pygame.K_BACKSPACE:
                self.message = self.message[0:-1]
            elif in_key == pygame.K_RETURN:
                return self.message
            # elif in_key == K_MINUS:
            #  current_string.append("_")
            elif in_key <= 127:
                self.message += chr(in_key)
            return None
