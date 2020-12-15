#!/usr/bin/env python
import hashlib

test_data = [
]


def load_data():
    data = 'ckczppom'
    return data


def test_part1():
    data = 'abcdef'
    result = compute_lowest_md5(data)
    print(f'test1 is {result}')
    assert result == 609043

    data = 'pqrstuv'
    result = compute_lowest_md5(data)
    print(f'test1 is {result}')
    assert result == 1048970


def compute_lowest_md5(data, length=5):
    index = 1
    stop = False
    while True:
        if index % 1000 == 0:
            print(f'testing {index}')
        to_hash = f'{data}{index}'.encode()
        result = hashlib.md5(to_hash)
        test = str(result.hexdigest())
        if test.startswith(''.join(['0' for i in range(length)])):
            return index
        else:
            index += 1

def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = 'ckczppom'
    result = compute_lowest_md5(data)
    print(f'part1 is {result}')


def part2():
    data = 'ckczppom'
    result = compute_lowest_md5(data, 6)
    print(f'part2 is {result}')


test_part1()
part1()
part2()
