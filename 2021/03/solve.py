#!/usr/bin/env python

test_data = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010',
]



def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

def get_most_common(index, data):
    total_values = len(data)
    total_of_one = len(list(filter(lambda x: x[index] == '1', data)))
    if total_values - total_of_one > total_of_one:
        return '0'
    else:
        return '1'


def get_least_common(index, data):
    if get_most_common(index, data) == '1':
        return '0'
    else:
        return '1'


def get_power_consumption(data):
    gamma_rate = ''

    total_values = len(data)
    length_of_line = len(data[0])
    mask = ''
    for i in range(0, length_of_line):
        gamma_rate += get_most_common(i, data)
        mask += '1'

    gamma_rate = int(gamma_rate, 2)
    mask = int(mask, 2)
    epsilon_rate = ~ gamma_rate & mask

    print(f'gamma_rate is {gamma_rate}')
    print(f'epsilon_rate is {epsilon_rate}')
    return epsilon_rate * gamma_rate
        

def get_life_support_rating(data):
    oxygen_generator_rating = ''

    test_data = data.copy()
    index = 0
    while len(test_data) > 1:
        value_to_test_at_index = get_most_common(index, test_data)
        test_data = list(filter(lambda x: x[index] == value_to_test_at_index, test_data))
        index += 1
    oxygen_generator_rating = test_data[0]

    test_data = data.copy()
    index = 0
    while len(test_data) > 1:
        value_to_test_at_index = get_least_common(index, test_data)
        test_data = list(filter(lambda x: x[index] == value_to_test_at_index, test_data))
        index += 1
    co2_scrubber_rating = test_data[0]

    oxygen_generator_rating = int(oxygen_generator_rating, 2)
    co2_scrubber_rating = int(co2_scrubber_rating, 2)
    print(f'oxygen_generator_rating is {oxygen_generator_rating}')
    print(f'co2_scrubber_rating is {co2_scrubber_rating}')

    return co2_scrubber_rating * oxygen_generator_rating



def test_part1():
    data = test_data
    result = get_power_consumption(data)
    print(f'test1 is {result}')
    assert result == 198


def test_part2():
    data = test_data
    result = get_life_support_rating(data)
    print(f'test2 is {result}')
    assert result == 230


def part1():
    data = load_data()
    result = get_power_consumption(data)
    print(f'part1 is {result}')
    assert result == 4139586


def part2():
    data = load_data()
    result = get_life_support_rating(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
