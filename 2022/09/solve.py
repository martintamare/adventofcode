#!/usr/bin/env python

test_data = [
    'R 4',
    'U 4',
    'L 3',
    'D 1',
    'R 4',
    'D 1',
    'L 5',
    'R 2',
]

test_data_2 = [
    'R 5',
    'U 8',
    'L 8',
    'D 3',
    'R 17',
    'D 10',
    'L 25',
    'U 20',
]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def position(self):
        return (self.x, self.y)

    def move(self, x_delta, y_delta):
        self.x += x_delta
        self.y += y_delta

    def follow(self, head):
        x_delta = head.x - self.x
        y_delta = head.y - self.y

        # Adjacent, no move
        if abs(x_delta) < 2 and abs(y_delta) < 2:
            return

        x_move = 0
        y_move = 0
        if x_delta >= 1:
            x_move = 1
        if x_delta <= -1:
            x_move = -1
        if y_delta >= 1:
            y_move = 1
        if y_delta <= -1:
            y_move = -1

        self.move(x_move, y_move)


def solve(data, rope_length):
    knots = []
    for i in range(rope_length):
        knots.append(Point(0, 0))

    tail = knots[rope_length-1]
    positions = set()
    positions.add(tail.position)
    print(positions)

    vectors_map = {
            'R': (0, 1),
            'L': (0, -1),
            'U': (1, 0),
            'D': (-1, 0),
    }

    for line in data:
        direction = line.split(' ')[0]
        length = int(line.split(' ')[1])
        y_delta, x_delta = vectors_map[direction]
        for i in range(length):
            head = knots[0]
            head.move(x_delta, y_delta)
            for knot_index in range(1, rope_length):
                knot_to_follow = knots[knot_index-1]
                following_knot = knots[knot_index]
                following_knot.follow(knot_to_follow)
            tail = knots[rope_length-1]
            positions.add(tail.position)
            # input(f'Iteration {i} head is {head.position} tail is {tail.position}')  # noqa
    print(positions)
    return len(positions)


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = solve(data, rope_length=2)
    print(f'test1 is {result}')
    assert result == 13


def test_part2():
    data = test_data
    result = solve(data, rope_length=10)
    print(f'test2 part1 is {result}')
    assert result == 1

    data = test_data_2
    result = solve(data, rope_length=10)
    print(f'test2 part2 is {result}')
    assert result == 36


def part1():
    data = load_data()
    result = solve(data, rope_length=2)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve(data, rope_length=10)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
