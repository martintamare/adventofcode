#!/usr/bin/env python
import functools
from collections import Counter

test_data = [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data



@functools.total_ordering
class Hand:
    def __init__(self, cards, bid, deck, power_data, version=1):
        self.cards = cards
        self.bid = bid
        self.deck = deck
        self.power_data = power_data
        self.version = version

    @property
    def type(self):
        if self.version == 1:
            return self.type_with_cards(self.cards)
        elif self.version == 2:
            # be smart
            if 'J' not in self.cards:
                return self.type_with_cards(self.cards)
            else:
                card_counter = Counter(self.cards)
                j_kind = card_counter['J']
                current_power, current_type = self.type_with_cards(self.cards)
                if current_type == 'five':
                    return current_power, current_type
                elif current_type == 'four':
                    return 7, 'five'
                elif current_type == 'full':
                    if j_kind == 1:
                        print('fezfzefzefzefefezfzefze')
                        exit(0)
                    elif j_kind == 2:
                        return 7, 'five'
                    elif j_kind == 3:
                        return 7, 'five'
                    else:
                        print('fnzaufnzajkfazfaz')
                        exit(0)
                elif current_type == 'three':
                    if j_kind == 1:
                        return 6, 'four'
                    elif j_kind == 2:
                        return 7, 'five'
                    elif j_kind == 3:
                        return 6, 'four'
                    else:
                        print('fzafazfzafazfnefgez')
                        exit(0)
                elif current_type == 'two_pair':
                    if j_kind == 1:
                        return 5, 'full'
                    elif j_kind == 2:
                        return 6, 'four'
                    else:
                        print('ngezjkfgnzejkgnzekgze')
                        exit(0)
                elif current_type == 'pair':
                    print(f"{self.cards}")
                    if j_kind == 1:
                        return 4, 'three'
                    elif j_kind == 2:
                        return 4, 'three'
                    else:
                        print('gnezjgnezjgkzegzegze')
                        exit(0)
                elif current_type == 'high_card':
                    if j_kind == 1:
                        return 2, 'pair'
                    else:
                        return current_power, current_type

    def type_with_cards(self, cards):
        card_counter = Counter(cards)
        max_kind = max(card_counter.values())
        kind_counter = Counter(card_counter.values())
        if max_kind == 5:
            return 7, 'five'
        elif max_kind == 4:
            return 6, 'four'
        elif 2 in card_counter.values() and 3 in card_counter.values():
            return 5, 'full'
        elif 3 in card_counter.values():
            return 4, 'three'
        elif 2 in kind_counter.keys() and kind_counter[2] == 2:
            return 3, 'two_pair'
        elif 2 in card_counter.values():
            return 2, 'pair'
        else:
            return 1, 'high_card'
        

    def __eq__(self, other):
        self_power, _ = self.type
        other_power, _ = other.type
        if self_power != other_power:
            return False
        for index, card in enumerate(self.cards):
            self_power_card = self.power_data[card]
            other_power_card = self.power_data[other.cards[index]]
            if self_power_card != other_power_card:
                return False
        return True

        
    def __lt__(self, other):
        self_power, _ = self.type
        other_power, _ = other.type
        if self_power == other_power:
            for index, card in enumerate(self.cards):
                self_power_card = self.power_data[card]
                other_power_card = self.power_data[other.cards[index]]
                if self_power_card != other_power_card:
                    return self_power_card < other_power_card
            # test card
        else:
            return self_power < other_power


def solve_part1(data):
    keys = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    power_data = {}
    for index, key in enumerate(keys):
        power_data[key] = len(keys) - index

    deck = []
    for line in data:
        cards = line.split(' ')[0]
        bid = int(line.split(' ')[1])
        hand = Hand(cards, bid, deck, power_data)
        deck.append(hand)
        power, power_type = hand.type

    deck.sort()
    total = 0
    for index, card in enumerate(deck):
        real_index = index+1
        total += real_index * card.bid
    return total



def solve_part2(data):
    keys = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    power_data = {}
    for index, key in enumerate(keys):
        power_data[key] = len(keys) - index

    deck = []
    for line in data:
        cards = line.split(' ')[0]
        bid = int(line.split(' ')[1])
        hand = Hand(cards, bid, deck, power_data, version=2)
        deck.append(hand)
        power, power_type = hand.type
        v1 = Hand(cards, bid, deck, power_data)
        v1_power, v1_power_type = v1.type
        print(f"2->{hand.cards} = {power_type}")
        print(f"1->{v1.cards} = {v1_power_type}")

    deck.sort()
    total = 0
    for index, card in enumerate(deck):
        real_index = index+1
        total += real_index * card.bid
    return total
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 6440


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 253866470


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 5905


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result < 254721929
    assert result < 254605710 
    assert result < 254796637


#test_part1()
#part1()
test_part2()
part2()
