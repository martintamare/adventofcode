#!/usr/bin/env python
test_data = [
    '498,4 -> 498,6 -> 496,6',
    '503,4 -> 502,4 -> 502,9 -> 494,9',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Grid:
    def __init__(self, y_max):
        self.x_min = 0
        self.x_max = 1000
        self.y_min = 0
        self.y_max = y_max
        self.structure = []
        self.build_structure()
        self.full = False
        self.sands = 0

    def add_floor(self, y):
        for x in range(0, self.x_max+1):
            self.structure[y][x] = '#'

    def build_structure(self):
        for y in range(0, self.y_max+1):
            line = []
            for x in range(0, self.x_max+1):
                line.append('.')
            self.structure.append(line)

    def add_rocks(self, source, destination):
        x_source, y_source = source
        x_destination, y_destination = destination
        if x_source == x_destination:
            y_range = range(min(y_source, y_destination),
                            max(y_source, y_destination)+1)
            x = x_source
            for y in y_range:
                self.structure[y][x] = '#'
        else:
            x_range = range(min(x_source, x_destination),
                            max(x_source, x_destination)+1)
            y = y_source
            for x in x_range:
                self.structure[y][x] = '#'

    def __repr__(self):
        data = []
        min_x = None
        max_x = None
        for y in range(len(self.structure)):
            if y == len(self.structure) - 1:
                continue
            line = self.structure[y]
            for x in range(len(line)):
                if line[x] != '.':
                    if min_x is None:
                        min_x = x
                    elif x < min_x:
                        min_x = x
                    if max_x is None:
                        max_x = x
                    elif x > max_x:
                        max_x = x

        for line in self.structure:
            data.append(''.join(line[min_x:max_x+1]))
        return '\n'.join(data)

    def iterate(self, part=1):
        x = 500
        y = 0

        sand_x = x
        sand_y = y

        stop = False
        while not stop:
            x = sand_x
            y = sand_y

            # Down
            y += 1
            if y > self.y_max:
                self.full = True
                break
            current_block = self.structure[y][x]
            if current_block == '.':
                sand_x = x
                sand_y = y
                continue

            # Down left
            x = sand_x
            y = sand_y
            y += 1
            x -= 1
            if y > self.y_max:
                self.full = True
                break
            elif x < 0:
                self.full = True
                break
            else:
                current_block = self.structure[y][x]
                if current_block == '.':
                    sand_x = x
                    sand_y = y
                    continue

            # Down right
            x = sand_x
            y = sand_y
            y += 1
            x += 1
            if y > self.y_max:
                self.full = True
                break
            elif x > self.x_max:
                self.full = True
                break
            else:
                current_block = self.structure[y][x]
                if current_block == '.':
                    sand_x = x
                    sand_y = y
                    continue
            stop = True

        if part == 1 and self.full:
            return
        elif part == 2 and sand_x == 500 and sand_y == 0:
            self.structure[sand_y][sand_x] = 'o'
            self.sands += 1
            self.full = True
            return
        else:
            self.structure[sand_y][sand_x] = 'o'
            self.sands += 1
            return


def build_grid(data, part=1):
    y_max = None

    ranges = list(map(lambda line: list(map(lambda x: (int(x.split(',')[0]), int(x.split(',')[1])), line.split(' -> '))), data))  # noqa: gorio style
    for r in ranges:
        test_y = max(map(lambda x: x[1], r))
        if y_max is None:
            y_max = test_y
        elif test_y > y_max:
            y_max = test_y

    if part == 2:
        y_max = y_max + 2

    grid = Grid(y_max)
    for r in ranges:
        for index in range(1, len(r)):
            source = r[index-1]
            destination = r[index]
            grid.add_rocks(source, destination)
    if part == 2:
        grid.add_floor(y_max)
    return grid


def solve_part2(data):
    grid = build_grid(data, part=2)
    while not grid.full:
        grid.iterate(part=2)
    return grid.sands


def solve_part1(data):
    grid = build_grid(data)
    while not grid.full:
        grid.iterate()
    return grid.sands


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 24


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 93


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 1298


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result == 25585


test_part1()
part1()
test_part2()
part2()
