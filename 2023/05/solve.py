#!/usr/bin/env python
import itertools

test_data = [
    'seeds: 79 14 55 13',
    '',
    'seed-to-soil map:',
    '50 98 2',
    '52 50 48',
    '',
    'soil-to-fertilizer map:',
    '0 15 37',
    '37 52 2',
    '39 0 15',
    '',
    'fertilizer-to-water map:',
    '49 53 8',
    '0 11 42',
    '42 0 7',
    '57 7 4',
    '',
    'water-to-light map:',
    '88 18 7',
    '18 25 70',
    '',
    'light-to-temperature map:',
    '45 77 23',
    '81 45 19',
    '68 64 13',
    '',
    'temperature-to-humidity map:',
    '0 69 1',
    '1 0 69',
    '',
    'humidity-to-location map:',
    '60 56 37',
    '56 93 4',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class MapperRange:
    def __init__(self, destination_range_start, source_range_start, range_length):
        self.destination_range_start = destination_range_start
        self.source_range_start = source_range_start
        self.range_length = range_length

    def __repr__(self):
        return f"destination_range_start={self.destination_range_start} source_range_start={self.source_range_start} range_length={self.range_length}"

    def has_mapping(self, value):
        if value >= self.source_range_start:
            if value < self.source_range_start+ self.range_length:
                return True
        else:
            return False

    def mapping(self, value):
        delta = value - self.source_range_start
        return self.destination_range_start + delta


class Mapper:
    def __init__(self, source, destination, data):
        self.source = source
        self.destination = destination

        self.ranges = []
        for line in data:
            real_data = list(map(int, line.split(' ')))
            mapper_range = MapperRange(real_data[0], real_data[1], real_data[2])
            self.ranges.append(mapper_range)
            print(real_data)

    def __repr__(self):
        return f"{self.source}-to-{self.destination}"

    def find_next(self, value_to_map):
        for r in self.ranges:
            if r.has_mapping(value_to_map):
                test = r.mapping(value_to_map)
                #print(f"current={value_to_map} map to {test}")
                return test
        return value_to_map


def get_mappers(data):
    mappers = []
    while len(data):
        base_line = data.pop(0)
        source = base_line.split(' ')[0].split('-to-')[0]
        destination = base_line.split(' ')[0].split('-to-')[1]
        lines = []
        stop = False
        while not stop:
            if not len(data):
                stop = True
                break
            line = data.pop(0)
            if not line:
                stop = True
                break
            print(line)
            lines.append(line)
        mapper = Mapper(source, destination, lines)
        mappers.append(mapper)
    return mappers


def solve_part1(data):
    seeds_line = data.pop(0)
    seeds = map(int, seeds_line.split(':')[1].strip().split(' '))
    data.pop(0)
    mappers = get_mappers(data)

    lowest = None
    for seed in seeds:
        print(f"{seed=}")
        current = seed
        for mapper in mappers:
            new_current = mapper.find_next(current)
            print(f"mapper {mapper} map {current} to {new_current}")
            if not new_current:
                exit(0)
            current = new_current

        if lowest is None:
            lowest = current
        elif current < lowest:
            lowest = current
    return lowest


def solve_part2(data):
    seeds_line = data.pop(0)
    seeds = list(map(int, seeds_line.split(':')[1].strip().split(' ')))
    data.pop(0)

    ranges = []
    for index in range(int(len(seeds)/2)):
        real_index = index*2
        ranges.append(range(seeds[real_index], seeds[real_index]+seeds[real_index+1]))
    print(ranges)

    mappers = get_mappers(data)
    lowest = None
    for r in itertools.chain(ranges):
        for seed in r:
            current = seed
            for mapper in mappers:
                new_current = mapper.find_next(current)
                current = new_current

            if lowest is None:
                lowest = current
                print(f"{seed=} {lowest=}")
            elif current < lowest:
                lowest = current
                print(f"{seed=} {lowest=}")
    return lowest

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 35


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 46


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
