#!/usr/bin/env python
from collections import defaultdict
from itertools import combinations

test_data = [
    '............',
    '........0...',
    '.....0......',
    '.......0....',
    '....0.......',
    '......A.....',
    '............',
    '............',
    '........A...',
    '.........A..',
    '............',
    '............',
]

class Cell:
    def __init__(self, row, col, data, grid):
        self.row = row
        self.col = col
        self.data = data
        self.grid = grid
        self.antinode = False

    def __repr__(self):
        return f"({self.row},{self.col}):{self.data}"

    @property
    def is_antenna(self):
        return self.data != '.'

    @property
    def index(self):
        return f"({self.row},{self.col})"

    @property
    def rows(self):
        return self.grid.rows

    @property
    def columns(self):
        return self.grid.columns

    def print(self):
        if self.antinode:
            return "#"
        else:
            return self.data


class Grid:
    def __init__(self, data, part=1):
        self.raw_data = data
        self.data = []
        self.part = part

        for row_index, columns in enumerate(data):
            row = []
            for column_index, cell_data in enumerate(columns):
                cell = Cell(row_index, column_index, cell_data, self)
                row.append(cell)
            self.data.append(row)

    def compute_antinode(self):
        # Build dict of antenna
        antennas = defaultdict(list)
        for row in self.data:
            for cell in filter(lambda x: x.is_antenna, row):
                antennas[cell.data].append(cell)

        for antenna, cells in antennas.items():
            for combination in combinations(cells, 2):
                a_cell, b_cell= combination
                # b-a
                delta_row = b_cell.row - a_cell.row
                delta_col = b_cell.col - a_cell.col

                if self.part == 1:
                    # antinode 1 : b_cell + vector 
                    # antinode 2 : a_cell - vector
                    antinode_row = b_cell.row + delta_row
                    antinode_col = b_cell.col + delta_col
                    cell = self.get_cell_at(antinode_row, antinode_col)
                    if cell is not None:
                        cell.antinode = True

                    antinode_row = a_cell.row - delta_row
                    antinode_col = a_cell.col - delta_col
                    cell = self.get_cell_at(antinode_row, antinode_col)
                    if cell is not None:
                        cell.antinode = True
                else:
                    # antinode 1 : b_cell + (vector * delta)
                    # antinode 2 : a_cell - (vector * delta)
                    a_cell.antinode = True
                    b_cell.antinode = True
                    delta = 1
                    while True:
                        antinode_row = b_cell.row + (delta_row * delta)
                        antinode_col = b_cell.col + (delta_col * delta)
                        cell = self.get_cell_at(antinode_row, antinode_col)
                        if cell is not None:
                            cell.antinode = True
                            delta += 1
                        else:
                            break

                    delta = 1
                    while True:
                        antinode_row = a_cell.row - (delta_row * delta)
                        antinode_col = a_cell.col - (delta_col * delta)
                        cell = self.get_cell_at(antinode_row, antinode_col)
                        if cell is not None:
                            cell.antinode = True
                            delta += 1
                        else:
                            break

    def get_cell_at(self, row, col):
        if row < 0:
            return None
        if col < 0:
            return None
        if row > self.rows - 1:
            return None
        if col > self.columns - 1:
            return None

        wanted_row = self.data[row]
        return wanted_row[col]

    @property
    def rows(self):
        return len(self.data)

    @property
    def columns(self):
        return len(self.data[0])

    def print(self):
        for row in self.data:
            line = ''.join(list(map(lambda x: x.print(), row)))
            print(line)


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    grid = Grid(data)
    grid.compute_antinode()
    result = 0
    for row in grid.data:
        for cell in filter(lambda x: x.antinode, row):
            result += 1
    return result

def solve_part2(data):
    grid = Grid(data, part=2)
    grid.compute_antinode()
    result = 0
    for row in grid.data:
        for cell in filter(lambda x: x.antinode, row):
            result += 1
    return result

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 14


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 34


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
