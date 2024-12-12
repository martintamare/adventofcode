#!/usr/bin/env python
import sys

sys.path.append("../../")
from utils import Grid, Cell
from collections import defaultdict
from functools import cached_property

test_data = [
    "AAAA",
    "BBCD",
    "BBCC",
    "EEEC",
]

test_data_2 = [
    "OOOOO",
    "OXOXO",
    "OOOOO",
    "OXOXO",
    "OOOOO",
]

test_data_3 = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE",
]

test_data_4 = [
    "EEEEE",
    "EXXXX",
    "EEEEE",
    "EXXXX",
    "EEEEE",

]

test_data_5 = [
    "AAAAAA",
    "AAABBA",
    "AAABBA",
    "ABBAAA",
    "ABBAAA",
    "AAAAAA",
]

class Fence:
    def __init__(self, direction):
        self.direction = direction
        self.cells = []

    def add_cell(self, cell):
        if cell not in self.cells:
            self.cells.append(cell)

    def __repr__(self):
        cells = self.cells
        direction = self.direction
        return f"{direction=} {cells=}"

class CustomCell(Cell):
    def __init__(self, row, col, data, grid):
        super().__init__(row, col, data, grid)
        self.fences = []

    @cached_property
    def neighbors(self, inline=True, diagonals=False, fullline=False):
        all_neighbors = super().neighbors(inline, diagonals, fullline)
        return list(filter(lambda x: x.data == self.data, all_neighbors))

    def add_fence(self, fence):
        if fence not in self.fences:
            self.fences.append(fence)

    def has_fence(self, direction):
        for fence in self.fences:
            if fence.direction == direction:
                return True
        return False

    def get_fence(self, direction):
        for fence in self.fences:
            if fence.direction == direction:
                return fence
        return None



def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Region:
    def __init__(self, name):
        self.name = name
        self.cells = []
        self.fences = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def __repr__(self):
        return f"{self.name=} {self.cells=}"

    @property
    def aera(self):
        return len(self.cells)

    @property
    def perimeter(self):
        result = 0
        for cell in self.cells:
            result += 4 - len(cell.neighbors)
        return result

    @property
    def sides(self):
        return len(self.fences)

    def populate(self):
        to_test = [self.cells[0]]
        while len(to_test):
            cell = to_test.pop()
            for neighbor in cell.neighbors:
                if neighbor not in self.cells:
                    self.cells.append(neighbor)
                    to_test.append(neighbor)

    def compute_fences(self):

        def add_fence(cell, direction):
            fence = Fence(direction)
            fence.add_cell(cell)
            self.fences.append(fence)
            cell.add_fence(fence)

        to_test = [self.cells[0]]
        tested = []

        while len(to_test):
            cell = to_test.pop()
            if cell in tested:
                continue

            for direction in ["right", "down", "left", "up"]:
                attr = f"{direction}_cell"
                create_fence = True
                test_cell = getattr(cell, attr)
                if test_cell:
                    if test_cell.data == cell.data:
                        to_test.append(to_test)
                        create_fence = False
                if create_fence:
                    add_fence(cell, direction)

            directions = {
                "right": ["up_cell", "down_cell"],
                "down": ["left_cell", "right_cell"],
                "left": ["up_cell", "down_cell"],
                "up": ["left_cell", "right_cell"],
            }
            for direction, neighbors in directions.items():
                attr = f"{direction}_cell"
                test_cell = getattr(cell, attr)
                create_fence = True
                if test_cell and test_cell.data == cell.data:
                    create_fence = False
                    to_test.append(test_cell)

                if create_fence:
                    for neighbor in neighbors:
                        test_cell = getattr(cell, neighbor)
                        if test_cell and test_cell.data == cell.data:
                            if test_cell.has_fence(direction):
                                fence = test_cell.get_fence(direction)
                                fence.add_cell(cell)
                                cell.add_fence(fence)
                                create_fence = False
                                break
                if create_fence:
                    add_fence(cell, direction)

            tested.append(cell)


    def is_valid_cell(self, test_cell):
        if self.name != test_cell.data:
            return False

        for cell in self.cells:
            if test_cell in cell.neighbors():
                return True
        return False



def solve_part1(data):
    regions = []
    grid = Grid(data, cell_obj=CustomCell)
    print(grid)
    inserted = []

    for cell in grid.cells:
        print(f"testing {cell=}")
        if cell in inserted:
            continue
        else:
            print(f"Creating region for {cell}")
            region = Region(cell.data)
            region.add_cell(cell)
            region.populate()
            regions.append(region)
            inserted += region.cells

    result = 0
    for region in regions:
        print(f"{region.name=} {region.aera=} {region.perimeter=}")
        result += region.aera * region.perimeter
    return result


def solve_part2(data):
    regions = []
    grid = Grid(data, cell_obj=CustomCell)
    print(grid)
    inserted = []

    for cell in grid.cells:
        print(f"testing {cell=}")
        if cell in inserted:
            continue
        else:
            print(f"Creating region for {cell}")
            region = Region(cell.data)
            region.add_cell(cell)
            region.populate()
            region.compute_fences()
            regions.append(region)
            inserted += region.cells

    result = 0
    for region in regions:
        print(f"{region.name=} {region.aera=} {region.sides=}")
        for fence in region.fences:
            print(fence)
        result += region.aera * region.sides
    return result


def test_part1():
    data = test_data_2
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 772

    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 140

    data = test_data_3
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 1930


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 80

    data = test_data_2
    result = solve_part2(data)
    print(f'test2_2 is {result}')
    assert result == 436

    data = test_data_3
    result = solve_part2(data)
    print(f'test2_3 is {result}')
    assert result == 1206

    data = test_data_4
    result = solve_part2(data)
    print(f'test2_4 is {result}')
    assert result == 236

    data = test_data_5
    result = solve_part2(data)
    print(f'test2_5 is {result}')
    assert result == 368


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
