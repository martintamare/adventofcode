#!/usr/bin/env python

test_data = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    result = 0
    for line in data:
        test_line = line[:-1]
        digits = sorted(list(set(map(int, test_line))), reverse=True)
        max_digit = digits[0]
        max_index = line.find(f"{max_digit}")
        new_line = line[max_index+1:]
        new_digits = sorted(list(set(map(int, new_line))), reverse=True)
        second_digit = new_digits[0]
        to_add = f"{max_digit}{second_digit}"
        print(f"{line=} {to_add}")
        result += int(to_add)

    return result


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 357


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


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
