#!/usr/bin/env python
import sys
import itertools
from math import inf as infinity
from heapq import heappop, heappush
from collections import defaultdict

test_data = [
    '#.#####################',
    '#.......#########...###',
    '#######.#########.#.###',
    '###.....#.>.>.###.#.###',
    '###v#####.#v#.###.#.###',
    '###.>...#.#.#.....#...#',
    '###v###.#.#.#########.#',
    '###...#.#.#.......#...#',
    '#####.#.#.#######.#.###',
    '#.....#.#.#.......#...#',
    '#.#####.#.#.#########v#',
    '#.#...#...#...###...>.#',
    '#.#.#v#######v###.###v#',
    '#...#.>.#...>.>.#.###.#',
    '#####v#.#.###v#.#.###.#',
    '#.....#...#...#.#.#...#',
    '#.#########.###.#.#.###',
    '#...###...#...#...#.###',
    '###.###.#.###v#####v###',
    '#...#...#.#.>.>.#.>.###',
    '#.###.###.#.###.#.#v###',
    '#.....###...###...#...#',
    '#####################.#',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Tile:
    def __init__(self, island, value, row, col):
        self.island = island
        self.row = row
        self.col = col
        self.value = value
        self._neighbors = {}

    def __lt__(self, other):
        return self.row < self.row and self.col < self.col

    def neighbors(self, coming_from=None):
        to_check = []

        # up
        row = self.row + 1
        col = self.col
        if row < self.island.rows:
            neighbor = self.island.matrix[row][col]
            if self.value in ['.', 'v']:
                to_check.append(neighbor)

        # left
        row = self.row
        col = self.col - 1
        if col >= 0:
            neighbor = self.island.matrix[row][col]
            if self.value in ['.', '<']:
                to_check.append(neighbor)

        # down
        row = self.row - 1
        col = self.col
        if row >= 0:
            neighbor = self.island.matrix[row][col]
            if self.value in ['.', '^']:
                to_check.append(neighbor)



        # right
        row = self.row
        col = self.col + 1
        if col < self.island.cols:
            neighbor = self.island.matrix[row][col]
            if self.value in ['.', '>']:
                to_check.append(neighbor)

        result = []
        for neighbor in to_check:
            if neighbor.value == '#':
                continue
            elif coming_from is not None:
                if neighbor != coming_from:
                    result.append(neighbor)
            else:
                result.append(neighbor)

        return result


    def __repr__(self):
        return self.value

    @property
    def position(self):
        return f"{self.row},{self.col}"


class Island:
    def __init__(self, data, version=1):
        # Build 2x2 matrix : line and cols
        self.matrix = []

        initial_rows = len(data)
        initial_cols = len(data[0])
        self.rows = initial_rows
        self.cols = initial_cols

        for row, line in enumerate(data):
            matrix_row = []
            for col, char in enumerate(line):
                if version == 2:
                    if char in ['^', 'v', '<', '>']:
                        char = '.'
                tile = Tile(self, char, row, col)
                matrix_row.append(tile)
            self.matrix.append(matrix_row)

        self.start = self.matrix[0][1]
        self.end = self.matrix[initial_rows-1][initial_cols-2]

    def __repr__(self):
        display = []
        for row, row_data in enumerate(self.matrix):
            line = ''
            for col, char in enumerate(row_data):
                line += char.value
            display.append(line)
        return '\n'.join(display)

    @property
    def area(self):
        return self.rows * self.cols

    def print_path(self, path):
        display = []
        for row, row_data in enumerate(self.matrix):
            line = ''
            for col, char in enumerate(row_data):
                if char in path:
                    line += 'O'
                else:
                    line += char.value
            display.append(line)
        print('\n'.join(display))


def dijkstra(edges, f, t):

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            path = (v1, path)
            if v1 == t: return (cost, path)

            for v2 in v1.neighbors():
                if v2 in path: continue
                prev = mins.get(v2, None)
                next = cost + 1
                if prev is None or next > prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf"), None


max_path = 0
memory = {}

def solve(data, version=1):
    island = Island(data, version)
    start = island.start
    end = island.end

    result = dijkstra(island, start, end)
    print('test', result)
    exit(0)
    return result


def test_part1():
    data = test_data
    result = solve(data)
    print(f'test1 is {result}')
    assert result == 94

def part1():
    data = load_data()
    result = solve(data)
    print(f'part1 is {result}')
    assert result == 2070


def test_part2():
    data = test_data
    result = solve(data, 2)
    print(f'test2 is {result}')
    assert result == 154


def part2():
    data = load_data()
    result = solve(data, 2)
    print(f'part2 is {result}')
    assert result > 5906


test_part1()
part1()
test_part2()
part2()
