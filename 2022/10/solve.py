#!/usr/bin/env python

test_data = [
    'addx 15',
    'addx -11',
    'addx 6',
    'addx -3',
    'addx 5',
    'addx -1',
    'addx -8',
    'addx 13',
    'addx 4',
    'noop',
    'addx -1',
    'addx 5',
    'addx -1',
    'addx 5',
    'addx -1',
    'addx 5',
    'addx -1',
    'addx 5',
    'addx -1',
    'addx -35',
    'addx 1',
    'addx 24',
    'addx -19',
    'addx 1',
    'addx 16',
    'addx -11',
    'noop',
    'noop',
    'addx 21',
    'addx -15',
    'noop',
    'noop',
    'addx -3',
    'addx 9',
    'addx 1',
    'addx -3',
    'addx 8',
    'addx 1',
    'addx 5',
    'noop',
    'noop',
    'noop',
    'noop',
    'noop',
    'addx -36',
    'noop',
    'addx 1',
    'addx 7',
    'noop',
    'noop',
    'noop',
    'addx 2',
    'addx 6',
    'noop',
    'noop',
    'noop',
    'noop',
    'noop',
    'addx 1',
    'noop',
    'noop',
    'addx 7',
    'addx 1',
    'noop',
    'addx -13',
    'addx 13',
    'addx 7',
    'noop',
    'addx 1',
    'addx -33',
    'noop',
    'noop',
    'noop',
    'addx 2',
    'noop',
    'noop',
    'noop',
    'addx 8',
    'noop',
    'addx -1',
    'addx 2',
    'addx 1',
    'noop',
    'addx 17',
    'addx -9',
    'addx 1',
    'addx 1',
    'addx -3',
    'addx 11',
    'noop',
    'noop',
    'addx 1',
    'noop',
    'addx 1',
    'noop',
    'noop',
    'addx -13',
    'addx -19',
    'addx 1',
    'addx 3',
    'addx 26',
    'addx -30',
    'addx 12',
    'addx -1',
    'addx 3',
    'addx 1',
    'noop',
    'noop',
    'noop',
    'addx -9',
    'addx 18',
    'addx 1',
    'addx 2',
    'noop',
    'noop',
    'addx 9',
    'noop',
    'noop',
    'noop',
    'addx -1',
    'addx 2',
    'addx -37',
    'addx 1',
    'addx 3',
    'noop',
    'addx 15',
    'addx -21',
    'addx 22',
    'addx -6',
    'addx 1',
    'noop',
    'addx 2',
    'addx 1',
    'noop',
    'addx -10',
    'noop',
    'noop',
    'addx 20',
    'addx 1',
    'addx 2',
    'addx 2',
    'addx -6',
    'addx -11',
    'noop',
    'noop',
    'noop',
]


def solve(data):

    strengths = {}
    counter_index = 0
    x = 1
    for line in data:
        if line == 'noop':
            counter_index += 1
            strengths[counter_index] = x
            print(f'cycle={counter_index} x={x}')
            continue

        counter_index += 1
        print(f'cycle={counter_index} x={x}')
        strengths[counter_index] = x

        to_add = int(line.split(' ')[1])
        counter_index += 1
        print(f'cycle={counter_index} x={x}')
        strengths[counter_index] = x
        x += to_add

    total = 0
    for cycle, strength in strengths.items():
        to_add = False
        if cycle == 20:
            to_add = True
        elif (cycle - 20) % 40 == 0:
            to_add = True

        if to_add:
            print(f'cycle={cycle} strengh={strength} adding={cycle*strength}')
            total += cycle * strength
    return total


def solve_part_2(data):

    lines = []
    counter_index = 0
    sprite_position = 1

    def update_display(display_data, counter_index, sprite_position):
        test_index = counter_index % 40
        if test_index in range(sprite_position, sprite_position+3):
            display_data.append('#')
        else:
            display_data.append('.')
        print(f'sprite_position={sprite_position} cycle={counter_index}')
        if len(display_data) == 40:
            lines.append(''.join(display_data))
            display_data.clear()

    display_data = []
    for line in data:
        if line == 'noop':
            counter_index += 1
            update_display(display_data, counter_index, sprite_position)
        else:
            counter_index += 1
            update_display(display_data, counter_index, sprite_position)

            to_add = int(line.split(' ')[1])
            counter_index += 1
            update_display(display_data, counter_index, sprite_position)
            sprite_position += to_add
    for line in lines:
        print(line)


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = solve(data)
    print(f'test1 is {result}')
    assert result == 13140


def test_part2():
    data = test_data
    solve_part_2(data)


def part1():
    data = load_data()
    result = solve(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    solve_part_2(data)


test_part1()
part1()
test_part2()
part2()
