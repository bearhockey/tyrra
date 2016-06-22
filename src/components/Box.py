import pygame


class Box(object):
    def __init__(self, rect, box_color=None, border_color=None, highlight_color=None, active_color=None, border=2,
                 highlight_box=True, name=None, image=None):
        self.rect = rect
        self.box_color = box_color
        self.border_color = {
            'NORMAL': border_color,
            'HIGHLIGHT': highlight_color,
            'ACTIVE': active_color
        }
        self.status = 'NORMAL'
        self.active = False
        self.border = border
        self.highlight_box = highlight_box
        self.name = name
        self.image = image

    def update(self, key, mouse, offset=(0, 0)):
        return self.check_click(mouse=mouse, offset=offset)

    def check_mouse_inside(self, mouse, offset=(0, 0)):
        pos = (pygame.mouse.get_pos()[0] - offset[0], pygame.mouse.get_pos()[1] - offset[1])
        return self.rect.collidepoint(pos)

    def check_click(self, mouse, offset=(0, 0)):
        if self.check_mouse_inside(mouse=mouse, offset=offset):
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
        if self.image:
            screen.blit(self.image, self.rect)
        elif self.box_color:
            pygame.draw.rect(screen, self.box_color, self.rect, 0)
        border_color = self.border_color['NORMAL']
        if self.highlight_box:
            border_color = self.border_color[self.status]
        if border_color:
            pygame.draw.rect(screen, border_color, self.rect, 2)
