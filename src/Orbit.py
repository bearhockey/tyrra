import src.Color as Color

from src.components.Ellipse import Ellipse


class Orbit(object):
    def __init__(self, position=(0, 0), orbit=0, color=Color.white, outline=2):
        self.position = position
        self.orbit = orbit

        self.ellipse = Ellipse(self.position, x_radius=0, y_radius=0)
        self.set_orbit(orbit)

        self.color = color
        self.outline = outline

    def get_point(self, angle):
        return self.ellipse.get_point(angle)

    def set_orbit(self, orbit=0):
        self.orbit = orbit
        self.ellipse.x_radius = orbit
        self.ellipse.y_radius = orbit/3

    def draw(self, screen):
        self.ellipse.draw(screen, color=self.color, outline=self.outline)
