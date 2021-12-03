#!/usr/bin/env python
import re
from html import escape
import ast

test_data = [
    r'""',
    r'"abc"',
    r'"aaa\"aaa"',
    r'"\x27"',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve(data):
    number_of_string_litterals = 0
    number_of_memory_values = 0
    number_quoted = 0

    for line in data:
        string_litterals = len(line)
        memory_values = len(ast.literal_eval(line))
        double_quotes = len(line) - len(line.replace('"', ''))
        test = repr(line)
        quoted = len(test) + double_quotes
        number_of_string_litterals += string_litterals
        number_of_memory_values += memory_values
        number_quoted += quoted

    return number_of_string_litterals, number_of_memory_values, number_quoted


def test_part1():
    data = test_data
    number_of_string_litterals, number_of_memory_values, number_quoted = solve(data)
    print(f'test1 is {number_of_string_litterals} - {number_of_memory_values} = {number_of_string_litterals - number_of_memory_values}')
    assert number_of_string_litterals == 23
    assert number_of_memory_values == 11


def test_part2():
    data = test_data
    number_of_string_litterals, number_of_memory_values, number_quoted = solve(data)
    assert number_quoted == 42


def part1():
    data = load_data()
    number_of_string_litterals, number_of_memory_values, number_quoted = solve(data)
    print(f'part1 is {number_of_string_litterals} - {number_of_memory_values} = {number_of_string_litterals - number_of_memory_values}')


def part2():
    data = load_data()
    number_of_string_litterals, number_of_memory_values, number_quoted = solve(data)
    print(f'part1 is {number_quoted} - {number_of_string_litterals} = {number_quoted - number_of_string_litterals}')


test_part1()
part1()
test_part2()
part2()
