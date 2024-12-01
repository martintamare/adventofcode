#!/usr/bin/env python
import re
from collections import Counter

test_data = [
"3   4",
"4   3",
"2   5",
"1   3",
"3   9",
"3   3",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    pattern = re.compile(r"^(\d+) *(\d+)$")
    first_array = []
    second_array = []
    for line in data:
        m = pattern.match(line)
        if not m:
            raise Exception("cnazjkdnakzjdnazk")
        first, second = m.groups()
        first_array.append(int(first))
        second_array.append(int(second))

    first_array = sorted(first_array)
    second_array = sorted(second_array)

    result = 0
    for index in range(0, len(first_array)):
        result += abs(first_array[index] - second_array[index])

    return result


def solve_part2(data):
    pattern = re.compile(r"^(\d+) *(\d+)$")
    first_array = []
    second_array = []
    for line in data:
        m = pattern.match(line)
        if not m:
            raise Exception("cnazjkdnakzjdnazk")
        first, second = m.groups()
        first_array.append(int(first))
        second_array.append(int(second))

    first_counter = Counter(first_array)
    second_counter = Counter(second_array)

    result = 0
    for elem in first_array:
        if elem in second_counter:
            similarity = second_counter[elem] * elem
            result += similarity
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 11


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 31


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
