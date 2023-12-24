#!/usr/bin/env python
from itertools import combinations

test_data = [
'19, 13, 30 @ -2,  1, -2',
'18, 19, 22 @ -1, -1, -2',
'20, 25, 34 @ -2, -2, -4',
'12, 31, 28 @ -1, -2, -1',
'20, 19, 15 @  1, -5, -3',
]


class Line2D:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"y = {self.a}*x + {self.b}"

    def intersects(self, other):
        # y = ax + c and y = bx + d
        a = self.a
        c = self.b
        b = other.a
        d = other.b

        # line // 
        if a == b:
            return None

        x = (d-c)/(a-b)
        y = a * x + c

        # Check that t value for self and other and > 0
        return (x, y)


class Hailstone:
    def __init__(self, data):
        positions = data.split(' @ ')[0]
        velocities = data.split(' @ ')[1]
        self.positions = list(map(int, positions.split(', ')))
        self.velocities = list(map(int, velocities.split(', ')))

        self.a = self.velocities[1]/self.velocities[0]
        self.b = self.positions[1] - self.a * self.positions[0]
        self.line_2d = Line2D(self.a, self.b)

    def __repr__(self):
        return f"{self.positions} {self.velocities}"

    def intersects(self, other):
        intersection = self.line_2d.intersects(other.line_2d)
        if intersection is None:
            return intersection

        # now compute iteration
        x, y = intersection

        # need to be with a timeldeta > 0
        self_time = (x - self.positions[0]) / self.velocities[0]
        other_time = (x - other.positions[0]) / other.velocities[0]

        if self_time < 0 or other_time < 0:
            return None

        return intersection
        

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data, x_min=None, x_max=None, y_min=None, y_max=None):
    hailstones = []
    for line in data:
        hailstone = Hailstone(line)
        hailstones.append(hailstone)

    count = 0
    for ha, hb in combinations(hailstones, 2):
        print(f"{ha} {ha.line_2d}")
        print(f"{hb} {hb.line_2d}")
        intersection = ha.intersects(hb)
        if intersection:
            x, y = intersection
            if x_min is not None:
                if x <= x_min:
                    continue
            if y_min is not None:
                if y <= y_min:
                    continue
            if x_max is not None:
                if x > x_max:
                    continue
            if y_max is not None:
                if y > y_max:
                    continue

            print("Yes inside", intersection)
            count += 1
    return count



def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data, x_min=7, y_max=27)
    print(f'test1 is {result}')
    assert result == 2


def part1():
    data = load_data()
    result = solve_part1(data, x_min=200000000000000, x_max=400000000000000, y_min=200000000000000, y_max=400000000000000)
    print(f'part1 is {result}')
    assert result < 25855


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
