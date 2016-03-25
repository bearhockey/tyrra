import Color
from Ellipse import Ellipse


class Range(object):
    def __init__(self, distance, center=(0, 0), ring_color=Color.d_gray, ship_color=Color.white):
        self.distance = distance
        self.circle = Ellipse(position=center, x_radius=distance, y_radius=distance)
        self.enemies = []
        self.ring_color = ring_color
        self.ship_color = ship_color

    def add_enemy(self, enemy):
        self.enemies.append(enemy)
        orbit_position = 360 / len(self.enemies)
        i = 1
        for ship in self.enemies:
            ship.orbit_point = orbit_position*i
            i += 1

    def draw(self, screen, target, zoom=4):
        self.circle.draw(screen, self.ring_color)
        if len(self.enemies) > 0:
            orbit_position = 360 / len(self.enemies)
            i = 1
            for enemy in self.enemies:
                orbit_point = orbit_position * i
                ship_size = enemy.get_ship_size(zoom=zoom)
                draw_point = (self.circle.get_point(orbit_point)[0] - ship_size[0] / 2,
                              self.circle.get_point(orbit_point)[1] - ship_size[1] / 2)
                if enemy == target:
                    color = Color.red
                else:
                    color = self.ship_color
                enemy.draw_ship(screen, position=draw_point, color=color, zoom=zoom)
                i += 1
