#!/usr/bin/env python
import operator

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
    pass


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
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
