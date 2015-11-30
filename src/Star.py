import pygame
import math


class Star(object):
    def __init__(self, position=(0, 0), radius=128, luminosity=128, temperature=128, name='SUN', orbit=None,
                 orbit_point=0):
        self.position = position
        self.radius = radius
        self.luminosity = luminosity
        self.temperature = temperature
        self.name = name
        self.orbit = orbit
        self.orbit_point = orbit_point

        self.radius_mod = 2

    def get_temperature(self):
        return 2000 + (self.temperature * 32)

    def get_size(self):
        return round(float(self.radius) / 255 * 10, 3)

    def get_luminosity(self):
        return round(float(self.luminosity) / 255, 3)

    def draw_grid(self, screen, position):
        pygame.draw.circle(screen, self.convert_temperature_to_color(), position, self.radius / self.radius_mod)
        pygame.draw.circle(screen, (0, 0, 0), position, self.radius / self.radius_mod, 1)

    def draw_orbit(self, screen, orbit):
        self.draw_grid(screen, position=orbit.get_point(self.orbit_point))

    def draw(self, screen):
        if self.orbit is not None:
            self.draw_orbit(screen, orbit=self.orbit)
        else:
            self.draw_grid(screen, self.position)

    def convert_temperature_to_color(self):
        red_limit = 144
        # red
        if self.temperature < red_limit:
            red = 255
        else:
            red = self.temperature - 125
            red = 330 * (pow(red, -0.133))
            if red < 0:
                red = 0
            elif red > 255:
                red = 255
        # green
        if self.temperature < red_limit:
            green = self.temperature
            green = 99.5 * math.log(green) - 161
        else:
            green = self.temperature - 125
            green = 288 * (pow(green, -0.0755))
        if green < 0:
            green = 0
        elif green > 255:
            green = 255

        # blue
        if self.temperature > red_limit:
            blue = 255
        else:
            blue = self.temperature - 32
            if blue <= 0:
                blue = 1
            blue = 138.5 * math.log(blue) - 305
            if blue < 0:
                blue = 0
            elif blue > 255:
                blue = 255

        return red, green, blue
