#!/usr/bin/env python

from functools import cached_property
import itertools
from math import inf as infinity
from heapq import heappop, heappush

import sys
from collections import defaultdict

sys.path.append("../../")
from utils import Grid, Cell

sys.setrecursionlimit(1000000)


test_data = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############",
]

test_data_2 = [
    "#################",
    "#...#...#...#..E#",
    "#.#.#.#.#.#.#.#.#",
    "#.#.#.#...#...#.#",
    "#.#.#.#.###.#.#.#",
    "#...#.#.#.....#.#",
    "#.#.#.#.#.#####.#",
    "#.#...#.#.#.....#",
    "#.#.#####.#.###.#",
    "#.#.#.......#...#",
    "#.#.###.#####.###",
    "#.#.#...#.....#.#",
    "#.#.#.#####.###.#",
    "#.#.#.........#.#",
    "#.#.#.#########.#",
    "#S#.............#",
    "#################",
]

def update_cache(path, cache, best_cost, mins):
    current = path[0]
    current_vector = (0, 1)
    total_cost = 0
    mapping = {}
    for cell in path[1:]:
        vector = cell.get_vector_to(current)
        if vector == current_vector:
            cost = 1
        else:
            cost = 1001
        total_cost += cost
        cache_key = f"{cell.row}_{cell.col}_{vector}"
        cache[cache_key] = best_cost - total_cost
        mins[cache_key] = total_cost
        current_vector = vector
        current = cell


class CustomCell(Cell):
    def __init__(self, row, col, data, grid):
        super().__init__(row, col, data, grid)
        self.min_path = infinity

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

    @cached_property
    def path_neighbors(self):
        neighbors = []
        for attr in ["right_cell", "left_cell", "down_cell", "up_cell"]:
            cell = getattr(self, attr)
            if cell and not cell.is_wall:
                neighbors.append(cell)
        return neighbors

    def cost_to_neighbor(self, neighbor, path):
        if len(path) > 1:
            previous = path[1]
        else:
            previous = None

        if previous is None:
            vector = self.get_vector_to(neighbor)
            # Init -> only up or right ?
            if vector == (-1, 0):
                cost_to_neighbor = 1001
            elif vector == (0, 1):
                cost_to_neighbor = 1
            else:
                raise Exception('zanajdnazkjdazkdza')
        else:
            vector = self.get_vector_to(neighbor)
            previous_vector = previous.get_vector_to(self)
            if vector == previous_vector:
                cost_to_neighbor = 1
            else:
                cost_to_neighbor = 1001
        return cost_to_neighbor


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class CustomGrid(Grid):
    @property
    def start(self):
        for cell in self.cells:
            if cell.is_start:
                return cell

    @property
    def end(self):
        for cell in self.cells:
            if cell.is_end:
                return cell

    def compute_all_best_path(self, start, end):
        # compute mins based on previously computed best_path 
        mins = {start: 0}
        current = None
        previous = None
        total_cost = 0
        cache = defaultdict(int)

        # queue
        q = [
            # cost, start, path
            (0, start, []),
        ]
        mins = {}
        update_cache(self.best_path, cache, self.best_path_cost, mins)

        self.best_paths = [self.best_path]
        while q:
            (cost, cell, path) = q.pop(0)
            if cost > self.best_path_cost:
                print(f"skipping because {cost=} > {self.best_path_cost}")
                continue

            path = [cell] + path

            if cell == end:
                if cost == self.best_path_cost:
                    print("Found one more !")
                    ok_path = list(reversed(path))
                    self.best_paths.append(ok_path)
                    update_cache(ok_path, cache, self.best_path_cost, mins)


            else:
                for neighbor in cell.path_neighbors:
                    if neighbor in path:
                        continue

                    vector = neighbor.get_vector_to(cell)
                    cache_key = f"{neighbor.row}_{neighbor.col}_{vector}"
                    cache_cost = cache.get(cache_key, None)

                    cost_to_neighbor = cell.cost_to_neighbor(neighbor, path)
                    next_cost = cost + cost_to_neighbor

                    if cache_cost is not None:
                        if cost + cache_cost > self.best_path_cost:
                            continue

                    prev_cost = mins.get(cache_key, None)
                    if prev_cost is not None:
                        if prev_cost < next_cost:
                            continue
                    else:
                        mins[cache_key] = next_cost

                    q.append((next_cost, neighbor, path))



def solve_part1(data):
    grid = CustomGrid(data, cell_obj=CustomCell)
    print(grid)
    grid.compute_best_path(grid.start, grid.end)
    return grid.best_path_cost


def solve_part2(data):
    grid = CustomGrid(data, cell_obj=CustomCell)
    print(grid)
    grid.compute_best_path(grid.start, grid.end)
    grid.compute_all_best_path(grid.start, grid.end)
    cells = set()
    for path in grid.best_paths:
        for cell in path:
            cells.add(cell)
    return len(cells)


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 7036

    data = test_data_2
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 11048


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 45

    data = test_data_2
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 64


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
