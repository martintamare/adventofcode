#!/usr/bin/env python
from collections import defaultdict, Counter

test_data = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732",
]


class Cell:
    def __init__(self, row, column, data, grid):
        self.row = row
        self.column = column
        try:
            self.data = int(data)
        except ValueError:
            self.data = - 1
        self.grid = grid

    def __repr__(self):
        return f"({self.row},{self.column}):{self.data}"

    @property
    def index(self):
        return f"({self.row},{self.column})"

    @property
    def rows(self):
        return self.grid.rows

    @property
    def columns(self):
        return self.grid.columns

    @property
    def part(self):
        return self.grid.part

    def can_go(self, direction):
        if direction == "left":
            if self.column - 1 < 0:
                return False
        elif direction == "right":
            if self.column + 2 > self.columns:
                return False
        elif direction == "up":
            if self.row - 1 < 0:
                return False
        elif direction == "down":
            if self.row + 2 > self.rows:
                return False
        else:
            raise Exception(",dzaindazindaz")
        return True

    @property
    def can_go_left(self):
        return self.can_go("left")

    @property
    def can_go_right(self):
        return self.can_go("right")

    @property
    def can_go_up(self):
        return self.can_go("up")

    @property
    def can_go_down(self):
        return self.can_go("down")

    def print(self):
        if self.data < 0:
            return '.'
        return self.data

    def can_move(self, vector):
        if vector == (-1,0):
            return self.can_go_up
        elif vector == (1,0):
            return self.can_go_down
        elif vector == (0,1):
            return self.can_go_right
        elif vector == (0,-1):
            return self.can_go_left
        else:
            raise Exception("ndazjdnazjdkaz")

    def get_next(self, vector):
        if self.can_move(vector):
            row = self.row
            column = self.column
            row_delta = vector[0]
            column_delta = vector[1]
            cell = self.grid.data[row+row_delta][column+column_delta]
            if cell.data == self.data + 1:
                return cell
            else:
                return None
        else:
            return None

    def compute_paths(self, current_path=[]):
        current_path.append(self)

        if self.data == 9:
            print(current_path[0])
            print(current_path)
            return [current_path]

        result = []
        for vector in [(-1,0), (1,0), (0,-1), (0, 1)]:
            next_cell = self.get_next(vector)
            if next_cell is None:
                continue
            elif next_cell not in current_path:
                new_path = current_path.copy()
                result += next_cell.compute_paths(new_path)
        return result


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

    @property
    def trailheads(self):
        start = []
        for row in self.data:
            for col in filter(lambda x: x.data == 0, row):
                start.append(col)
        
        trailheads = []
        result = 0
        for cell in start:
            paths = cell.compute_paths([])
            cell_result = []
            for trailhead in paths:
                if trailhead[-1] not in cell_result:
                    cell_result.append(trailhead[-1])

            if self.part == 2:
                result += len(paths)
            else:
                result += len(cell_result)

        return result


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    grid = Grid(data)
    trailheads = grid.trailheads
    return trailheads


def solve_part2(data):
    grid = Grid(data, part=2)
    trailheads = grid.trailheads
    return trailheads


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 36


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 81


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
