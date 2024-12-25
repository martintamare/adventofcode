#!/usr/bin/env python

import sys
from collections import defaultdict, Counter

sys.path.append("../../")
from utils import Grid, Cell

test_data = [
    "#####",
    ".####",
    ".####",
    ".####",
    ".#.#.",
    ".#...",
    ".....",
    "",
    "#####",
    "##.##",
    ".#.##",
    "...##",
    "...#.",
    "...#.",
    ".....",
    "",
    ".....",
    "#....",
    "#....",
    "#...#",
    "#.#.#",
    "#.###",
    "#####",
    "",
    ".....",
    ".....",
    "#.#..",
    "###..",
    "###.#",
    "###.#",
    "#####",
    "",
    ".....",
    ".....",
    ".....",
    "#....",
    "#.#..",
    "#.#.#",
    "#####",
]

class CustomCell(Cell):
    pass

class CustomGrid(Grid):
    @property
    def is_lock(self):
        return all(map(lambda x: x.data == "#", self.data[0]))

    @property
    def is_key(self):
        return all(map(lambda x: x.data == "#", self.data[-1]))

    @property
    def heights(self):
        if self.is_lock:
            return self.lock_heights
        elif self.is_key:
            return self.key_heights

    @property
    def lock_heights(self):
        heights = []
        for col in range(self.cols):
            current_index = None
            for row in range(self.rows):
                if self.data[row][col].data == "#":
                    current_index = row
                else:
                    break
            heights.append(current_index)
        return heights

    @property
    def key_heights(self):
        heights = []
        for col in range(self.cols):
            current_index = None
            for row in reversed(list(range(self.rows))):
                if self.data[row][col].data == "#":
                    current_index = row
                else:
                    break
            heights.append(self.rows - current_index - 1)
        return heights

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):

    lock = []
    locks = []
    keys = []
    for line in data:
        if line == "":
            l = CustomGrid(lock)
            if l.is_key:
                keys.append(l)
            elif l.is_lock:
                locks.append(l)
            else:
                raise Exception("dzanjdkazdaz")
            lock = []
        else:
            lock.append(line)
    l = CustomGrid(lock)
    if l.is_key:
        keys.append(l)
    elif l.is_lock:
        locks.append(l)
    else:
        raise Exception("dzanjdkazdaz")

    matching = 0
    for lock in locks:
        for key in keys:
            result = []
            for index in range(len(lock.heights)):
                value = lock.heights[index] + key.heights[index]
                if value < lock.rows - 1:
                    result.append(value)
                else:
                    break
            if len(result) == len(lock.heights):
                matching += 1
    return matching


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 3


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
