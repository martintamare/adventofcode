#!/usr/bin/env python

test_data = [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Card:
    def __init__(self, id, winners_numbers, current_numbers):
        self.id = id
        self.winners_numbers = winners_numbers
        self.current_numbers = current_numbers
        self.copies = 1

    @property
    def matching_numbers(self):
        return len(set(self.current_numbers).intersection(set(self.winners_numbers)))

    @property
    def score(self):
        correct = 0
        for number in self.current_numbers:
            if number in self.winners_numbers:
                if correct == 0:
                    correct += 1
                else:
                    correct *= 2
        return correct


def solve_part1(data):
    total = 0
    cards = {}
    for line in data:
        card_id = int(line.split(':')[0].strip()[5:].strip())
        card_data = line.split(':')[1].strip()
        winners_numbers = list(map(lambda x: int(x.strip()), filter(lambda x: x, card_data.split('|')[0].split(' '))))
        current_numbers = list(map(lambda x: int(x.strip()), filter(lambda x: x, card_data.split('|')[1].split(' '))))
        card = Card(card_id, winners_numbers, current_numbers)
        cards[card_id] = card

    for card_id, card in cards.items():
        total += card.score
    return total


def solve_part2(data):
    cards = {}
    for line in data:
        card_id = int(line.split(':')[0].strip()[5:].strip())
        card_data = line.split(':')[1].strip()
        winners_numbers = list(map(lambda x: int(x.strip()), filter(lambda x: x, card_data.split('|')[0].split(' '))))
        current_numbers = list(map(lambda x: int(x.strip()), filter(lambda x: x, card_data.split('|')[1].split(' '))))
        card = Card(card_id, winners_numbers, current_numbers)
        cards[card_id] = card

    for card_id in sorted(cards.keys()):
        card = cards[card_id]
        matching_numbers = card.matching_numbers
        for test in range(card.copies):
            for to_add_index in range(card_id+1, card_id+matching_numbers+1):
                cards[to_add_index].copies += 1

        
    total = 0
    for card_id, card in cards.items():
        total += card.copies
    return total

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 13


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 25183


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 30


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
