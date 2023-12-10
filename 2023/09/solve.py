#!/usr/bin/env python

test_data = [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45',
]

test_data_2 = [
    '10 13 16 21 30 45',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Suite:
    def __init__(self, numbers):
        self.numbers = numbers
        self.annexes = []

    def __repr__(self):
        return f"{self.numbers}"

    def compute_new_annexe(self):
        current_numbers = self.numbers
        if len(self.annexes):
            current_numbers = self.annexes[-1]

        new_annex = []
        for index in range(1, len(current_numbers)):
            diff = current_numbers[index] - current_numbers[index-1]
            new_annex.append(diff)
        self.annexes.append(new_annex)

    def find_next(self):
        if not len(self.annexes):
            self.compute_new_annexe()

        while len(list(filter(lambda x: x!=0, self.annexes[-1]))):
            self.compute_new_annexe()

        new_value = 0
        for index in reversed(list(range(0, len(self.annexes)))):
            print(index)
            print(self.annexes[index])
            new_value += self.annexes[index][-1]
        new_value += self.numbers[-1]
        return new_value

    def find_previous(self):
        if not len(self.annexes):
            self.compute_new_annexe()

        while len(list(filter(lambda x: x!=0, self.annexes[-1]))):
            self.compute_new_annexe()

        new_value = 0
        for index in reversed(list(range(len(self.annexes)))):
            new_value = self.annexes[index][0] - new_value

            print(f"{index=} {self.annexes[index]} {new_value}")
        new_value = self.numbers[0] - new_value
        print(f"{index=} {self.annexes[index]} {new_value}")
        return new_value




def solve_part1(data):
    numbers_suite = []
    for line in data:
        numbers = list(map(int, line.split(' ')))
        numbers_suite.append(Suite(numbers))
    print(numbers_suite)

    total = 0
    for suite in numbers_suite:
        total += suite.find_next()
    return total


def solve_part2(data):
    numbers_suite = []
    for line in data:
        numbers = list(map(int, line.split(' ')))
        numbers_suite.append(Suite(numbers))
    print(numbers_suite)

    total = 0
    for suite in numbers_suite:
        total += suite.find_previous()
    return total



def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 114


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
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
