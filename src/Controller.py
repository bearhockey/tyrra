import pygame


class Controller(object):
    def __init__(self):
        self.numbers = {1: pygame.K_1,
                        2: pygame.K_2,
                        3: pygame.K_3,
                        4: pygame.K_4,
                        5: pygame.K_5}
        self.keys = {"DOWN": pygame.K_DOWN,
                     "UP": pygame.K_UP,
                     "LEFT": pygame.K_LEFT,
                     "RIGHT": pygame.K_RIGHT,
                     "ACTION": pygame.K_SPACE
                     }
        self.press = None

    def poll_keyboard(self):
        if pygame.key.get_focused():
            self.press = pygame.key.get_pressed()
            return self.press

    def check_key(self, key):
        if self.press is not None:
            if self.press[self.keys[key]]:
                return True
            else:
                return False
        else:
            return False

    def poll_keyboard_old(self, map_object=None):
        if pygame.key.get_focused():
            press = pygame.key.get_pressed()

            if map_object:
                for key, value in self.numbers.items():
                    if press[value]:
                        map_object.create_map(zoom_level=key)

                if press[self.keys["LEFT"]]:
                    map_object.x_offset += map_object.zoom*2
                elif press[self.keys["RIGHT"]]:
                    map_object.x_offset -= map_object.zoom*2
                if press[self.keys["DOWN"]]:
                    map_object.y_offset -= map_object.zoom*2
                elif press[self.keys["UP"]]:
                    map_object.y_offset += map_object.zoom*2

            return press

