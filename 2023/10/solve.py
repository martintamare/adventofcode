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

test_20 = [
    '...........',
    '.S-------7.',
    '.|F-----7|.',
    '.||.....||.',
    '.||.....||.',
    '.|L-7.F-J|.',
    '.|..|.|..|.',
    '.L--J.L--J.',
    '...........',
]

test_21 = [
    '..........',
    '.S------7.',
    '.|F----7|.',
    '.||....||.',
    '.||....||.',
    '.|L-7F-J|.',
    '.|..||..|.',
    '.L--JL--J.',
    '..........',
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

DEBUG = False



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

    def is_exterior(self):
        if self.contained is not None and not self.contained:
            return True
        return False

    def can_squeeze(self, to_test):
        diff_row = self.row - to_test.row
        diff_col = self.col - to_test.col
        if diff_row != 0 and diff_col != 0:
            return None

        if diff_col == 0:
            if diff_row == -1:
                print(f"testing {self.value} agains {to_test.value} {diff_row=} {diff_col=}")
                if to_test.value in ['|', '7', 'J', 'F', 'L']:
                    print("OK")
                    row = self.row + 2
                    col = self.col
                    if row < len(self.maze.matrix):
                        next_to_test = self.maze.matrix[row][col]
                        if self.row == 5 and self.col == 5:
                            print(self.maze)
                            print(f"will return {next_to_test.value} {next_to_test.position}")
                            input('test2')
                        return next_to_test

        if self.row == 5 and self.col == 5:
            print(self.maze)
            input('test')

    def is_contained(self):
        if self in self.maze.loop:
            return False

        if self.row == 0 or self.row == len(self.maze.matrix) - 1 or self.col == 0 or self.col == len(self.maze.matrix[0]) - 1:
            self.contained = False
            return False

        if not self.is_ground:
            return False

        print(f"self {self} {self.row=} {self.col=}")

        reachable = []

        # up
        min_row = max(0, self.row-1)
        max_row = min(self.row+2, len(self.maze.matrix))
        min_col = max(0, self.col-1)
        max_col = min(self.col+2, len(self.maze.matrix[0]))

        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                if row == self.row and col == self.col:
                    continue
                to_test = self.maze.matrix[row][col]
                if to_test in self.maze.loop:
                    
                    current = self
                    while True:
                        next_to_test = current.can_squeeze(to_test)
                        if next_to_test is None:
                            break
                        elif next_to_test.is_exterior():
                            self.contained = False
                            return False
                        else:
                            print("Will test next")
                            current = to_test
                            to_test = next_to_test
                elif to_test.is_exterior():
                    self.contained = False
                    return False


        if self.row == 2 and self.col == 4:
            input(f"Should be marked contained {self} {self.position} YEAH")
        return True



    def init_for_astar(self):
        self.gscore = infinity
        self.fscore = infinity
        self.closed = False
        self.in_openset = False
        self.came_from = None

    def __repr__(self):
        return f"{self.value}"
        if self in self.maze.loop:
            return f"{self.value}"

        if self.contained is not None:
            if self.contained:
                return 'I'
            else:
                return 'O'
        else:
            return f"{self.value}"

    @property
    def squeeze(self):
        return self.value in ['|', '-', '-']

    @property
    def is_pipe(self):
        return self.value not in ['.', '#']

    @property
    def is_ground(self):
        return self.value == '.'


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
            for col in range(min_col, max_col):
                if row == self.row and col == self.col:
                    continue

                tile = self.maze.matrix[row][col]
                if tile.value in ['.', '#']:
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
            print(self)
            new_value = input('Enter correct S value : ')
            self.start_tile.value = new_value

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
        if len(start_neighbors) != 2:
            print(f'Weird {len(start_neighbors)} voisins')
            for neighbor in start_neighbors:
                print(f"{neighbor} at {neighbor.position}")
            exit(0)
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
                    loop.append(current)
                    break
                else:
                    previous = current
                    current = neighbor
                    loop.append(current)
                    break
        self._loop = loop
        return loop

    def expand(self):
        new_data = []
        start_tile_row = 0
        start_tile_col = 0
        current_row = 0
        for row in self.matrix:
            new_row = []
            current_col = 0
            for tile in row:
                if tile == self.start_tile:
                    start_tile_row = current_row
                    start_tile_col = current_col

                new_row.append(tile)
                current_col += 1
                if tile in self.loop and tile.value in ['F', 'L', '-']:
                    new_row.append(Tile(self, '-', current_row, current_col))
                    current_col += 1
                else:
                    new_row.append(Tile(self, '#', current_row, current_col))
                    current_col += 1
            new_data.append(new_row)
            current_row += 1
            duplicated_row = []
            for elem in new_row:
                if elem in self.loop and elem.value in ['|', '7', 'F']:
                    duplicated_row.append(Tile(self, '|', 0, 0))
                else:
                    duplicated_row.append(Tile(self, '#', 0, 0))
            current_row += 1
            new_data.append(duplicated_row)

        final_data = []
        for line in new_data:
            final_data.append(''.join(list(map(lambda x: x.value, line))))
        new_maze = Maze(final_data)
        start_tile = new_maze.matrix[start_tile_row][start_tile_col]
        new_maze.start_tile = start_tile
        return new_maze

    @property
    def part2(self):
        contained = []
        goal = self.matrix[0][0]
        for row in self.matrix:
            for item in row:
                if item.value == '#':
                    continue
                if item not in self.loop:
                    found_path = self.astar(item, goal)
                    if found_path:
                        continue
                    else:
                        print(f'No path found for {item} {item.position=}')
                        contained.append(item)
                        DEBUG and input("Test")
        return len(contained)





    @property
    def score2(self):

        has_changes = True
        
        last_change = None
        while has_changes:
            current_change = 0
            for row in self.matrix:
                for tile in row:
                    if tile.is_contained():
                        print(f"tile {tile} {tile.position} is contained")
                        current_change += 1
            if last_change is None:
                last_change = current_change
            else:
                print(f"{last_change=} {current_change=}")
                print(self)
                input('test')
                if last_change == current_change:
                    break
                else:
                    last_change = current_change

        contained = []
        for row in self.matrix:
            for tile in row:
                if tile.is_contained():
                    contained.append(tile)
                    tile.contained = True
        print(self)
        input()
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


    def astar(self, start, goal):
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
            print(f"testing {current}@{current.position}")

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
    expanded_m = m.expand()
    print(expanded_m)
    result = expanded_m.part2
    return result
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
    #data = test_20
    #result = solve_part2(data)
    #print(f'test2 is {result}')
    #assert result == 4

    #data = test_21
    #result = solve_part2(data)
    #print(f'test2 is {result}')
    #assert result == 4

    #data = test_data_3
    #result = solve_part2(data)
    #print(f'test2 is {result}')
    #assert result == 8

    data = test_data_4
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 10


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result < 739


#test_part1()
#part1()
test_part2()
part2()
