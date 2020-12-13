#!/usr/bin/env python


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = [
        '16',
        '10',
        '15',
        '5',
        '1',
        '11',
        '7',
        '19',
        '6',
        '12',
        '4',
    ]
    data = [int(x) for x in data]

    jolt_1_differences = compute_jolt_differences(data, diff=1)
    print(f'jolt_1_differences {jolt_1_differences}')
    assert jolt_1_differences == 7
    jolt_3_differences = compute_jolt_differences(data, diff=3)
    print(f'jolt_3_differences {jolt_3_differences}')
    assert jolt_3_differences == 5

    data = [
        '28',
        '33',
        '18',
        '42',
        '31',
        '14',
        '46',
        '20',
        '48',
        '47',
        '24',
        '23',
        '49',
        '45',
        '19',
        '38',
        '39',
        '11',
        '1',
        '32',
        '25',
        '35',
        '8',
        '17',
        '7',
        '9',
        '4',
        '2',
        '34',
        '10',
        '3',
    ]
    data = [int(x) for x in data]

    jolt_1_differences = compute_jolt_differences(data, diff=1)
    print(f'jolt_1_differences {jolt_1_differences}')
    assert jolt_1_differences == 22
    jolt_3_differences = compute_jolt_differences(data, diff=3)
    print(f'jolt_3_differences {jolt_3_differences}')
    assert jolt_3_differences == 10


class Candidate:

    def __init__(self, effective_rating_jolt, data):
        self.effective_rating_jolt = effective_rating_jolt
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def find_children(self):
        children = []
        for index in range(len(self.data)):
            jolt = self.data[index]
            if jolt - self.effective_rating_jolt < 4:
                child = Candidate(jolt, self.data[index:])
                children.append(child)
        return children


def compute_jolt_differences(data, diff):
    effective_rating_jolt = 0
    data = sorted(data)
    data.append(data[-1] + 3)
    number_of_diff = 0
    for jolt in data:
        jolt = int(jolt)
        if jolt - effective_rating_jolt < 4:
            if jolt - effective_rating_jolt == diff:
                number_of_diff += 1
            effective_rating_jolt = jolt
        else:
            print(f'weird jolt {jolt}')
            exit(1)

    return number_of_diff


def test_part2():
    data = [
        '16',
        '10',
        '15',
        '5',
        '1',
        '11',
        '7',
        '19',
        '6',
        '12',
        '4',
    ]
    data = [int(x) for x in data]
    arrgements = find_arrangement(data)
    print(f'arrgements are {arrgements}')
    assert arrgements == 8


def test_part22():

    data = [
        '28',
        '33',
        '18',
        '42',
        '31',
        '14',
        '46',
        '20',
        '48',
        '47',
        '24',
        '23',
        '49',
        '45',
        '19',
        '38',
        '39',
        '11',
        '1',
        '32',
        '25',
        '35',
        '8',
        '17',
        '7',
        '9',
        '4',
        '2',
        '34',
        '10',
        '3',
    ]
    data = [int(x) for x in data]
    arrgements = find_arrangement(data)
    print(f'arrgements are {arrgements}')
    assert arrgements == 19208


def find_arrangement_recurse(data):
    data = sorted(data)
    data.append(data[-1] + 3)
    data.insert(0, 0)

    def recurse(data, current):
        if len(data) == 1:
            return 1
        else:
            count = 0
            jolt = data[0]
            for test_index in range(1, len(data)):
                test_jolt = data[test_index]
                if test_jolt - jolt < 4:
                    test_current = current.copy()
                    test_current.append(test_jolt)
                    count = count + recurse(data[test_index:], test_current)
            return count

    arrgements = recurse(data, [])
    return arrgements


def find_arrangement(data):
    data = sorted(data)
    data.append(data[-1] + 3)
    data.insert(0, 0)

    result_at_level = [1]
    for index in range(1, len(data)):
        jolt = data[index]
        candidates = 0
        for test_index in range(max(0, index-3), index):
            test_jolt = data[test_index]
            if jolt - test_jolt < 4:
                candidates += result_at_level[test_index]
        result_at_level.append(candidates)
    return result_at_level[-1]


def part1():
    data = load_data()
    data = [int(x) for x in data]
    result = compute_jolt_differences(data, diff=1) * compute_jolt_differences(data, diff=3)
    print(f'result1 is {result}')


def part2():
    data = load_data()
    data = [int(x) for x in data]
    result = find_arrangement(data)
    print(f'result2 is {result}')


test_part1()
part1()
test_part2()
test_part22()
part2()
