#!/usr/bin/env python

test_data = [
    '2-4,6-8',
    '2-3,4-5',
    '5-7,7-9',
    '2-8,3-7',
    '6-6,4-6',
    '2-6,4-8',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    total = 0
    for line in data:
        elve_1 = line.split(',')[0]
        elve_1_set = set(range(int(elve_1.split('-')[0]), int(elve_1.split('-')[1]) + 1))
        print(elve_1_set)
        elve_2 = line.split(',')[1]
        elve_2_set = set(range(int(elve_2.split('-')[0]), int(elve_2.split('-')[1]) + 1))
        print(elve_2_set)
        if elve_1_set.issubset(elve_2_set) or elve_2_set.issubset(elve_1_set):
            print('included')
            total += 1
    return total


def solve_part2(data):
    total = 0
    for line in data:
        elve_1 = line.split(',')[0]
        elve_1_set = set(range(int(elve_1.split('-')[0]), int(elve_1.split('-')[1]) + 1))
        print(elve_1_set)
        elve_2 = line.split(',')[1]
        elve_2_set = set(range(int(elve_2.split('-')[0]), int(elve_2.split('-')[1]) + 1))
        print(elve_2_set)
        if elve_1_set.intersection(elve_2_set) or elve_2_set.intersection(elve_1_set):
            print('included')
            total += 1
    return total


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 2


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 4


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
