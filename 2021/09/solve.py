#!/usr/bin/env python

test_data = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Point:
    def __init__(self, height, x, y, matrix):
        self.height = height
        self.x = x
        self.y = y
        self.matrix = matrix
        self._neighbors = None
        self._is_low_point = None

    def __str__(self):
        return f'{self.height} at {self.x},{self.y}'

    def __repr__(self):
        return f'{self}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f'{self.x},{self.y}')

    @property
    def neighbors(self):
        if self._neighbors is not None:
            return self._neighbors

        neighbors = []
        min_x = max(0, self.x - 1)
        min_y = max(0, self.y - 1)
        max_x = min(self.matrix.width - 1, self.x + 1)
        max_y = min(self.matrix.height - 1, self.y + 1)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                point = self.matrix.matrix[y][x]
                if point == self:
                    continue
                neighbors.append(point)
        self._neighbors = neighbors
        return self._neighbors

    @property
    def direct_neighbors(self):
        points = []
        # left
        if self.x > 0:
            points.append(self.matrix.matrix[self.y][self.x - 1])
        # up
        if self.y > 0:
            points.append(self.matrix.matrix[self.y - 1][self.x])
        # down
        if self.y < self.matrix.height - 1:
            points.append(self.matrix.matrix[self.y + 1][self.x])
        # right
        if self.x < self.matrix.width - 1:
            points.append(self.matrix.matrix[self.y][self.x + 1])
        return points


    @property
    def is_low_point(self):
        if self._is_low_point is not None:
            return self._is_low_point

        is_low = True
        for point in self.neighbors:
            if point.height < self.height:
                is_low = False
                break
        self._is_low_point = is_low
        return is_low

    def bassin(self, visited=[]):
        points = set()
        points.add(self)

        for neighbor in self.direct_neighbors:
            if neighbor.height == 9:
                continue

            if neighbor.height > self.height:
                points.add(neighbor)
                visited.append(neighbor)
                points.update(neighbor.bassin(visited))

        return points





class Floor:
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

    def get_low_points(self):
        low_points = []
        for row in self.matrix:
            for point in row:
                if point.is_low_point:
                    low_points.append(point)
        return low_points
                


def solve_part_1(data):
    floor = Floor(data)
    low_points = floor.get_low_points()
    return sum(map(lambda x: x.height + 1, low_points))


def solve_part_2(data):
    floor = Floor(data)
    low_points = floor.get_low_points()
    bassins = []
    for low_point in low_points:
        bassin = low_point.bassin()
        bassins.append(bassin)

    lenght_bassins = sorted(list(map(len, bassins)), reverse=True)
    return lenght_bassins[0] * lenght_bassins[1] * lenght_bassins[2]


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 15


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 1134


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')
    assert result == 554


def part2():
    data = load_data()
    result = solve_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
