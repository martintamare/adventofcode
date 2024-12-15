#!/usr/bin/env python
import sys

sys.path.append("../../")
from utils import Grid, Cell
from functools import cached_property
from collections import Counter, defaultdict

test_data = [
    "p=0,4 v=3,-3",
    "p=6,3 v=-1,-3",
    "p=10,3 v=-1,2",
    "p=2,0 v=2,-1",
    "p=0,0 v=1,3",
    "p=3,0 v=-2,-2",
    "p=7,6 v=-1,-3",
    "p=3,0 v=-1,-2",
    "p=9,3 v=2,3",
    "p=7,3 v=-1,2",
    "p=2,4 v=2,-3",
    "p=9,5 v=-3,-3",
]


class CustomCell(Cell):
    def __init__(self, row, col, data, grid):
        super().__init__(row, col, data, grid)

    @cached_property
    def quadrant(self):
        row = self.row
        col = self.col
        middle_row = int(self.grid.rows - 1) / 2
        middle_col = int(self.grid.cols - 1) / 2
        if row == middle_row:
            return None
        elif col == middle_col:
            return None

        quadrant = ""
        if row < middle_row:
            quadrant += "u"
        else:
            quadrant += "d"

        if col < middle_col:
            quadrant += "l"
        else:
            quadrant += "r"
        return quadrant





def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Robot:
    def __init__(self, cell, velocity):
        self.cell = cell
        self.velocity = velocity
        self.grid = cell.grid

    def __repr__(self):
        return f"Robot {self.cell=} {self.velocity=}"

    def move(self, seconds):
        delta_row = seconds * self.velocity[0]
        delta_col = seconds * self.velocity[1]
        new_row = (self.cell.row + delta_row) % self.cell.grid.rows
        new_col = (self.cell.col + delta_col) % self.cell.grid.cols
        self.cell = self.grid.data[new_row][new_col]


def solve_part1(data, row, col):
    grid_data = []
    for r in range(row):
        line = []
        for c in range(col):
            line.append('.')
        grid_data.append(line)
    grid = Grid(grid_data, cell_obj=CustomCell)

    robots = []
    for r_data in data:
        print(r_data)
        position = list(map(int, r_data.split(' ')[0].strip().split('=')[1].strip().split(',')))
        velocity = list(map(int, r_data.split(' ')[1].strip().split('=')[1].strip().split(',')))
        cell = grid.data[position[1]][position[0]]
        robot = Robot(cell, (velocity[1], velocity[0]))
        robots.append(robot)


    counter = Counter(map(lambda x: x.cell, robots))
    print(counter)

    for robot in robots:
        robot.move(100)

    quadrants = defaultdict(list)
    for cell in map(lambda x: x.cell, robots):
        if cell.quadrant is not None:
            quadrants[cell.quadrant].append(cell)

    result = 1
    for quadrant, cells in quadrants.items():
        print(f"{quadrant=}")
        counter = Counter(cells)
        print(counter)
        print(counter.total())
        result *= counter.total()
    return result


def solve_part2(data, row, col):
    grid_data = []
    for r in range(row):
        line = []
        for c in range(col):
            line.append('.')
        grid_data.append(line)
    grid = Grid(grid_data, cell_obj=CustomCell)

    robots = []
    for r_data in data:
        print(r_data)
        position = list(map(int, r_data.split(' ')[0].strip().split('=')[1].strip().split(',')))
        velocity = list(map(int, r_data.split(' ')[1].strip().split('=')[1].strip().split(',')))
        cell = grid.data[position[1]][position[0]]
        robot = Robot(cell, (velocity[1], velocity[0]))
        robots.append(robot)



    stop = False
    iteration = 0
    while not stop:
        iteration += 1
        print(f"{iteration=}")
        for robot in robots:
            robot.move(1)
        cells = set(map(lambda x: x.cell, robots))
        if len(cells) == len(robots):
            stop = True

    return iteration


def test_part1():
    data = test_data
    result = solve_part1(data, row=7, col=11)
    print(f'test1 is {result}')
    assert result == 12


def part1():
    data = load_data()
    result = solve_part1(data, row=103, col=101)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data, row=103, col=101)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
part2()
