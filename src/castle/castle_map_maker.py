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
        return len(grid)-2, len(grid[0])-2

    @staticmethod
    def is_out_of_bounds(y, x, grid):
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
    def get_random_node(grid):
        return grid[random.randint(0, len(grid)-1)][random.randint(0, len(grid[0])-1)]

    @staticmethod
    def count_adjacent_walls(grid, x, y):
        walls = 0
        doors = 0
        count = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if CastleMapMaker.is_out_of_bounds(y=j, x=i, grid=grid):
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
    def fix_border(grid):
        for row in grid:
            for node in row:
                if node.tile.x < 1 or node.tile.y < 1:
                    node.set(node="WALL", passable=False)
                elif node.tile.x > len(grid[0])-2 or node.tile.y > len(grid)-2:
                    node.set(node="WALL", passable=False)

    @staticmethod
    def fix_doors(grid, door_list):
        remove_doors = []
        for door in door_list:
            walls = CastleMapMaker.count_adjacent_walls(grid, door['x'], door['y'])
            if walls[0] < 4 or walls[0] > 7:
                try:
                    grid[door['y']][door['x']].set()
                    print("Removing door at {0} {1}".format(door['x'], door['y']))
                except Exception as e:
                    raise Exception("Whoops: {0}/{1}\n{2})".format(door['y'], door['x'], e))
                remove_doors.append(door)
        for door in remove_doors:
            door_list.remove(door)

    @staticmethod
    def mark_dead_ends(grid, dead_end="DEAD_END"):
        for y in range(0, len(grid)):
            for x in range(0, len(grid[0])):
                if not CastleMapMaker.is_wall(grid[y][x]):
                    if CastleMapMaker.count_adjacent_walls(grid, x=x, y=y)[0] == 7:
                        grid[y][x].set(node=dead_end)

    @staticmethod
    def section_search(grid, cords, node_list):
        try:
            node = grid[cords[0]][cords[1]]
        except IndexError as e:
            raise Exception("GRUMBLE ({0}): {1}".format(cords, e))
        if node.node != "WALL" and node.tile.get_cords() not in node_list:
            node_list.append(node.tile.get_cords())
            CastleMapMaker.section_search(grid=grid, cords=node.tile.get_north(), node_list=node_list)
            CastleMapMaker.section_search(grid=grid, cords=node.tile.get_south(), node_list=node_list)
            CastleMapMaker.section_search(grid=grid, cords=node.tile.get_east(), node_list=node_list)
            CastleMapMaker.section_search(grid=grid, cords=node.tile.get_west(), node_list=node_list)
        else:
            return

    @staticmethod
    def tunnel(grid, start_point, end_point):
        cursor = start_point
        while cursor != end_point:
            # y pass
            y = cursor[0]
            x = cursor[1]
            if y < end_point[0]:
                y += 1
            elif y > end_point[0]:
                y -= 1
            node = grid[y][x]
            if CastleMapMaker.is_wall(node):
                node.set()
            # x pass
            if x < end_point[1]:
                x += 1
            elif x > end_point[1]:
                x -= 1
            node = grid[y][x]
            if CastleMapMaker.is_wall(node):
                node.set()
            cursor = (y, x)

    @staticmethod
    def place_spawners(grid, number_of_spawners=10):
        placed = 0
        while placed < number_of_spawners:
            node = CastleMapMaker.get_random_node(grid)
            if node.node == "FLOOR":
                node.set("SPAWNER", passable=True)
                placed += 1
            elif node.node == "LIGHT":
                node.set("SPAWNER_LIGHT", passable=True)
                placed += 1

    @staticmethod
    def carve_room(grid, min_size=3, max_size=10, door_max=4, center=None, overlap=False, door_list=None):
        # build room first
        room_size = (random.randint(min_size, max_size), random.randint(min_size, max_size))
        valid = CastleMapMaker.get_valid_size(grid)
        if center is None:
            center = (random.randint(2+int(room_size[0]/2), valid[0]-int(room_size[0]/2)),
                      random.randint(2+int(room_size[1]/2), valid[1]-int(room_size[1]/2)))
        left = int(center[1]-room_size[0]/2)
        right = int(center[1]+room_size[0]/2)
        top = int(center[0]-room_size[1]/2)
        bottom = int(center[0]+room_size[1]/2)
        valid_cords = []
        can_build = True
        for y in range(top, bottom):
            for x in range(left, right):
                if CastleMapMaker.is_out_of_bounds(y=y, x=x, grid=grid):
                    can_build = False
                    break
                elif not overlap and CastleMapMaker.count_adjacent_walls(grid, x, y)[0] < 9:
                    can_build = False
                    break
                else:
                    valid_cords.append((y, x))
        if can_build:
            circle = random.random()
            lit = random.random()
            if lit > 0.5:
                floor = "LIGHT"
            else:
                floor = "FLOOR"
            for cords in valid_cords:
                if right-left == bottom-top and 4 < right-left and circle > 0.6:
                    if 1 < cords[1]-left < right-left-2 or 1 < cords[0]-top < bottom-top-2:
                        grid[cords[0]][cords[1]].set(node=floor, passable=True)
                else:
                    try:
                        grid[cords[0]][cords[1]].set(node=floor, passable=True)
                    except Exception as e:
                        raise Exception("Cords are at {0} {1}: {2}".format(cords[0], cords[1], e))

            # if the door list is empty, this is the first room (probably)
            if not door_list:
                grid[center[0]][center[1]].set(node="ENTRANCE", passable=True)

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
                        print("WHOPOS: {0}\n{1}".format(e, door))
                if door_tries > 0:
                    door_tries -= 1
                else:
                    break
            return {"CORNER_1": (top, left), "CORNER_2": (bottom, right), "CENTER": center}

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
    def link_door(grid, door, max_distance=10):
        cursor = door.copy()
        distance = random.randint(0, max_distance-1)
        while distance < max_distance:
            CastleMapMaker.cursor_move(cursor)
            x = cursor['x']
            y = cursor['y']
            if not CastleMapMaker.is_out_of_bounds(y=y, x=x, grid=grid):
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
        rooms = []
        doors = []
        while CastleMapMaker.get_filled_percentage(grid) > percent_filled:
            room = CastleMapMaker.carve_room(grid, door_list=doors)
            if room:
                rooms.append(room)
        for door in doors:
            CastleMapMaker.link_door(grid, door, max_distance=width)
        CastleMapMaker.fix_doors(grid, doors)
        CastleMapMaker.fix_border(grid)
        sections = []
        for room in rooms:
            # check if its there yet
            used = False
            for cord_list in sections:
                if room["CENTER"] in cord_list:
                    used = True
                    break
            if not used:
                node_list = []
                CastleMapMaker.section_search(grid, room["CENTER"], node_list)
                sections.append(node_list)
        print("Should be {0} sections.".format(len(sections)))
        if len(sections) > 1:
            for i in range(1, len(sections)):
                if not sections[i]:
                    print("Don't know how this happened but we caught it: {0}".format(sections[i]))
                else:
                    start_point = random.choice(sections[i-1])
                    try:
                        end_point = random.choice(sections[i])
                    except Exception as e:
                        raise Exception("Why not: {0} {1}".format(sections[i], e))
                    CastleMapMaker.tunnel(grid=grid, start_point=start_point, end_point=end_point)
        CastleMapMaker.mark_dead_ends(grid)
        CastleMapMaker.place_spawners(grid)
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
                elif node.node == "SPAWNER":
                    output += '&'
                elif node.node == "DEAD_END":
                    output += '-'
                elif node.node == "DOOR":
                    output += '@'
                elif node.node == "LIGHT":
                    output += '.'
                elif node.node == "FLOOR":
                    output += ' '
                else:
                    output += '#'
            i += 1
        print(output)
