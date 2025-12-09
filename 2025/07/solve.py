#!/usr/bin/env python

import sys
sys.path.append("../../")
from utils import Grid, Cell

test_data = [
    ".......S.......",
    "...............",
    ".......^.......",
    "...............",
    "......^.^......",
    "...............",
    ".....^.^.^.....",
    "...............",
    "....^.^...^....",
    "...............",
    "...^.^...^.^...",
    "...............",
    "..^...^.....^..",
    "...............",
    ".^.^.^.^.^...^.",
    "...............",
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
    splitted = 0
    for r_index in range(grid.rows):
        if r_index == 0:
            continue

        previous_row_index = r_index - 1
        previous_row = grid.data[previous_row_index]
        current_row = grid.data[r_index]
        for c_index in range(len(previous_row)):
            prev = previous_row[c_index].data
            cur = current_row[c_index].data
            if cur == ".":
                if prev == "|":
                    current_row[c_index].data = "|"
                elif prev == "S":
                    current_row[c_index].data = "|"
                elif prev == ".":
                    pass
            elif cur == "|":
                pass
            elif cur == "^":
                if prev == "|":
                    splitted += 1
                    if c_index > 0:
                        current_row[c_index-1].data = "|"
                    if c_index < len(current_row) - 1:
                        current_row[c_index+1].data = "|"
                elif prev == "S":
                    raise Exception("totottoto")
                elif prev == ".":
                    pass
            else:
                print(f"TODO {cur=}")
                exit(0)
    return splitted


def solve_part2(data):
    grid = CustomGrid(data, cell_obj=CustomCell)
    path_grid = CustomGrid(data.copy(), cell_obj=CustomCell)

    count = []
    for line in data:
        count_line = []
        for char in line:
            count_line.append(0)
        count.append(count_line)

    def print_count():
        lines = []
        for row in count:
            line = ' '.join(map(str, row))
            lines.append(line)
        print("\n".join(lines))



    # Compute cell cost
    for r_index in range(grid.rows):
        if r_index == 0:
            continue

        previous_row_index = r_index - 1
        previous_row = grid.data[previous_row_index]
        current_row = grid.data[r_index]
        for c_index in range(len(previous_row)):
            prev = previous_row[c_index].data
            cur = current_row[c_index].data
            if cur == ".":
                if prev == "|":
                    current_row[c_index].data = "|"
                    count[r_index][c_index] += 1
                elif prev == "S":
                    current_row[c_index].data = "|"
                    count[r_index][c_index] += 1
                elif prev == ".":
                    pass
            elif cur == "|":
                pass
            elif cur == "^":
                if prev == "|":
                    if c_index > 0:
                        current_row[c_index-1].data = "|"
                        count[r_index][c_index-1] += 1
                    if c_index < len(current_row) - 1:
                        current_row[c_index+1].data = "|"
                        count[r_index][c_index+1] += 1
                elif prev == "S":
                    raise Exception("totottoto")
                elif prev == ".":
                    pass
            else:
                print(f"TODO {cur=}")
                exit(0)

    # now compute path
    init_cell = None
    for cell in path_grid.data[0]:
        if cell.data == "S":
            init_cell = cell
            break
    cache = {}
    paths = []

    def compute_best_path(cell, path):
        if cell.row == grid.rows - 1:
            print("end")
            print(path)
            exit(0)
        path.append(cell)
        print(cell)
        exit(0)

    compute_best_path(init_cell, [])

    print(init_cell)
    print_count()
    exit(0)

    total = 0
    for line in count:
        for s in line:
            total += s
    return total



def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 21


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    #assert result == 40


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
