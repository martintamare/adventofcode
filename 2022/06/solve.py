#!/usr/bin/env python

test_data = [
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    marker = set()
    for index in range(3, len(data)):
        marker = set(data[index-3:index+1])
        print(f'testing "{marker}" lenght={len(marker)}')
        if len(marker) == 4:
            print(f'ok marker at {index}')
            return index + 1


def solve_part2_not_understood(data):
    start_index = solve_part1(data) - 1
    for index in range(start_index+13, len(data)):
        testing = data[index-13:index+1]
        print(f'testing={testing} len={len(testing)}')
        start_of_message = set(testing)
        print(f'message "{start_of_message}" lenght={len(start_of_message)}')
        if len(start_of_message) == 14:
            return index + 1


def solve_part2(data):
    marker = set()
    for index in range(13, len(data)):
        marker = set(data[index-13:index+1])
        print(f'testing "{marker}" lenght={len(marker)}')
        if len(marker) == 14:
            print(f'ok marker at {index}')
            return index + 1


def test_part1():
    data = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
    result = solve_part1(data)
    print(f'{data} is {result}')
    assert result == 5

    data = 'nppdvjthqldpwncqszvftbrmjlhg'
    result = solve_part1(data)
    print(f'{data} is {result}')
    assert result == 6

    data = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
    result = solve_part1(data)
    print(f'{data} is {result}')
    assert result == 10

    data = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
    result = solve_part1(data)
    print(f'{data} is {result}')
    assert result == 11


def test_part2():
    data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
    result = solve_part2(data)
    print(f'{data} is {result}')
    assert result == 19

    data = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
    result = solve_part2(data)
    print(f'{data} is {result}')
    assert result == 23

    data = 'nppdvjthqldpwncqszvftbrmjlhg'
    result = solve_part2(data)
    print(f'{data} is {result}')
    assert result == 23

    data = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
    result = solve_part2(data)
    print(f'{data} is {result}')
    assert result == 29

    data = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
    result = solve_part2(data)
    print(f'{data} is {result}')
    assert result == 26


def part1():
    data = load_data()
    result = solve_part1(data[0])
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data[0])
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
