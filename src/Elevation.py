from Maths import Maths


class Elevation(object):
    def __init__(self):
        print 'elevation is cool'

    @staticmethod
    def flat_land(node_map, level=0.5):
        for row in node_map:
            for node in row:
                node.elevation = level

    @staticmethod
    def build_land(node_map, x, y, val, render_limit, increment):
        if val > 0:
            if node_map[x][y].elevation < val and abs(val) > render_limit:
                node_map[x][y].elevation += val
                Elevation.build_check(node_map, x, y, val, render_limit, increment)


    @staticmethod
    def build_check(node_map, x, y, val, render_limit, increment):
        #for i in range(0, 3):
        if x > 0:
            Elevation.build_land(node_map, x-1, y, Maths.move_to_zero(val, increment, 0.01), render_limit, increment)
        else:
            print 'poop'

        if y > 0:
            Elevation.build_land(node_map, x, y-1, Maths.move_to_zero(val, increment, 0.01), render_limit, increment)