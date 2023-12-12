#!/usr/bin/env python
from functools import cache

test_data = [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1',
]

test_result = [
        1,
        4,
        1,
        1,
        4,
        10,
]

test_result_2 = [
        1,
        16384,
        1,
        16,
        2500,
        506250,
]

@cache
def do_recursion(pattern, groups):
    if len(groups) == 0:
        # If ? or empty or ''
        if '#' not in pattern:
            return 1
        else:
            return 0

    max_group = max(groups)
    max_group_index = groups.index(max_group)

    result = 0
    # Sliding
    for i in range(len(pattern) - max_group + 1):
        # On a que des # ou des ? dans notre slide
        condition_1 = pattern[i:i+max_group].count('.') == 0
        # Au début ou juste après un . ou un ?
        condition_2 = i==0 or pattern[i-1] in ['.', '?']
        # En fin de patterne ou juste avant un . ou ?
        condition_3 = i + max_group == len(pattern) or pattern[i+max_group] in ['.', '?']

        # position that can fit
        if condition_1 and condition_2 and condition_3:
            left_pattern = pattern[:max(0,i-1)]
            left_group = groups[:max_group_index]

            right_pattern = pattern[i+max_group+1:]
            right_group = groups[max_group_index+1:]

            left = do_recursion(left_pattern, left_group)
            right = do_recursion(right_pattern, right_group)

            result += left * right
    return result


class Record:
    def __init__(self, data, version=1):
        records = data.split(' ')[0]
        groups = list(map(int, data.split(' ')[1].split(',')))

        if version == 2:
            new_records = ''
            new_groups = []
            for i in range(5):
                new_groups += groups
                if i == 0:
                    new_records = records
                else:
                    new_records += '?' + records
            records = new_records
            groups = new_groups
            print(records)
            print(groups)

        self.groups = tuple(groups)
        self.records = records


    @property
    def arrangements(self):
        return do_recursion(self.records, self.groups)

    def __repr__(self):
        return f"{self.groups=} {self.records=}"



def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    total = 0
    l = len(data)
    for index, line in enumerate(data):
        print(f"{index} / {l}")
        test = Record(line).arrangements
        print(f"{line} arrangements {test}")
        total += test
    return total


def solve_part2(data):
    total = 0
    l = len(data)
    for index, line in enumerate(data):
        print(f"{index} / {l}")
        test = Record(line, version=2).arrangements
        print(f"{line} arrangements {test}")
        total += test
    return total


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 21


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 7792


def test_part2():
    data = test_data
    for index, line in enumerate(data):
        test = Record(line, version=2).arrangements
        print(f"{line} arrangements {test}")
        assert test == test_result_2[index]


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
