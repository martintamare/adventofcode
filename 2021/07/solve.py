#!/usr/bin/env python

from statistics import median, mean
from math import ceil, floor

test_data = [
    '16,1,2,0,4,2,7,1,2,14',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part_1(data):
    data = list(map(int, data.split(',')))
    data_median = median(data)
    fuels = list(map(lambda x: abs(data_median-x), data))
    return sum(fuels)

# 1 -> 1                 =  1
# 2 -> 1 + 2             =  3
# 3 -> 1 + 2 + 3         =  6
# 4 -> 1 + 2 + 3 + 4     = 10
# 5 -> 1 + 2 + 3 + 4 + 5 = 15
#                           

CACHE = {}

def compute_fuel(step):
    if step not in CACHE:
        cache = sum(list(range(1, step+1)))
        CACHE[step] = cache
    return CACHE[step]


def solve_part_2(data):
    data = list(map(int, data.split(',')))
    data_mean = mean(data)
    solutions = [int(floor(data_mean)), int(ceil(data_mean))]

    current_min_fuel = None
    for solution in solutions:
        fuel = sum(list(map(lambda x: compute_fuel(abs(solution-x)), data)))
        if current_min_fuel is None:
            current_min_fuel = fuel
        elif fuel < current_min_fuel:
            current_min_fuel = fuel
    return current_min_fuel


def test_part1():
    data = test_data
    result = solve_part_1(data[0])
    print(f'test1 is {result}')
    assert result == 37


def test_part2():
    data = test_data
    result = solve_part_2(data[0])
    print(f'test2 is {result}')
    assert result == 168
    assert compute_fuel(1) == 1
    assert compute_fuel(2) == 3
    assert compute_fuel(3) == 6
    assert compute_fuel(11) == 66


def part1():
    data = load_data()
    result = solve_part_1(data[0])
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part_2(data[0])
    print(f'part2 is {result}')
    assert result == 97038163


test_part1()
part1()
test_part2()
part2()
