#!/usr/bin/env python

test_data = [
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Grid:
    def __init__(self):
        self.grid = {}

    def add_beacon(self, c):
        self.grid[c] = 'B'

    def add_sensor(self, c):
        self.grid[c] = 'S'

    def __str__(self):
        min_x = min(map(lambda c: c[0], self.grid.keys()))
        min_y = min(map(lambda c: c[1], self.grid.keys()))
        max_x = max(map(lambda c: c[0], self.grid.keys()))
        max_y = max(map(lambda c: c[1], self.grid.keys()))
        data = []
        for y in range(min_y, max_y+1):
            line = ''
            for x in range(min_x, max_x+1):
                c = (x, y)
                to_add = '.'
                if c in self.grid:
                    to_add = self.grid[c]
                line += to_add
            data.append(line)
        return '\n'.join(data)

    def apply_mask_at_y(self, sensor, beacon, wanted_y):
        distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        print(f'{sensor} {beacon} distance is {distance}')
        has_beacon = False

        for y_delta in range(-distance, distance+1):
            if sensor[1] + y_delta != wanted_y:
                continue
            x_to_pad = distance-abs(y_delta)
            delta = 2 * x_to_pad + 1
            for x_delta in range(-x_to_pad, -x_to_pad+delta):
                if y_delta == 0 and x_delta == 0:
                    continue
                test_c = (sensor[0] + x_delta, sensor[1] + y_delta)
                if test_c in self.grid:
                    if self.grid[test_c] == '#':
                        pass
                    elif self.grid[test_c] == 'S':
                        pass
                    elif self.grid[test_c] != 'B':
                        print(f'Weird {self.grid[test_c]} and {test_c}')
                        print(self)
                        exit(0)
                    elif has_beacon:
                        print('Two beacons ??')
                        print(self)
                        exit(0)
                    else:
                        has_beacon = True
                else:
                    self.grid[test_c] = '#'

    def apply_mask(self, sensor, beacon):
        distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        print(f'{sensor} {beacon} distance is {distance}')
        has_beacon = False

        for y_delta in range(-distance, distance+1):
            x_to_pad = distance-abs(y_delta)
            delta = 2 * x_to_pad + 1
            for x_delta in range(-x_to_pad, -x_to_pad+delta):
                if y_delta == 0 and x_delta == 0:
                    continue
                test_c = (sensor[0] + x_delta, sensor[1] + y_delta)
                if test_c in self.grid:
                    if self.grid[test_c] == '#':
                        pass
                    elif self.grid[test_c] == 'S':
                        pass
                    elif self.grid[test_c] != 'B':
                        print(f'Weird {self.grid[test_c]} and {test_c}')
                        print(self)
                        exit(0)
                    elif has_beacon:
                        print('Two beacons ??')
                        print(self)
                        exit(0)
                    else:
                        has_beacon = True
                else:
                    self.grid[test_c] = '#'


def solve_part1(data, wanted_y):
    grid = Grid()
    for line in data:
        ok_values = list(filter(lambda x: '=' in x, line.split(' ')))

        def keep_digits_only(s):
            result = ''
            for c in s:
                if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']:  # noqa
                    result += c
            return result

        beacon_data = list(map(int, map(keep_digits_only, ok_values)))
        sensor = (beacon_data[0], beacon_data[1])
        beacon = (beacon_data[2], beacon_data[3])
        grid.add_sensor(sensor)
        grid.add_beacon(beacon)
        grid.apply_mask_at_y(sensor, beacon, wanted_y)

    keys = filter(lambda x: x[1] == wanted_y, grid.grid.keys())
    count = 0
    for key in keys:
        if grid.grid[key] == '#':
            count += 1
    return count


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data, 10)
    print(f'test1 is {result}')
    assert result == 26


def part1():
    data = load_data()
    result = solve_part1(data, 2000000)
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
