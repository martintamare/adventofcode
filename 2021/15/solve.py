#!/usr/bin/env python
import sys
sys.setrecursionlimit(15000)


test_data = [
    '1163751742',
    '1381373672',
    '2136511328',
    '3694931569',
    '7463417111',
    '1319128137',
    '1359912421',
    '3125421639',
    '1293138521',
    '2311944581',
]

MIN_RISK=None
CACHE={}


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Point:
    def __init__(self, risk, x, y, matrix):
        self.matrix = matrix
        self.x = x
        self.y = y
        self.risk = risk
        self._neighbors = None
        self._min_risk = None
        self._min_risk_calculated_once = False
        self._is_valid = None
        self.cache = {}

    def __repr__(self):
        return f'{self.x},{self.y}'

    def __str__(self):
        return f'{self.x},{self.y}'

    def __hash__(self):
        return hash(f'{self.x},{self.y}')

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x

    @property
    def neighbors(self):
        if self._neighbors is not None:
            return self._neighbors

        points = []
        min_point = None
        # down
        if self.y < self.matrix.height - 1:
            neighbor = self.matrix.matrix[self.y + 1][self.x]
            points.append(neighbor)

        # right
        if self.x < self.matrix.width - 1:
            neighbor = self.matrix.matrix[self.y][self.x + 1]
            points.append(neighbor)

        # left
        if self.x > 0:
            points.append(self.matrix.matrix[self.y][self.x - 1])
        # up
        if self.y > 0:
            points.append(self.matrix.matrix[self.y - 1][self.x])

        self._neighbors = points
        return points

    def min_risk(self, visited=set()):
        global MIN_RISK

        visited.add(self)
        path_risk = sum(map(lambda x: x.risk, visited)) - self.matrix.matrix[0][0].risk
        if MIN_RISK is not None:
            if path_risk > MIN_RISK:
                return None

        if self.x == self.matrix.width - 1:
            if self.y == self.matrix.height - 1:
                if MIN_RISK is None:
                    MIN_RISK = path_risk
                    print(f'MIN_RISK {MIN_RISK}')
                elif path_risk < MIN_RISK:
                    MIN_RISK = path_risk
                    print(f'new MIN_RISK {MIN_RISK}')
                return self.risk

        init_risk = self.risk
        if self.x == 0 and self.y == 0:
            init_risk = 0

        neighbor_min_risk = None
        correct_neighbor = None
        for neighbor in self.neighbors:
            if neighbor in visited:
                continue

            new_visited = visited.copy()
            neighbor_risk = neighbor.min_risk(new_visited)
            if neighbor_risk is None:
                continue
            elif neighbor_min_risk is None:
                neighbor_min_risk = neighbor_risk
                correct_neighbor = neighbor
            elif neighbor_risk < neighbor_min_risk:
                neighbor_min_risk = neighbor_risk
                correct_neighbor = neighbor

        self._min_risk_calculated_once = True
        if neighbor_min_risk is None:
            return None
        else:
            final_risk = init_risk + neighbor_min_risk
            return final_risk


            

class Matrix:
    def __init__(self, data):
        self.matrix = []
        self.width = len(data[0])
        self.height = len(data)

        for y in range(0, self.height):
            matrix_row = []
            for x in range(0, self.width):
                height = int(data[y][x])
                point = Point(height, x, y, self)
                matrix_row.append(point)
            self.matrix.append(matrix_row)

    def __str__(self):
        rows = []
        for y in range(0, len(self.matrix[0])):
            str_row = ''
            for x in range(0, len(self.matrix)):
                str_row += f'{self.matrix[x][y].risk}'
            rows.append(str_row)

        return '\n'.join(rows) + '\n'


    def __repr__(self):
        return f'{self}'


class MatrixReloaded(Matrix):
    def __init__(self, data):
        self.matrix = []
        self.original_width = len(data[0])
        self.original_height = len(data)
        self.width = self.original_width * 5
        self.height = self.original_width * 5

        for y in range(0, self.height):
            matrix_row = []
            for x in range(0, self.width):
                x_addition = x // self.original_width
                y_addition = y // self.original_height
                x_real_index = x % self.original_width
                y_real_index = y % self.original_height

                # Init risk
                risk = int(data[y_real_index][x_real_index])

                # Add offsets
                new_risk = (risk + x_addition + y_addition) % 9

                # Reset
                if new_risk == 0:
                    new_risk = 9
                point = Point(new_risk, x, y, self)
                matrix_row.append(point)
            self.matrix.append(matrix_row)


def solve(data):
    global MIN_RISK
    MIN_RISK = None
    global CACHE
    CACHE = {}
    matrix = Matrix(data)
    start_point = matrix.matrix[0][0]
    result = start_point.min_risk()
    return result


def solve_part_2(data):
    global MIN_RISK
    MIN_RISK = None
    global CACHE
    CACHE = {}
    matrix = MatrixReloaded(data)
    start_point = matrix.matrix[0][0]
    result = start_point.min_risk()
    return result


def test_part1():
    data = test_data
    result = solve(data)
    print(f'test1 is {result}')
    assert result == 40


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 315


def part1():
    data = load_data()
    result = solve(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
