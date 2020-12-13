#!/usr/bin/env python
import re

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        group_data = []
        for r in f.readlines():
            line = r.strip()
            if not line:
                data.append(group_data)
                group_data = []
            else:
                group_data.append(line)
        data.append(group_data)
    return data


def test_part1():
    data = [
            ['abc'],
            ['a', 'b', 'c'], 
            ['ab', 'ac'],
            ['a', 'a', 'a', 'a'],
            ['b']
    ]

    assert compute_yes(data[0]) == 3
    assert compute_yes(data[1]) == 3
    assert compute_yes(data[2]) == 3
    assert compute_yes(data[3]) == 1
    assert compute_yes(data[4]) == 1


def compute_yes(data):
    yes_dict = {}
    for raw in data:
        for l in raw:
            if l not in yes_dict:
                yes_dict[l] = 1
    return len(yes_dict.keys())


def compute_yes_part2(data):
    yes_dict = {}
    group_size = len(data)
    for raw in data:
        for l in raw:
            if l not in yes_dict:
                yes_dict[l] = 1
            else:
                yes_dict[l] += 1
    total_yes = 0
    for question, total in yes_dict.items():
        if total == group_size:
            total_yes += 1
    return total_yes


def part1():
    groups = load_data()
    total_sum = 0
    for group in groups:
        total_sum += compute_yes(group)
    print(f'Sum is {total_sum}')



def test_part2():
    data = [
            ['abc'],
            ['a', 'b', 'c'], 
            ['ab', 'ac'],
            ['a', 'a', 'a', 'a'],
            ['b']
    ]

    assert compute_yes_part2(data[0]) == 3
    assert compute_yes_part2(data[1]) == 0
    assert compute_yes_part2(data[2]) == 1
    assert compute_yes_part2(data[3]) == 1
    assert compute_yes_part2(data[4]) == 1


def part2():
    groups = load_data()
    total_sum = 0
    for group in groups:
        total_sum += compute_yes_part2(group)
    print(f'Sum for part2 is {total_sum}')
    


test_part1()
part1()
test_part2()
part2()
