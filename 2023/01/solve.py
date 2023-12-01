#!/usr/bin/env python

test_data = [
    '1abc2',
    'pqr3stu8vwx',
    'a1b2c3d4e5f',
    'treb7uchet',
]

test_data_2 = [
    'two1nine',
    'eightwothree',
    'abcone2threexyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    numbers = []
    for line in data:
        number = ''
        for c in line:
            try:
                i = int(c)
                number += c
            except:
                continue
        number = number[0] + number[-1]
        numbers.append(int(number))
    return sum(numbers)


def solve_part2(data):
    new_data = []
    sub = {
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9',
    }
    for line in data:
        new_line = ''
        for index in range(len(line)):
            match = False
            for old_value, new_value in sub.items():
                word_length = len(old_value)
                final_index = min(len(line), index+word_length)
                to_check = line[index:final_index]
                if to_check == old_value:
                    new_line += new_value
                    match = True
                    break
                else:
                    pass
            if not match:
                new_line += line[index]
        new_data.append(new_line)

    return solve_part1(new_data)


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 142


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data_2
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 281


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
