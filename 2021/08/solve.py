#!/usr/bin/env python

test_data = [
    'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
    'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
    'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
    'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
    'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
    'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
    'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
    'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
    'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
    'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
]


def solve_part_1(data):
    digits = []

    #                1  4  7  8
    unique_length = [2, 4, 3, 7]

    for line in data:
        all_digits = line.split('|')[1].strip().split(' ')
        digits += list(filter(lambda x: len(x) in unique_length, all_digits))

    return len(digits)


def solve_part_2(data):
    total = 0

    for line in data:
        all_inputs = line.split('|')[0].strip()
        matcher = solve_number(all_inputs)

        all_digits = line.split('|')[1].strip().split(' ')
        current_total = ''
        for digit in all_digits:
            for match_number, match_data in matcher.items():
                if match_data['set'] == set(digit):
                    current_total += f'{match_number}'
        current_total = int(current_total)
        total += current_total
    return total



def solve_number(data):
    inputs = data.split(' ')

    results = {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        7: {},
        8: {},
        9: {},
    }

    # Unique length first easy one
    unique_length = {
        2: 1,
        4: 4,
        3: 7, 
        7: 8,
    }
    remaining_inputs = []
    for i in inputs:
        if len(i) in unique_length:
            index = unique_length[len(i)]
            results[index]['raw'] = i
            results[index]['set'] = set(i)
        else:
            remaining_inputs.append(i)

    # Next one that can be computed directly
    # 9 is length 6 and contains 1 4 and 7
    # 6 is length 6 and match nothing
    # 0 is the other one with length 6
    # 3 is length 5 and contains 1 and 7
    # 2 and 5 length 5 and contains nothing => Will need a third treatment
    inputs = remaining_inputs
    remaining_inputs = []
    for i in inputs:
        if len(i) == 6:
            matches = []
            for index in [1,4,7]:
                if set(i) & results[index]['set'] == results[index]['set']:
                    matches.append(index)
            if len(matches) == 3:
                results[9]['raw'] = i
                results[9]['set'] = set(i)
            elif len(matches) == 0:
                results[6]['raw'] = i
                results[6]['set'] = set(i)
            else:
                results[0]['raw'] = i
                results[0]['set'] = set(i)
        elif len(i) == 5:
            matches = []
            for index in [1,7]:
                if set(i) & results[index]['set'] == results[index]['set']:
                    matches.append(index)
            if len(matches) == 2:
                results[3]['raw'] = i
                results[3]['set'] = set(i)
            else:
                remaining_inputs.append(i)

    # Final round : we should have 2 remaining_inputs
    # 5 match set of 9 and set of 6 combined
    # 2 the otherone
    inputs = remaining_inputs
    assert len(inputs) == 2
    remaining_inputs = []
    for i in inputs:
        if set(i) == results[6]['set'] & results[9]['set']:
            results[5]['raw'] = i
            results[5]['set'] = set(i)
        else:
            results[2]['raw'] = i
            results[2]['set'] = set(i)

    return results


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 26


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 61229


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
