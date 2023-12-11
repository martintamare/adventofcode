#!/usr/bin/env python
from math import inf as infinity

test_data = [
    '.....',
    '.S-7.',
    '.|.|.',
    '.L-J.',
    '.....',
]

test_data_2 = [
    '..F7.',
    '.FJ|.',
    'SJ.L7',
    '|F--J',
    'LJ...',
]

test_data_3 = [
    '.F----7F7F7F7F-7....',
    '.|F--7||||||||FJ....',
    '.||.FJ||||||||L7....',
    'FJL7L7LJLJ||LJ.L-7..',
    'L--J.L7...LJS7F-7L7.',
    '....F-J..F7FJ|L7L7L7',
    '....L7.F7||L7|.L7L7|',
    '.....|FJLJ|FJ|F7|.LJ',
    '....FJL-7.||.||||...',
    '....L---J.LJ.LJLJ...',
    ]

test_data_4 = [
    'FF7FSF7F7F7F7F7F---7',
    'L|LJ||||||||||||F--J',
    'FL-7LJLJ||||||LJL-77',
    'F--JF--7||LJLJ7F7FJ-',
    'L---JF-JLJ.||-FJLJJ7',
    '|F|F-JF---7F7-L7L|7|',
    '|FFJF7L7F-JF7|JL---7',
    '7-L-JL7||F7|L7F-7F7|',
    'L.L7LFJ|||||FJL7||LJ',
    'L7JLJL-JLJLJL--JLJ.L',
]

DEBUG = True



global_mapping = {
        '|':
        { 
         (1,0): ['|', 'L', 'J', 'S'],
         (-1,0): ['|', '7', 'F', 'S'],
         },
        '-':
        { 
         (0,1): ['-', '7', 'J', 'S'],
         (0,-1): ['-', 'L', 'F', 'S'],
         },
        'L': 
        { 
         (0,1): ['-', '7', 'J', 'S'],
         (-1,0): ['|', 'F', '7', 'S'],
         },
        'J':
        { 
         (0,-1): ['-', 'F', 'L', 'S'],
         (-1,0): ['|', 'F', '7', 'S'],
         },
        '7':
        { 
         (0,-1): ['-', 'F', 'L', 'S'],
         (1,0): ['|', 'L', 'J', 'S'],
         },
        'F':  
        { 
         (0,1): ['-', 'J', '7', 'S'],
         (1,0): ['|', 'L', 'J', 'S'],
         },
        '.': {},  
        'S': {
         (0,-1): ['-', 'F', 'L', 'S'],
         (0,1): ['-', 'J', '7', 'S'],
         (-1,0): ['|', 'F', '7', 'S'],
         (1,0): ['|', 'L', 'J', 'S'],
         }
        }

class OpenSet:
    def __init__(self):
        self.sortedlist = sortedcontainers.SortedList(key=lambda x: x.fscore)

    def push(self, item):
        item.in_openset = True
        self.sortedlist.add(item)

    def pop(self):
        item = self.sortedlist.pop(0)
        item.in_openset = False
        return item

    def remove(self, item):
        self.sortedlist.remove(item)
        item.in_openset = False

    def __len__(self) -> int:
        return len(self.sortedlist)


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

    def init_for_astar(self):
        self.gscore = infinity
        self.fscore = infinity
        self.closed = False
        self.in_openset = False
        self.came_from = None

    def __repr__(self):
        return f"{self.value}"

    @property
    def squeeze(self):
        return self.value == '|' or self.value == '-'

    @property
    def is_pipe(self):
        return self.value != '.'


    @property
    def position(self):
        return f"{self.row},{self.col}"

    def can_match_with(self, other):
        #print(f"testing neighbor {other} at {other.position}")
        vector_row = other.row - self.row
        vector_col = other.col - self.col
        #print(f"{vector_row=},{vector_col=}")
        vector = (vector_row, vector_col)
        mapping = global_mapping[self.value]
        if vector not in mapping:
            #print("No")
            return False
        can_match = mapping[vector]
        if other.value in can_match:
            #print("YES!")
            return True
        #print("No")
        return False

    @property
    def neighbors(self):
        if self._neighbors is not None:
            return self._neighbors

        neighbors = []

        # Will go from row-1 col-1 to row+1 col+len+1
        min_row = max(0, self.row - 1)
        max_row = min(self.row + 2, len(self.maze.matrix))

        min_col = max(0, self.col -1)
        max_col = min(self.col + 2, len(self.maze.matrix[0]))

        for row in range(min_row, max_row):
            if row == self.row:
                continue

            tile = self.maze.matrix[row][self.col]
            if tile.is_pipe:
                if self.can_match_with(tile):
                    neighbors.append(tile)

        for col in range(min_col, max_col):
            if col == self.col:
                continue

            tile = self.maze.matrix[self.row][col]
            if tile.is_pipe:
                if self.can_match_with(tile):
                    neighbors.append(tile)
        self._neighbors = neighbors
        return neighbors

    @property
    def in_loop(self):
        return self in self.maze.loop

    @property
    def neighbors_for_astar(self):
        if self._neighbors_for_astar is not None:
            return self._neighbors_for_astar

        neighbors = []

        # Will go from row-1 col-1 to row+1 col+len+1
        min_row = max(0, self.row - 1)
        max_row = min(self.row + 2, len(self.maze.matrix))

        min_col = max(0, self.col -1)
        max_col = min(self.col + 2, len(self.maze.matrix[0]))

        for row in range(min_row, max_row):
            if row == self.row:
                continue

            tile = self.maze.matrix[row][self.col]
            if tile in self.maze.loop:
                continue
            else:
                neighbors.append(tile)

        for col in range(min_col, max_col):
            if col == self.col:
                continue

            tile = self.maze.matrix[self.row][col]
            if tile in self.maze.loop:
                continue
            else:
                neighbors.append(tile)

        self._neighbors_for_astar = neighbors
        return neighbors






class Maze:
    def __init__(self, data, version=1):
        # Build 2x2 matrix : line and columns
        self.matrix = []
        self._loop = None

        initial_rows = len(data)
        initial_columns = len(data[0])

        if version == 2:
            matrix_row = []
            for index in range(initial_columns+2):
                tile = Tile(self, '.', 0, index)
                matrix_row.append(tile)
            self.matrix.append(matrix_row)

        for row, line in enumerate(data):
            matrix_row = []

            if version == 2:
                tile = Tile(self, '.', row+1, 0)
                matrix_row.append(tile)

            for col, char in enumerate(line):
                if version == 2:
                    tile = Tile(self, char, row+1, col+1)
                else:
                    tile = Tile(self, char, row, col)
                matrix_row.append(tile)
                if char == 'S':
                    self.start_tile = tile

            if version == 2:
                tile = Tile(self, '.', row+1, initial_columns+1)
                matrix_row.append(tile)

            self.matrix.append(matrix_row)

        if version == 2:
            matrix_row = []
            for index in range(initial_columns+2):
                tile = Tile(self, '.', 0, index)
                matrix_row.append(tile)
            self.matrix.append(matrix_row)

    def __repr__(self):
        display = []
        for row in self.matrix:
            line_repr = ''.join(list(map(str, row)))
            display.append(line_repr)
        return '\n'.join(display)

    @property
    def loop(self):
        if self._loop is not None:
            return self._loop

        start_neighbors = self.start_tile.neighbors
        assert len(start_neighbors) == 2
        start = start_neighbors[0]
        end = start_neighbors[1]
        
        previous = self.start_tile
        current = start
        loop = [previous, current]
        while current != end:
            for neighbor in current.neighbors:
                if neighbor == previous:
                    continue
                elif neighbor == end:
                    current = end
                    break
                else:
                    previous = current
                    current = neighbor
                    loop.append(current)
                    break
        self._loop = loop
        return loop

    @property
    def score2(self):
        contained = []
        goal = self.matrix[0][0]

        rows = len(self.matrix)
        columns = len(self.matrix[0])

        for index_row, row in enumerate(self.matrix):
            if index_row == 0:
                continue
            if index_row == rows - 1:
                continue

            for col_index, tile in enumerate(row):
                if col_index == 0:
                    continue
                elif col_index == columns - 1:
                    continue
                elif tile.in_loop:
                    continue
                if tile.contained is not None and tile.contained:
                    contained.append(tile)
                elif self.astart(tile, goal):
                    for tile in self.valid_path:
                        tile.contained = False

                else:
                    print(f"contained {tile.position}")
                    print("neighbors")
                    for neighbor in tile.neighbors:
                        print(f"{neighbor} {neighbor.position}")
                    for tile in self.valid_path:
                        tile.contained = True
                    contained.append(tile)
                    DEBUG and input('press enter')
                    

        print(contained)
        return len(contained)

    @property
    def score1(self):
        is_pair = (len(self.loop) % 2) == 0
        assert not is_pair
        index = int(len(self.loop) / 2) + 1
        return index

    def cost_estimate(self, current, goal):
        return abs(current.row-goal.row) + abs(current.col-goal.col)

    def distance_between(self, current, goal):
        return abs(current.row-goal.row) + abs(current.col-goal.col)

    def neighbors(self, current):
        return current.neighbors_for_astar

    def is_goal_reached(self, current, goal):
        return current == goal

    def reconstruct_path(self, last):
        def _gen():
            current = last
            while current:
                yield current
                current = current.came_from

        return _gen()


    def astart(self, start, goal):
        print(f"testing {start} {start.position}")
        for row in self.matrix:
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
                self.valid_path = self.reconstruct_path(current)
                return True

            current.closed = True
            for neighbor in current.neighbors_for_astar:
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


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    m = Maze(data)
    return m.score1


def solve_part2(data):
    m = Maze(data, version=2)
    print(m)
    return m.score2
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 4

    data = test_data_2
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 8


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 6828


def test_part2():
    data = test_data_3
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 8

    data = test_data_4
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 10


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result < 739


test_part1()
part1()
test_part2()
part2()
