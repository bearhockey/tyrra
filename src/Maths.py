import random


class Maths(object):
    def __init__(self):
        print 'Maths'

    @staticmethod
    def move_to_zero(value, increment, minimum):
        if abs(value) < increment:
            return 0
        if value > 0:
            return value - random.uniform(minimum, increment)
        elif value < 0:
            return value + random.uniform(minimum, increment)
        else:
            return 0
