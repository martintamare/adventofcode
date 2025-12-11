#!/usr/bin/env python
from collections import defaultdict
from functools import cache

test_data = [
    "aaa: you hhh",
    "you: bbb ccc",
    "bbb: ddd eee",
    "ccc: ddd eee fff",
    "ddd: ggg",
    "eee: out",
    "fff: out",
    "ggg: out",
    "hhh: ccc fff iii",
    "iii: out",
]

test_data_2 = [
    "svr: aaa bbb",
    "aaa: fft",
    "fft: ccc",
    "bbb: tty",
    "tty: ccc",
    "ccc: ddd eee",
    "ddd: hub",
    "hub: fff",
    "eee: dac",
    "dac: fff",
    "fff: ggg hhh",
    "ggg: out",
    "hhh: out",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    nodes = {}
    result = 0
    for line in data:
        source = line.split(':')[0]
        destinations = line.split(':')[1].strip().split(' ')
        if source not in nodes:
            nodes[source] = []
        for destination in destinations:
            if destination not in nodes[source]:
                nodes[source].append(destination)

    @cache
    def recurse(current_node):
        nonlocal result
        if current_node == "out":
            return 1
        else:
            return sum(recurse(destination) for destination in nodes[current_node])

    return recurse("you")

def solve_part2(data):
    nodes = {}
    result = 0
    for line in data:
        source = line.split(':')[0]
        destinations = line.split(':')[1].strip().split(' ')
        if source not in nodes:
            nodes[source] = []
        for destination in destinations:
            if destination not in nodes[source]:
                nodes[source].append(destination)

    @cache
    def recurse(current_node, wanted_destination):
        if current_node == wanted_destination:
            return 1
        elif current_node == "out":
            return 0
        else:
            return sum(recurse(destination, wanted_destination) for destination in nodes[current_node])
            
    total = 1

    print("srv to fft")
    total *= recurse("svr", "fft")
    print(total)

    print("fft to dac")
    total *= recurse("fft", "dac")
    print(total)

    print("dac to out")
    total *= recurse("dac", "out")
    print(total)

    return total

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 5


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data_2
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 2


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
