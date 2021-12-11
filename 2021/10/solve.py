#!/usr/bin/env python
from statistics import median

test_data = [
    '[({(<(())[]>[[{[]{<()<>>',
    '[(()[<>])]({[<{<<[]>>(',
    '{([(<{}[<>[]}>{[]{[(<()>',
    '(((({<>}<{<{<>}{[]{[]{}',
    '[[<[([]))<([[{}[[()]]]',
    '[{[{({}]{}}([{[{{{}}([]',
    '{<[[]]>}<{[{[{[]{()[[[]',
    '[<(<(<(<{}))><([]([]()',
    '<{([([[(<>()){}]>(<<{{',
    '<{([{{}}[<[[[<>{}]]]>[]]',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def parse_lines(data):
    mapper = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }

    corrumpted_lines = []
    valid_lines = []
    for line in data:
        recap = []
        to_find = None
        is_valid = True
        for char in line:
            if char in mapper.keys():
                recap.append(char)
                to_find = mapper[char]
            elif char == to_find:
                recap.pop()
                if len(recap):
                    to_find = mapper[recap[-1]]
            else:
                corrumption = {
                        'to_find': to_find,
                        'char': char,
                        'line': line
                }
                corrumpted_lines.append(corrumption)
                is_valid = False
                break
        if is_valid:
            ok_line = {
                'remaining': recap,
                'line': line,
            }
            valid_lines.append(ok_line)

    return valid_lines, corrumpted_lines


def solve_part_1(data):
    valid_lines, corrumpted_lines = parse_lines(data)

    mapper = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    total = 0
    for line in corrumpted_lines:
        total += mapper[line['char']]
    return total


def solve_part_2(data):
    valid_lines, corrumpted_lines = parse_lines(data)

    scores = []

    mapper = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4,
    }

    for line in valid_lines:
        score = 0
        temp = line['remaining']
        temp.reverse()
        for char in temp:
            score = score * 5 + mapper[char]
        scores.append(score)

    return median(scores)


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 26397


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 288957


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')
    assert result == 341823


def part2():
    data = load_data()
    result = solve_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
