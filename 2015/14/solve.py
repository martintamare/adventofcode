#!/usr/bin/env python

test_data = [
    'Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.',
    'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Rain:
    def __init__(self, name, flying_speed, flying_duration, resting_duration):
        self.name = name
        self.flying_speed = flying_speed
        self.flying_duration = flying_duration
        self.resting_duration = resting_duration
        self.resting_time = 0
        self.flying_time = 0
        self.distance = 0
        self.status = 'flying'
        self.points = 0

    def add_point(self):
        self.points += 1

    def run(self):
        if self.status == 'flying':
            if self.flying_time == self.flying_duration:
                self.status = 'resting'
                self.resting_time = 1
            else:
                self.distance += self.flying_speed
                self.flying_time += 1
        else:
            if self.resting_time == self.resting_duration:
                self.status = 'flying'
                self.flying_time = 1
                self.distance += self.flying_speed
            else:
                self.resting_time += 1


def get_rains(data):
    rains = []
    for line in data:
        splitted = line.split(' ')
        flying_speed = int(splitted[3])
        flying_duration = int(splitted[6])
        resting_duration = int(splitted[13])
        name = splitted[0]
        rain = Rain(name, flying_speed, flying_duration, resting_duration)
        rains.append(rain)
    return rains


def solve_part1(data, time_to_run):
    rains = get_rains(data)

    print(f'Running for {time_to_run} seconds')
    for second in range(time_to_run):
        if second + 1 in [1, 10, 11, 12, 1000, 2503]:
            print(f'second {second + 1}')
        for rain in rains:
            rain.run()
            if second + 1 in [1, 10, 11, 12, 1000, 2503]:
                print(f'Rain {rain.name} is at {rain.distance} with status {rain.status}')

    maximum_distance = max(map(lambda x: x.distance, rains))
    return maximum_distance


def solve_part2(data, time_to_run):
    rains = get_rains(data)

    print(f'Running for {time_to_run} seconds')
    for second in range(time_to_run):
        if second + 1 in [1, 10, 11, 12, 1000, 2503]:
            print(f'second {second + 1}')
        for rain in rains:
            rain.run()
            if second + 1 in [1, 10, 11, 12, 1000, 2503]:
                print(f'Rain {rain.name} is at {rain.distance} with status {rain.status}')  # noqa

        maximum_distance = max(map(lambda x: x.distance, rains))
        for rain in rains:
            if rain.distance == maximum_distance:
                rain.add_point()

    maximum_points = max(map(lambda x: x.points, rains))
    return maximum_points


def test_part1():
    data = test_data
    result = solve_part1(data, 1000)
    print(f'test1 is {result}')
    assert result == 1120


def test_part2():
    data = test_data
    result = solve_part2(data, 1000)
    print(f'test2 is {result}')
    assert result == 689


def part1():
    data = load_data()
    result = solve_part1(data, 2503)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data, 2503)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
