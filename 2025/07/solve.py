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
    # On veut computer un chemin
    # Stocker le chemin 
    # Computer les subschema
    # A chaque diversion => gauche + droite
    # Cache malin pour un chemin donné ?
    max_row_index = len(data) - 1
    cache = {}
    ok_path = 0

    def compute_path(current_cell, path):
        nonlocal ok_path
        print(f"{path=} {ok_path=}")
        cache_key = "_".join(map(lambda x: f"{x}", path))
        if cache_key in cache:
            return cache[cache_key]

        r_index = current_cell.row
        c_index = current_cell.col
        next_cell = current_cell.down_cell
        if next_cell is None:
            cache[cache_key] = 1
            ok_path = ok_path + 1
            return 1
        else:
            next_value = next_cell.data
            if next_value == ".":
                new_path = path.copy()
                new_path.append(current_cell)
                return compute_path(next_cell, new_path)
            elif next_value == "^":
                left_cell = next_cell.left_cell
                right_cell = next_cell.right_cell
                result = 0
                if left_cell:
                    new_path = path.copy()
                    new_path.append(current_cell)
                    result += compute_path(left_cell, path=new_path)
                if right_cell:
                    new_path = path.copy()
                    new_path.append(current_cell)
                    result += compute_path(left_cell, path=new_path)
                cache_key = "_".join(map(lambda x: f"{x}", path))
                cache[cache_key] = result
                ok_path = ok_path + result
                return result

    ok_cell = None
    for cell in grid.data[0]:
        if cell.data == "S":
            ok_cell = cell

    compute_path(ok_cell, [])
    return ok_path



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
    assert result == 40


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
