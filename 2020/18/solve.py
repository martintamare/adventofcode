#!/usr/bin/env python
import operator
import re

test_data = [
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

        
def compute_part_1(text):
    x = Infix(lambda x, y: x * y)
    plus = Infix(lambda x, y: x + y)

    to_eval = ''
    for char in text:
        if char == '+':
            to_eval += '|plus|'
        elif char == '*':
            to_eval += '|x|'
        else:
            to_eval += char
    names = {'x': x, 'plus': plus}
    result = eval(to_eval, names)
    return result


def compute_part_2(text):
    x = Infix(lambda x, y: x * y)
    plus = Infix(lambda x, y: x + y)

    to_eval = ''
    for char in text:
        if char == '+':
            to_eval += '<<plus>>'
        elif char == '*':
            to_eval += '|x|'
        else:
            to_eval += char
    names = {'x': x, 'plus': plus}
    result = eval(to_eval, names)
    return result


def test_part1():
    test_data = {
        '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2': 13632,
        '(2 * 3) + (4 * 5)': 26,
        '2 * 3 + (4 * 5)': 26,
        '5 + (8 * 3 + 9 + 3 * 4 * 3)': 437,
        '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))': 12240,
    }

    for text, wanted_value in test_data.items():
        result = compute_part_1(text)
        print(f'test1 for {text} is {result}')
        assert result == wanted_value


def part1():
    data = load_data()
    total = 0
    for text in data:
        total += compute_part_1(text)
    print(f'part1 is {total}')


def test_part2():
    test_data = {
        '2 * 3 + (4 * 5)': 46,
        '5 + (8 * 3 + 9 + 3 * 4 * 3)': 1445,
        '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))': 669060,
        '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2': 23340,
    }

    for text, wanted_value in test_data.items():
        result = compute_part_2(text)
        print(f'test2 for {text} is {result}')
        assert result == wanted_value


def part2():
    data = load_data()
    total = 0
    for text in data:
        total += compute_part_2(text)
    print(f'part2 is {total}')


test_part1()
part1()
test_part2()
part2()
