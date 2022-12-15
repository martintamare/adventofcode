#!/usr/bin/env python
import itertools

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
        self.sensors = {}
        self.checked = []
        self.sensors_range = {}

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

    def apply_mask_with_range(self, sensor, beacon, max_range):
        distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        print(f'{sensor} {beacon} distance is {distance}')
        has_beacon = False

        for y_delta in range(-distance, distance+1):
            if abs(sensor[1] + y_delta) > max_range:
                continue
            x_to_pad = distance-abs(y_delta)
            delta = 2 * x_to_pad + 1
            for x_delta in range(-x_to_pad, -x_to_pad+delta):
                if y_delta == 0 and x_delta == 0:
                    continue
                test_c = (sensor[0] + x_delta, sensor[1] + y_delta)
                if abs(test_c[0]) > max_range:
                    continue

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

    def find_hidden_beacon_smart(self, max_range):
        x = 0
        y = 0
        while True:
            if x > max_range or y > max_range:
                print('No nonononononooooooooooooooooooooooooooo')
            found = False
            print(f'testing y={y}')
            for sensor in self.sensors:
                distance = self.sensors[sensor]
                test = abs(x - sensor[0]) + abs(y - sensor[1])
                if test <= distance:
                    found = True
                    x_delta = x - sensor[0]
                    y_delta = y - sensor[1]
                    x_to_pad = distance-abs(y_delta)
                    x_to_move = sensor[0] + x_to_pad + 1 - x
                    if x + x_to_move > max_range:
                        x = 0
                        y = y+1
                    else:
                        x += x_to_move
                    break
            if not found:
                return (x,y)

    def find_hidden_beacon_smart_not_math(self, max_range):
        global_max_1 = None
        global_max_2 = None
        for sensor in self.sensors.keys():
            x1 = sensor[0]
            y1 = sensor[1]
            z1 = self.sensors[sensor]
            print('soit')
            max_1 = z1 + x1 - y1
            max_2 = z1 + x1 + y1
            if global_max_1 is None:
                global_max_1 = max_1
            elif max_1 > global_max_1:
                global_max_1 = max_1
            if global_max_2 is None:
                global_max_2 = max_2
            elif max_2 > global_max_2:
                global_max_2 = max_2
            
            print(f'y-x={-x1+y1-z1}')
            print(f'y-x={-x1+y1+z1}')
            print(f'y+x={x1+y1+z1}')
            print(f'y+x={x1+y1-z1}')
            input()


    def find_hidden_beacon_smart_but_really_not(self, max_range):
        for y in range(max_range + 1):
            print(f'testing y={y}')
            for x in range(max_range + 1):
                found = False
                for sensor in self.sensors.keys():
                    distance = self.sensors[sensor]
                    test = abs(x - sensor[0]) + abs(y - sensor[1])
                    if test <= distance:
                        found = True
                        break
                if not found:
                    return (x,y)



    def find_hidden_beacon_smart_not(self, max_range):

        def build_sensor_range(sensor, distance):
            if sensor in self.sensors_range:
                return self.sensors_range[sensor]

            sensor_range = set()
            min_x = max(0, sensor[0]-distance)
            max_x = min(sensor[0]+distance, max_range)
            min_y = max(0, sensor[1]-distance)
            max_y = min(sensor[1]+distance, max_range)

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    c = (x,y)
                    sensor_range.add(c)
            if sensor not in self.sensors_range:
                self.sensors_range[sensor] = sensor_range
            return sensor_range

        to_test = set()
        sensors = list(self.sensors.keys())
        for c in itertools.combinations(sensors, 2):
            source = c[0]
            source_distance = self.sensors[source]

            destination = c[1]
            destination_distance = self.sensors[destination]

            print(source, destination)
            distance = source_distance
            min_x = max(0, source[0]-distance)
            max_x = min(source[0]+distance, max_range)
            min_y = max(0, source[1]-distance)
            max_y = min(source[1]+distance, max_range)
            print(min_x, max_x, min_y, max_y)
            distance = destination_distance
            min_x = max(0, destination[0]-distance)
            max_x = min(destination[0]+distance, max_range)
            min_y = max(0, destination[1]-distance)
            max_y = min(destination[1]+distance, max_range)
            print(min_x, max_x, min_y, max_y)


            source_set = build_sensor_range(source, source_distance)
            destination_set = build_sensor_range(destination, destination_distance)

            intersection = source_set.intersection(destination_set)
            print(f'intersection is {len(intersection)}')
            to_test.update(intersection)

        print(f'we have {len(to_test)} locations to check')

        for elem in to_test:
            x = elem[0]
            y = elem[1]
            test_beacon = (x, y)
            if test_beacon in self.checked:
                continue
            found = False

            for sensor, distance in self.sensors.items():
                for y_delta in range(-distance, distance+1):
                    if abs(sensor[1] + y_delta) > max_range:
                        continue
                    x_to_pad = distance-abs(y_delta)
                    delta = 2 * x_to_pad + 1
                    for x_delta in range(-x_to_pad, -x_to_pad+delta):
                        test_c = (sensor[0] + x_delta, sensor[1] + y_delta)
                        if abs(test_c[0]) > max_range:
                            continue
                        self.checked.append(test_c)
                        if test_c == test_beacon:
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
            if not found:
                return test_beacon




    def find_hidden_beacon_smart_not_to_smart(self, max_range):
        for y in range(max_range + 1):
            for x in range(max_range + 1):
                test_beacon = (x, y)
                if test_beacon in self.checked:
                    continue
                found = False

                for sensor, distance in self.sensors.items():
                    for y_delta in range(-distance, distance+1):
                        if abs(sensor[1] + y_delta) > max_range:
                            continue
                        x_to_pad = distance-abs(y_delta)
                        delta = 2 * x_to_pad + 1
                        for x_delta in range(-x_to_pad, -x_to_pad+delta):
                            test_c = (sensor[0] + x_delta, sensor[1] + y_delta)
                            if abs(test_c[0]) > max_range:
                                continue
                            self.checked.append(test_c)
                            if test_c == test_beacon:
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                if not found:
                    return test_beacon


    def find_hidden_beacon(self, max_range):
        for y in range(max_range + 1):
            for x in range(max_range + 1):
                c = (x, y)
                if c not in self.grid:
                    return c

    def add_sensor_distance(self, sensor, distance):
        self.sensors[sensor] = distance

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


def solve_part2(data, max_range):
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
        distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        grid.add_sensor_distance(sensor, distance)

    beacon = grid.find_hidden_beacon_smart(max_range)
    print(f'found beacon at {beacon}')
    return beacon[0] * 4000000 + beacon[1]


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
    result = solve_part2(data, 20)
    print(f'test2 is {result}')
    assert result == 56000011


def part2():
    data = load_data()
    result = solve_part2(data, 4000000)
    print(f'part2 is {result}')


# test_part1()
# part1()
test_part2()
part2()
