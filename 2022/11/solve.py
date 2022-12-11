#!/usr/bin/env python
import operator

test_data = [
    'Monkey 0:',
    '  Starting items: 79, 98',
    '  Operation: new = old * 19',
    '  Test: divisible by 23',
    '    If true: throw to monkey 2',
    '    If false: throw to monkey 3',
    '',
    'Monkey 1:',
    '  Starting items: 54, 65, 75, 74',
    '  Operation: new = old + 6',
    '  Test: divisible by 19',
    '    If true: throw to monkey 2',
    '    If false: throw to monkey 0',
    '',
    'Monkey 2:',
    '  Starting items: 79, 60, 97',
    '  Operation: new = old * old',
    '  Test: divisible by 13',
    '    If true: throw to monkey 1',
    '    If false: throw to monkey 3',
    '',
    'Monkey 3:',
    '  Starting items: 74',
    '  Operation: new = old + 3',
    '  Test: divisible by 17',
    '    If true: throw to monkey 0',
    '    If false: throw to monkey 1',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Monkey:
    def __init__(self,
                 index,
                 items,
                 operation,
                 test_operation,
                 monkey_true,
                 monkey_false,
                 monkeys,
                 part=1):
        self.index = index
        self.items = items
        self.operation = operation
        self.test_operation = test_operation
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.monkeys = monkeys
        self.inspected_items = 0
        self.part = part
        # From grep 'Test' input.txt | cut -d' ' -f6 | sort -n
        self.root_ppdm = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19

    def ppdm(self, item):
        # Because of operation old * old
        # If we want new_item to be divisabled, we need to add current idem
        return self.root_ppdm * item

    def apply_operator(self, item):
        operation_map = {
            '*': operator.mul,
            '+': operator.add,
        }
        operation = operation_map[self.operation[1]]
        try:
            b = int(self.operation[2])
        except ValueError:
            b = item
        new_item = operation(item, b)
        if self.part == 1:
            new_item = int(new_item / 3)
        return new_item

    def do_round(self):
        for item in self.items:
            self.inspected_items += 1
            update_item = self.apply_operator(item)
            remaining = update_item % self.test_operation

            destination_monkey = self.monkeys[self.monkey_false]
            if remaining == 0:
                destination_monkey = self.monkeys[self.monkey_true]

            if self.part == 1:
                to_inject = update_item
            elif self.part == 2:
                to_inject = update_item % self.ppdm(item)
            destination_monkey.items.append(to_inject)

        self.items.clear()


def build_monkeys(data, part):
    monkeys = {}
    for monkey in range(int((len(data) + 1)/7)):
        items = map(lambda x: int(x.strip()), data[7*monkey+1].split(':')[1].split(','))  # noqa
        items = list(items)

        operation = data[7*monkey+2].strip().split('=')[1].strip().split(' ')
        test_operation = int(data[7*monkey+3].split(' ')[-1])
        true_operation = int(data[7*monkey+4].split(' ')[-1])
        false_operation = int(data[7*monkey+5].split(' ')[-1])
        m = Monkey(monkey,
                   items,
                   operation,
                   test_operation,
                   true_operation,
                   false_operation,
                   monkeys,
                   part)
        monkeys[monkey] = m
    return monkeys


def solve_part1(data):
    monkeys = build_monkeys(data, 1)
    for _ in range(20):
        for index in sorted(monkeys.keys()):
            monkey = monkeys[index]
            monkey.do_round()
        for index in sorted(monkeys.keys()):
            monkey = monkeys[index]
            print(f'monkey {index} items : {monkey.items}')
    inspected_items = map(lambda x: x.inspected_items, monkeys.values())
    inspected_items = sorted(inspected_items)
    return inspected_items[-1] * inspected_items[-2]


def solve_part2(data):
    monkeys = build_monkeys(data, 2)
    for iteration in range(1, 10001):
        if iteration % 100 == 0:
            print(f'iteration {iteration}')
        for index in sorted(monkeys.keys()):
            monkey = monkeys[index]
            monkey.do_round()
    inspected_items = list(map(lambda x: x.inspected_items, monkeys.values()))
    inspected_items = sorted(inspected_items)
    return inspected_items[-1] * inspected_items[-2]


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 10605


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 2713310158


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 61005


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
