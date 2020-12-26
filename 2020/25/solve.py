#!/usr/bin/env python

test_data = [
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

def get_loop(key):
    subject = 7
    value = 1
    loop = 1
    while True:
        value = value * subject
        value = value % 20201227
        if value == key:
            return loop
        else:
            loop += 1


def compute_encryption_key(pkey, door_loop):
    loop = 0
    value = 1
    subject = pkey
    while loop < door_loop:
        value = value * subject
        value = value % 20201227
        loop += 1
    return value




def test_part1():
    card_pkey = 5764801
    card_loop = get_loop(card_pkey)
    print(f'found card_loop {card_loop}')
    assert card_loop == 8

    door_pkey = 17807724
    door_loop = get_loop(door_pkey)
    print(f'found door_loop {door_loop}')
    assert door_loop == 11

    encryption_key = compute_encryption_key(door_pkey, card_loop)
    print(f'encryption_key is {encryption_key}')
    assert encryption_key == 14897079


def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = load_data()
    card_pkey = int(data[0])
    door_pkey = int(data[1])
    card_loop = get_loop(card_pkey)
    door_loop = get_loop(door_pkey)
    encryption_key = compute_encryption_key(door_pkey, card_loop)
    print(f'encryption_key is {encryption_key}')


def part2():
    data = load_data()
    result = None
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
