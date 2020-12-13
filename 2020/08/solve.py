#!/usr/bin/env python
import re

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = [
        'nop +0',
        'acc +1',
        'jmp +4',
        'acc +3',
        'jmp -3',
        'acc -99',
        'acc +1',
        'jmp -4',
        'acc +6',
    ]

    is_valid, result = find_accumulator_before_loop(data)
    print(f'test result is {result}')
    assert result == 5

def find_accumulator_before_loop(data):
    accumulator = 0
    index = 0
    processed_index = []
    stop = False
    is_valid = False
    while not stop:
        if index == len(data):
            is_valid = True
            stop = True
            break
        current = data[index]
        if index in processed_index:
            stop = True
            break
        operation = current.split(' ')[0]
        delta = int(current.split(' ')[1])

        processed_index.append(index)
        if operation == 'nop':
            index += 1
        elif operation == 'acc':
            accumulator += delta
            index += 1
        elif operation == 'jmp':
            index += delta
    return is_valid, accumulator


def test_part2():
    data = [
        'nop +0',
        'acc +1',
        'jmp +4',
        'acc +3',
        'jmp -3',
        'acc -99',
        'acc +1',
        'jmp -4',
        'acc +6',
    ]
    result = fix_part2(data)
    print(f'test part2 is {result}')
    assert result == 8


def fix_part2(data):

    is_valid = False
    index_tested = []
    index = len(data) - 1
    accumulator = 0
    while not is_valid:
        print(f'index {index}')
        current = data[index]

        operation = current.split(' ')[0]
        delta = int(current.split(' ')[1])

        if operation == 'nop':
            operation = 'jmp'
        elif operation == 'jmp':
            operation = 'nop'

        new_data = data.copy()
        new_data[index] = '{0} {1}'.format(operation, delta)
        is_valid, accumulator = find_accumulator_before_loop(new_data)
        if not is_valid:
            index -= 1
    print(f'stop at index {index} {data[index]}')

    return accumulator



def part1():
    data = load_data()
    is_valid, result = find_accumulator_before_loop(data)
    print(f'result1 is {result}')

def part2():
    data = load_data()
    result = fix_part2(data)
    print(f'result2 is {result}')



test_part1()
part1()
test_part2()
part2()
