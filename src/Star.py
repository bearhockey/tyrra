import pygame


class Star(object):
    def __init__(self, radius=128, luminosity=128, temperature=128):
        self.radius = radius
        self.luminosity = luminosity
        self.temperature = temperature

    def get_color(self):
        r = 255 - self.temperature
        b = self.luminosity
        g = max((self.temperature + self.luminosity) / 2, 128)

        return r, g, b

    def draw_grid(self, screen, position):
        pygame.draw.circle(screen, self.get_color(), position, self.radius/2)
