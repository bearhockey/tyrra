import pygame
from Box import Box


class TextBox(Box):
    def __init__(self, rect, box_color=None, border_color=None, message='', text_color=None, font=None):
        Box.__init__(self, rect, box_color, border_color)
        self.message = message
        self.text_color = text_color
        self.font = font
        self.text_rect = pygame.Rect(self.rect.left + self.border * 2,
                                     self.rect.top + self.border * 2,
                                     self.rect.width - self.border * 4,
                                     self.rect.height - self.border * 4)

    def draw(self, screen):
        Box.draw(self, screen)
        if len(self.message) != 0:
            screen.blit(self.font.render(self.message, True, self.text_color), self.text_rect)
