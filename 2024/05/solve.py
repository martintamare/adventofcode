#!/usr/bin/env python

test_data = [
    '47|53',
    '97|13',
    '97|61',
    '97|47',
    '75|29',
    '61|13',
    '75|53',
    '29|13',
    '97|29',
    '53|29',
    '61|53',
    '97|53',
    '61|29',
    '47|13',
    '75|47',
    '97|75',
    '47|61',
    '75|61',
    '47|29',
    '75|13',
    '53|13',
    '',
    '75,47,61,53,29',
    '97,61,53,29,13',
    '75,29,13',
    '75,97,47,61,53',
    '61,13,29',
    '97,13,75,29,47',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Rule:
    def __init__(self, number):
        self.number = number
        self.childrens = []
        self.parents = []

    def add_child(self, rule):
        if rule not in self.childrens:
            self.childrens.append(rule)

    def add_parent(self, rule):
        if rule not in self.parents:
            self.parents.append(rule)

    def __repr__(self):
        return f"{self.number}"

class Update:
    def __init__(self, numbers, rules):
        self.numbers = numbers
        self.rules = rules

    def __repr__(self):
        return f"{self.numbers}"

    def fix_numbers(self):
        print(f"Fixing {self}")
        new_numbers = []
        already_printed = []
        for number in self.numbers:
            print(f"Checking {number}")
            if number in already_printed:
                continue
            rule = self.rules[number]

            for parent in rule.parents:
                if parent.number not in self.numbers:
                    continue
                elif parent.number not in already_printed:
                    # Need to insert it at the right places
                    print(f"False because of {parent} not printed")
                    ok_numbers = None
                    if not already_printed:
                        ok_numbers=[parent.number]
                        already_printed.append(parent.number)
                        continue
                    else:
                        for index in range(len(already_printed) + 1):
                            test_numbers = already_printed.copy()
                            test_numbers.insert(index, parent.number)
                            print(f"testing {test_numbers}")
                            test = Update(test_numbers, self.rules)
                            if test.correctly_ordered:
                                ok_numbers = test_numbers
                                break
                    already_printed = ok_numbers
            already_printed.append(number)
        print(f"After fix {already_printed}")
        return Update(already_printed, self.rules)

    @property
    def correctly_ordered(self):
        print(f"Checking {self}")
        already_printed = []
        for number in self.numbers:
            rule = self.rules[number]

            for parent in rule.parents:
                if parent.number not in self.numbers:
                    continue
                elif parent.number not in already_printed:
                    print(f"False because of {parent} not printed")
                    return False
            already_printed.append(number)

        return True

    @property
    def middle_number(self):
        print(len(self.numbers))
        middle = int((len(self.numbers) - 1 )/ 2)
        return self.numbers[middle]


def solve_part1(data):

    rules = {}
    updates = []
    mode = "rules"
    for line in data:
        if line == "":
            mode = "update"
            continue

        if mode == "rules":
            splitted = line.split('|')
            r1 = int(splitted[0])
            r2 = int(splitted[1])

            if r1 not in rules:
                rules[r1] = Rule(r1)
            r1obj = rules[r1]

            if r2 not in rules:
                rules[r2] = Rule(r2)
            r2obj = rules[r2]
            r1obj.add_child(r2obj)
            r2obj.add_parent(r1obj)

        elif mode == "update":
            updates.append(Update(list(map(int, line.split(','))), rules))

        
    result = 0
    for update in updates:
        if update.correctly_ordered:
            result += update.middle_number
    return result
    print(rules)
    print(updates)
    pass


def solve_part2(data):
    rules = {}
    updates = []
    mode = "rules"
    for line in data:
        if line == "":
            mode = "update"
            continue

        if mode == "rules":
            splitted = line.split('|')
            r1 = int(splitted[0])
            r2 = int(splitted[1])

            if r1 not in rules:
                rules[r1] = Rule(r1)
            r1obj = rules[r1]

            if r2 not in rules:
                rules[r2] = Rule(r2)
            r2obj = rules[r2]
            r1obj.add_child(r2obj)
            r2obj.add_parent(r1obj)

        elif mode == "update":
            updates.append(Update(list(map(int, line.split(','))), rules))

        
    result = 0
    for update in updates:
        if not update.correctly_ordered:
            new_update = update.fix_numbers()
            assert new_update.correctly_ordered
            result += new_update.middle_number
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 143


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 5948


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 123


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
