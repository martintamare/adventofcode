#!/usr/bin/env python


def load_data():
    data = [1, 0, 18, 10, 19, 6]
    return data


def test_part1():
    data = [0, 3, 6]
    result = find_spoken_number(data)
    print(f'test1 is {result}')
    assert result == 436

    data = [1, 3, 2]
    result = find_spoken_number(data)
    print(f'test1 is {result}')
    assert result == 1

    data = [2, 1, 3]
    result = find_spoken_number(data)
    print(f'test1 is {result}')
    assert result == 10

    data = [1, 2, 3]
    result = find_spoken_number(data)
    print(f'test1 is {result}')
    assert result == 27

    data = [2,1,3]
    result = find_spoken_number(data)
    print(f'test1 is {result}')
    assert result == 10

    data = [2, 3, 1]
    result = find_spoken_number(data)
    print(f'test1 is {result}')
    assert result == 78

    data = [3, 2, 1]
    result = find_spoken_number(data)
    print(f'test1 is {result}')
    assert result == 438

    data = [3, 1, 2]
    result = find_spoken_number(data)
    print(f'test1 is {result}')
    assert result == 1836


def find_spoken_number(data, limit=2020):
    last_spoken_number = None
    spoken_numbers = []
    number_index_dict = {}

    for index in range(len(data)):
        number = data[index]
        spoken_numbers.append(number)
        last_spoken_number = number
        number_index_dict[number] = [index]

    while len(spoken_numbers) < limit:
        times_number_was_spoken = len(number_index_dict[last_spoken_number])
        if times_number_was_spoken == 1:
            last_spoken_number = 0
        else:
            last_indexes = number_index_dict[last_spoken_number]
            last_spoken_number = last_indexes[-1] - last_indexes[-2]

        current_index = len(spoken_numbers)
        if last_spoken_number in number_index_dict:
            if len(number_index_dict[last_spoken_number]) == 1:
                number_index_dict[last_spoken_number].append(current_index)
            else:
                last_index = number_index_dict[last_spoken_number][-1]
                number_index_dict[last_spoken_number] = [last_index, current_index]
        else:
            number_index_dict[last_spoken_number] = [current_index]

        spoken_numbers.append(last_spoken_number)

    return spoken_numbers[-1]




def test_part2():
    data = [0, 3, 6]
    result = find_spoken_number(data, 30000000)
    print(f'test2 is {result}')
    assert result == 175594

    data = [1, 3, 2]
    result = find_spoken_number(data, 30000000)
    print(f'test2 is {result}')
    assert result == 2578

    data = [2, 1, 3]
    result = find_spoken_number(data, 30000000)
    print(f'test2 is {result}')
    assert result == 3544142

    data = [1, 2, 3]
    result = find_spoken_number(data, 30000000)
    print(f'test2 is {result}')
    assert result == 261214

    data = [2, 3, 1]
    result = find_spoken_number(data, 30000000)
    print(f'test2 is {result}')
    assert result == 6895259

    data = [3, 2, 1]
    result = find_spoken_number(data, 30000000)
    print(f'test2 is {result}')
    assert result == 18

    data = [3, 1, 2]
    result = find_spoken_number(data, 30000000)
    print(f'test2 is {result}')
    assert result == 362


def part1():
    data = load_data()
    result = find_spoken_number(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = find_spoken_number(data, limit=30000000)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
part2()
