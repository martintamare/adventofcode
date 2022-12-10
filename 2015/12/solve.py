#!/usr/bin/env python
import json


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    total_sum = get_sum(data)
    return total_sum


def solve_part2(data):
    total_sum = get_sum_without_red(data)
    return total_sum


def get_sum(data):
    total_sum = 0
    if isinstance(data, list):
        for element in data:
            total_sum += get_sum(element)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(key, int):
                total_sum += key
            total_sum += get_sum(value)
    elif isinstance(data, int):
        total_sum += data
    else:
        pass
    return total_sum


def get_sum_without_red(data):
    total_sum = 0
    if isinstance(data, list):
        for element in data:
            total_sum += get_sum_without_red(element)
    elif isinstance(data, dict):
        has_red = False
        element_sum = 0
        for key, value in data.items():
            if key == 'red':
                has_red = True
            elif value == 'red':
                has_red = True
            if isinstance(key, int):
                element_sum += key
            element_sum += get_sum_without_red(value)
        if not has_red:
            return element_sum
        else:
            return 0
    elif isinstance(data, int):
        total_sum += data
    else:
        pass
    return total_sum


def test_part1():
    data = [1,2,3,{"a":2,"b":4}]  # noqa
    result = solve_part1(data)
    print(f'part1 for {data} is {result}')
    assert result == 12

    data = [[[3]], {"a":{"b":4},"c":-1}]  # noqa
    result = solve_part1(data)
    print(f'part1 for {data} is {result}')
    assert result == 6

    data = [{"a":[-1,1]}, [-1,{"a":1}]]  # noqa
    result = solve_part1(data)
    print(f'part1 for {data} is {result}')
    assert result == 0

    data = [{},[]]  # noqa
    result = solve_part1(data)
    print(f'part1 for {data} is {result}')
    assert result == 0


def test_part2():
    data = [1,{"c":"red","b":2},3]  # noqa
    result = solve_part2(data)
    print(f'part2 for {data} is {result}')
    assert result == 4

    data = {"d":"red","e":[1,2,3,4],"f":5}  # noqa
    result = solve_part2(data)
    print(f'part2 for {data} is {result}')
    assert result == 0

    data = [1,"red",5]  # noqa
    result = solve_part2(data)
    print(f'part2 for {data} is {result}')
    assert result == 6


def part1():
    data = load_data()
    result = solve_part1(json.loads(data[0]))
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(json.loads(data[0]))
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
