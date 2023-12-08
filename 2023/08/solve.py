#!/usr/bin/env python
import itertools

test_data = [
    'LLR',
    '',
    'AAA = (BBB, BBB)',
    'BBB = (AAA, ZZZ)',
    'ZZZ = (ZZZ, ZZZ)',
]

test_data_2 = [
    'LR',
    '',
    '11A = (11B, XXX)',
    '11B = (XXX, 11Z)',
    '11Z = (11B, XXX)',
    '22A = (22B, XXX)',
    '22B = (22C, 22C)',
    '22C = (22Z, 22Z)',
    '22Z = (22B, 22B)',
    'XXX = (XXX, XXX)',
]



def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

def load_edges(data):
    data = data.copy()

    instructions = data.pop(0)
    data.pop(0)

    edges = {}
    for line in data:
        edge_source = line.split('=')[0].strip()
        destination = line.split('=')[1].strip().replace('(', '').replace(')', '').split(', ')
        destination_left = destination[0].strip()
        destination_right = destination[1].strip()
        if destination_left not in edges:
            edges[destination_left] = {'L': None, 'R': None}
        if destination_right not in edges:
            edges[destination_right] = {'L': None, 'R': None}

        if edge_source in edges:
            edges[edge_source]['L'] = destination_left
            edges[edge_source]['R'] = destination_right
        else:
            edges[edge_source] = {'L': destination_left, 'R': destination_right}
    return instructions, edges


def solve_part1(data):
    instructions, edges = load_edges(data)


    step = 0
    current = 'AAA'
    for instruction in itertools.cycle(instructions):
        next_edge = edges[current][instruction]
        current = next_edge
        step += 1
        if next_edge == 'ZZZ':
            break
    return step


def gcd(a, b):
    if a == 0:
        return b
    # recursively calculating the gcd.
    return gcd(b % a, a)


def lcm(a, b):
    return (a / gcd(a, b)) * b

def solve_part2(data):
    instructions, edges = load_edges(data)

    source_edges = list(filter(lambda x: x.endswith('A'), edges.keys()))
    print(f"computing each score for {source_edges}")

    source_edge_score = {}
    for current in source_edges:
        start_edge = current
        current_edge = current
        step = 0
        for instruction in itertools.cycle(instructions):
            next_edge = edges[current_edge][instruction]
            current_edge = next_edge
            step += 1
            if next_edge.endswith('Z'):
                break
        source_edge_score[start_edge] = step

    result = None
    for edge, score in source_edge_score.items():
        if result is None:
            result = score
        else:
            result = lcm(score, result)
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 6


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 16697


def test_part2():
    data = test_data_2
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 6


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result < 68432364574438008329351
    assert result < 19366359174565956357206333
    assert result > 100182


test_part1()
#part1()
test_part2()
part2()
