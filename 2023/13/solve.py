#!/usr/bin/env python

test_data = [
    '#.##..##.',
    '..#.##.#.',
    '##......#',
    '##......#',
    '..#.##.#.',
    '..##..##.',
    '#.#.##.#.',
    '',
    '#...##..#',
    '#....#..#',
    '..##..###',
    '#####.##.',
    '#####.##.',
    '..##..###',
    '#....#..#',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Case:
    def __init__(self, land, value, row, col):
        self.land = land
        self.value = value
        self.row = row
        self.col = col

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def invert(self):
        if self.value == '.':
            return '#'
        else:
            return '.'

class Land:
    def __init__(self, data):
        self.data = data
        self.matrix = []

        for row, line in enumerate(data):
            row_data = []
            for col, value in enumerate(line):
                case = Case(self, value, row, col)
                row_data.append(case)
            self.matrix.append(row_data)

    def __repr__(self):
        data = []
        for row in self.matrix:
            data.append(''.join(list(map(lambda x: x.value, row))))
        return '\n'.join(data)

    @property
    def rows(self):
        return len(self.matrix)
    @property
    def columns(self):
        return len(self.matrix[0])

    @property
    def iterations(self):
        new_lands = []
        for row in self.matrix:
            for cell in row:
                new_data = self.data.copy()
                row = cell.row
                col = cell.col
                new_value = cell.invert()
                new_row = list(new_data[row])
                new_row[col] = new_value
                new_data[row] = ''.join(new_row)
                yield Land(new_data)

    def reflection(self, should_not_match=None):
        row_match = None
        row_match_index = None
        for w_size in range(1, (self.rows // 2) + 1):
            match = True
            match_index = None
            for index in range(w_size):
                source_index = index
                destination_index = 2 * w_size - index - 1
                source_row = self.matrix[source_index]
                destination_row = self.matrix[destination_index]
                if source_row != destination_row:
                    match = False
                    break
                else:
                    match_index = source_index + 1
            if match:
                row_match = True
                row_match_index = match_index
                result = match_index * 100
                if should_not_match is None:
                    return result
                elif should_not_match != result:
                    return result

            match = True
            for index in range(w_size):
                source_index = index
                destination_index = 2 * w_size - index - 1
                end_source_index = self.rows - destination_index - 1
                end_destination_index = self.rows - source_index - 1
                source_row = self.matrix[end_source_index]
                destination_row = self.matrix[end_destination_index]
                if source_row != destination_row:
                    match = False
                    break
                else:
                    match_index = end_source_index + 1
            if match:
                row_match = True
                row_match_index = match_index
                result = match_index * 100
                if should_not_match is None:
                    return result
                elif should_not_match != result:
                    return result


        column_match = None
        column_match_index = None
        for w_size in range(1, (self.columns // 2) + 1):
            match = True
            match_index = None
            for index in range(w_size):
                source_index = index
                destination_index = 2 * w_size - index - 1
                source_column = list(map(lambda x: x[source_index], self.matrix))
                destination_column = list(map(lambda x: x[destination_index], self.matrix))
                if source_column != destination_column:
                    match = False
                    break
                else:
                    match_index = source_index + 1
            if match:
                column_match = True
                column_match_index = match_index
                result = match_index
                if should_not_match is None:
                    return result
                elif should_not_match != result:
                    return result

            match = True
            for index in range(w_size):
                source_index = index
                destination_index = 2 * w_size - index - 1
                end_source_index = self.columns - destination_index - 1
                end_destination_index = self.columns - source_index - 1
                source_column = list(map(lambda x: x[end_source_index], self.matrix))
                destination_column = list(map(lambda x: x[end_destination_index], self.matrix))
                if source_column != destination_column:
                    match = False
                    break
                else:
                    match_index = end_source_index + 1
            if match:
                column_match = True
                column_match_index = match_index
                result = match_index
                if should_not_match is None:
                    return result
                elif should_not_match != result:
                    return result

        return None


def load_lands(data):
    lands = []
    while len(data):
        land = []
        row = data.pop(0)
        while row:
            land.append(row)
            if len(data):
                row = data.pop(0)
            else:
                break
        obj = Land(land)
        lands.append(Land(land))
    return lands


def solve_part1(data):
    lands = load_lands(data)
    return sum(map(lambda x: x.reflection(), lands))

def solve_part2(data):
    lands = load_lands(data)
    ok_lands = []
    for land in lands:
        current_reflection = land.reflection()
        for test_land in land.iterations:
            new_reflection = test_land.reflection(current_reflection)
            if new_reflection is not None:
                ok_lands.append(new_reflection)
                break
    return sum(ok_lands)

def test_part1():
    data = test_data.copy()
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 405


def part1():
    data = load_data()
    data = data.copy()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 33735


def test_part2():
    data = test_data.copy()
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 400


def part2():
    data = load_data()
    data = data.copy()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result > 32611
    assert result < 53228


test_part1()
part1()
test_part2()
part2()
