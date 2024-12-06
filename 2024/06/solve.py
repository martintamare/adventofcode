#!/usr/bin/env python

test_data = [
    '....#.....',
    '.........#',
    '..........',
    '..#.......',
    '.......#..',
    '..........',
    '.#..^.....',
    '........#.',
    '#.........',
    '......#...',
]

class Cell:
    def __init__(self, row, column, data, grid):
        self.row = row
        self.column = column
        self.data = data
        self.grid = grid
        self.visited = False
        self.vector = None
        self.visited_from_vectors = []

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

    @property
    def obstructed(self):
        return self.data == "#"

    def print(self):
        if self.visited:
            return "X"
        else:
            return self.data

    @property
    def can_move(self):
        vector = self.vector
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

    def move(self):
        vector = self.vector
        if vector == (-1,0):
            if self.can_go_up:
                next_cell = self.get_next_cell(vector)
                if next_cell.obstructed:
                    self.vector = (0,1)
                    return self.move()
                else:
                    return next_cell
            else:
                raise Exception("Unable to go up")
        elif vector == (1,0):
            if self.can_go_down:
                next_cell = self.get_next_cell(vector)
                if next_cell.obstructed:
                    self.vector = (0,-1)
                    return self.move()
                else:
                    return next_cell
            else:
                raise Exception("Unable to go down")
        elif vector == (0,-1):
            if self.can_go_left:
                next_cell = self.get_next_cell(vector)
                if next_cell.obstructed:
                    self.vector = (-1, 0)
                    return self.move()
                else:
                    return next_cell
            else:
                raise Exception("Unable to go left")
        elif vector == (0,1):
            if self.can_go_right:
                next_cell = self.get_next_cell(vector)
                if next_cell.obstructed:
                    self.vector = (1,0)
                    return self.move()
                else:
                    return next_cell
            else:
                raise Exception("Unable to go right")
        else:
            raise Exception(f"Wrong {vector=}")

    def get_next_cell(self, vector):
        row = self.row
        column = self.column
        row_delta = vector[0]
        column_delta = vector[1]
        cell = self.grid.data[row+row_delta][column+column_delta]
        return cell


class Grid:
    def __init__(self, data, part=1):
        self.raw_data = data
        self.data = []
        self.part = part
        self.guard = None

        for row_index, columns in enumerate(data):
            row = []
            for column_index, cell_data in enumerate(columns):
                cell = Cell(row_index, column_index, cell_data, self)
                if cell_data == "^":
                    self.guard = cell
                    cell.visited = True
                    cell.vector = (-1,0)
                row.append(cell)
            self.data.append(row)

    def move_guard(self):
        if self.guard.can_move:
            next_cell = self.guard.move()
            next_cell.visited = True
            next_cell.vector = self.guard.vector
            self.guard = next_cell
            return True
        else:
            return False

    def move_guard_part2(self):
        if self.guard.can_move:
            next_cell = self.guard.move()
            next_cell.visited = True
            # Means we already came from the same direction
            if self.guard.vector in next_cell.visited_from_vectors:
                return False
            next_cell.visited_from_vectors.append(self.guard.vector)
            next_cell.vector = self.guard.vector
            self.guard = next_cell
            return True
        else:
            return False

    @property
    def visited(self):
        result = 0
        for row in self.data:
            for cell in row:
                if cell.visited:
                    result += 1
        return result

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


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    grid = Grid(data)
    print(grid.guard)
    print(f"{grid.guard.can_move=}")

    # First compute path
    while grid.move_guard():
        pass

    grid.print()
    return grid.visited

def solve_part2(data):
    grid = Grid(data)
    print(grid.guard)
    print(f"{grid.guard.can_move=}")

    # First compute path
    init_guard = grid.guard
    while grid.move_guard():
        pass

    # Build cell to test obstruction
    to_test = []
    for row in grid.data:
        for cell in row:
            if cell.visited:
                if cell == init_guard:
                    pass
                else:
                    to_test.append(cell)


    # For all of theses, create a new grid
    result = 0
    print(f"We have {len(to_test)} cell to test")
    for cell in to_test:
        print(f"Testing {cell=}")
        new_data = data.copy()
        row = cell.row
        column = cell.column
        old_line = new_data[row]
        new_line = old_line[:column] + "#" + old_line[column+1:]
        new_data[row] = new_line
        new_grid = Grid(new_data)
        while new_grid.move_guard_part2():
            pass
        if new_grid.guard.can_move:
            result += 1
        else:
            pass
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 41


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 6


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
