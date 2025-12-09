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


    init_cell = None
    for cell in grid.data[0]:
        if cell.data == "S":
            init_cell = cell
            break

    cache = {}
    def compute_path(cell):
        print(f"{cell=}")
        if cell.index in cache:
            return cache[cell.index]
        current_row = cell.row
        current_col = cell.col
        next_cell = cell.down_cell
        if next_cell is None:
            return 1
        elif next_cell.data == ".":
            result = compute_path(next_cell)
            cache[cell.index] = result
            return result
        elif next_cell.data == "^":
            left_cell = next_cell.left_cell
            right_cell = next_cell.right_cell
            result = 0
            if left_cell:
                left_cell_result = compute_path(left_cell)
                result += left_cell_result
            if right_cell:
                result += compute_path(right_cell)
            cache[cell.index] = result
            return result
        else:
            print(f"WHAT TO DO {next_cell=}")
            exit(0)

    print(init_cell)
    compute_path(init_cell)
    return cache[init_cell.index]


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
