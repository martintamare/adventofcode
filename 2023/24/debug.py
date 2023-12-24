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
        if self_time < 0:
            print("A past")
        other_time = (x - other.positions[0]) / other.velocities[0]
        if other_time < 0:
            print("B past")

        if self_time < 0 or other_time < 0:
            return None

        return intersection
        

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_lines(left, right):
    a1, b1, c1, d1, = left.velocities[0], left.positions[0], left.velocities[1], left.positions[1]
    a2, b2, c2, d2, = right.velocities[0], right.positions[0], right.velocities[1], right.positions[1]
    try:
        t2 = (a1 * (d2 - d1) + c1 * (b1 - b2)) / (a2 * c1 - c2 * a1)
        t1 = (t2 * a2 + b2 - b1) / a1
    except ZeroDivisionError:
        # parallel lines
        return None, None, None, None

    xl = t1 * a1 + b1
    xb = t2 * a2 + b2
    yl = t1 * c1 + d1
    yb = t2 * c2 + d2

    return xl, yl, t1, t2

def check(l, r, left_bound, right_bound):
    x, y, t1, t2 = solve_lines(l, r)
    if not x:
        return False
    return (left_bound <= x <= right_bound) and (left_bound <= y <= right_bound) and (t1 >= 0) and (t2 >= 0)



def solve_part1(data, at_least_x, at_most_y):
    hailstones = []
    for line in data:
        hailstone = Hailstone(line)
        hailstones.append(hailstone)

    count = 0
    for ha, hb in combinations(hailstones, 2):
        print(f"{ha} {ha.line_2d}")
        print(f"{hb} {hb.line_2d}")

        if check(ha, hb, at_least_x, at_most_y):
            count += 1
            print("Yes inside")
        else:
            print("No")

    return count



def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data, 7, 27)
    print(f'test1 is {result}')
    assert result == 2


def part1():
    data = load_data()
    result = solve_part1(data, 200000000000000, 400000000000000)
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
