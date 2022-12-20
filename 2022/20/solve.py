#!/usr/bin/env python

test_data = [
    1,
    2,
    -3,
    3,
    -2,
    0,
    4,
]

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(int(r.strip()))
    return data


def solve_part1(data):
    indexes = []
    positions = []
    for index in range(len(data)):
        indexes.append({'data': data[index], 'position': index})
        positions.append({'data': data[index], 'mapping': index})

    def print_positions():
        for index in range(len(positions)):
            position = positions[index]['data']
            if index == len(positions) - 1:
                print(position)
            else:
                print(position, end=', ')

    def print_indexes():
        test = set()
        for index in range(len(positions)):
            print(indexes[index])
            test.add(indexes[index]['position'])
            data = indexes[index]['data']
            position = indexes[index]['position']
            assert positions[position]['data'] == data
        print(f'we have {len(test)}')
        if len(test) < len(positions):
            print('BYUGGGGGGGGGGGGGG')
            input()

    print('=====Init=====')
    print_positions()

    total_length = len(positions)

    # Iteration 1
    for index in range(len(data)):
        current_position = indexes[index]['position']
        delta = indexes[index]['data']
        to_insert = positions.pop(current_position)
        new_position = (current_position+delta) % (total_length - 1)
        if new_position == 0:
            new_position = total_length - 1
        delta_to_add = -1
        if current_position > new_position:
            delta_to_add = 1
        range_to_reduce = range(min(current_position, new_position), max(current_position, new_position))
        for index_to_reduce in range_to_reduce:
            real_index = positions[index_to_reduce]['mapping']
            x_current = indexes[real_index]['position']
            new_x = x_current + delta_to_add
            indexes[real_index]['position'] = new_x
        positions.insert(new_position, to_insert)
        indexes[index]['position'] = new_position

    # position of the 0
    position = None
    for index in range(len(indexes)):
        v = indexes[index]
        if v['data'] == 0:
            position = v['position']

    print(f'0 is at {position}')
    result = 0
    for to_check in [1000, 2000, 3000]:
        position_to_check = (position + to_check) % (total_length)
        print(f'For {to_check} position is {position_to_check}={positions[position_to_check]}')
        result += positions[position_to_check]['data']
    return result



def solve_part2(data):
    data = list(map(lambda x: x * 811589153, data))
    indexes = []
    positions = []
    for index in range(len(data)):
        indexes.append({'data': data[index], 'position': index})
        positions.append({'data': data[index], 'mapping': index})

    def print_positions():
        for index in range(len(positions)):
            position = positions[index]['data']
            if index == len(positions) - 1:
                print(position)
            else:
                print(position, end=', ')

    def print_indexes():
        test = set()
        for index in range(len(positions)):
            print(indexes[index])
            test.add(indexes[index]['position'])
            data = indexes[index]['data']
            position = indexes[index]['position']
            assert positions[position]['data'] == data
        print(f'we have {len(test)}')
        if len(test) < len(positions):
            print('BYUGGGGGGGGGGGGGG')
            input()

    print('=====Init=====')
    print_positions()

    total_length = len(positions)

    # Iteration 1
    for i in range(10):
        for index in range(len(data)):
            current_position = indexes[index]['position']
            delta = indexes[index]['data']
            to_insert = positions.pop(current_position)
            new_position = (current_position+delta) % (total_length - 1)
            if new_position == 0:
                new_position = total_length - 1
            delta_to_add = -1
            if current_position > new_position:
                delta_to_add = 1
            range_to_reduce = range(min(current_position, new_position), max(current_position, new_position))
            for index_to_reduce in range_to_reduce:
                real_index = positions[index_to_reduce]['mapping']
                x_current = indexes[real_index]['position']
                new_x = x_current + delta_to_add
                indexes[real_index]['position'] = new_x
            positions.insert(new_position, to_insert)
            indexes[index]['position'] = new_position

    # position of the 0
    position = None
    for index in range(len(indexes)):
        v = indexes[index]
        if v['data'] == 0:
            position = v['position']

    print(f'0 is at {position}')
    result = 0
    for to_check in [1000, 2000, 3000]:
        position_to_check = (position + to_check) % (total_length)
        print(f'For {to_check} position is {position_to_check}={positions[position_to_check]}')
        result += positions[position_to_check]['data']
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 3


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result != 8155


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 1623178306


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
