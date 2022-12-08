#!/usr/bin/env python

test_data = [
    '30373',
    '25512',
    '65332',
    '33549',
    '35390',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Tree:
    def __init__(self, height, row, column, grid):
        self.height = int(height)
        self.row = row
        self.column = column
        self.grid = grid

    @property
    def is_edge(self):
        if self.row == 0:
            return True
        if self.column == 0:
            return True
        if self.row == len(self.grid) - 1:
            return True
        if self.column == len(self.grid[0]) - 1:
            return True
        return False

    @property
    def scenic_score(self):
        if self.is_edge:
            return 0

        def check_neighbor_row(indexes):
            count = 0
            for row in indexes:
                neighbor_height = int(self.grid[row][self.column])
                if neighbor_height >= self.height:
                    count += 1
                    break
                else:
                    count += 1
            return count

        def check_neighbor_column(indexes):
            count = 0
            for column in indexes:
                neighbor_height = int(self.grid[self.row][column])
                if neighbor_height >= self.height:
                    count += 1
                    break
                else:
                    count += 1
            return count

        # Top
        indexes = list(range(0, self.row))
        indexes.reverse()
        top = check_neighbor_row(indexes)
        if not top:
            return 0
        print(f'tree {self.row},{self.column} can see top {top}')

        # Down
        indexes = list(range(self.row + 1, len(self.grid)))
        down = check_neighbor_row(indexes)
        if not down:
            return 0
        print(f'tree {self.row},{self.column} can see down {down}')

        # Left
        indexes = list(range(0, self.column))
        indexes.reverse()
        left = check_neighbor_column(indexes)
        if not left:
            return 0
        print(f'tree {self.row},{self.column} can see left {left}')

        # Right
        indexes = list(range(self.column + 1, len(self.grid[0])))
        right = check_neighbor_column(indexes)
        if not left:
            return 0
        print(f'tree {self.row},{self.column} can see right {right}')

        total = top * down * left * right
        # print(f'tree {self.row},{self.column} scenic_score={total}')
        return total

    @property
    def visible(self):
        if self.is_edge:
            # print(f'tree {self.row},{self.column} visible because is_edge')
            return True

        def check_neighbor_row(indexes):
            is_visible = True
            for row in indexes:
                neighbor_height = int(self.grid[row][self.column])
                if neighbor_height >= self.height:
                    is_visible = False
                    break
            return is_visible

        def check_neighbor_column(indexes):
            is_visible = True
            for column in indexes:
                neighbor_height = int(self.grid[self.row][column])
                if neighbor_height >= self.height:
                    is_visible = False
                    break
            return is_visible

        # Top
        indexes = list(range(0, self.row))
        indexes.reverse()
        if check_neighbor_row(indexes):
            # print(f'tree {self.row},{self.column} visible because top')
            return True

        # Down
        indexes = list(range(self.row + 1, len(self.grid)))
        if check_neighbor_row(indexes):
            # print(f'tree {self.row},{self.column} visible because down')
            return True

        # Left
        indexes = list(range(0, self.column))
        indexes.reverse()
        if check_neighbor_column(indexes):
            # print(f'tree {self.row},{self.column} visible because left')
            return True

        # Right
        indexes = list(range(self.column + 1, len(self.grid[0])))
        if check_neighbor_column(indexes):
            # print(f'tree {self.row},{self.column} visible because right')
            return True

        # print(f'tree {self.row},{self.column} NOT visible')
        return False


def solve(data, part=1):
    rows = len(data)
    columns = len(data[0])
    trees = []
    for row in range(rows):
        for column in range(columns):
            height = data[row][column]
            tree = Tree(height, row, column, data)
            trees.append(tree)

    if part == 1:
        visible = 0
        for tree in trees:
            if tree.visible:
                visible += 1
        return visible
    else:
        scenic_score = None
        for tree in trees:
            if scenic_score is None:
                scenic_score = tree.scenic_score
            elif tree.scenic_score > scenic_score:
                scenic_score = tree.scenic_score
        return scenic_score


def test_part1():
    data = test_data
    result = solve(data)
    print(f'test1 is {result}')
    assert result == 21


def test_part2():
    data = test_data
    result = solve(data, part=2)
    print(f'test2 is {result}')
    assert result == 8


def part1():
    data = load_data()
    result = solve(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve(data, part=2)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
