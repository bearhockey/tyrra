import pygame


class Box(object):
    def __init__(self, rect, box_color=None, border_color=None):
        self.rect = rect
        self.box_color = box_color
        self.border_color = border_color
        self.border = 2

    def check_click(self, offset=(0, 0)):
        pos = (pygame.mouse.get_pos()[0] - offset[0], pygame.mouse.get_pos()[1] - offset[1])
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

    def draw(self, screen):
        if self.box_color:
            pygame.draw.rect(screen, self.box_color, self.rect, 0)
        if self.border_color:
            pygame.draw.rect(screen, self.border_color, self.rect, 2)
