import random

from castle.castle_node import CastleNode as Node


class CastleMapMaker(object):
    @staticmethod
    def get_new_grid(width, height, tile_size, style="blank"):
        grid = []
        book = {0: "WALL", 1: "FLOOR"}
        for y in range(0, height):
            grid.append([])
            for x in range(0, width):
                if style.lower() == "random":
                    node = random.randint(0, 1)
                elif style.lower() == "filled":
                    node = 0
                else:
                    node = 1
                if node > 0:
                    p = True
                else:
                    p = False
                grid[y].append(Node(node=book[node], x=x, y=y, tile_size=tile_size, passable=p))
        return grid

    @staticmethod
    def get_valid_size(grid):
        return len(grid[0])-2, len(grid)-2

    @staticmethod
    def is_out_of_bounds(x, y, grid):
        if x < 0 or x > len(grid[0])-1:
            return True
        elif y < 0 or y > len(grid)-1:
            return True
        else:
            return False

    @staticmethod
    def is_wall(node):
        if node.node == "WALL":
            return 1
        else:
            return 0

    @staticmethod
    def is_door(node):
        if node.node == "DOOR":
            return 1
        else:
            return 0

    @staticmethod
    def get_filled_percentage(grid):
        filled = 0
        total = 0
        for y in grid:
            for x in y:
                total += 1
                if x.node == "WALL":
                    filled += 1
        return int((filled/total)*100)

    @staticmethod
    def count_adjacent_walls(grid, x, y):
        walls = 0
        doors = 0
        count = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if CastleMapMaker.is_out_of_bounds(i, j, grid):
                    walls += 1
                else:
                    try:
                        walls += CastleMapMaker.is_wall(grid[j][i])
                        doors += CastleMapMaker.is_door(grid[j][1])
                    except IndexError as e:
                        raise Exception("{0}\nFucking balls: i={1}, j={2}".format(e, i, j))
                count += 1
        return walls, doors

    @staticmethod
    def carve_room(grid, min_size=3, max_size=10, door_max=4, center=None, overlap=False, door_list=None):
        # build room first
        room_size = (random.randint(min_size, max_size), random.randint(min_size, max_size))
        valid = CastleMapMaker.get_valid_size(grid)
        if center is None:
            center = (random.randint(2+int(room_size[0]/2), valid[0]-int(room_size[0]/2)),
                      random.randint(2+int(room_size[1]/2), valid[1]-int(room_size[1]/2)))
        left = int(center[0]-room_size[0]/2)
        right = int(center[0]+room_size[0]/2)
        top = int(center[1]-room_size[1]/2)
        bottom = int(center[1]+room_size[1]/2)
        valid_cords = []
        can_build = True
        for y in range(top, bottom):
            for x in range(left, right):
                if not overlap and CastleMapMaker.count_adjacent_walls(grid, x, y)[0] < 9:
                    can_build = False
                    break
                else:
                    valid_cords.append((x, y))
        if can_build:
            if random.random() > 0.6:
                circle = True
            else:
                circle = False
            for cords in valid_cords:
                if right-left == bottom-top and 4 < right-left and circle:
                    if 1 < cords[0]-left < right-left-2 or 1 < cords[1]-top < bottom-top-2:
                        grid[cords[1]][cords[0]].set(node="FLOOR", passable=True)
                else:
                    grid[cords[1]][cords[0]].set(node="FLOOR", passable=True)

            # if the door list is empty, this is the first room (probably)
            if not door_list:
                grid[center[1]][center[0]].set(node="ENTRANCE", passable=True)

            door_num = 0
            door_tries = 20
            while door_num < random.randint(1, door_max):
                side = random.randint(0, 3)
                if side == 0:
                    door = {'x': random.randint(left, right), 'y': top-1, "direction": "north"}
                elif side == 1:
                    door = {'x': random.randint(left, right), 'y': bottom, "direction": "south"}
                elif side == 2:
                    door = {'x': left-1, 'y': random.randint(top, bottom), "direction": "west"}
                else:
                    door = {'x': right, 'y': random.randint(top, bottom), "direction": "east"}
                walls, existing_doors = CastleMapMaker.count_adjacent_walls(grid, door['x'], door['y'])
                if walls < 8 and existing_doors < 1:
                    try:
                        grid[door['y']][door['x']].set(node="DOOR", passable=True)
                        door_num += 1
                        door_list.append(door)
                    except Exception as e:
                        raise Exception("WHOPOS: {0}\n{1".format(e, door))
                if door_tries > 0:
                    door_tries -= 1
                else:
                    break

    @staticmethod
    def cursor_move(cursor):
        # has the same properties as a door (x, y, direction)
        if cursor["direction"] == "north":
            cursor['y'] -= 1
        elif cursor["direction"] == "south":
            cursor['y'] += 1
        elif cursor["direction"] == "west":
            cursor['x'] -= 1
        else:
            cursor['x'] += 1

    @staticmethod
    def link_door(grid, door):
        cursor = door
        distance = 0
        while distance < 6:
            CastleMapMaker.cursor_move(cursor)
            x = cursor['x']
            y = cursor['y']
            if not CastleMapMaker.is_out_of_bounds(x, y, grid):
                if CastleMapMaker.is_wall(grid[y][x]):
                    grid[y][x].set(node="FLOOR", passable=True)
                    distance += 1
                else:
                    distance += 100
            else:
                distance += 100

    @staticmethod
    def make_test_map(width=32, height=32, tile_size=64):
        grid = []
        book = {0: "WALL", 1: "FLOOR"}
        for y in range(0, height):
            grid.append([])
            for x in range(0, width):
                node = 0
                if y > 1 or x > 1:
                    node += x % 2
                    node += y % 2
                if node > 1:
                    node = 1
                if node > 0:
                    p = True
                else:
                    p = False
                grid[y].append(Node(node=book[node], x=x, y=y, tile_size=tile_size, passable=p))
        return grid

    @staticmethod
    def make_cave_map(width=50, height=50, tile_size=64, iterations=5):
        grid = CastleMapMaker.get_new_grid(width, height, tile_size, style="random")
        for i in range(0, iterations):
            grid_copy = []
            for y in range(0, len(grid)):
                grid_copy.append([])
                for x in range(0, len(grid[y])):
                    if CastleMapMaker.count_adjacent_walls(grid, x, y)[0] > 4:
                        node = "WALL"
                        passing = False
                    else:
                        node = "FLOOR"
                        passing = True
                    grid_copy[y].append(Node(node=node, x=x, y=y, tile_size=tile_size, passable=passing))
            grid = grid_copy

        return grid

    @staticmethod
    def make_dungeon_map(width=50, height=50, tile_size=64, percent_filled=50):
        grid = CastleMapMaker.get_new_grid(width, height, tile_size, style="filled")
        doors = []
        while CastleMapMaker.get_filled_percentage(grid) > percent_filled:
            CastleMapMaker.carve_room(grid, door_list=doors)
        for door in doors:
            CastleMapMaker.link_door(grid, door)
        return grid

    @staticmethod
    def print_map(grid):
        output = "Filled: {0}%".format(CastleMapMaker.get_filled_percentage(grid))
        i = 0
        for row in grid:
            output += "\n{0}:\t".format(i)
            for node in row:
                if node.node == "ENTRANCE":
                    output += '!'
                elif node.node == "DOOR":
                    output += 'O'
                elif node.node == "FLOOR":
                    output += '.'
                else:
                    output += '#'
            i += 1
        print(output)
