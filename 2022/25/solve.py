#!/usr/bin/env python

test_data = [
    '1=-0-2',
    '12111',
    '2=0=',
    '21',
    '2=01',
    '111',
    '20012',
    '112',
    '1=-1=',
    '1-12',
    '12',
    '1=',
    '122',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Number:
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_decimal(cls, decimal):
        max_value = 5
        iteration = 0
        stop = False
        while not stop:
            if decimal // max_value > 0:
                max_value *= 5
                iteration += 1
            else:
                stop = True

        mapping = {
                -2: '=',
                -1: '-',
                0: '0',
                1: '1',
                2: '2',
        }

        remaining = decimal
        value = ''
        for i in reversed(range(iteration+1)):
            to_divide = pow(5, i)
            correct = None
            min_delta = None
            for j in range(-2,2):
                delta_1 = j * to_divide
                delta_2 = (j+1) * to_divide
                r_1 = delta_1 - remaining
                r_2 = delta_2 - remaining
                delta = abs(r_1+r_2)
                if min_delta is None:
                    min_delta = delta
                    correct = j
                elif delta < min_delta:
                    min_delta = delta
                    correct = j

            r_1 = (correct*to_divide) - remaining
            r_2 = ((correct+1)*to_divide) - remaining
            if abs(r_1) < abs(r_2):
                final_correct = correct
            elif abs(r_1) > abs(r_2):
                final_correct = correct + 1
            elif r_1 == 0:
                final_correct = correct
            elif r_2 == 0:
                final_correct = correct + 1

            remaining -= final_correct * to_divide
            value += mapping[final_correct]
        return cls(value)

    def __str__(self):
        return self.value

    def to_decimal(self):
        length = len(self.value)
        decimal = 0
        for i in range(length):
            value = self.value[i]
            power = length - i - 1
            if value == '=':
                value = -2
            elif value == '-':
                value = -1
            else:
                value = int(value)
            decimal += pow(5, power) * value
        return decimal


def solve_part1(data):
    assert Number('2=-01').to_decimal() == 976
    assert str(Number.from_decimal(976)) == '2=-01'
    total = 0
    for line in data:
        number = Number(line)
        total += number.to_decimal()
    return total


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 4890

    number = Number.from_decimal(result)
    assert f'{number}' == '2=-1=0'


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    number = Number.from_decimal(result)
    print(f'input is {number}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
