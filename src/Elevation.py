from Maths import Maths
import random


class Elevation(object):
    def __init__(self):
        print 'elevation is cool'

    @staticmethod
    def flat_land(node_map, level=0.5):
        for row in node_map:
            for node in row:
                node.elevation = level

    @staticmethod
    def build_land(node_map, x, y, val, base_line, render_limit, increment):
        if val > 0:
            if node_map[x][y].elevation < val + base_line and abs(val) > render_limit:
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
                    Elevation.build_land(node_map, x - 1, y, Maths.move_to_zero(val, increment, .01), base_line,
                                         render_limit, increment)
                else:
                    Elevation.build_land(node_map, len(node_map) - 1, y, Maths.move_to_zero(val, increment, .01),
                                         base_line, render_limit, increment)
            elif i == 2:
                if x < len(node_map) - 1:
                    # print len(node_map)
                    Elevation.build_land(node_map, x + 1, y, Maths.move_to_zero(val, increment, .01), base_line,
                                         render_limit, increment)
                else:
                    Elevation.build_land(node_map, 0, y, Maths.move_to_zero(val, increment, .01), base_line,
                                         render_limit, increment)
            elif i == 3:
                if y > 0:
                    Elevation.build_land(node_map, x, y - 1, Maths.move_to_zero(val, increment, 0.01), base_line,
                                         render_limit, increment)
            elif i == 4:
                if y < len(node_map[x]) - 1:
                    Elevation.build_land(node_map, x, y + 1, Maths.move_to_zero(val, increment, 0.01), base_line,
                                         render_limit, increment)
            else:
                print 'something is wrong'
