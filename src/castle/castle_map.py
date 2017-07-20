from castle_node import CastleNode as Node


class CastleMap(object):
    def __init__(self, width=50, height=50):
        self.x = []
        self.y = []
        for _ in range(0, width):
            self.x.append(Node())
        for _ in range(0, height):
            self.y.append(Node())
