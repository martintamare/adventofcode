#!/usr/bin/env python

test_data = [
    '6,10',
    '0,14',
    '9,10',
    '0,3',
    '10,4',
    '4,11',
    '6,0',
    '6,12',
    '4,1',
    '0,13',
    '10,12',
    '3,4',
    '3,0',
    '8,4',
    '1,10',
    '2,14',
    '8,10',
    '9,0',
    '',
    'fold along y=7',
    'fold along x=5',
]

class Point:
    def __init__(self, x, y, matrix):
        self.matrix = matrix
        self.x = x
        self.y = y
        self.value = '.'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

class Matrix:
    def __init__(self, max_x, max_y):
        self.matrix = []

        for x in range(0, max_x+1):
            column = []
            for y in range(0, max_y+1):
                column.append(Point(x, y, self))
            self.matrix.append(column)
        self.height = len(self.matrix[0])
        self.width = len(self.matrix)

    def __str__(self):
        rows = []
        for y in range(0, len(self.matrix[0])):
            str_row = ''
            for x in range(0, len(self.matrix)):
                str_row += self.matrix[x][y].value
            rows.append(str_row)

        return '\n'.join(rows) + '\n'

    def __repr__(self):
        return f'{self}'

    def fold(self, axis, index):

        new_matrix = []
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0

        if axis == 'y':
            max_y = index
            max_x = self.width
        elif axis == 'x':
            max_y = self.height
            max_x = index

        print(f'fold along axis {axis}={index}')
        print(f'x = {self.width} y = {self.height}')
        print(f'x = {max_x} y = {max_y}')

        rows = []
        for y in range(0, len(self.matrix[0])):
            str_row = ''
            for x in range(0, len(self.matrix)):
                if axis == 'y' and y == index:
                    str_row += '='
                elif axis == 'x' and x == index:
                    str_row += '|'
                else:
                    str_row += self.matrix[x][y].value
            rows.append(str_row)
        to_print = '\n'.join(rows) + '\n'
        #print(to_print)
        input('press enter')

        for x in range(0, max_x):
            column = []
            for y in range(0, max_y):
                new_point = Point(x, y, self)
                existing_points = []
                new_point.value = self.matrix[x][y].value
                if axis == 'y':
                    opposity_y = 2 * index - y
                    if len(self.matrix[x]) > opposity_y:
                        existing_points.append(self.matrix[x][opposity_y])
                elif axis == 'x':
                    opposity_x = 2 * index - x
                    if len(self.matrix) > opposity_x:
                        existing_points.append(self.matrix[opposity_x][y])
                for point in existing_points:
                    if point.value == '#':
                        new_point.value = '#'
                        break
                column.append(new_point)

            new_matrix.append(column)
        self.matrix = new_matrix
        self.height = len(new_matrix[0])
        self.width = len(new_matrix)

    @property
    def dots(self):
        dot = 0
        for row in self.matrix:
            for col in row:
                if col.value == '#':
                    dot += 1
        return dot


def solve_part_1(data, part=1):

    method = 1
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    coords = []
    folds = []
    for line in data:
        if method == 1:
            if not line:
                method = 2
                continue

            x = int(line.split(',')[0])
            y = int(line.split(',')[1])
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            coords.append((x,y))
        elif method == 2:
            wanted_part = line.split(' ')[2]
            axis = wanted_part.split('=')[0]
            index = int(wanted_part.split('=')[1])
            folds.append((axis, index))

    print(f'{max_x}, {max_y}')
    matrix = Matrix(max_x, max_y)

    for coord in coords:
        x, y = coord
        matrix.matrix[x][y].value = '#'

    for fold in folds:
        axis, index = fold
        matrix.fold(axis, index)
        if part == 1:
            return matrix.dots
    print(f'{matrix}')
    input()
    return 0


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 17


def test_part2():
    data = test_data
    result = solve_part_1(data, part=2)
    print(f'test2 is {result}')


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')
    assert result == 788


def part2():
    data = load_data()
    result = solve_part_1(data, part=2)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
