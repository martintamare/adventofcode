#!/usr/bin/env python

from functools import cached_property

import sys
from collections import defaultdict

sys.path.append("../../")
from utils import Grid, Cell

test_data = [
    "5,4",
    "4,2",
    "4,5",
    "3,0",
    "2,1",
    "6,3",
    "2,4",
    "1,5",
    "0,6",
    "3,3",
    "2,6",
    "5,1",
    "1,2",
    "5,5",
    "2,5",
    "6,5",
    "1,4",
    "0,4",
    "6,4",
    "1,1",
    "6,1",
    "1,0",
    "0,5",
    "1,6",
    "2,0",
]

class CustomCell(Cell):
    def __init__(self, row, col, data, grid):
        super().__init__(row, col, data, grid)

    @property
    def is_start(self):
        return self.row == 0 and self.col == 0

    @property
    def is_end(self):
        return self.row == self.grid.rows - 1 and self.col == self.grid.cols - 1

    @property
    def is_wall(self):
        return self.data == "#"

    @cached_property
    def neighbors_for_astar(self):
        return list(filter(lambda x: not x.is_wall, self.neighbors()))

    def get_vector_to(self, target):
        return (target.row-self.row, target.col-self.col)

    @property
    def path_neighbors(self):
        neighbors = []
        for attr in ["right_cell", "left_cell", "down_cell", "up_cell"]:
            cell = getattr(self, attr)
            if cell and not cell.is_wall:
                neighbors.append(cell)
        return neighbors

    def cost_to_neighbor(self, neighbor, path):
        return 1


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data, rows=71, cols=71, steps=1024):
    grid_data = []
    for row in range(rows):
        line = []
        for col in range(cols):
            line.append('.')
        grid_data.append(line)

    grid = Grid(grid_data, cell_obj=CustomCell)

    print(grid)

    for byte in data[0:steps]:
        vector = list(map(int, byte.split(',')))
        col = vector[0]
        row = vector[1]
        cell = grid.get_cell(row, col)
        cell.data = "#"

    start = grid.get_cell(0, 0)
    end = grid.get_cell(rows-1, cols-1)
    grid.compute_best_path(start, end)
    return len(grid.best_path) - 1


def solve_part2(data, rows=71, cols=71, steps=1024):
    grid_data = []
    for row in range(rows):
        line = []
        for col in range(cols):
            line.append('.')
        grid_data.append(line)

    grid = Grid(grid_data, cell_obj=CustomCell)

    print(grid)

    for byte in data[0:steps]:
        vector = list(map(int, byte.split(',')))
        col = vector[0]
        row = vector[1]
        cell = grid.get_cell(row, col)
        cell.data = "#"

    start = grid.get_cell(0, 0)
    end = grid.get_cell(rows-1, cols-1)

    for byte in data[steps:]:
        vector = list(map(int, byte.split(',')))
        col = vector[0]
        row = vector[1]
        cell = grid.get_cell(row, col)
        cell.data = "#"
        grid.compute_best_path(start, end)
        print(f"{byte=} {grid.best_path_cost=}")
        if not grid.best_path_cost:
            return byte


def test_part1():
    data = test_data
    result = solve_part1(data, 7, 7, 12)
    print(f'test1 is {result}')
    assert result == 22


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data, 7, 7, 12)
    print(f'test2 is {result}')
    assert result == "6,1"


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
