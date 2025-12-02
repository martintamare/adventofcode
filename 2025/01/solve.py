#!/usr/bin/env python

test_data = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    result = 0
    current = 50
    for line in data:
        direction = line[0]
        amount = int(line[1:])
        after = current 
        if direction == "R":
            after = (after + amount) % 100
        elif direction == "L":
            after = (after- amount) % 100
        print(f"{current=} {direction=} {amount=} {after=}")
        current = after
        if current == 0:
            result += 1
    return result


def solve_part2(data):
    result = 0
    dial = 50
    for line in data:
        print(f"{dial=}")
        direction = line[0]
        amount = int(line[1:])
        if direction == "R":
            for i in range(amount):
                dial += 1
                if dial == 0:
                    result += 1
                elif dial == 100:
                    result += 1
                    dial = 0
        elif direction == "L":
            for i in range(amount):
                dial -= 1
                if dial == 0:
                    result += 1
                elif dial == -1:
                    dial = 99
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 3


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 6


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result > 5776


test_part1()
part1()
test_part2()
part2()
