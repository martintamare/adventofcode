#!/usr/bin/env python

test_data = [
    '5483143223',
    '2745854711',
    '5264556173',
    '6141336146',
    '6357385478',
    '4167524645',
    '2176841721',
    '6882881134',
    '4846848554',
    '5283751526',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Octopus:
    def __init__(self, energy, x, y, matrix):
        self.energy = energy
        self.x = x
        self.y = y
        self.matrix = matrix
        self._neighbors = None
        self.flashed = False

    def __str__(self):
        return f'{self.energy} at {self.x},{self.y}'

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

    def increase_energy(self):
        self.energy += 1

    def flash(self):
        if self.flashed:
            return

        self.flashed = True

        for neighbor in self.neighbors:
            neighbor.increase_energy()


class Grid:
    def __init__(self, data):
        self.matrix = []
        self.width = len(data[0])
        self.height = len(data)
        self.total_flashes = 0
        self.step_flashes = 0

        for y in range(0, self.height):
            matrix_row = []
            for x in range(0, self.width):
                energy = int(data[y][x])
                point = Octopus(energy, x, y, self)
                matrix_row.append(point)
            self.matrix.append(matrix_row)

    def __str__(self):
        rows = []
        for row in self.matrix:
            display_row = ''.join(list(map(lambda x: f'{x.energy}', row)))
            rows.append(display_row)
        return '\n'.join(rows)

    def __repr__(self):
        return f'{self}'

    def iterate(self):
        # First, the energy level of each octopus increases by 1
        for row in self.matrix:
            for octopus in row:
                octopus.increase_energy()

        # Second steps: flash and recurse
        stop = False
        last_flash = None
        while not stop:
            flashed = 0
            for row in self.matrix:
                for octopus in row:
                    if octopus.energy > 9:
                        octopus.flash()
                    if octopus.flashed:
                        flashed += 1
            if last_flash is None:
                last_flash = flashed
            elif last_flash == flashed:
                stop = True
            else:
                last_flash = flashed

        # Third steps : reset
        step_flashes = 0
        for row in self.matrix:
            for octopus in row:
                if octopus.flashed:
                    step_flashes += 1
                    self.total_flashes += 1
                    octopus.energy = 0
                    octopus.flashed = False
        self.step_flashes = step_flashes



def solve_part_1(data):
    grid = Grid(data)
    print(f'{grid}\n')
    for i in range(0, 100):
        grid.iterate()
        print(f'grid after {i+1} step\n{grid}\n')
    return grid.total_flashes


def solve_part_2(data):
    grid = Grid(data)
    stop = False
    step = 0
    while not stop:
        grid.iterate()
        step += 1
        if grid.step_flashes == 100:
            stop = True
            print(f'step {step}\n{grid}\n')
    return step


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 1656


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 195


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
