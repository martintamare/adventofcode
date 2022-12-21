#!/usr/bin/env python
import operator
from copy import deepcopy

test_data = [
    'root: pppw + sjmn',
    'dbpl: 5',
    'cczh: sllz + lgvd',
    'zczc: 2',
    'ptdq: humn - dvpt',
    'dvpt: 3',
    'lfqf: 4',
    'humn: 5',
    'ljgn: 2',
    'sjmn: drzm * dbpl',
    'sllz: 4',
    'pppw: cczh / lfqf',
    'lgvd: ljgn * ptdq',
    'drzm: hmdt - zczc',
    'hmdt: 32',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def build_monkeys(data):
    monkeys = {}
    operation_map = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
    }
    for line in data:
        splitted = line.split(' ')
        name = splitted[0][0:4]
        if len(splitted) == 2:
            value = int(splitted[1])
            monkeys[name] = {'value': value}
        else:
            needs = [splitted[1], splitted[3]]
            operation = operation_map[splitted[2]]
            monkeys[name] = {'needs': needs, 'operator': operation}
    return monkeys





def solve_part1(data):
    monkeys = build_monkeys(data)

    def can_yell(monkey):
        monkey_dict = monkeys[monkey]
        if 'value' in monkey_dict:
            return False
        ok = True
        if 'needs' in monkey_dict:
            for need_monkey in monkey_dict['needs']:
                if 'value' not in monkeys[need_monkey]:
                    ok = False
                    break
        return ok

    def compute_monkey_value(monkey):
        monkey_dict = monkeys[monkey]
        v1 = monkey_dict['needs'][0]
        v2 = monkey_dict['needs'][1]
        v1 = monkeys[v1]['value']
        v2 = monkeys[v2]['value']
        value = monkey_dict['operator'](v1, v2)
        return value

    while 'value' not in monkeys['root']:
        to_do_monkeys = filter(lambda x: can_yell(x), monkeys.keys())
        for monkey in to_do_monkeys:
            print(f'Computing {monkey}')
            value = compute_monkey_value(monkey)
            monkeys[monkey]['value'] = value
    return monkeys['root']['value']


def solve_part2(data):

    # Fix root
    monkeys = build_monkeys(data)
    monkeys['root']['operator'] = operator.sub

    def can_yell(monkey, test_monkeys):
        monkey_dict = test_monkeys[monkey]
        if 'value' in monkey_dict:
            return False
        ok = True
        if 'needs' in monkey_dict:
            for need_monkey in monkey_dict['needs']:
                if 'value' not in test_monkeys[need_monkey]:
                    ok = False
                    break
        return ok

    def compute_monkey_value(monkey, test_monkeys):
        monkey_dict = test_monkeys[monkey]
        v1 = monkey_dict['needs'][0]
        v2 = monkey_dict['needs'][1]
        v1 = test_monkeys[v1]['value']
        v2 = test_monkeys[v2]['value']
        value = monkey_dict['operator'](v1, v2)
        return value


    stop = False
    previous = None
    current = None
    me_value = 0
    best_value = None
    best_root = None
    min_value = 0
    max_value = 400000000000000
    median_value = int((max_value+min_value)/2)
    median_result = None
    while not stop:
        for me_value in [min_value, max_value, median_value]:
            print(f'testing {me_value}')
            test_monkeys = deepcopy(monkeys)
            test_monkeys['humn']['value'] = me_value
            while 'value' not in test_monkeys['root']:
                to_do_monkeys = filter(lambda x: can_yell(x, test_monkeys), test_monkeys.keys())
                for monkey in to_do_monkeys:
                    value = compute_monkey_value(monkey, test_monkeys)
                    test_monkeys[monkey]['value'] = value
            root_value = test_monkeys['root']['value']
            print(f'result is {root_value}')
            if me_value == min_value:
                min_value_result = root_value
            elif me_value == max_value:
                max_value_result = root_value
            else:
                median_result = root_value

            if root_value == 0:
                return me_value
                stop = True
                break

        new_min_result = None
        new_max_result = None
        for result in [min_value_result, max_value_result, median_result]:
            if result < 0:
                if new_min_result is None:
                    new_min_result = result
                elif result > new_min_result:
                    new_min_result = result
            else:
                if new_max_result is None:
                    new_max_result = result
                elif result < new_max_result:
                    new_max_result = result

        print(f'{min_value} {max_value} {median_value}')
        print(f'{min_value_result} {max_value_result} {median_result}')
        new_min = None
        if new_min_result == min_value_result:
            new_min = min_value
        elif new_min_result == max_value_result:
            new_min = max_value
        else:
            new_min = median_value

        new_max = None
        if new_max_result == max_value_result:
            new_max = max_value
        elif new_max_result == min_value_result:
            new_max = min_value
        else:
            new_max = median_value

        print(f'{new_min} {new_max}')
        if new_max == max_value and new_min == min_value:
            print('FUCK')
            input()

        min_value = min(new_min, new_max)
        max_value = max(new_max, new_min)
        median_value = int((max_value + min_value)/2)
        print(f'new_min={min_value} new_max={max_value} median={median_value}')


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 152


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 301


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
#test_part2()
part2()
