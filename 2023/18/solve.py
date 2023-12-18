#!/usr/bin/env python
from math import inf as infinity

test_data = [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Tile:
    def __init__(self, maze, value, row, col):
        self._neighbors = None
        self._neighbors_for_astar = None
        self.maze = maze
        self.row = row
        self.col = col
        self.value = value
        self.contained = None
        self.init_for_astar()
        self.internal = False
        self.external = False

    def init_for_astar(self):
        self.gscore = infinity
        self.fscore = infinity
        self.closed = False
        self.in_openset = False
        self.came_from = None

    @property
    def neighbors_for_astar(self):
        if self._neighbors_for_astar is not None:
            return self._neighbors_for_astar

        neighbors = []

        # Will go from row-1 col-1 to row+1 col+len+1
        min_row = max(0, self.row - 1)
        max_row = min(self.row + 2, len(self.maze.array))

        min_col = max(0, self.col -1)
        max_col = min(self.col + 2, len(self.maze.array[0]))

        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                if row == self.row and col == self.col:
                    continue

                tile = self.maze.array[row][col]
                if tile.internal:
                    continue
                if tile.value in ['.']:
                    neighbors.append(tile)

        self._neighbors_for_astar = neighbors
        return neighbors


class Terrain:
    def __init__(self):
        self.matrix = {}
        self.array = []

    def add_trench(self, row, col):
        if row not in self.matrix:
            self.matrix[row] = {}
        self.matrix[row][col] = '#'

    def __repr__(self):
        min_row = min(self.matrix.keys())
        max_row = max(self.matrix.keys())

        min_col = None
        max_col = None
        for row, col_data in self.matrix.items():
            test_min_col = min(col_data.keys())
            test_max_col = max(col_data.keys())
            if min_col is None:
                min_col = test_min_col
            elif test_min_col < min_col:
                min_col = test_min_col
            if max_col is None:
                max_col = test_max_col
            elif test_max_col > max_col:
                max_col = test_max_col

        lines = []

        for row in range(min_row, max_row+1):
            line = ''
            for col in range(min_col, max_col+1):
                if row in self.matrix:
                    if col in self.matrix[row]:
                        line += self.matrix[row][col]
                    else:
                        line += '.'
                else:
                    line += '.'
            lines.append(line)

        return '\n'.join(lines)

    def fill(self):
        min_row = min(self.matrix.keys())
        max_row = max(self.matrix.keys())

        min_col = None
        max_col = None
        for row, col_data in self.matrix.items():
            test_min_col = min(col_data.keys())
            test_max_col = max(col_data.keys())
            if min_col is None:
                min_col = test_min_col
            elif test_min_col < min_col:
                min_col = test_min_col
            if max_col is None:
                max_col = test_max_col
            elif test_max_col > max_col:
                max_col = test_max_col

        real_row = 0
        for row in range(min_row-1, max_row+2):
            line = []
            real_col = 0
            for col in range(min_col-1, max_col+2):
                if row in self.matrix:
                    if col in self.matrix[row]:
                        data = self.matrix[row][col]
                        tile = Tile(self, data, real_row, real_col)
                        line.append(tile)
                    else:
                        tile = Tile(self, '.', real_row, real_col)
                        line.append(tile)
                else:
                    tile = Tile(self, '.', real_row, real_col)
                    line.append(tile)
                real_col += 1
            self.array.append(line)
            real_row += 1

        print(self)
        count = 0
        goal = self.array[0][0]
        for row, row_data in enumerate(self.array):
            row_count = 0
            for col, data in enumerate(row_data):
                if row == 0 or row == len(self.array) - 1:
                    continue
                if col == 0 or col == len(self.array[0]) - 1:
                    continue
                if data.value == '#':
                    row_count += 1
                elif data.value == '.':
                    if not self.astar(data, goal):
                        print(f"{row},{col} cannot exit")
                        row_count += 1
                        data.internal = True
                    else:
                        data.external = True
                else:
                    print('WTG????')
                    exit(0)
            row_print = list(map(lambda x: x.value, row_data))
            count += row_count
        print(self)
        return count

    def reconstruct_path(self, last):
        def _gen():
            current = last
            while current:
                yield current
                current = current.came_from

        return _gen()
    def cost_estimate(self, current, goal):
        return abs(current.row-goal.row) + abs(current.col-goal.col)

    def distance_between(self, current, goal):
        return abs(current.row-goal.row) + abs(current.col-goal.col)

    def neighbors(self, current):
        return current.neighbors_for_astar

    def is_goal_reached(self, current, goal):
        return current == goal

    def astar(self, start, goal):
        for row in self.array:
            for tile in row:
                tile.init_for_astar()

        self.valid_path = []
        if self.is_goal_reached(start, goal):
            self.valid_path = [start]
            return True

        open_set = []
        search_nodes = {}
        start_node = start
        start_node.gscore = 0.0
        start_node.fscore = self.cost_estimate(start_node, goal)

        open_set.append(start_node)

        while open_set:
            current = open_set.pop(0)

            if self.is_goal_reached(current, goal):
                return True

            current.closed = True
            #print(f"current {current.row},{current.col}")
            for neighbor in current.neighbors_for_astar:
                #print(f"neighbor {neighbor.row},{neighbor.col}")
                if neighbor.external:
                    return True
                if neighbor.internal:
                    return False
                if neighbor.closed:
                    continue

                tentative_gscore = current.gscore + self.distance_between(current, neighbor)

                if tentative_gscore >= neighbor.gscore:
                    continue

                if neighbor.in_openset:
                    open_set.remove(neighbor)

                neighbor.came_from = current
                neighbor.gscore = tentative_gscore
                neighbor.fscore = tentative_gscore + self.cost_estimate(neighbor, goal)
                open_set.append(neighbor)
        return False


def solve_part1(data):

    terrain = Terrain()

    current_row = None
    current_col = None

    for instruction in data:
        direction, amount, color = instruction.split(' ')
        amount = int(amount)
        if direction == 'R':
            delta_row = 0
            delta_col = 1
        elif direction == 'L':
            delta_row = 0
            delta_col = -1
        elif direction == 'U':
            delta_row = -1
            delta_col = 0
        elif direction == 'D':
            delta_row = 1
            delta_col = 0
        else:
            print('WTF')
            exit(0)

        for a in range(amount):
            if current_row is None:
                current_row = 0
                current_col = 0
            else:
                test_row = current_row + delta_row
                test_col = current_col + delta_col
                current_row = test_row
                current_col = test_col
            terrain.add_trench(current_row, current_col)
    return terrain.fill()

def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 62


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result < 34903


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
