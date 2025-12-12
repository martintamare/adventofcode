#!/usr/bin/env python
from itertools import chain
from functools import cached_property

test_data = [
    "0:",
    "###",
    "##.",
    "##.",
    "",
    "1:",
    "###",
    "##.",
    ".##",
    "",
    "2:",
    ".##",
    "###",
    "##.",
    "",
    "3:",
    "##.",
    "###",
    "##.",
    "",
    "4:",
    "###",
    "#..",
    "###",
    "",
    "5:",
    "###",
    ".#.",
    "###",
    "",
    "4x4: 0 0 0 0 2 0",
    "12x5: 1 0 1 0 2 2",
    "12x5: 1 0 1 0 3 2",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Shape:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        lines = []
        for line in self.data:
            display_line = ""
            for item in line:
                if item:
                    display_line += "#"
                else:
                    display_line += "."
            lines.append(display_line)
        return "\n".join(lines)

    @cached_property
    def size(self):
        total = 0
        for line in self.data:
            total += sum(filter(lambda x: x, line))
        return total


class Region:
    def __init__(self, width, length, needs, shapes):
        self.width = width
        self.length = length
        self.needs = needs
        self.shapes = shapes

    def __repr__(self):
        return f"{self.width}x{self.length}: {self.needs}"

    @cached_property
    def needed_size(self):
        needed_size = 0
        for index, need in enumerate(self.needs):
            if need == 0:
                continue
            shape = self.shapes[index]
            shape_need = shape.size * need
            needed_size += shape_need
        return needed_size

    @cached_property
    def size(self):
        return self.width * self.length

    @cached_property
    def has_compatible_size(self):
        needed_size = self.needed_size
        current_size = self.size
        if needed_size > current_size:
            return False
        else:
            return True



def solve_part1(data):
    shapes = []
    data = data.copy()
    def mapping(x):
        if x == ".":
            return False
        elif x == "#":
            return True
        else:
            raise Exception("dznajdknazd")
    for index in range(6):
        data.pop(0)
        shape = []
        line = data.pop(0)
        line = list(map(lambda x: mapping(x), line))
        shape.append(line)

        line = data.pop(0)
        line = list(map(lambda x: mapping(x), line))
        shape.append(line)

        line = data.pop(0)
        line = list(map(lambda x: mapping(x), line))
        shape.append(line)

        data.pop(0)
        shape = Shape(shape)
        print(f"{index=}")
        print(shape)
        print("")
        shapes.append(shape)

    regions = []
    for remaining in data:
        grid_x = int(remaining.split(':')[0].split("x")[0])
        grid_y = int(remaining.split(':')[0].split("x")[1])
        wanted_shapes = list(map(int, remaining.split(':')[1].strip().split(" ")))
        region = Region(width=grid_x, length=grid_y, needs=wanted_shapes, shapes=shapes)
        regions.append(region)

    result = 0
    for region in regions:
        print(f"{region.needed_size=} vs {region.size=}")
        if not region.has_compatible_size:
            continue
        result += 1
    return result

def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 25


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


#test_part1()
part1()
#test_part2()
#part2()
