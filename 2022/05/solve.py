#!/usr/bin/env python
from collections import deque

test_data = [
    '    [D]    ',
    '[N] [C]    ',
    '[Z] [M] [P]',
    ' 1   2   3 ',
    '',
    'move 1 from 2 to 1',
    'move 3 from 1 to 3',
    'move 2 from 2 to 1',
    'move 1 from 1 to 2',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r)
    return data


def solve(data, length=9, model='CrateMover9000'):
    data = data.copy()
    deques = []
    for i in range(length):
        deques.append(deque())

    stop = False
    while not stop:
        line = data.pop(0)
        if '[' not in line:
            stop = True
            continue
        for i in range(length):
            index = (i*3) + 1 + i
            element = line[index]
            if element and element != ' ':
                deques[i].append(element)
    data.pop(0)

    for line in data:
        splitted = line.split(' ')
        move = int(splitted[1])
        _from = int(splitted[3])
        to = int(splitted[5])

        index_source = _from - 1
        index_destination = to - 1

        if model == 'CrateMover9000':
            for i in range(move):
                try:
                    item = deques[index_source].popleft()
                except IndexError:
                    continue
                deques[index_destination].appendleft(item)
        elif model == 'CrateMover9001':
            items = [deques[index_source].popleft() for i in range(move)]
            items.reverse()
            for item in items:
                deques[index_destination].appendleft(item)

    final_result = ''
    for d in deques:
        final_result += d.popleft()
    return final_result


def test_part1():
    data = test_data
    result = solve(data, length=3)
    print(f'test1 is {result}')
    assert result == 'CMZ'


def test_part2():
    data = test_data
    result = solve(data, length=3, model='CrateMover9001')
    print(f'test2 is {result}')
    assert result == 'MCD'


def part1():
    data = load_data()
    result = solve(data, length=9)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve(data, length=9, model='CrateMover9001')
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
