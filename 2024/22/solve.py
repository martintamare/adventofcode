#!/usr/bin/env python
from collections import defaultdict

test_data = [
    "1",
    "10",
    "100",
    "2024",
]

test_data_2 = [
    "1",
    "2",
    "3",
    "2024",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Number:
    def __init__(self, data):
        self.data = int(data)
        self.prev = None
        self.prev_price = None
        self.delta = None
        self.original = int(data)

    def __repr__(self):
        return f"{self.data}"

    @property
    def price(self):
        str_data = f"{self.data}"
        return int(f"{str_data[-1]}")

    def next(self):
        self.prev = self.data
        self.prev_price = self.price

        result = (self.data ^ (self.data * 64)) % 16777216
        result = (result ^ int(result / 32)) % 16777216
        result = (result ^ (result * 2048)) % 16777216
        self.data = result
        self.delta = self.price - self.prev_price


def solve_part1(data):
    result = 0
    vectors = defaultdict(dict)
    for n in data:
        number = Number(n)
        print(number)
        current_price = number.price
        deltas = []
        for _ in range (2000):
            number.next()
            deltas.append(number.delta)
            if len(deltas) > 3:
                key = f"{deltas[len(deltas)-4:]}"
                if number.original not in vectors[key]:
                    vectors[key][number.original] = number.price
    print(vectors)
    max_result = None
    max_key = None
    for key, data in vectors.items():
        result = sum(data.values())
        if max_result is None:
            max_result = result
            max_key = key
        elif result > max_result:
            max_result = result
            max_key = key
    print(max_key)
    print(vectors[max_key])
    return max_result


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 37327623


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data_2
    result = solve_part1(data)
    print(f'test2 is {result}')
    assert result == 23


def part2():
    data = load_data()
    result = solve_part1(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
