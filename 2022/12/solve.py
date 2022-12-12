#!/usr/bin/env python
import sys
sys.setrecursionlimit(15000)


test_data = [
    'Sabqponm',
    'abcryxxl',
    'accszExk',
    'acctuvwj',
    'abdefghi',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Node:
    def __init__(self, x, y, value, grid):
        self.x = x
        self.y = y
        self.value = value
        self.grid = grid
        self._neighbors = None
        self._index = None

    @property
    def index(self):
        if self._index is not None:
            return self._index

        i = f'{self.x}_{self.y}'
        self._index = i
        return i

    def __str__(self):
        return f'{self.x},{self.y} => {self.value}'

    def __repr__(self):
        return str(self)

    @property
    def neighbors(self):
        x = self.x
        y = self.y
        for index in [
                    f'{x-1}_{y}',
                    f'{x+1}_{y}',
                    f'{x}_{y-1}',
                    f'{x}_{y+1}'
                ]:
            if index not in self.grid:
                continue
            neighbor = self.grid[index]
            if neighbor.value < self.value:
                continue
            if neighbor.value - self.value > 1:
                continue
            yield neighbor

    def find_shortest_path(self, destination, current_path=[], shortest=None):
        current_path.append(self.index)

        for n in self.neighbors:
            test_path = current_path.copy()

            if n.index == destination.index:
                print(f'Valid path of length {len(current_path)}')
                if shortest is None:
                    shortest = len(test_path)
                elif len(test_path) < shortest:
                    shortest = len(test_path)
            elif n.index in test_path:
                continue
            else:
                test = n.find_shortest_path(destination, test_path, shortest)
                if test is None:
                    continue
                elif shortest is None:
                    shortest = test
                elif test < shortest:
                    shortest = test
        return shortest

    def find_path(self, destination, current_path=[], shortest_path=None):
        print(f'{current_path}')
        current_path = current_path.copy()
        current_path.append(self.index)

        if shortest_path is not None:
            if len(current_path) >= shortest_path:
                yield [current_path]

        if self.index == destination.index:
            print('WOOOOOO2')
            print(f'{current_path} {len(current_path)}')
            yield [current_path]

        to_return_path = []
        for n in self.neighbors:
            if n.index in current_path:
                continue
            else:
                new_path = n.find_path(destination, current_path, shortest_path)  # noqa
                to_return_path += new_path
        yield to_return_path


def solve_part1(data):
    start = None
    end = None
    grid = []
    distances = []

    for x in range(len(data)):
        line = data[x]
        grid_line = []
        distance_line = []
        for y in range(len(line)):
            char = line[y]
            value = ord(char)
            if char == 'S':
                value = ord('a')
            elif char == 'E':
                value = ord('z')
            grid_line.append(value)
            distance_line.append(len(data) * len(line))
            if char == 'S':
                start = x, y
            elif char == 'E':
                end = x, y
        grid.append(grid_line)
        distances.append(distance_line)

    print(f'start is {start} and end is {end}')

    def iterate(x, y):
        if x-1 >= 0 and \
                grid[x-1][y] - grid[x][y] <= 1 and \
                distances[x-1][y] > distances[x][y] + 1:
            distances[x-1][y] = distances[x][y] + 1
            iterate(x-1, y)
        if x+1 < len(data) and \
                grid[x+1][y] - grid[x][y] <= 1 and \
                distances[x+1][y] > distances[x][y] + 1:
            distances[x+1][y] = distances[x][y] + 1
            iterate(x+1, y)
        if y-1 >= 0 and \
                grid[x][y-1] - grid[x][y] <= 1 and \
                distances[x][y-1] > distances[x][y] + 1:
            distances[x][y-1] = distances[x][y] + 1
            iterate(x, y-1)
        if y+1 < len(data[0]) and \
                grid[x][y+1] - grid[x][y] <= 1 and \
                distances[x][y+1] > distances[x][y] + 1:
            distances[x][y+1] = distances[x][y] + 1
            iterate(x, y+1)

    start_x, start_y = start
    distances[start_x][start_y] = 0
    iterate(start_x, start_y)
    end_x, end_y = end
    print(distances)
    shortest_path = distances[end_x][end_y]
    return shortest_path


def solve_part2(data):
    start = None
    end = None
    grid = []
    distances = []
    start_points = []

    for x in range(len(data)):
        line = data[x]
        grid_line = []
        distance_line = []
        for y in range(len(line)):
            char = line[y]
            value = ord(char)
            if char == 'S':
                value = ord('a')
            elif char == 'E':
                value = ord('z')
            if value == ord('a'):
                start_points.append((x, y))
            grid_line.append(value)
            distance_line.append(len(data) * len(line))
            if char == 'S':
                start = x, y
            elif char == 'E':
                end = x, y
        grid.append(grid_line)
        distances.append(distance_line)

    def iterate(x, y):
        if x-1 >= 0 and \
                grid[x-1][y] - grid[x][y] <= 1 and \
                distances[x-1][y] > distances[x][y] + 1:
            distances[x-1][y] = distances[x][y] + 1
            iterate(x-1, y)
        if x+1 < len(data) and \
                grid[x+1][y] - grid[x][y] <= 1 and \
                distances[x+1][y] > distances[x][y] + 1:
            distances[x+1][y] = distances[x][y] + 1
            iterate(x+1, y)
        if y-1 >= 0 and \
                grid[x][y-1] - grid[x][y] <= 1 and \
                distances[x][y-1] > distances[x][y] + 1:
            distances[x][y-1] = distances[x][y] + 1
            iterate(x, y-1)
        if y+1 < len(data[0]) and \
                grid[x][y+1] - grid[x][y] <= 1 and \
                distances[x][y+1] > distances[x][y] + 1:
            distances[x][y+1] = distances[x][y] + 1
            iterate(x, y+1)

    backup_distance = distances.copy()
    shortest_path = None
    for start in start_points:
        print(f'testing {start}')
        start_x, start_y = start
        distances = backup_distance.copy()
        distances[start_x][start_y] = 0
        iterate(start_x, start_y)
        end_x, end_y = end
        shortest = distances[end_x][end_y]
        print(f'shortest={shortest}')
        if shortest_path is None:
            shortest_path = shortest
        elif shortest < shortest_path:
            shortest_path = shortest
    return shortest_path


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 31


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 29


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


# test_part1()
# part1()
test_part2()
part2()
