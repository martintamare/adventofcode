#!/usr/bin/env python


test_data = [
    '1000',
    '2000',
    '3000',
    '',
    '4000',
    '',
    '5000',
    '6000',
    '',
    '7000',
    '8000',
    '9000',
    '',
    '10000',
]


def get_calories_per_elves(data):
    elves_count = []
    current = 0
    for item in data:
        if not item:
            elves_count.append(current)
            current = 0
        else:
            current += int(item)
    elves_count.append(current)
    return elves_count


def solve_part_1(data):
    return max(get_calories_per_elves(data))


def solve_part_2(data):
    bags = sorted(get_calories_per_elves(data), reverse=True)
    return bags[0] + bags[1] + bags[2]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 24000


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 45000


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
