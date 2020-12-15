#!/usr/bin/env python
from collections import Counter

test_data = [
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    to_test = {
        'ugknbfddgicrmopn': True,
        'aaa': True,
        'jchzalrnumimnmhp': False,
        'haegwjzuvuyypxyu': False,
        'dvszwmarrgswjxmb': False,
    }
    for string, test_data in to_test.items():
        result = is_nice(string)
        print(f'test {string} is {result}')
        assert result == test_data


def is_nice(data):
    deal_breakers = ['ab', 'cd', 'pq', 'xy']
    for deal_breaker in deal_breakers:
        if deal_breaker in data:
            return False

    vowels = len(list(filter(lambda x: x in ['a', 'e', 'i', 'o', 'u'], data)))
    if vowels < 3:
        return False

    has_double = False
    last_char = data[0]
    for index in range(1, len(data)):
        test_char = data[index]
        if test_char == last_char:
            has_double = True
            break
        else:
            last_char = test_char

    if not has_double:
        return False

    return True


def is_really_nice(data):
    has_double = False

    def gen_key(input_1, input_2):
        return f'{input_1}{input_2}'

    tuple_dict = {}

    for index in range(1, len(data)):
        dict_index = gen_key(data[index-1], data[index])
        if dict_index in tuple_dict:
            for other_index in tuple_dict[dict_index]:
                if abs(other_index-index) > 1:
                    has_double = True
                    break
            tuple_dict[dict_index].append(index)
        else:
            tuple_dict[dict_index] = [index]
    if not has_double:
        return False

    has_double = False
    last_char = data[0]
    middle_char = data[1]
    for index in range(2, len(data)):
        test_char = data[index]
        if test_char == last_char:
            has_double = True
            break
        else:
            last_char = middle_char
            middle_char = test_char

    if not has_double:
        return False

    return True


def test_part2():
    to_test = {
        'qjhvhtzxzqqjkmpb': True,
        'xxyxx': True,
        'uurcxstgmygtbstg': False,
        'ieodomkazucvgmuy': False,
    }
    for string, test_data in to_test.items():
        result = is_really_nice(string)
        print(f'test {string} is {result}')
        assert result == test_data


def part1():
    data = load_data()
    result = len(list(filter(lambda x: is_nice(x), data)))
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = len(list(filter(lambda x: is_really_nice(x), data)))
    print(f'part2 is {result}')


test_part1()
#part1()
test_part2()
part2()
