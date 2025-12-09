#!/usr/bin/env python
from itertools import combinations

import sys
sys.path.append("../../")
from utils import Grid, Cell

test_data = [
    "7,1",
    "11,1",
    "11,7",
    "9,7",
    "9,5",
    "2,5",
    "2,3",
    "7,3",
]

class CustomCell(Cell):
    def print(self):
        if self.data == 1:
            return "#"
        elif self.data == 2:
            return "x"
        else:
            return "."

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.data = None

    @property
    def vector(self):
        return (self.x, self.y)

    def area_to(self, other):
        x = abs(self.x - other.x) + 1
        y = abs(self.y - other.y) + 1
        return x * y

    def inside(self, mapping, ko_mapping, global_max_x, global_max_y):
        # Inside if present in mapping
        if self.vector in mapping:
            return True
        if self.vector in ko_mapping:
            return False

        # Not in mapping : should have 4 neighbords in mapping
        # Up : -y
        has_up = False
        test_y = self.y - 1
        tested_vectors = set()
        while test_y >= 0:
            test_vector = (self.x, test_y)
            tested_vectors.add(test_vector)
            if test_vector in mapping:
                has_up = True
                break
            test_y -= 1
        if not has_up:
            for vector in tested_vectors:
                if vector not in ko_mapping:
                    x, y = vector
                    point = Point(x, y)
                    ko_mapping[point.vector] = point
                    point.data = -1
                ko_mapping[self.vector] = self
            return False
        else:
            for vector in tested_vectors:
                if vector not in mapping:
                    x, y = vector
                    point = Point(x, y)
                    mapping[point.vector] = point
                    point.data = 3

        # Down : +y
        has_down = False
        test_y = self.y + 1
        tested_vectors = set()
        while test_y <= global_max_y:
            test_vector = (self.x, test_y)
            tested_vectors.add(test_vector)
            if test_vector in mapping:
                has_down = True
                break
            test_y += 1
        if not has_down:
            for vector in tested_vectors:
                if vector not in ko_mapping:
                    x, y = vector
                    point = Point(x, y)
                    ko_mapping[point.vector] = point
                    point.data = -1
                ko_mapping[self.vector] = self
            return False
        else:
            for vector in tested_vectors:
                if vector not in mapping:
                    x, y = vector
                    point = Point(x, y)
                    mapping[point.vector] = point
                    point.data = 3

        # Left : -x
        has_left = False
        test_x = self.x - 1
        tested_vectors = set()
        while test_x >= 0:
            test_vector = (test_x, self.y)
            tested_vectors.add(test_vector)
            if test_vector in mapping:
                has_left = True
                break
            test_x -= 1
        if not has_left:
            for vector in tested_vectors:
                if vector not in ko_mapping:
                    x, y = vector
                    point = Point(x, y)
                    ko_mapping[point.vector] = point
                    point.data = -1
                ko_mapping[self.vector] = self
            return False
        else:
            for vector in tested_vectors:
                if vector not in mapping:
                    x, y = vector
                    point = Point(x, y)
                    mapping[point.vector] = point
                    point.data = 3

        # Right : +x
        has_right = False
        test_x = self.x + 1
        tested_vectors = set()
        while test_x <= global_max_x:
            test_vector = (test_x, self.y)
            tested_vectors.add(test_vector)
            if test_vector in mapping:
                has_left = True
                break
            test_x += 1
        if not has_left:
            for vector in tested_vectors:
                if vector not in ko_mapping:
                    x, y = vector
                    point = Point(x, y)
                    ko_mapping[point.vector] = point
                    point.data = -1
                ko_mapping[self.vector] = self
            return False
        else:
            for vector in tested_vectors:
                if vector not in mapping:
                    x, y = vector
                    point = Point(x, y)
                    mapping[point.vector] = point
                    point.data = 3

        return True

    def area_ok_to(self, other, mapping, ko_mapping, global_max_x, global_max_y):
        # Ok if all points are 1 or 2 within grid
        min_x = min(self.x, other.x)
        max_x = max(self.x, other.x)
        min_y = min(self.y, other.y)
        max_y = max(self.y, other.y)
        middle_x = int((min_x + max_x)/2)
        middle_y = int((min_y + max_y)/2)

        # A-----C
        # |  E  |
        # B-----D
        vector_a = (min_x,min_y)
        vector_b = (min_x,max_y)
        vector_c = (max_x,min_y)
        vector_d = (max_x,max_y)
        vector_e = (middle_x, middle_y)

        point_a = mapping.get(vector_a, None)
        point_b = mapping.get(vector_b, None)
        point_c = mapping.get(vector_c, None)
        point_d = mapping.get(vector_d, None)
        point_e = mapping.get(vector_e, None)

        # Check corner they should exist and be 1
        corner_1 = False
        if point_a is not None and point_d is not None:
            if point_a.data == 1 and point_d.data == 1:
                corner_1 = True

        corner_2 = False
        if point_b is not None and point_c is not None:
            if point_b.data == 1 and point_c.data == 1:
                corner_2 = True

        if not corner_1 and not corner_2:
            return False

        # Now check that each point is inside
        for x in range(min_x, max_x + 1):
            test = Point(x, max_y)
            if not test.inside(mapping, ko_mapping, global_max_x, global_max_y):
                return False

        for x in range(min_x, max_x + 1):
            test = Point(x, min_y)
            if not test.inside(mapping, ko_mapping, global_max_x, global_max_y):
                return False

        for y in range(min_y, max_y + 1):
            test = Point(min_x, y)
            if not test.inside(mapping, ko_mapping, global_max_x, global_max_y):
                return False

        for y in range(min_y, max_y + 1):
            test = Point(max_x, y)
            if not test.inside(mapping, ko_mapping, global_max_x, global_max_y):
                return False

        return True

    def __repr__(self):
        return f"{self.vector}"


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    points = []
    for line in data:
        splitted = line.split(',')
        point = Point(int(splitted[0]), int(splitted[1]))
        points.append(point)

    max_area = None
    for p1, p2 in combinations(points, 2):
        area = p1.area_to(p2)
        if max_area is None:
            max_area = area
        elif area > max_area:
            max_area = area

    return max_area

def solve_part2(data):
    
    points = []
    mapping = {}
    max_x = None
    max_y = None
    for line in data:
        splitted = line.split(',')
        point = Point(int(splitted[0]), int(splitted[1]))
        points.append(point)
        mapping[point.vector] = point
        point.data = 1
        if max_x is None:
            max_x = point.x
        elif point.x > max_x:
            max_x = point.x
        if max_y is None:
            max_y = point.y
        elif point.y > max_y:
            max_y = point.y

    global_max_x = max_x
    global_max_y = max_y
           

    greens = []
    last_point = None
    for index, point in enumerate(points):
        if index == 0:
            last_point = points[-1]
        print(index)
        print(f"{point=} {last_point=}")
        # y change
        if last_point.x == point.x:
            min_y = min(last_point.y, point.y)
            max_y = max(last_point.y, point.y)
            for y in range(min_y+1, max_y):
                green = Point(last_point.x, y)
                greens.append(green)
                mapping[green.vector] = green
                green.data = 2
        elif last_point.y == point.y:
            min_x = min(last_point.x, point.x)
            max_x = max(last_point.x, point.x)
            for x in range(min_x+1, max_x):
                green = Point(x, last_point.y)
                greens.append(green)
                mapping[green.vector] = green
                green.data = 2
        else:
            raise Exception(f"{last_point=} {point=}")
        last_point = point

    print(f"{len(points)=} {len(greens)=} {len(mapping.keys())}")

    heap = []

    ko_mapping = {}
    max_area = None
    iteration = 0
    for p1, p2 in combinations(points, 2):
        iteration += 1
        print(f"{iteration=}")
        area = p1.area_to(p2)
        if max_area is not None and area < max_area:
            continue
        if p1.area_ok_to(p2, mapping, ko_mapping, global_max_x, global_max_y):
            if max_area is None:
                max_area = area
                print(f"{p1=} {p2=} {max_area=}")
            elif area > max_area:
                max_area = area
                print(f"{p1=} {p2=} {max_area=}")
    return max_area

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 50


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 24


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result < 4771356500
    assert result < 4743489398
    assert result < 4615432660
    assert result != 1329648570


test_part1()
part1()
test_part2()
part2()
