#!/usr/bin/env python
import re

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = [
        'light red bags contain 1 bright white bag, 2 muted yellow bags.',
        'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
        'bright white bags contain 1 shiny gold bag.',
        'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
        'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
        'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
        'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
        'faded blue bags contain no other bags.',
        'dotted black bags contain no other bags.',
    ]

    processed_data = process_data(data)

    result = find_bag_contenants('shiny gold', processed_data)   
    print(f'test result is {result}')
    assert result == 4


def test_part2():
    data = [
        'shiny gold bags contain 2 dark red bags.',
        'dark red bags contain 2 dark orange bags.',
        'dark orange bags contain 2 dark yellow bags.',
        'dark yellow bags contain 2 dark green bags.',
        'dark green bags contain 2 dark blue bags.',
        'dark blue bags contain 2 dark violet bags.',
        'dark violet bags contain no other bags.',
	]
    processed_data = process_data(data)
    result = find_bag_count('shiny gold', processed_data)
    print(f'test2 result is {result}')
    assert result == 126
	


def process_data(data):
    regex = re.compile(r'^(.*) bags contain (.*)$')
    subregex = re.compile(r'^\s?(\d+) (.*) bags?.?$')

    processed_data = {}
    for line in data:
        m = regex.search(line)
        if not m:
            print(f'line {line} doest not match')
            exit(0)

        source, remaining = m.groups()
        if source in processed_data:
            print(f'twice the same color {source} ?')
            exit(1)

        processed_data[source] = {'children': {}, 'parents': {}}

    for line in data:
        m = regex.search(line)
        if not m:
            print(f'line {line} doest not match')
            exit(0)

        source, remaining = m.groups()
        if source not in processed_data:
            print(f'weird the same color {source} ?')
            exit(1)

        if remaining.startswith('no other bags'):
            continue

        for rule in remaining.split(','):
            m = subregex.search(rule)
            if not m:
                print(f'rule "{rule}" doest not match sub line "{line}"')
                exit(1)
            number, color = m.groups()
            processed_data[source]['children'][color] = {'count': int(number), 'node': processed_data[color]}
            processed_data[color]['parents'][source] = processed_data[source]
    return processed_data


def find_bag_contenants(search, processed_data):
    total_sum = 0
    find_colors = {}

    already_checked = []
    total_sum = find_color_in_parents(processed_data[search]['parents'], already_checked)

    return total_sum

def find_bag_count(search, processed_data):
    return count_bag(processed_data[search]['children'])

def count_bag(data, level=0):
    print(f'level {level}')
    total = 0
    for color, color_data in data.items():
        next_node = color_data['node']
        count = color_data['count']
        if 'children' in next_node:
            level += 1
            total += count + (count * count_bag(next_node['children'], level))
        else:
            total += count
    return total


def find_color_in_parents(data, already_checked):
    found = 0
    for color, color_data in data.items():
        if color in already_checked:
            continue
        already_checked.append(color)
        found += 1
        found += find_color_in_parents(color_data['parents'], already_checked)
    return found



def part1():
    data = load_data()
    processed_data = process_data(data)
    result = find_bag_contenants('shiny gold', processed_data)   
    print(f'result is {result}')

def part2():
    data = load_data()
    processed_data = process_data(data)
    result = find_bag_count('shiny gold', processed_data)   
    print(f'result part2 is {result}')



test_part1()
part1()
test_part2()
part2()
