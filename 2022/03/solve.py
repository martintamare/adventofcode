#!/usr/bin/env python
test_data = [
    'vJrwpWtwJgWrhcsFMMfFFhFp',
    'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    'PmmdzqPrVvPwwTWBwg',
    'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    'ttgJtRGJQctTZtZT',
    'CrZsJsPPZsGzwwsLwLmpwMDw',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Rucksack:
    def __init__(self, data):
        print(data)
        mid = int(len(data) / 2)
        assert mid * 2 == len(data)
        self.first_bag = data[0:mid]
        self.second_bag = data[mid:]

    @property
    def unique_item(self):
        first_bag_set = set(self.first_bag)
        second_bag_set = set(self.second_bag)
        intersection = list(first_bag_set.intersection(second_bag_set))
        assert len(intersection) == 1
        return intersection[0]

    @property
    def unique_item_score(self):
        unique_item = self.unique_item
        if unique_item.lower() == unique_item:
            return ord(unique_item) - 96
        else:
            return ord(unique_item) - 38


def solve_part_1(data):
    score = 0
    for line in data:
        rucksack = Rucksack(line)
        print(f'{line} has unique {rucksack.unique_item}')
        score += rucksack.unique_item_score
    return score


def solve_part_2(data):
    score = 0
    for i in range(int(len(data) / 3)):
        test_1 = set(data[0+i*3])
        test_2 = set(data[1+i*3])
        test_3 = set(data[2+i*3])
        unique = list(test_1.intersection(test_2).intersection(test_3))
        assert len(unique) == 1
        unique = unique[0]
        if unique.lower() == unique:
            score += (ord(unique) - 96)
        else:
            score += (ord(unique) - 38)
    return score


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 157


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 70


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
