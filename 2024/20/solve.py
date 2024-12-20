#!/usr/bin/env python
from functools import cached_property

import sys
from collections import defaultdict, Counter

sys.path.append("../../")
from utils import Grid, Cell

test_data = [
    "###############",
    "#...#...#.....#",
    "#.#.#.#.#.###.#",
    "#S#...#.#.#...#",
    "#######.#.#.###",
    "#######.#.#...#",
    "#######.#.###.#",
    "###..E#...#...#",
    "###.#######.###",
    "#...###...#...#",
    "#.#####.#.###.#",
    "#.#...#.#.#...#",
    "#.#.#.#.#.#.###",
    "#...#...#...###",
    "###############",
]

class CustomCell(Cell):
    def __init__(self, row, col, data, grid):
        super().__init__(row, col, data, grid)

    @property
    def is_start(self):
        return self.data == "S"

    @property
    def is_end(self):
        return self.data == "E"

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

    @property
    def cheat_neigbors(self):
        neighbors = []
        for attr in ["right_cell", "left_cell", "down_cell", "up_cell"]:
            cell = getattr(self, attr)
            if cell and cell.is_wall:
                neighbors.append(cell)
        return neighbors

    def cost_to_neighbor(self, neighbor, path):
        return 1


class CustomGrid(Grid):
    @cached_property
    def start(self):
        for cell in self.cells:
            if cell.is_start:
                return cell
        return None

    @cached_property
    def end(self):
        for cell in self.cells:
            if cell.is_end:
                return cell
        return None

    def find_cheats(self):
        if self.part == 1:
            self.find_cheats_part1()
        elif self.part == 2:
            self.find_cheats_part2()

    def find_cheats_part1(self):
        self.compute_best_path(self.start, self.end)
        assert self.best_path is not None

        mins = self.best_path_mins
        saves = Counter()

        for cell in self.best_path:
            for vector in [(0,1), (0,-1), (1,0), (-1, 0)]:
                neighbor = cell.get_next(vector)
                if neighbor is None:
                    continue
                elif not neighbor.is_wall:
                    continue

                should_be_in_path = neighbor.get_next(vector)
                if should_be_in_path is None:
                    continue
                elif should_be_in_path not in mins:
                    continue

                current_cell_min = mins[cell]
                shortcut_min = mins[should_be_in_path]
                if shortcut_min > current_cell_min:
                    # it takes two pico secondes for shortcut
                    save = shortcut_min - current_cell_min - 2
                    saves[save] += 1

        self.saves = saves

    def find_cheats_part2(self):
        self.compute_best_path(self.start, self.end)
        assert self.best_path is not None

        mins = self.best_path_mins
        saves = Counter()

        # Compute manhattan distance for every cell
        # If < 20 and cell in path and destination in path and better cost : add
        total = len(self.best_path)
        for source_index, source in enumerate(self.best_path):
            print(f"{source_index}/{total}")
            for destination_index, destination in enumerate(self.best_path):
                distance = self.manhattan_distance(source, destination)
                if distance > 20:
                    continue

                destination_min = mins[destination]
                source_min = mins[source]
                if destination_min <= source_min:
                    continue
                elif destination_min - source_min - distance <= 0:
                    continue

                # it takes distance pico secondes for shortcut
                save = destination_min - source_min - distance
                cheat = f"{source}_{destination}"
                saves[save] += 1

        self.saves = saves


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    grid = CustomGrid(data, cell_obj=CustomCell)
    grid.find_cheats()

    result = 0
    for save in sorted(grid.saves.keys()):
        total = grid.saves[save]
        print(f"{save=} {total=}")
        if save >= 100:
            result += total
    return result


def solve_part2(data, wanted_min_save):
    grid = CustomGrid(data, cell_obj=CustomCell, part=2)
    grid.find_cheats()

    result = 0
    for save in sorted(grid.saves.keys()):
        total = grid.saves[save]
        print(f"{save=} {total=}")
        if save >= wanted_min_save:
            result += total
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data, 50)
    print(f'test2 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data, 100)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
