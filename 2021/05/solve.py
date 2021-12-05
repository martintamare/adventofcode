#!/usr/bin/env python

test_data = [
    '0,9 -> 5,9',
    '8,0 -> 0,8',
    '9,4 -> 3,4',
    '2,2 -> 2,1',
    '7,0 -> 7,4',
    '6,4 -> 2,0',
    '0,9 -> 2,9',
    '3,4 -> 1,4',
    '0,0 -> 8,8',
    '5,5 -> 8,2',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def index(self):
        return f'{self.x}_{self.y}'

    def get_points_to(self, point, method):
        source_x = self.x
        source_y = self.y
        dest_x = point.x
        dest_y = point.y


        delta = None
        if source_x == dest_x:
            delta = 'row'
        elif source_y == dest_y:
            delta = 'column'
        elif abs(source_x - dest_x) != abs(source_y - dest_y):
            raise Exception('Weird)')

        if method == 'part1':
            if delta not in ['row', 'column']:
                return []

        connecting_points = []

        if delta == 'row':
            for delta_y in range(0, abs(dest_y - source_y) + 1):
                new_x = source_x
                if dest_y > source_y:
                    new_y = source_y + delta_y
                else:
                    new_y = source_y - delta_y

                new_point = Point(new_x, new_y)
                connecting_points.append(new_point)
        elif delta == 'column':
            for delta_x in range(0, abs(dest_x - source_x) + 1):
                new_y = source_y
                if dest_x > source_x:
                    new_x = source_x + delta_x
                else:
                    new_x = source_x - delta_x

                new_point = Point(new_x, new_y)
                connecting_points.append(new_point)
        else:
            for delta in range(0, abs(dest_x - source_x) + 1):
                if dest_x > source_x:
                    new_x = source_x + delta
                else:
                    new_x = source_x - delta

                if dest_y > source_y:
                    new_y = source_y + delta
                else:
                    new_y = source_y - delta

                new_point = Point(new_x, new_y)
                connecting_points.append(new_point)
        return connecting_points

    def __str__(self):
        return f'{self.x},{self.y}'

    def __repr__(self):
        return f'{self.x},{self.y}'


def solve(data, method):

    results = {}
    for line in data:
        point_a = line.split(' ')[0]
        point_a = Point(int(point_a.split(',')[0]), int(point_a.split(',')[1]))
        point_b = line.split(' ')[2]
        point_b = Point(int(point_b.split(',')[0]), int(point_b.split(',')[1]))
        for point in point_a.get_points_to(point_b, method):
            if point.index in results:
                results[point.index] += 1
            else:
                results[point.index] = 1
    return len(list(filter(lambda x: results[x] > 1, results.keys())))


def test_part1():
    data = test_data
    result = solve(data, method='part1')
    print(f'test1 is {result}')
    assert result == 5


def test_part2():
    data = test_data
    result = solve(data, method='part2')
    print(f'test2 is {result}')
    assert result == 12


def part1():
    data = load_data()
    result = solve(data, method='part1')
    print(f'part1 is {result}')
    assert result == 4993


def part2():
    data = load_data()
    result = solve(data, method='part2')
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
