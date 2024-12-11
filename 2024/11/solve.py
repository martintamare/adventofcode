#!/usr/bin/env python

test_data = [
    "125 17",
]

test_data_2 = [
    "0 1 10 99 999",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def get_next_numbers(number):
    if number == 0:
        return [1]
    elif len(f"{number}") % 2 == 0:
        str_number = f"{number}"
        middle_index = int(len(str_number) / 2)
        return [int(str_number[0:middle_index]), int(str_number[middle_index:])]
    else:
        return[number * 2024]

def solve_part1(data, iterations):
    init_numbers = list(map(int, data.split(' ')))
    
    shortcuts = {}
    result = 0
    for number in sorted(init_numbers):
        shortcuts[number] = get_next_numbers(number)
    
    finished = False
    while not finished:
        finished = True
        to_add = {}
        for numbers in shortcuts.values():
            for number in numbers:
                if number not in shortcuts:
                    to_add[number] = get_next_numbers(number)
                    finished = False
        shortcuts.update(to_add)

    print("Shortcuts computed")

    result_shortcut = {}

    def compute_result(iteration, number):
        index = f"{iteration}_{number}"
        if index in result_shortcut:
            return result_shortcut[index]

        if iteration == 1:
            result = len(shortcuts[number])
        else:
            result = 0
            for next_number in shortcuts[number]:
                result += compute_result(iteration-1, next_number)
        result_shortcut[index] = result
        return result

    result = 0
    for number in init_numbers:
        result += compute_result(iterations, number)

    return result


def test_part1():
    data = test_data[0]
    iteration_result = [
        (1,3),
        (2,4),
        (3,5),
        (4,9),
        (5,13),
        (6,22),
        (25,55312),
    ]

    for vector in iteration_result:
        iteration = vector[0]
        wanted_result = vector[1]
        result = solve_part1(data, iteration)
        print(f'test1 is {result} {iteration=} {wanted_result=}')
        assert result == wanted_result


def part1():
    data = load_data()[0]
    result = solve_part1(data, 25)
    print(f'part1 is {result}')
    assert result == 233050


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()[0]
    result = solve_part1(data, 75)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
part2()
