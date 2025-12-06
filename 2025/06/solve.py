#!/usr/bin/env python
from operator import mul, add

test_data = [
"123 328  51 64",
" 45 64  387 23",
"  6 98  215 314",
"*   +   *   +",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def prepare_data(data):
    final_data = []
    for line in data:
        raw = line.strip().split()
        final_data.append(raw)
    return final_data


def solve_part1(data):
    line = len(data)
    columns = len(data[0])
    total = 0
    for c in range(columns):
        op = data[-1][c]
        if op == "*":
            result = 1
        elif op == "+":
            result = 0
        else:
            raise Exception("d nzhadbzadaz")

        for l in range(line-1):
            number = int(data[l][c])
            if op == "*":
                result *= number
            elif op == "+":
                result += number

        total += result
    return total


def solve_part2(data):
    final_data = []
    for line in data:
        line_data = []
        for char in line:
            try:
                char = int(char)
            except ValueError:
                pass
            line_data.append(char)
        print(line_data)
        print(len(line_data))
        final_data.append(line_data)

    max_index = max(map(len, final_data))
    print(final_data)
    print(f"{max_index=}")

    total = 0
    numbers = []
    for i in range(max_index):
        index = max_index - 1 - i
        print(f"Look at column {index}")
        current_number = ""
        for line in final_data[0:-1]:
            if len(line) - 1 >= index and line[index] != " ":
                print("OK")
                current_number += f"{line[index]}"
            else:
                print("KO")
            print(f"{current_number=}")
        if current_number:
            current_number = int(current_number)
            numbers.append(current_number)

        operator = None
        if len(final_data[-1]) - 1 >= index and final_data[-1][index] in ["*", "+"]:
            print("Got operator will do something")
            operator = final_data[-1][index]
            if operator == "+":
                result = 0
                for number in numbers:
                    result += number
            elif operator == "*":
                result = 1
                for number in numbers:
                    result *= number
            print(f"{result=}")
            total += result
            numbers = []
        else:
            pass
    return total

def test_part1():
    data = prepare_data(test_data)
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 4277556


def part1():
    data = prepare_data(load_data())
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 3263827


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
