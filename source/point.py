import math
import random


def getSurroundingPoints(point):
    pointList = [(point[0], point[1] - 1),
                 (point[0] - 1, point[1]),
                 (point[0], point[1] + 1),
                 (point[0] + 1, point[1])]
    return pointList


def getAllSurroundingPoints(point):
    pointList = [(point[0] - 1, point[1] - 1),
                 (point[0], point[1] - 1),
                 (point[0] + 1, point[1] - 1),
                 (point[0] + 1, point[1]),
                 (point[0] + 1, point[1] + 1),
                 (point[0], point[1] + 1),
                 (point[0] - 1, point[1] + 1),
                 (point[0] - 1, point[1]), ]
    return pointList


def GetPointFromDirection(position, direction):
    next_point: tuple
    if direction == 'n':
        next_point = (position[0], position[1] - 1)
    elif direction == 'e':
        next_point = (position[0] + 1, position[1])
    elif direction == 's':
        next_point = (position[0], position[1] + 1)
    elif direction == 'w':
        next_point = (position[0] - 1, position[1])
    else:
        raise ValueError
    return next_point


def GetDirectionFromPoint(point_current, point_next):
    if point_current[0] < point_next[0]:
        return 'e'
    elif point_current[0] > point_next[0]:
        return 'w'
    elif point_current[1] < point_next[1]:
        return 'n'
    else:
        return 's'


# def calculateDistance(start, end):
#     return math.sqrt(((start[0] - end[0]) ** 2) + ((start[1] - end[1]) ** 2))


def getManhattenDistance(start, end):
    return abs(int(start[0] - end[0])) + abs(int(start[1] - end[1]))


def calculateDirection(start, end):
    primary_list: list = []
    secondary_list: list = []
    third_list: list = []

    vertical_distance = end[0] - start[0]
    horizontal_distance = end[1] - start[1]

    if vertical_distance < 0:  # go west
        if horizontal_distance < 0:  # go north
            primary_list += ['n', 'w']
            secondary_list += ['s', 'e']
        elif horizontal_distance > 0:  # or go south
            primary_list += ['s', 'w']
            secondary_list += ['n', 'e']
        else:
            primary_list += 'w'
            secondary_list += ['n', 's']
            third_list += 'e'
    elif vertical_distance > 0:  # go east
        if horizontal_distance < 0:  # go north
            primary_list += ['n', 'e']
            secondary_list += ['s', 'w']
        elif horizontal_distance > 0:  # or go south
            primary_list += ['s', 'e']
            secondary_list += ['n', 'w']
        else:
            primary_list += 'e'
            secondary_list += ['n', 's']
            third_list += 'w'
    else:  # go nort or south
        secondary_list += ['e', 'w']
        if horizontal_distance < 0:  # go north
            primary_list += ['n']
            third_list += ['s']
        elif horizontal_distance > 0:  # or go south
            primary_list += ['s']
            third_list += ['n']

    random.shuffle(primary_list)
    random.shuffle(secondary_list)
    random.shuffle(third_list)
    return [primary_list, secondary_list, third_list]

# class Point(tuple):
#
#     def __new__(cls, point):
#         cls.steps = None
#         return tuple.__new__(Point, (point[0], point[1]))

# def __new__(cls, x, y):
#     return tuple.__new__(Point, (x, y))

# def __init__(self, *args, **kwargs):
#     self.steps = None
#     super().__init__(args, kwargs)

# Point.x = property(operator.itemgetter(0))
# Point.y = property(operator.itemgetter(1))
