#!/usr/bin/env python
import itertools

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = [
        '35',
        '20',
        '15',
        '25',
        '47',
        '40',
        '62',
        '55',
        '65',
        '95',
        '102',
        '117',
        '150',
        '182',
        '127',
        '219',
        '299',
        '277',
        '309',
        '576',
    ]

    result = find_number_not_having_property(data, preamble=5)
    print(f'test result is {result}')
    assert result == 127

def test_part2():
    data = [
        '35',
        '20',
        '15',
        '25',
        '47',
        '40',
        '62',
        '55',
        '65',
        '95',
        '102',
        '117',
        '150',
        '182',
        '127',
        '219',
        '299',
        '277',
        '309',
        '576',
    ]

    wanted_number = find_number_not_having_property(data, preamble=5)
    result = find_weakness(data, wanted_number)
    print(f'test result is {result}')
    assert result == 62


def find_weakness(data, wanted_number):
    start_index = 0
    found = False
    current_sum = 0

    while not found:
        if start_index >= len(data):
            print('Weird')
            exit(1)

        current_sum = 0
        smallest = None
        largest = None
        for line in data[start_index:]:
            line = int(line)
            if not smallest:
                smallest = line
            else:
                smallest = min(smallest, line)
            if not largest:
                largest = line
            else:
                largest = max(largest, line)

            current_sum += line
            if current_sum == wanted_number:
                found = True
                return largest + smallest
        start_index += 1



def find_number_not_having_property(data, preamble):
    data_to_search = []
    for line in data:
        line = int(line)
        if len(data_to_search) < preamble:
            data_to_search.append(line)
            continue

        is_valid = is_number_valid(line, data_to_search)
        if not is_valid:
            return line
        else:
            data_to_search.pop(0)
            data_to_search.append(line)
    return None

def is_number_valid(number, data):
    for a, b in itertools.combinations(data, 2):
        if a + b == number:
            return True
    return False



def part1():
    data = load_data()
    result = find_number_not_having_property(data, preamble=25)
    print(f'result1 is {result}')

def part2():
    data = load_data()
    wanted_number = find_number_not_having_property(data, preamble=25)
    result = find_weakness(data, wanted_number)
    print(f'result2 is {result}')



test_part1()
part1()
test_part2()
part2()
