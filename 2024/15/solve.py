#!/usr/bin/env python
import sys

sys.path.append("../../")
from utils import Grid, Cell

test_data = [
    "##########",
    "#..O..O.O#",
    "#......O.#",
    "#.OO..O.O#",
    "#..O@..O.#",
    "#O#..O...#",
    "#O..O..O.#",
    "#.OO.O.OO#",
    "#....O...#",
    "##########",
    "",
    "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^",
    "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v",
    "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<",
    "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^",
    "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><",
    "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^",
    ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^",
    "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>",
    "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>",
    "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^",
]

test_data_2 = [
    "########",
    "#..O.O.#",
    "##@.O..#",
    "#...O..#",
    "#.#.O..#",
    "#...O..#",
    "#......#",
    "########",
    "",
    "<^^>>>vv<v>>v<<",
]

class CustomCell(Cell):
    def __init__(self, row, col, data, grid):
        super().__init__(row, col, data, grid)

    @property
    def is_wall(self):
        return self.data == "#"

    @property
    def is_box(self):
        return self.data == "O"

    @property
    def is_robot(self):
        return self.data == "@"

    @property
    def is_empty(self):
        return self.data == "."

    def can_robot_move(self, vector):
        next_cell = self.get_next(vector)
        print(f"{self} {vector=} {next_cell=}")
        if next_cell is None:
            return False
        elif next_cell.is_wall:
            return False
        elif next_cell.is_box:
            return next_cell.can_robot_move(vector)
        elif next_cell.is_empty:
            return True
        else:
            raise Exception("dnazjkdnazjkdnazjk")

    def move(self, vector):
        to_return = None
        if self.can_robot_move(vector):
            next_cell = self.get_next(vector)
            if next_cell.is_box:
                next_cell.move(vector)

            if next_cell.is_empty:
                next_cell.data = self.data
                self.data = "."
                if next_cell.is_robot:
                    return next_cell
        else:
            return self


class Grid:
    def __init__(self, data, part=1, cell_obj=CustomCell):
        self.raw_data = data
        self.data = []
        self.part = part
        self.robot = None

        for row_index, cols in enumerate(data):
            row = []
            for col_index, cell_data in enumerate(cols):
                cell = cell_obj(row_index, col_index, cell_data, self)
                if cell.is_robot:
                    self.robot = cell
                row.append(cell)
            self.data.append(row)

    @property
    def rows(self):
        return len(self.data)

    @property
    def cols(self):
        return len(self.data[0])

    @property
    def nb_cells(self):
        return self.rows * self.cols

    @property
    def cells(self):
        for row in self.data:
            for cell in row:
                yield cell

    @property
    def gps(self):
        result = 0
        for cell in self.cells:
            if cell.is_box:
                row = cell.row
                col = cell.col
                result += row * 100 + col
        return result

    def __repr__(self):
        lines = []
        for row in self.data:
            line = ''.join(list(map(lambda x: x.print(), row)))
            lines.append(line)
        return "\n".join(lines)


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    grid_data = []
    instructions = ""

    mode = "grid"
    for item in data:
        if not item:
            mode = "instructions"
        if mode == "grid":
            grid_data.append(item)
        elif mode == "instructions":
            instructions += item

    grid = Grid(grid_data)
    robot = grid.robot
    vectors = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }
    for instruction in instructions:
        vector = vectors[instruction]
        robot = robot.move(vector)
    print(grid)
    return grid.gps


def solve_part2(data):
    pass


def test_part1():
    data = test_data_2
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 2028

    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 10092


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
