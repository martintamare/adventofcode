#!/usr/bin/env python
from functools import cached_property
from itertools import pairwise

test_data = [
    '7 6 4 2 1',
    '1 2 7 8 9',
    '9 7 6 2 1',
    '1 3 2 4 5',
    '8 6 4 4 1',
    '1 3 6 7 9',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Report:
    def __init__(self, numbers):
        self.numbers = numbers

    @property
    def safe(self):
        if self.level is None:
            return False
        min_level = min(list(self.adjacent_levels))
        max_level = max(list(self.adjacent_levels))
        if min_level >= 1 and max_level <= 3:
            return True
        return False

    @cached_property
    def level(self):
        result = None
        current_number = None
        for number in self.numbers:
            if current_number is None:
                current_number = number
                continue
            elif number == current_number:
                return None
            elif number > current_number:
                if result is None:
                    result = "increasing"
                elif result != "increasing":
                    return None
            elif number < current_number:
                if result is None:
                    result = "decreasing"
                elif result != "decreasing":
                    return None
            current_number = number
        return result

    @property
    def adjacent_levels(self):
        levels = map(lambda x: abs(x[0] - x[1]), pairwise(self.numbers))
        return levels

    def __repr__(self):
        return f"{self.numbers}"


def solve_part1(data):
    result = 0
    for line in data:
        numbers = list(map(int, line.split()))
        report = Report(numbers)
        print(f"{report} {report.safe=} {report.level=}")
        if report.safe:
            result += 1
    return result


def solve_part2(data):
    result = 0
    for line in data:
        numbers = list(map(int, line.split()))
        report = Report(numbers)
        print(f"{report} {report.safe=} {report.level=}")
        if report.safe:
            result += 1
        else:
            for index in range(len(numbers)):
                new_numbers = numbers.copy()
                del new_numbers[index]
                report = Report(new_numbers)
                print(f"{report} {report.safe=} {report.level=}")
                if report.safe:
                    result += 1
                    break

    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 2


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 4


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
