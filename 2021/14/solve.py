#!/usr/bin/env python
from collections import Counter

test_data = [
    'NNCB',
    '',
    'CH -> B',
    'HH -> N',
    'CB -> H',
    'NH -> C',
    'HB -> C',
    'HC -> B',
    'HN -> C',
    'NN -> C',
    'BH -> H',
    'NC -> B',
    'NB -> B',
    'BN -> B',
    'BB -> N',
    'BC -> B',
    'CC -> N',
    'CN -> C',
]

CACHE = {}




def solve_part_1(data, iteration=10):

    data = data.copy()
    template = data.pop(0)
    data.pop(0)

    links = {}
    for line in data:
        source = line.split(' -> ')[0]
        dest = line.split(' -> ')[1]
        if source in links:
            print('fdazjdnakzjfnazkjfnazjk')
            exit(0)
        links[source] = dest

    cache = {}

    def recurse(value, iteration_remaining):
        print(f'iteration {iteration_remaining}')
        new_value = list(range(0, 2*len(value)-1))
        new_value = ''

        if value in cache:
            print('we have cache')
            exit(0)

        for i in range(len(value) - 1):
            window = value[i:i+2]
            if i == 0:
                new_value += value[i]
                new_value += links[window]
                new_value += value[i+1]
            else:
                new_value += links[window]
                new_value += value[i+1]
        new_value = ''.join(new_value)

        if iteration_remaining == 1:
            return new_value
        else:
            cache[value] = new_value
            return recurse(new_value, iteration_remaining - 1)
    def recurse2(value, iteration_remaining):
        print(f'iteration {iteration_remaining}')
        if iteration_remaining == 0:
            return value

        if len(value) == 2:
            new_value = ''
            new_value += value[0]
            new_value += links[value]
            new_value += value[1]
            return new_value
        else:
            new_value = value[0]
            temp_value = recurse2(value[1:], iteration_remaining)
            new_value += temp_value
            return recurse2(new_value, iteration_remaining - 1)

            
    final_value = recurse2(template, iteration)
    counter = Counter(final_value)
    most_common = None
    least_common = None

    for key, data in counter.items():
        if most_common is None:
            most_common = data
        elif data > most_common:
            most_common = data
        if least_common is None:
            least_common = data
        elif data < least_common:
            least_common = data

    return most_common - least_common



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
    assert result == 1588


def test_part2():
    data = test_data
    result = solve_part_1(data, iteration=40)
    print(f'test2 is {result}')
    assert result == 2188189693529


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')
    assert result == 2223


def part2():
    data = load_data()
    result = solve_part_1(data, iteration=40)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
#part2()
