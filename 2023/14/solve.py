#!/usr/bin/env python

test_data = [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....',
]

class Cell:
    def __init__(self, land, value, row, col):
        self.land = land
        self.value = value
        self.row = row
        self.col = col

    def __repr__(self):
        return self.value

    @property
    def empty(self):
        return self.value == '.'

    @property
    def is_rock(self):
        return self.value == 'O'

    def can_move_north(self):
        if not self.is_rock:
            return False

        if self.row == 0:
            return False

        test_cell = self.land.matrix[self.row-1][self.col]

        if test_cell.empty:
            return True
        else:
            return False

    def can_move_south(self):
        if not self.is_rock:
            return False

        if self.row == self.land.rows - 1:
            return False

        test_cell = self.land.matrix[self.row+1][self.col]

        if test_cell.empty:
            return True
        else:
            return False

    def can_move_west(self):
        if not self.is_rock:
            return False

        if self.col == 0:
            return False

        test_cell = self.land.matrix[self.row][self.col-1]

        if test_cell.empty:
            return True
        else:
            return False

    def can_move_east(self):
        if not self.is_rock:
            return False

        if self.col == self.land.columns - 1:
            return False

        test_cell = self.land.matrix[self.row][self.col+1]

        if test_cell.empty:
            return True
        else:
            return False


class Land:
    def __init__(self, data):
        self.data = data
        self.matrix = []

        for row, line in enumerate(data):
            row_data = []
            for col, value in enumerate(line):
                cell = Cell(self, value, row, col)
                row_data.append(cell)
            self.matrix.append(row_data)

    def __repr__(self):
        data = []
        for row in self.matrix:
            data.append(''.join(list(map(lambda x: x.value, row))))
        return '\n'.join(data)

    @property
    def cache_key(self):
        data = []
        for row in self.matrix:
            data.append(''.join(list(map(lambda x: x.value, row))))
        return ''.join(data)

    @property
    def rows(self):
        return len(self.matrix)

    @property
    def columns(self):
        return len(self.matrix[0])

    def move_cell(self, source_cell, destination_cell):
        destination_cell_row = destination_cell.row
        destination_cell_col = destination_cell.col
        source_cell_row = source_cell.row
        source_cell_col = source_cell.col

        self.matrix[destination_cell_row][destination_cell_col] = source_cell
        source_cell.row = destination_cell_row
        source_cell.col = destination_cell_col

        self.matrix[source_cell_row][source_cell_col] = destination_cell
        destination_cell.row = source_cell_row
        destination_cell.col = source_cell_col

    def move_cell_north(self, source_cell):
        source_cell_row = source_cell.row
        source_cell_col = source_cell.col

        destination_cell_row = source_cell_row - 1
        destination_cell_col = source_cell_col
        destination_cell = self.matrix[destination_cell_row][destination_cell_col]
        self.move_cell(source_cell, destination_cell)

    def move_cell_south(self, source_cell):
        source_cell_row = source_cell.row
        source_cell_col = source_cell.col

        destination_cell_row = source_cell_row + 1
        destination_cell_col = source_cell_col
        destination_cell = self.matrix[destination_cell_row][destination_cell_col]
        self.move_cell(source_cell, destination_cell)

    def move_cell_west(self, source_cell):
        source_cell_row = source_cell.row
        source_cell_col = source_cell.col

        destination_cell_row = source_cell_row
        destination_cell_col = source_cell_col - 1
        destination_cell = self.matrix[destination_cell_row][destination_cell_col]
        self.move_cell(source_cell, destination_cell)

    def move_cell_east(self, source_cell):
        source_cell_row = source_cell.row
        source_cell_col = source_cell.col

        destination_cell_row = source_cell_row
        destination_cell_col = source_cell_col + 1
        destination_cell = self.matrix[destination_cell_row][destination_cell_col]
        self.move_cell(source_cell, destination_cell)


    def move_north(self):
        has_changes = True
        while has_changes:
            has_changes = False
            for row in self.matrix:
                for cell in row:
                    if cell.can_move_north():
                        self.move_cell_north(cell)
                        has_changes = True

    def move_south(self):
        has_changes = True
        while has_changes:
            has_changes = False
            for row in self.matrix:
                for cell in row:
                    if cell.can_move_south():
                        self.move_cell_south(cell)
                        has_changes = True

    def move_east(self):
        has_changes = True
        while has_changes:
            has_changes = False
            for row in self.matrix:
                for cell in row:
                    if cell.can_move_east():
                        self.move_cell_east(cell)
                        has_changes = True

    def move_west(self):
        has_changes = True
        while has_changes:
            has_changes = False
            for row in self.matrix:
                for cell in row:
                    if cell.can_move_west():
                        self.move_cell_west(cell)
                        has_changes = True

    def cycle(self):
        self.move_north()
        self.move_west()
        self.move_south()
        self.move_east()

    @property
    def load(self):
        score = 0
        for index, row in enumerate(self.matrix):
            weight = self.rows - index
            rocks = len(list(filter(lambda x: x.value == 'O', row)))
            print(f"{weight=} {rocks=}")
            score += weight * rocks
        return score


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    land = Land(data)
    land.move_north()
    return land.load
    print(land)
    exit(0)
    pass


def solve_part2(data):
    land = Land(data)
    iterations = 1000000000
    cache = {}
    index = 1
    cache_ok = False
    while True:
        print(f"iteration {index}/{iterations}")
        land.cycle()
        if land.cache_key in cache and not cache_ok:
            cache_index = cache[land.cache_key]
            print(f"Do something smart with {index} {cache_index}")
            iterations_remaining = iterations - index
            delta_index = index - cache_index
            iterations_to_skip = (iterations_remaining // delta_index) * delta_index
            index += iterations_to_skip
            cache_ok = True
        else:
            cache[land.cache_key] = index
        if index == iterations:
            break
        index+=1
    return land.load
    exit(0)
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 136


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 64


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
