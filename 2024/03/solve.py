#!/usr/bin/env python
import re

test_data = [
"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
]

test2_data = [
"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    result = 0
    pattern = re.compile(r"(mul\((\d{1,3}),(\d{1,3})\))")
    for line in data:
        for mul in pattern.finditer(line):
            data_all, x1, x2 = mul.groups()
            print(mul)
            result += int(x1) * int(x2)
    return result


def solve_part2(data):
    result = 0
    pattern = re.compile(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))")
    do = True
    for line in data:
        for mul in pattern.finditer(line):
            test, x1, x2 = mul.groups()
            if test.startswith("do()"):
                do = True
                continue
            elif test.startswith("don't()"):
                do = False
            else:
                if not do:
                    continue
                else:
                    result += int(x1) * int(x2)
            continue
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 161


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test2_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 48


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
