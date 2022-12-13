#!/usr/bin/env python
from itertools import permutations
import functools
cache = {}

test_data = [
    '[1,1,3,1,1]',
    '[1,1,5,1,1]',
    '[[1],[2,3,4]]',
    '[[1],4]',
    '[9]',
    '[[8,7,6]]',
    '[[4,4],4,4]',
    '[[4,4],4,4,4]',
    '[7,7,7,7]',
    '[7,7,7]',
    '[]',
    '[3]',
    '[[[]]]',
    '[[]]',
    '[1,[2,[3,[4,[5,6,7]]]],8,9]',
    '[1,[2,[3,[4,[5,6,0]]]],8,9]',
]

test_data_2 = [
    '[]',
    '[[]]',
    '[[[]]]',
    '[1,1,3,1,1]',
    '[1,1,5,1,1]',
    '[[1],[2,3,4]]',
    '[1,[2,[3,[4,[5,6,0]]]],8,9]',
    '[1,[2,[3,[4,[5,6,7]]]],8,9]',
    '[[1],4]',
    '[[2]]',
    '[3]',
    '[[4,4],4,4]',
    '[[4,4],4,4,4]',
    '[[6]]',
    '[7,7,7]',
    '[7,7,7,7]',
    '[[8,7,6]]',
    '[9]',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            if r.strip():
                data.append(r.strip())
    return data


def compare(left, right):
    cache_index = f'{left}_{right}'
    if cache_index in cache:
        return cache[cache_index]

    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return True
            elif left == right:
                return None
            else:
                return False
        elif isinstance(right, list):
            result = compare([left], right)
            cache[cache_index] = result
            return result
        else:
            print(f'right wtf {right}')
            exit(0)
    elif isinstance(left, list):
        if isinstance(right, int):
            result = compare(left, [right])
            cache[cache_index] = result
            return result
        elif isinstance(right, list):
            left_len = len(left)
            right_len = len(right)

            result = None
            for i in range(left_len):
                if i >= right_len:
                    result = False
                    break
                test_left = left[i]
                test_right = right[i]
                temp_result = compare(test_left, test_right)
                if temp_result is None:
                    continue
                else:
                    result = temp_result
                    break
            if result is None:
                if left_len < right_len:
                    result = True
                elif left_len > right_len:
                    result = False
            cache[cache_index] = result
            return result
    else:
        print(f'left wtf {left}')
        exit(0)


class Pair:
    def __init__(self, index, left, right):
        self.index = index
        self.left = eval(left)
        self.right = eval(right)
        self._in_right_order = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'pair {self.index} : {self.left} vs {self.right}'

    @property
    def in_right_order(self):
        if self._in_right_order is not None:
            return self._in_right_order

        result = compare(self.left, self.right)
        self._in_right_order = result
        return result


def solve_part1(data):
    pairs = []
    for i in range(int(len(data)/2)):
        left = data[i*2]
        right = data[i*2+1]
        pair = Pair(i+1, left, right)
        pairs.append(pair)

    total = 0
    for pair in pairs:
        print(f'testing {pair}')
        if pair.in_right_order:
            print(f'{pair.index} in right order')
            total += pair.index
        else:
            print(f'{pair.index} NOT in right order')
    return total


def custom_sorted(x, y):
    test_x = list(x.replace('[', '').replace(']', '').replace(',' , ''))  # noqa
    test_y = list(y.replace('[', '').replace(']', '').replace(',' , ''))  # noqa
    if not test_x:
        test_x.append('-1')
    if not test_y:
        test_y.append('-1')

    x_length = len(test_x)
    y_length = len(test_y)
    for i in range(min(x_length, y_length)):
        x_test = int(test_x[i])
        y_test = int(test_y[i])
        if x_test == y_test:
            continue
        else:
            return x_test - y_test
    return len(x) - len(y)


def solve_part2_too_long(data):
    data.append('[[2]]')
    data.append('[[6]]')
    data = sorted(data, key=functools.cmp_to_key(custom_sorted))
    print(data)

    correct_set = None
    iteration = 1
    for to_test in permutations(data, len(data)):
        is_ok = True
        if iteration % 1000 == 0:
            print(f'iteration {iteration}')
        for i in range(int(len(to_test)/2)):
            left = to_test[i*2]
            right = to_test[i*2+1]
            pair = Pair(i+1, left, right)
            if not pair.in_right_order:
                is_ok = False
                break
        iteration += 1
        if is_ok:
            correct_set = to_test
            break

    print(correct_set)
    index = 1
    result = 1
    for item in correct_set:
        if item == '[[2]]':
            result *= index
        if item == '[[6]]':
            result *= index
            break
        index += 1
    return result


def solve_part2(data):
    data.append('[[2]]')
    data.append('[[6]]')

    valid_pairs_for = {}
    for line in data:
        valid_pairs_for[line] = []

    for i in range(len(data)):
        left = data[i]
        valid_with = []
        for j in range(len(data)):
            if j == i:
                continue
            right = data[j]
            pair = Pair(i+1, left, right)
            if pair.in_right_order:
                valid_with.append(right)
        valid_pairs_for[left] = valid_with
    print('OK all values computed')

    final_set = []

    to_look_for = None
    for source, valid_next in valid_pairs_for.items():
        if not valid_next:
            final_set.append(source)
            to_look_for = source

    while len(final_set) != len(data):
        print(f'Will find {to_look_for}')
        min_next = None
        source_next = None
        for source, valid_next in valid_pairs_for.items():
            if to_look_for in valid_next:
                if min_next is None:
                    min_next = len(valid_next)
                    source_next = source
                elif min_next > len(valid_next):
                    min_next = len(valid_next)
                    source_next = source
        final_set.insert(0, source_next)
        to_look_for = source_next
    print(final_set)

    index = 1
    result = 1
    for item in final_set:
        if item == '[[2]]':
            result *= index
        if item == '[[6]]':
            result *= index
            break
        index += 1
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 13


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 140


def part1():
    data = load_data()
    print(data)
    result = solve_part1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
