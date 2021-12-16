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

    def recurse_smart(value, iteration_remaining):
        """Only count added value."""
        cache_index = f'{value}_{iteration_remaining}'
        if cache_index in cache:
            return cache[cache_index]

        result = Counter()

        if iteration_remaining == 1:
            # Value is always of length 2 here
            new_value = links[value]
            result.update(new_value)
            cache[cache_index] = result
            return result


        for i in range(len(value) - 1):
            window = value[i:i+2]

            # Add added value to the counter
            # NN -> C
            # Add C
            new_value = links[window]
            result.update(new_value)

            # Recurse on pattern before 
            # NC
            window_before = f'{value[i]}{new_value}'
            window_result = recurse_smart(window_before, iteration_remaining - 1)
            result.update(window_result)

            # Recurse on patterne after
            # CN
            window_after = f'{new_value}{value[i+1]}'
            window_result = recurse_smart(window_after, iteration_remaining - 1)
            result.update(window_result)

        cache[cache_index] = result
        return result


    def compute_result(c):
        most_common = None
        least_common = None
        for key, data in c.items():
            if most_common is None:
                most_common = data
            elif data > most_common:
                most_common = data
            if least_common is None:
                least_common = data
            elif data < least_common:
                least_common = data
        return most_common - least_common

    counter = recurse_smart(template, iteration)
    counter.update(template)
    result = compute_result(counter)
    return result



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
part2()
