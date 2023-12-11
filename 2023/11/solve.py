#!/usr/bin/env python
from itertools import combinations

test_data = [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....',
]

class Pixel:
    def __init__(self, image, value, row, col, row_delta=None, col_delta=None, expansion=1):
        self._neighbors = None
        self.image = image
        self.row = row
        self.col = col
        self.value = value
        self.col_delta = col_delta
        self.row_delta = row_delta
        self.expansion = expansion

    def __repr__(self):
        return f"{self.value}"

    @property
    def type(self):
        if self.value == '.':
            return 'space'
        else:
            return 'galaxy'

    @property
    def is_space(self):
        return self.type == 'space'

    @property
    def is_galaxy(self):
        return self.type == 'galaxy'

    @property
    def position(self):
        return f"{self.row},{self.col}"

    @property
    def expanded_row(self):
        return self.row + self.row_delta * self.expansion

    @property
    def expanded_col(self):
        return self.col + self.col_delta * self.expansion


class Image:
    def __init__(self, data, matrix=None, expansion=1):
        # Build 2x2 matrix : line and columns
        self.matrix = []
        self.expansion = expansion

        if matrix is not None:
            self.matrix = matrix
            return

        for row, line in enumerate(data):
            matrix_row = []

            for col, char in enumerate(line):
                pixel = Pixel(self, char, row, col)
                matrix_row.append(pixel)
            self.matrix.append(matrix_row)

    def __repr__(self):
        display = []
        for row in self.matrix:
            line_repr = ''.join(list(map(str, row)))
            display.append(line_repr)
        return '\n'.join(display)

    @property
    def galaxies(self):
        result = []
        for row in self.matrix:
            for item in row:
                if item.is_galaxy:
                    result.append(item)
        return result

    @property
    def part1(self):
        score = 0
        combination = 0
        for source, destination in combinations(self.galaxies, 2):
            distance = self.distance_between(source, destination)
            print(f"{source.position} {destination.position} {distance=}")
            score += distance
            combination += 1
        return score

    def distance_between(self, current, goal):
        current_row = current.expanded_row
        goal_row = goal.expanded_row

        current_col = current.expanded_col
        goal_col = goal.expanded_col

        diff_row = abs(current_row - goal_row)
        diff_col = abs(current_col - goal_col)

        if diff_row % 2 == 1:
            if diff_col % 2 == 1:
                diff_row -= 1
                diff_col += 1

        return diff_row + diff_col
        return manhattan

    def next(self):
        empty_rows = []
        empty_columns = []
        for row, data in enumerate(self.matrix):
            filtered = list(filter(lambda x: x.is_galaxy, data))
            if not filtered:
                print(f'{row=} empty')
                empty_rows.append(row)

        for col in range(len(self.matrix[0])):
            row = map(lambda x: x[col], self.matrix)
            filtered = list(filter(lambda x: x.is_galaxy, row))
            if not filtered:
                print(f'{col=} empty')
                empty_columns.append(col)

        print(f"{empty_rows=} {empty_columns=}")

        row_delta = 0
        new_image_data = []
        for row, data in enumerate(self.matrix):
            new_row = []
            col_delta = 0
            for col, tile in enumerate(data):
                new_pixel = Pixel(self, tile.value, tile.row, tile.col, row_delta=row_delta, col_delta=col_delta, expansion=self.expansion)
                if col in empty_columns:
                    col_delta += 1
                new_row.append(new_pixel)

            new_image_data.append(new_row)
            if row in empty_rows:
                row_delta += 1

        return Image(data=None, matrix=new_image_data, expansion=self.expansion)




def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    image = Image(data)
    new_image = image.next()
    last_line = new_image.matrix[-1]
    for item in last_line:
        print(f"{item} {item.position} {item.row_delta=} {item.col_delta=}")
    return new_image.part1


def solve_part2(data, expansion):
    image = Image(data, expansion=expansion)
    new_image = image.next()
    return new_image.part1


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 374


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 9918828


def test_part2():
    data = test_data
    result_1 = solve_part2(data, 9)
    print(f'{result_1=}')
    assert result_1 == 1030

    data = test_data
    result_2 = solve_part2(data, 99)
    print(f'{result_2=}')

    assert result_2 == 8410


def part2():
    data = load_data()
    result = solve_part2(data, 1000000-1)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
