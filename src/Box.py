import pygame


class Box(object):
    def __init__(self, rect, box_color=None, border_color=None, highlight_color=None, active_color=None):
        self.rect = rect
        self.box_color = box_color
        self.border_color = {
            'NORMAL': border_color,
            'HIGHLIGHT': highlight_color,
            'ACTIVE': active_color
        }
        self.status = 'NORMAL'
        self.active = False
        self.border = 2

    def update(self, mouse, key, offset=(0, 0)):
        self.check_click(mouse=mouse, offset=offset)

    def check_click(self, mouse, offset=(0, 0)):
        pos = (pygame.mouse.get_pos()[0] - offset[0], pygame.mouse.get_pos()[1] - offset[1])
        if self.rect.collidepoint(pos):
            self.status = 'HIGHLIGHT'
            if 1 in mouse.values():
                self.active = True
                return True
        else:
            if 1 in mouse.values():
                self.active = False
                self.status = 'NORMAL'
            else:
                if self.active:
                    self.status = 'ACTIVE'
                else:
                    self.status = 'NORMAL'
            return False

    def draw(self, screen):
        if self.box_color:
            pygame.draw.rect(screen, self.box_color, self.rect, 0)
        if self.border_color[self.status]:
            pygame.draw.rect(screen, self.border_color[self.status], self.rect, 2)
