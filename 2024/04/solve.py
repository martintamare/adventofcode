#!/usr/bin/env python

test_data = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Cell:
    def __init__(self, row, column, data, grid):
        self.row = row
        self.column = column
        self.data = data
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

    @property
    def xmas_cross(self):
        if self.data != "A":
            return 0
        if not self.can_go_left:
            return 0
        if not self.can_go_right:
            return 0
        if not self.can_go_up:
            return 0
        if not self.can_go_down:
            return 0

        ok_set = set("MAS")
        value_1 = set("A")
        value_1.add(self.grid.data[self.row-1][self.column-1].data)
        value_1.add(self.grid.data[self.row+1][self.column+1].data)

        value_2 = set("A")
        value_2.add(self.grid.data[self.row-1][self.column+1].data)
        value_2.add(self.grid.data[self.row+1][self.column-1].data)

        if value_1 == ok_set and value_2 == ok_set:
            return 1
        return 0

    @property
    def xmas(self):
        if self.data != "X":
            return 0
        total = 0
        for attr in ["xmas_left", "xmas_right", "xmas_up", "xmas_down", "xmas_north_east", "xmas_north_west", "xmas_south_east", "xmas_south_west"]:
            value = getattr(self, attr)
            if value:
                total += 1
        return total

    def can_go(self, direction):
        if self.part == 1:
            if direction == "left":
                if self.column - 3 < 0:
                    return False
            elif direction == "right":
                if self.column + 4 > self.columns:
                    return False
            elif direction == "up":
                if self.row - 3 < 0:
                    return False
            elif direction == "down":
                if self.row + 4 > self.rows:
                    return False
            else:
                raise Exception(",dzaindazindaz")
        elif self.part == 2:
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

    def get_value(self, vector):
        row = self.row
        column = self.column
        value = ""
        for delta in range(4):
            row_delta = vector[0] * delta
            column_delta = vector[1] * delta
            cell = self.grid.data[row+row_delta][column+column_delta]
            value += cell.data
        assert len(value) == 4
        return value

    @property
    def xmas_left(self):
        # Need to be at least column 3
        if not self.can_go_left:
            return 0

        vector = (0,-1)
        to_check = self.get_value(vector)
        if to_check == "XMAS":
            print(f"LEFT : {self=} {to_check=}")
            return 1
        else:
            return 0

    @property
    def xmas_right(self):
        # Need to be at least column 3
        # 10 columns -> index 6 is OK, 7 is KO
        if not self.can_go_right:
            return 0

        vector = (0,1)
        to_check = self.get_value(vector)
        if to_check == "XMAS":
            print(f"RIGHT : {self=} {to_check=}")
            return 1
        else:
            return 0

    @property
    def xmas_up(self):
        # Need to be at least column 3
        if not self.can_go_up:
            return 0

        vector = (-1,0)
        to_check = self.get_value(vector)
        if to_check == "XMAS":
            print(f"UP : {self=} {to_check=}")
            return 1
        else:
            return 0

    @property
    def xmas_down(self):
        # Need to be at least column 3
        # 10 columns -> index 6 is OK, 7 is KO
        if not self.can_go_down:
            return 0

        vector = (1,0)
        to_check = self.get_value(vector)
        if to_check == "XMAS":
            print(f"DOWN : {self=} {to_check=}")
            return 1
        else:
            return 0

    @property
    def xmas_north_east(self):
        if not self.can_go_up:
            return 0
        if not self.can_go_right:
            return 0
        vector = (-1,1)
        to_check = self.get_value(vector)
        if to_check == "XMAS":
            print(f"NORTH EAST: {self=} {to_check=}")
            return 1
        else:
            return 0

    @property
    def xmas_north_west(self):
        if not self.can_go_up:
            return 0
        if not self.can_go_left:
            return 0
        vector = (-1,-1)
        to_check = self.get_value(vector)
        if to_check == "XMAS":
            print(f"NORTH EAST: {self=} {to_check=}")
            return 1
        else:
            return 0

    @property
    def xmas_south_east(self):
        if not self.can_go_down:
            return 0
        if not self.can_go_right:
            return 0
        vector = (1,1)
        to_check = self.get_value(vector)
        if to_check == "XMAS":
            print(f"NORTH EAST: {self=} {to_check=}")
            return 1
        else:
            return 0

    @property
    def xmas_south_west(self):
        if not self.can_go_down:
            return 0
        if not self.can_go_left:
            return 0
        vector = (1,-1)
        to_check = self.get_value(vector)
        if to_check == "XMAS":
            print(f"NORTH EAST: {self=} {to_check=}")
            return 1
        else:
            return 0

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



def solve_part1(data):
    grid = Grid(data)
    result = 0
    for row in grid.data:
        for cell in row:
            if cell.xmas:
                result += cell.xmas
    return result


def solve_part2(data):
    grid = Grid(data, part=2)
    result = 0
    for row in grid.data:
        for cell in row:
            if cell.xmas_cross:
                result += cell.xmas_cross
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 18


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 2562


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 9


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
