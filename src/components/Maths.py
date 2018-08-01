import math
import random


class Maths(object):
    minimum = 0.001

    def __init__(self):
        print('Why are you initializing this it should be static')

    @staticmethod
    def move_to_zero(value, increment):
        if abs(value) < increment:
            return 0
        if value > 0:
            return value - random.uniform(Maths.minimum, increment)
        elif value < 0:
            return value + random.uniform(Maths.minimum, increment)
        else:
            return 0

    @staticmethod
    def collide_circle(point, circle_center, circle_radius):
        return math.sqrt((point[0]-circle_center[0])**2+(point[1]-circle_center[1])**2) < circle_radius
