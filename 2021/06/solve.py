#!/usr/bin/env python

test_data = '3,4,3,1,2'

def load_data():
    return '5,4,3,5,1,1,2,1,2,1,3,2,3,4,5,1,2,4,3,2,5,1,4,2,1,1,2,5,4,4,4,1,5,4,5,2,1,2,5,5,4,1,3,1,4,2,4,2,5,1,3,5,3,2,3,1,1,4,5,2,4,3,1,5,5,1,3,1,3,2,2,4,1,3,4,3,3,4,1,3,4,3,4,5,2,1,1,1,4,5,5,1,1,3,2,4,1,2,2,2,4,1,2,5,5,1,4,5,2,4,2,1,5,4,1,3,4,1,2,3,1,5,1,3,4,5,4,1,4,3,3,3,5,5,1,1,5,1,5,5,1,5,2,1,5,1,2,3,5,5,1,3,3,1,5,3,4,3,4,3,2,5,2,1,2,5,1,1,1,1,5,1,1,4,3,3,5,1,1,1,4,4,1,3,3,5,5,4,3,2,1,2,2,3,4,1,5,4,3,1,1,5,1,4,2,3,2,2,3,4,1,3,4,1,4,3,4,3,1,3,3,1,1,4,1,1,1,4,5,3,1,1,2,5,2,5,1,5,3,3,1,3,5,5,1,5,4,3,1,5,1,1,5,5,1,1,2,5,5,5,1,1,3,2,2,3,4,5,5,2,5,4,2,1,5,1,4,4,5,4,4,1,2,1,1,2,3,5,5,1,3,1,4,2,3,3,1,4,1,1'

CACHE = {}


def recurse(fishes, iteration):
    dict_fish = {}
    for fish in fishes:
        if fish in dict_fish:
            dict_fish[fish] += 1
        else:
            dict_fish[fish] = 1

    total = 0
    for fish_value, fish_number in dict_fish.items():
        if fish == 0:
            if iteration == 1:
                total += 2 * fish_number
            else:
                index = f'6,8,{iteration - 1}'
                if index in CACHE:
                    total += CACHE[index] * fish_number
                else:
                    CACHE[index] = recurse([6,8], iteration - 1)
                    total += CACHE[index] * fish_number
        else:
            if iteration == 1:
                total += fish_number
            else:
                index = f'{fish_value - 1},{iteration - 1}'
                if index in CACHE:
                    total += CACHE[index] * fish_number
                else:
                    CACHE[index] = recurse([fish_value - 1], iteration - 1)
                    total += CACHE[index] * fish_number
    return total


def populate(data, iterations):
    fishes = list(map(int, data.split(',')))
    return recurse(fishes, iterations)

def test_part1():
    data = test_data
    result = populate(data, 18)
    print(f'test1 at 18 is {result}')
    assert result == 26
    result = populate(data, 80)
    print(f'test1 is 80 is {result}')
    assert result == 5934


def test_part2():
    data = test_data
    result = populate(data, 256)
    print(f'test2 is {result}')
    assert result == 26984457539


def part1():
    data = load_data()
    result = populate(data, 80)
    assert result == 350917
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = populate(data, 256)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
