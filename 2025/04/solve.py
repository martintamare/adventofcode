#!/usr/bin/env python

import sys
sys.path.append("../../")
from utils import Grid, Cell

test_data = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]

class CustomCell(Cell):
    pass

class CustomGrid(Grid):
    pass


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    grid = CustomGrid(data, cell_obj=CustomCell)
    ok_cells = []
    for cell in grid.cells:
        if cell.data != "@":
            continue
        rolls = 0
        for neighbor in cell.neighbors(inline=True, diagonals=True):
            if neighbor.data == "@":
                rolls += 1
        if rolls < 4:
            ok_cells.append(cell)
            print(f"Found cell {cell=}")
    return len(ok_cells)

def solve_part2(data):
    grid = CustomGrid(data, cell_obj=CustomCell)
    total = 0
    iteration = 1
    stop = False
    while not stop:
        print(f"{iteration=}")
        print(f"{grid}")
        ok_cells = []
        for cell in grid.cells:
            if cell.data != "@":
                continue
            rolls = 0
            for neighbor in cell.neighbors(inline=True, diagonals=True):
                if neighbor.data == "@":
                    rolls += 1
            if rolls < 4:
                ok_cells.append(cell)
                print(f"Found cell {cell=}")
        total += len(ok_cells)
        for cell in ok_cells:
            cell.data = "."
        if not ok_cells:
            stop = True
    return total


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 13


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 43


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
