import pygame


class Controller(object):
    def __init__(self):
        self.numbers = {1: pygame.K_1,
                        2: pygame.K_2,
                        3: pygame.K_3,
                        4: pygame.K_4,
                        5: pygame.K_5}
        self.keys = {'down': pygame.K_DOWN,
                     'up': pygame.K_UP,
                     'left': pygame.K_LEFT,
                     'right': pygame.K_RIGHT,
                     'action': pygame.K_SPACE
                     }

    def poll_keyboard(self, map_object):
        if pygame.key.get_focused():
            press = pygame.key.get_pressed()

            for key, value in self.numbers.iteritems():
                if press[value]:
                    map_object.create_map(zoom_level=key)

            if press[self.keys['left']]:
                map_object.x_offset += map_object.zoom*2
            elif press[self.keys['right']]:
                map_object.x_offset -= map_object.zoom*2
            if press[self.keys['down']]:
                map_object.y_offset -= map_object.zoom*2
            elif press[self.keys['up']]:
                map_object.y_offset += map_object.zoom*2

