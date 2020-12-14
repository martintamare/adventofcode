#!/usr/bin/env python
import re

test_data = [
    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    'mem[8] = 11',
    'mem[7] = 101',
    'mem[8] = 0',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = compute_memory_sum(data)
    print(f'test1 is {result}')
    assert result == 165


def compute_memory_sum(data):
    memory = {}
    mem_regex = re.compile(r'^mem\[(\d+)\] = (\d+)$')

    for line in data:
        if line.startswith('mask = '):
            mask = line[7:]
        elif line.startswith('mem'):
            match = mem_regex.search(line)
            memory_index, decimal = match.groups()
            decimal = int(decimal)
            memory_index = int(memory_index)
            final_decimal = compute_value_to_write(decimal, mask)
            memory[memory_index] = final_decimal
    return sum(memory.values())


def compute_value_to_write(value, mask):
    bytes_str = f'{value:b}'.zfill(36)

    final_bytes_str = []
    for index in range(len(bytes_str)):
        if mask[index] in ['1', '0']:
            final_bytes_str.append(mask[index])
        else:
            final_bytes_str.append(bytes_str[index])
    final_bytes_str = ''.join(final_bytes_str)
    final_value = int(final_bytes_str, 2)
    return final_value


def compute_indexes_to_write(value, mask):
    memory_indexes = []
    bytes_str = f'{value:b}'.zfill(36)
    for index in range(len(bytes_str)):
        new_index_to_add = []
        if mask[index] == '1':
            if not memory_indexes:
                memory_indexes.append(mask[index])
            else:
                for memory_index in memory_indexes:
                    memory_index += mask[index]
                    new_index_to_add.append(memory_index)
        elif mask[index] == '0':
            if not memory_indexes:
                memory_indexes.append(bytes_str[index])
            else:
                for memory_index in memory_indexes:
                    memory_index += bytes_str[index]
                    new_index_to_add.append(memory_index)
        else:
            if not memory_indexes:
                memory_indexes = ['0', '1']
            else:
                for memory_index in memory_indexes:
                    new_value = memory_index
                    memory_index += '0'
                    new_value += '1'
                    new_index_to_add.append(new_value)
                    new_index_to_add.append(memory_index)
        for new_index in new_index_to_add:
            memory_indexes.append(new_index)

        # Ugly part, reduce this list to only the max length
        max_length = max(list(map(len, memory_indexes)))
        new_memory_indexes = []
        for memory_index in memory_indexes:
            if len(memory_index) == max_length:
                new_memory_indexes.append(memory_index)
        memory_indexes = new_memory_indexes

    return [int(''.join(x), 2) for x in memory_indexes]


def compute_memory_sum_part2(data):
    memory = {}
    mem_regex = re.compile(r'^mem\[(\d+)\] = (\d+)$')

    for line in data:
        if line.startswith('mask = '):
            mask = line[7:]
        elif line.startswith('mem'):
            match = mem_regex.search(line)
            memory_index, decimal = match.groups()
            decimal = int(decimal)
            memory_index = int(memory_index)
            final_decimal = decimal
            memory_indexes = compute_indexes_to_write(memory_index, mask)

            for memory_index in memory_indexes:
                memory[memory_index] = final_decimal
    return sum(memory.values())


def test_part2():
    data = [
        'mask = 000000000000000000000000000000X1001X',
        'mem[42] = 100',
        'mask = 00000000000000000000000000000000X0XX',
        'mem[26] = 1',
    ]

    result = compute_memory_sum_part2(data)
    print(f'test2 is {result}')
    assert result == 208


def part1():
    data = load_data()
    result = compute_memory_sum(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = compute_memory_sum_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
