#!/usr/bin/env python
import re
import itertools

test_data = [
    'class: 1-3 or 5-7',
    'row: 6-11 or 33-44',
    'seat: 13-40 or 45-50',
    '',
    'your ticket:',
    '7,1,14',
    '',
    'nearby tickets:',
    '7,3,47',
    '40,4,50',
    '55,2,20',
    '38,6,12',
]

test_data_part_2 = [
    'class: 0-1 or 4-19',
    'row: 0-5 or 8-19',
    'seat: 0-13 or 16-19',
    '',
    'your ticket:',
    '11,12,13',
    '',
    'nearby tickets:',
    '3,9,18',
    '15,1,5',
    '5,14,9',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = ticket_error_rate(data)
    print(f'test1 is {result}')
    assert result == 71


def test_part2():
    to_test = {
        'class': 12,
        'row': 11,
        'seat': 13,
    }
    data = test_data_part_2
    rules, my_ticket, other_tickets = process_data(data)
    valid_tickets = []
    for ticket in other_tickets:
        is_valid, index = ticket_validation(ticket, rules)
        if is_valid:
            valid_tickets.append(ticket)
    valid_tickets.append(my_ticket)
    valid_permutation = get_valid_permutation(rules, valid_tickets)
    assert valid_permutation is not None
    print(f'valid_permutation is {valid_permutation}')

    for field, value in to_test.items():
        rule_index = get_rules_index_for_name(field, rules)
        print(f'rule_index is {rule_index}')
        ticket_index = int(valid_permutation[rule_index])
        print(f'ticket_index is {ticket_index} {my_ticket}')
        result = my_ticket[ticket_index]
        print(f'test2 for fiesld {field} = {result}')
        assert result == value


def part1():
    data = load_data()
    result = ticket_error_rate(data)
    print(f'part1 is {result}')
    assert result == 32835


def part2():
    data = load_data()
    rules, my_ticket, other_tickets = process_data(data)
    valid_tickets = []
    for ticket in other_tickets:
        is_valid, index = ticket_validation(ticket, rules)
        if is_valid:
            valid_tickets.append(ticket)
    valid_tickets.append(my_ticket)

    valid_permutation = get_valid_permutation(rules, valid_tickets)
    print(f'valid_permutation is {valid_permutation}')

    total = 1
    for r_index in range(len(rules)):
        rule = rules[r_index]
        if rule['name'].startswith('departure'):
            ticket_index = valid_permutation.index(r_index)
            ticket_value = my_ticket[ticket_index]
            print(f'result for {rule["name"]} is {ticket_value}')
            total *= ticket_value
    print(f'part2 is {total}')


def ticket_error_rate(data):
    rules, my_ticket, other_tickets = process_data(data)
    missing_index = []
    for ticket in other_tickets:
        is_valid, index = ticket_validation(ticket, rules)
        if not is_valid:
            missing_index.append(index)
    return sum(missing_index)


def process_data(data):
    sorted_data = []
    current_data = []
    for line in data:
        if not line:
            sorted_data.append(current_data)
            current_data = []
        else:
            current_data.append(line)
    sorted_data.append(current_data)
    rules = sorted_data[0]
    my_ticket = list(map(lambda x: [int(value) for value in x.split(',')], sorted_data[1][1:]))[0]
    other_tickets = list(map(lambda x: [int(value) for value in x.split(',')], sorted_data[2][1:]))

    processed_rules = []
    regex = re.compile(r'^(.*): (\d+)-(\d+) or (\d+)-(\d+)$')
    for rule in rules:
        match = regex.match(rule)
        if not match:
            print(f'weird rule {rule}')
            exit(1)
        rule_name, index_1, index_2, index_3, index_4 = match.groups()
        rule_data = {
            'name': rule_name,
            'indexes': [(int(index_1), int(index_2)), (int(index_3), int(index_4))],
        }
        processed_rules.append(rule_data)
    return processed_rules, my_ticket, other_tickets


def ticket_validation(ticket, rules_data):
    for ticket_index in ticket:
        index_found = False
        for rules in rules_data:
            for rule in rules['indexes']:
                start, end = rule
                if ticket_index in list(range(start, end + 1)):
                    index_found = True
                    break
        if not index_found:
            return False, ticket_index
    return True, None


def get_rules_index_for_name(field, rules):
    for index in range(len(rules)):
        rule = rules[index]
        if rule['name'] == field:
            return index
    raise('fnazjkfnazkfjazn')


def get_valid_permutation(rules, valid_tickets):
    my_ticket = valid_tickets[-1]

    # Rules : 0 to len(my_ticket)
    # Test each rules against all tickets
    # Make array of array
    # index -> list of index rules that are OK with all tickets
    permutations_array = []

    for p_index in range(len(my_ticket)):
        rules_that_match = []
        for r_index in range(len(my_ticket)):
            rule = rules[r_index]
            is_valid = is_rule_valid_at_index(rule, p_index, valid_tickets)
            if is_valid:
                rules_that_match.append(r_index)
        permutations_array.append(rules_that_match)
        rules_that_match = []

    # Do we have an index with only one choice ?
    permutations = {}
    while len(permutations.keys()) != len(my_ticket):
        number_of_elemets_per_index = list(map(lambda x: len(x), permutations_array))
        one_choices = list(map(lambda x: x == 1, number_of_elemets_per_index))
        one_choices_count = len(list(filter(lambda x: x == 1, number_of_elemets_per_index)))
        if one_choices_count != 1:
            print('WTF ?')
            exit(1)

        ok_index = one_choices.index(True)
        rule_index = permutations_array[ok_index][0]
        permutations[ok_index] = rule_index
        print(f'setting place at index {ok_index} for rule {rule_index}')

        # No clean permutations_array and remove rule_index
        for choices in permutations_array:
            if rule_index in choices:
                choices.remove(rule_index)

    final_permutation = []
    for index in range(len(my_ticket)):
        final_permutation.append(permutations[index])
    return final_permutation


def is_rule_valid_at_index(test_rule, index, valid_tickets):
    is_valid = True
    for ticket in valid_tickets:
        is_rule_valid = False
        for rule in test_rule['indexes']:
            start, end = rule
            if ticket[index] in list(range(start, end + 1)):
                is_rule_valid = True
                break
        if not is_rule_valid:
            is_valid = False
            break
    return is_valid


def get_valid_permutation_bruteforce(rules, valid_tickets):
    my_ticket = valid_tickets[-1]

    # Now compute combinations
    valid_permutation = None
    tested = {}
    permutations = [str(x) for x in range(1, len(my_ticket) + 1)]
    for permutation in itertools.permutations(permutations, len(my_ticket)):
        print(f'testing permutation {permutation}')
        is_valid = True
        for index in range(len(permutation)):
            if permutation[index] in tested:
                if index in tested[permutation[index]]:
                    if tested[permutation[index]][index]:
                        continue
                    else:
                        is_valid = False
                        break

            test_index = int(permutation[index]) - 1
            for ticket in valid_tickets:
                is_rule_valid = False
                for rule in rules[test_index]['indexes']:
                    start, end = rule
                    if ticket[index] in list(range(start, end + 1)):
                        is_rule_valid = True
                        break
                if not is_rule_valid:
                    is_valid = False
                    if permutation[index] in tested:
                        tested[permutation[index]][index] = False
                    else:
                        tested[permutation[index]] = {index: False}
                    break

            if not is_valid:
                break
            else:
                if permutation[index] in tested:
                    tested[permutation[index]][index] = True
                else:
                    tested[permutation[index]] = {index: True}

        if is_valid:
            print(f'bingo ! {permutation}')
            valid_permutation = permutation
            break
    return valid_permutation


test_part1()
part1()
test_part2()
part2()
