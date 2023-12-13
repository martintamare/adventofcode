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
    '',
    '##..#.#..##',
    '###...#....',
    '##.##.##...',
    '....###..##',
    '####..###..',
    '##.####....',
    '...####.###',
    '###...##...',
    '##...#..###',
    '##...#.....',
    '.##..##.###',
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

class Land:
    def __init__(self, data):
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
    def reflection(self):
        print(self)
        row_match = None
        row_match_index = None
        for w_size in range(1, (self.rows // 2) + 1):
            print(f"windows size = {w_size}")
            # 0:w_size to w_size:w_size+w_size
            print("testing begining")
            match = True
            match_index = None
            for index in range(w_size):
                source_index = index
                destination_index = 2 * w_size - index - 1
                print(f"testing row {source_index} vs {destination_index}")
                source_row = self.matrix[source_index]
                destination_row = self.matrix[destination_index]
                if source_row != destination_row:
                    print("match not")
                    match = False
                    break
                else:
                    print("match OKKKKKKKKKKKKKKKKKKKKK")
                    match_index = source_index + 1
            if match:
                print("Match detected at {match_index}")
                row_match = True
                row_match_index = match_index
                continue


            match = True
            for index in range(w_size):
                source_index = index
                destination_index = 2 * w_size - index - 1
                end_source_index = self.rows - destination_index - 1
                end_destination_index = self.rows - source_index - 1
                print(f"testing row {end_source_index} vs {end_destination_index}")
                source_row = self.matrix[end_source_index]
                destination_row = self.matrix[end_destination_index]
                if source_row != destination_row:
                    print("match not")
                    match = False
                    break
                else:
                    match_index = end_source_index + 1
            if match:
                print(f"Match detected at {match_index}")
                row_match = True
                row_match_index = match_index

        if row_match:
            print(f"Match at {row_match_index=}")
            return row_match_index * 100

        column_match = None
        column_match_index = None
        for w_size in range(1, (self.columns // 2) + 1):
            print(f"windows size = {w_size}")
            # 0:w_size to w_size:w_size+w_size
            print("testing begining")
            match = True
            match_index = None
            for index in range(w_size):
                source_index = index
                destination_index = 2 * w_size - index - 1
                print(f"testing column {source_index} vs {destination_index}")
                source_column = list(map(lambda x: x[source_index], self.matrix))
                destination_column = list(map(lambda x: x[destination_index], self.matrix))
                if source_column != destination_column:
                    print("match not")
                    match = False
                    break
                else:
                    print("match OKKKKKKKKKKKKKKKKKKKKK")
                    match_index = source_index + 1
            if match:
                print("Match detected at {match_index}")
                column_match = True
                column_match_index = match_index
                continue


            match = True
            for index in range(w_size):
                source_index = index
                destination_index = 2 * w_size - index - 1
                end_source_index = self.columns - destination_index - 1
                end_destination_index = self.columns - source_index - 1
                print(f"testing column {end_source_index} vs {end_destination_index}")
                source_column = list(map(lambda x: x[end_source_index], self.matrix))
                destination_column = list(map(lambda x: x[end_destination_index], self.matrix))
                if source_column != destination_column:
                    print("match not")
                    match = False
                    break
                else:
                    match_index = end_source_index + 1
            if match:
                print(f"Match detected at {match_index}")
                column_match = True
                column_match_index = match_index

        if column_match:
            print(f"Match at {column_match_index=}")
            return column_match_index

        print(self)
        print("You not come here")
        exit(0)


def solve_part1(data):
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

    return sum(map(lambda x: x.reflection, lands))

def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 415


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
