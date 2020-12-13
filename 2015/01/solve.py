#!/usr/bin/env python

test_data = [
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = '))((((('
    result = find_floor(data)
    print(f'test1 is {result}')
    assert result == 3


def find_floor(data):
    total = sum([1 if x == '(' else -1 for x in data])
    return total


def test_part2():
    data = '()())'
    result = find_basement_char(data)
    print(f'test2 is {result}')
    assert result == 5


def find_basement_char(data):
    total_sum = 0
    for index in range(len(data)):
        char = data[index]
        to_add = 1 if char == '(' else -1
        total_sum += to_add
        if total_sum == -1:
            return index+1
    return None


def part1():
    data = load_data()
    result = find_floor(data[0])
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = find_basement_char(data[0])
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
