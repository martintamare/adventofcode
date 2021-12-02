#!/usr/bin/env python

test_data = [
    'forward 5',
    'down 5',
    'forward 8',
    'up 3',
    'down 8',
    'forward 2',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

def get_position(data):
    horizontal = 0
    depth = 0

    for line in data:
        move = line.split(' ')[0]
        addition = int(line.split(' ')[1])
        if move == 'forward':
            horizontal += addition
        elif move == 'down':
            depth += addition
        elif move == 'up':
            depth -= addition
    return horizontal * depth


def get_position_part_2(data):
    horizontal = 0
    depth = 0
    aim = 0

    for line in data:
        move = line.split(' ')[0]
        addition = int(line.split(' ')[1])
        if move == 'forward':
            horizontal += addition
            depth += aim * addition
        elif move == 'down':
            aim += addition
        elif move == 'up':
            aim -= addition
    return horizontal * depth


def test_part1():
    data = test_data
    result = get_position(data)
    print(f'test1 is {result}')
    assert result == 150


def test_part2():
    data = test_data
    result = get_position_part_2(data)
    print(f'test2 is {result}')
    assert result == 900


def part1():
    data = load_data()
    result = get_position(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = get_position_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
