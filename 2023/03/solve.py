#!/usr/bin/env python

test_data = [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Part:
    def __init__(self, engine, value, row, col):
        self._neighbors = None
        self.engine = engine
        self.row = row
        self.col = col
        if value.isdigit():
            self.value_length = len(value)
            self.value = int(value)
            self.type = 'part'
        else:
            self.value = value
            self.value_length = 1
            if value == '.':
                self.type = 'void'
            else:
                self.type = 'operator'

    def __repr__(self):
        return f"{self.value}"

    @property
    def neighbors(self):
        if self._neighbors is not None:
            return self._neighbors

        neighbors = []

        # Will go from row-1 col-1 to row+1 col+len+1
        min_row = max(0, self.row - 1)
        max_row = min(self.row + 2, len(self.engine.matrix))

        min_col = max(0, self.col -1)
        max_col = min(self.col + self.value_length + 1, len(self.engine.matrix[0]))

        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                part = self.engine.matrix[row][col]
                if part == self:
                    continue
                if part in neighbors:
                    continue
                neighbors.append(part)

        self._neighbors = neighbors
        return neighbors


    @property
    def is_gear(self):
        if self.value != '*':
            return False
        part_neigbors = list(filter(lambda x: x.is_part, self.neighbors))
        if len(part_neigbors) == 2:
            self.gear_value = part_neigbors[0].value * part_neigbors[1].value
            return True

    @property
    def is_operator(self):
        return self.type == 'operator'

    @property
    def is_part(self):
        return self.type == 'part'

    @property
    def has_operator_in_neighbors(self):
        for neighbor in self.neighbors:
            if neighbor.is_operator:
                return True
        return False


class Engine:
    def __init__(self, data):
        # Build 2x2 matrix : line and columns
        self.matrix = []

        for row, line in enumerate(data):
            matrix_row = []

            col = 0
            while col < len(line):
                char = line[col]
                if char.isdigit():
                    start_col = col
                    current_value = char
                    col += 1
                    while True:
                        if col < len(line) and line[col].isdigit():
                            current_value += line[col]
                            col += 1
                        else:
                            break
                    part = Part(self, current_value, row, start_col) 
                    for index_to_insert in range(start_col, col):
                        matrix_row.append(part)
                else:
                    part = Part(self, char, row, col)
                    matrix_row.append(part)
                    col += 1
            self.matrix.append(matrix_row)

    @property
    def parts_with_operator(self):
        parts = []
        for row in self.matrix:
            for part in row:
                if not part.is_part:
                    continue
                if not part.has_operator_in_neighbors:
                    continue
                if part not in parts:
                    parts.append(part)
        return parts

    @property
    def gears(self):
        parts = []
        for row in self.matrix:
            for part in row:
                if part.is_gear:
                    if part not in parts:
                        parts.append(part)
        return parts



def solve_part1(data):
    engine = Engine(data)
    result = 0
    for part in engine.parts_with_operator:
        result += part.value
    return result
    return sum(map(lambda x: x.value, engine.parts_with_operator))


def solve_part2(data):
    engine = Engine(data)
    result = 0
    for part in engine.gears:
        result += part.gear_value
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 4361


def part1():
    data = load_data()
    length = len(data[0])
    for line in data:
        assert len(line) == length

    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 539590


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 467835


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
