#!/usr/bin/env python3

test_data = [
    '199',
    '200',
    '208',
    '210',
    '200',
    '207',
    '240',
    '269',
    '260',
    '263',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

def count_increases(data):
    increase = 0
    last = None
    for d in data:
        if last is None:
            last = int(d)
        elif int(d) > last:
            increase += 1
        last = int(d)
    return increase


def count_increases_part_2(data):
    increase = 0
    last = None
    total_range = range(0, len(data)-2)
    for i in range(0, len(data)-2):
        current_window = int(data[i]) + int(data[i+1]) + int(data[i+2])
        if last is None:
            last = current_window
        elif current_window > last:
            increase += 1
        last = current_window
    return increase


def test_part1():
    data = test_data
    result = count_increases(data)
    print(f'test1 is {result}')
    assert result == 7


def test_part2():
    data = test_data
    result = count_increases_part_2(data)
    print(f'test2 is {result}')
    assert result == 5


def part1():
    data = load_data()
    result = count_increases(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = count_increases_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
