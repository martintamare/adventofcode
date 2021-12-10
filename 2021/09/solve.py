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

    def __str__(self):
        return f'{self.x},{self.y}'

    def __repr__(self):
        return f'{self}'


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def is_low_point(self):
        min_x = max(0, self.x - 1)
        min_y = max(0, self.y - 1)
        max_x = min(self.matrix.width - 1, self.x + 1)
        max_y = min(self.matrix.height - 1, self.y + 1)

        print(f'{self} -> {list(range(min_x, max_x + 1))} {list(range(min_y, max_y + 1))}')
        is_low = True
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                point = self.matrix.matrix[y][x]
                if point == self:
                    continue
                print(f'testing {x},{y} {point.height} vs {self.height}')
                if point.height < self.height:
                    is_low = False
                    break
            if not is_low:
                break
        return is_low


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
                print(f'{point}')
            self.matrix.append(matrix_row)
        print(self.matrix)

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


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 15


def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = None
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
