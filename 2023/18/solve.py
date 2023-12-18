#!/usr/bin/env python
from math import inf as infinity
import sys

sys.setrecursionlimit(100000000)

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

    def __repr__(self):
        return self.value

    @property
    def position(self):
        return f"{self.row},{self.col}"

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

        # up
        row = self.row - 1
        col = self.col
        if row >= self.maze.min_row:
            tile = None
            if row in self.maze.matrix:
                if col in self.maze.matrix[row]:
                    tile = self.maze.matrix[row][col]
                else:
                    tile = Tile(self.maze, '.', row, col)
                    self.maze.matrix[row][col] = tile
            else:
                tile = Tile(self.maze, '.', row, col)
                self.maze.matrix[row][col] = tile
            if tile.value != '#':
                neighbors.append(tile)

        # Down
        row = self.row + 1
        col = self.col
        if row <= self.maze.max_row:
            tile = None
            if row in self.maze.matrix:
                if col in self.maze.matrix[row]:
                    tile = self.maze.matrix[row][col]
                else:
                    tile = Tile(self.maze, '.', row, col)
                    self.maze.matrix[row][col] = tile
            else:
                tile = Tile(self.maze, '.', row, col)
                self.maze.matrix[row][col] = tile
            if tile.value != '#':
                neighbors.append(tile)

        # Left
        row = self.row 
        col = self.col - 1
        if col >= self.maze.min_col:
            tile = None
            if row in self.maze.matrix:
                if col in self.maze.matrix[row]:
                    tile = self.maze.matrix[row][col]
                else:
                    tile = Tile(self.maze, '.', row, col)
                    self.maze.matrix[row][col] = tile
            else:
                tile = Tile(self.maze, '.', row, col)
                self.maze.matrix[row][col] = tile
            if tile.value != '#':
                neighbors.append(tile)

        # Right
        row = self.row
        col = self.col + 1
        if col <= self.maze.max_col:
            tile = None
            if row in self.maze.matrix:
                if col in self.maze.matrix[row]:
                    tile = self.maze.matrix[row][col]
                else:
                    tile = Tile(self.maze, '.', row, col)
                    self.maze.matrix[row][col] = tile
            else:
                tile = Tile(self.maze, '.', row, col)
                self.maze.matrix[row][col] = tile
            if tile.value != '#':
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

    @property
    def min_row(self):
        return min(self.matrix.keys())

    @property
    def max_row(self):
        return max(self.matrix.keys())

    @property
    def min_col(self):
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
        return min_col

    @property
    def max_col(self):
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
        return max_col


    def __repr__(self):

        lines = []
        for row in range(self.min_row, self.max_row+1):
            line = ''
            for col in range(self.min_col, self.max_col+1):
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

        print("Building indexes")
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
        print("Building indexes OK")


        # Add array of '.'
        min_row = self.min_row - 1
        max_row = self.max_row + 1
        min_col = self.min_col - 1
        max_col = self.max_col + 1

        print(f"{min_row=} {max_row=} {min_col=} {max_col=}")

        self.matrix[min_row] = {}
        self.matrix[max_row] = {}
        for col in range(min_col, max_col+1):
            self.matrix[min_row][col] = '.'
        for col in range(min_col, max_col+1):
            self.matrix[max_row][col] = '.'
        for row in range(min_row, max_row+1):
            if row not in self.matrix:
                self.matrix[row] = {}
            self.matrix[row][min_col] = '.'
            self.matrix[row][max_col] = '.'

        self.real_min_row = self.min_row
        self.real_max_row = self.max_row
        self.real_min_col = self.min_col
        self.real_max_col = self.max_col

        print("Flooding")
        self.flood(self.min_row, self.min_col)
        print("Flooding OK")

        count = 0
        for row in range(self.real_min_row, self.real_max_row+1):
            line = []
            for col in range(self.real_min_col, self.real_max_col+1):
                if row in self.matrix:
                    if col in self.matrix[row]:
                        data = self.matrix[row][col]
                        if data != '0':
                          count += 1
                    else:
                        count += 1


        return count



    def flood(self, row, col):
        condition_1 = row >= self.real_min_row and row <= self.real_max_row
        condition_2 = col >= self.real_min_col and col <= self.real_max_col
        condition_3 = False
        if row in self.matrix and col in self.matrix[row]:
            if self.matrix[row][col] == '.':
                condition_3 = True
        else:
            condition_3 = True

        if condition_1 and condition_2 and condition_3:
            if row in self.matrix:
                self.matrix[row][col] = '0'

            self.flood(row-1,col)
            self.flood(row+1,col)
            self.flood(row,col-1)
            self.flood(row,col+1)

    def flood_array(self, row, col):
        if ~0<row<self.rows and ~0<col<self.columns and self.array[row][col]  == '.':
            self.array[row][col] = '0'
            self.flood(row-1,col)
            self.flood(row+1,col)
            self.flood(row,col-1)
            self.flood(row,col+1)

    def reconstruct_path(self, last):
        def _gen():
            current = last
            while current:
                yield current
                current = current.came_from

        return _gen()
    def cost_estimate(self, current, goal):
        return abs(current.row-goal.row) + abs(current.col-goal.col) + 1

    def distance_between(self, current, goal):
        return abs(current.row-goal.row) + abs(current.col-goal.col)

    def neighbors(self, current):
        return current.neighbors_for_astar

    def is_goal_reached(self, current, goal):
        return current == goal

    def astar(self, start, goal):
        for row, row_data in self.matrix.items():
            for col, tile in row_data.items():
                tile.init_for_astar()

        self.valid_path = []
        if self.is_goal_reached(start, goal):
            self.valid_path = [start]
            return True

        open_set = []
        tested_set = []

        start_node = start
        start_node.gscore = 0.0
        start_node.fscore = self.cost_estimate(start_node, goal)

        open_set.append(start_node)

        while open_set:
            current = open_set.pop(0)

            if self.is_goal_reached(current, goal):
                self.valid_path = self.reconstruct_path(current)
                for node in self.valid_path:
                    node.external = True
                return True

            current.closed = True
            for neighbor in current.neighbors_for_astar:
                if neighbor.external:
                    return True
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
    terrain = Terrain()

    current_row = None
    current_col = None

    mapping_direction = {
        0: 'R',
        1: 'D',
        2: 'L',
        3: 'U',
    }

    for instruction in data:
        direction, amount, color = instruction.split(' ')
        print(color)
        real_amount = int(color[2:7], 16)
        real_direction = int(color[-2])
        if real_direction not in mapping_direction:
            print('njfkgezngkjzengkez')
            exit(0)
        direction = mapping_direction[real_direction]

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

        for a in range(real_amount):
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
    assert result == 33491


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 952408144115


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
