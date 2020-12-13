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
    data = test_data
    result = None
    print(f'test1 is {result}')
    assert result == 25


def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = load_data()
    result = find_number_of_houses_visited(data[0])
    print(f'part1 is {len(result)}')


def find_number_of_houses_visited(data, house_visited=None):
    current_position = (0,0)
    if house_visited is None:
        house_visited = set(current_position)
    for char in data:
        if char == '>':
            x, y = current_position
            x = x + 1
            current_position = (x, y)
        elif char == '<':
            x, y = current_position
            x = x - 1
            current_position = (x, y)
        elif char == 'v':
            x, y = current_position
            y = y - 1
            current_position = (x, y)
        elif char == '^':
            x, y = current_position
            y = y + 1
            current_position = (x, y)
        else:
            print('WRF ?')
            exit(0)
        house_visited.add(current_position)
    return house_visited


def part2():
    data = load_data()[0]

    santa_result = find_number_of_houses_visited(data[0::2])
    robot_result = find_number_of_houses_visited(data[1::2], santa_result)
    print(len(santa_result))
    print(len(robot_result))
    print(len(set.union(santa_result, robot_result)))

    print(f'part2 is {len(set.union(santa_result,robot_result))}')


#test_part1()
part1()
#test_part2()
part2()
