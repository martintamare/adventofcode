#!/usr/bin/env python
import itertools

test_data = [
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = ['2x3x4']
    result = find_size_paper(data)
    print(f'test1 is {result}')
    assert result == 58

    data = ['1x1x10']
    result = find_size_paper(data)
    print(f'test1 is {result}')
    assert result == 43

def find_size_paper(data):
    total = 0
    for line in data:
        dimensions = [int(x) for x in line.split('x')]
        min_side = min(list(map(lambda x: x[0] * x[1], itertools.combinations(dimensions, 2))))
        l = dimensions[0]
        w = dimensions[1]
        h = dimensions[2]
        total_line = (2 * l * w + 2 * w * h + 2 * h * l) + min_side
        total += total_line
    return total


def find_size_ribbon(data):
    total = 0
    for line in data:
        dimensions = [int(x) for x in line.split('x')]
        min_side = min(list(map(lambda x: 2 * x[0] + 2 * x[1], itertools.combinations(dimensions, 2))))
        l = dimensions[0]
        w = dimensions[1]
        h = dimensions[2]
        total_line = min_side + l * w * h
        total += total_line
    return total


def test_part2():
    data = ['2x3x4']
    result = find_size_ribbon(data)
    print(f'test1 is {result}')
    assert result == 34

    data = ['1x1x10']
    result = find_size_ribbon(data)
    print(f'test1 is {result}')
    assert result == 14


def part1():
    data = load_data()
    result = find_size_paper(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = find_size_ribbon(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
