import random

from src.components.perlin import SimplexNoise
from src.components.Maths import Maths


class Elevation(object):
    def __init__(self):
        print("elevation is cool")

    @staticmethod
    def rando_card(node_map, scale=1, octaves=1, seed=0):
        # freq = octaves * octaves
        map_width = len(node_map)
        for column in node_map:
            for node in column:
                noise = SimplexNoise()
                node.elevation = (noise.noise2(x=(node.x + seed) / scale, y=(node.y + seed) / scale) + 1) / 2

    @staticmethod
    def flat_land(node_map, level=0.5):
        for row in node_map:
            for node in row:
                node.elevation = level

    @staticmethod
    def land_ceiling(node_map, ceiling=0.5):
        for row in node_map:
            for node in row:
                if node.elevation > ceiling:
                    node.elevation = ceiling

    @staticmethod
    def land_floor(node_map, floor=0.5):
        for row in node_map:
            for node in row:
                if node.elevation < floor:
                    node.elevation = floor

    @staticmethod
    def amplify(node_map, base, ceiling, factor, direction='positive'):
        for row in node_map:
            for node in row:
                if direction == 'positive' or direction == 'up':
                    delta = factor
                else:
                    delta = 1/factor
                if base < node.elevation < ceiling:
                        node.elevation *= delta

    @staticmethod
    def build(node_map, x, y, floor, ceiling, branch):
        current_x = x
        current_y = y
        done_list = []
        while branch > 0:
            if (current_x, current_y) not in done_list:
                node_map[current_x][current_y].elevation = min(floor+random.random(), ceiling)
                done_list.append((current_x, current_y))
                branch -= 1
            if bool(random.getrandbits(1)):
                i_list = [0, -1]
            else:
                i_list = [0, 1]
            random.shuffle(i_list)
            current_x += i_list[0]
            current_y += i_list[1]
            if current_x < 0:
                current_x = len(node_map)-1
            elif current_x > len(node_map)-1:
                current_x = 0
            if current_y < 0:
                current_y = 0
            elif current_y > len(node_map[current_x]) - 1:
                current_y = len(node_map[current_x]) - 1

    @staticmethod
    def build_land(node_map, x, y, val, base_line, render_limit, increment):
        if val > 0:
            if node_map[x][y].elevation < val + base_line and abs(val) > render_limit:
                node_map[x][y].add_elevation(val)
                Elevation.build_check(node_map, x, y, val, base_line, render_limit, increment)
        else:
            if node_map[x][y].elevation > val - base_line and abs(val) > render_limit:
                node_map[x][y].add_elevation(val)
                Elevation.build_check(node_map, x, y, val, base_line, render_limit, increment)

    @staticmethod
    def build_check(node_map, x, y, val, base_line, render_limit, increment):
        i_list = [1, 2, 3, 4]
        random.shuffle(i_list)
        while i_list:
            i = i_list.pop()
            if i == 1:
                if x > 0:
                    Elevation.build_land(node_map, x - 1, y, Maths.move_to_zero(val, increment), base_line,
                                         render_limit, increment)
                else:
                    Elevation.build_land(node_map, len(node_map) - 1, y, Maths.move_to_zero(val, increment),
                                         base_line, render_limit, increment)
            elif i == 2:
                if x < len(node_map) - 1:
                    # print len(node_map)
                    Elevation.build_land(node_map, x + 1, y, Maths.move_to_zero(val, increment), base_line,
                                         render_limit, increment)
                else:
                    Elevation.build_land(node_map, 0, y, Maths.move_to_zero(val, increment), base_line,
                                         render_limit, increment)
            elif i == 3:
                if y > 0:
                    Elevation.build_land(node_map, x, y - 1, Maths.move_to_zero(val, increment), base_line,
                                         render_limit, increment)
            elif i == 4:
                if y < len(node_map[x]) - 1:
                    Elevation.build_land(node_map, x, y + 1, Maths.move_to_zero(val, increment), base_line,
                                         render_limit, increment)
            else:
                print('something is wrong')
