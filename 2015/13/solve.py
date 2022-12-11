#!/usr/bin/env python
from itertools import permutations

test_data = [
    'Alice would gain 54 happiness units by sitting next to Bob.',
    'Alice would lose 79 happiness units by sitting next to Carol.',
    'Alice would lose 2 happiness units by sitting next to David.',
    'Bob would gain 83 happiness units by sitting next to Alice.',
    'Bob would lose 7 happiness units by sitting next to Carol.',
    'Bob would lose 63 happiness units by sitting next to David.',
    'Carol would lose 62 happiness units by sitting next to Alice.',
    'Carol would gain 60 happiness units by sitting next to Bob.',
    'Carol would gain 55 happiness units by sitting next to David.',
    'David would gain 46 happiness units by sitting next to Alice.',
    'David would lose 7 happiness units by sitting next to Bob.',
    'David would gain 41 happiness units by sitting next to Carol.',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Guest:
    def __init__(self, name, guests):
        self.name = name
        self.guests = guests
        self.rules = {}

    def add_role(self, operation, points, neighbor):
        self.rules[neighbor] = {'operation': operation, 'points': points}

    def happiness_with(self, neighbor):
        if neighbor not in self.rules:
            return 0
        rule = self.rules[neighbor]
        operation = rule['operation']
        points = rule['points']
        if operation == 'gain':
            return points
        else:
            return - points


def solve_part1(data):
    guests = {}
    for line in data:
        splitted = line.split(' ')
        me = splitted[0].lower()
        if me not in guests:
            new_guest = Guest(me, guests)
            guests[me] = new_guest

    for line in data:
        splitted = line.split(' ')
        me = splitted[0].lower()
        guest = guests[me]

        gain_lose = splitted[2]
        points = int(splitted[3])
        neighbor = splitted[10][:-1].lower()
        guest.add_role(gain_lose, points, neighbor)

    keys = guests.keys()
    max_happiness = 0
    for test in permutations(keys, len(keys)):
        happiness = 0
        for i in range(len(keys)):
            guest_name = test[i]
            guest = guests[guest_name]
            next_guest_index = i + 1
            if next_guest_index == len(keys):
                next_guest_index = 0
            next_guest_name = test[next_guest_index]
            next_guest = guests[next_guest_name]

            # Compute the score from me to next guest
            happiness += guest.happiness_with(next_guest_name)
            happiness += next_guest.happiness_with(guest_name)

        if happiness > max_happiness:
            max_happiness = happiness
    return max_happiness


def solve_part2(data):
    guests = {}
    for line in data:
        splitted = line.split(' ')
        me = splitted[0].lower()
        if me not in guests:
            new_guest = Guest(me, guests)
            guests[me] = new_guest
    guests['me'] = Guest('me', guests)

    for line in data:
        splitted = line.split(' ')
        me = splitted[0].lower()
        guest = guests[me]

        gain_lose = splitted[2]
        points = int(splitted[3])
        neighbor = splitted[10][:-1].lower()
        guest.add_role(gain_lose, points, neighbor)

    keys = guests.keys()
    max_happiness = 0
    iteration = 0
    for test in permutations(keys, len(keys)):
        iteration += 1
        if iteration % 100 == 0:
            print(f'iteration {iteration}')
        happiness = 0
        for i in range(len(keys)):
            guest_name = test[i]
            guest = guests[guest_name]
            next_guest_index = i + 1
            if next_guest_index == len(keys):
                next_guest_index = 0
            next_guest_name = test[next_guest_index]
            next_guest = guests[next_guest_name]

            # Compute the score from me to next guest
            happiness += guest.happiness_with(next_guest_name)
            happiness += next_guest.happiness_with(guest_name)

        if happiness > max_happiness:
            max_happiness = happiness
    return max_happiness


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 330


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
part2()
