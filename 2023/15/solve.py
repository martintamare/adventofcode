#!/usr/bin/env python

test_data = [
    'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def hash_algo(iteration, current_value):
    if len(iteration) == 0:
        return current_value
    else:
        ascii_code = ord(iteration[0])
        current_value += ascii_code
        current_value *= 17
        current_value = current_value % 256
        return hash_algo(iteration[1:], current_value)


def solve_part1(data):
    iterations = data[0].split(',')
    total = 0
    for iteration in iterations:
        total += hash_algo(iteration, 0)
    return total

def print_boxes(boxes):
    for index, box in enumerate(boxes):
        if box is None:
            continue
        else:
            print(f"Box {index} = {box}")


def solve_part2(data):
    boxes = []
    for index in range(256):
        boxes.append(None)

    iterations = data[0].split(',')
    total = 0
    for iteration in iterations:
        if '=' in iteration:
            label, data = iteration.split('=')
            hash_label = hash_algo(label, 0)
            print(f"{iteration} box_to_check={hash_label}")
            data_to_insert = f'{label} {data}'
            if boxes[hash_label] is None:
                boxes[hash_label] = [data_to_insert]
            else:
                current_boxes = boxes[hash_label]
                boxes_matching = list(filter(lambda x: x.startswith(label), current_boxes))
                if boxes_matching:
                    box_to_remove = boxes_matching[0]
                    index = boxes[hash_label].index(box_to_remove)
                    boxes[hash_label][index] = data_to_insert
                else:
                    boxes[hash_label].append(data_to_insert)
        elif '-' in iteration:
            label, data = iteration.split('-')
            hash_label = hash_algo(label, 0)
            print(f"{iteration} box_to_check={hash_label}")
            if boxes[hash_label] is None:
                continue
            else:
                current_boxes = boxes[hash_label]
                boxes_matching = list(filter(lambda x: x.startswith(label), current_boxes))
                if boxes_matching:
                    box_to_remove = boxes_matching[0]
                    boxes[hash_label].remove(box_to_remove)
                    if not len(boxes[hash_label]):
                        boxes[hash_label] = None
                else:
                    continue
        else:
            print('WTH')
            exit(0)

    for index, box in enumerate(boxes):
        box_index = index + 1
        if box is None:
            continue
        for slot, value in enumerate(box):
            real_slot = slot + 1
            focal = int(value.split(' ')[1])
            print(f"{value} slot={real_slot} {focal=}")
            total += box_index * real_slot * focal
    return total


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 1320


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 145


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
