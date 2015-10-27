import pygame
from Box import Box

class Button(Box):
    def __init__(self, rect, box_color=None, border_color=None, message='', text_color=None, font=None):
        Box.__init__(self, rect, box_color, border_color)
        self.active = False
        self.message = message
        self.text_color = text_color
        self.font = font