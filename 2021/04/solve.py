#!/usr/bin/env python

test_data = [
'7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
'',
'22 13 17 11  0',
' 8  2 23  4 24',
'21  9 14 16  7',
' 6 10  3 18  5',
' 1 12 20 15 19',
'',
' 3 15  0  2 22',
' 9 18 13 17  5',
'19  8  7 25 23',
'20 11 10 24  4',
'14 21 16 12  6',
'',
'14 21 17 24  4',
'10 16 15  9 19',
'18  8 23 26 20',
'22 11 13  6  5',
' 2  0 12  3  7',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Seat:
    def __init__(self, number):
        self.number = number
        self.marked = False


class Card:
    def __init__(self, data):
        self.matrix = []
        self.load_data(data)
        self.win_at_number = None
        self.win_at_index = None
        self.win_sum = 0

    def load_data(self, data):
        for line in data:
            row = []
            for i in range(0, 5):
                row.append(Seat(int(line[3*i:3*i+2])))
            self.matrix.append(row)

    def update(self, number):
        for row in self.matrix:
            for seat in row:
                if seat.number == number:
                    seat.marked = True
                    return

    @property
    def is_winner(self):
        for i in range(0, 5):
            row_marked = True
            column_marked = True
            for j in range(0, 5):
                if not self.matrix[i][j].marked:
                    row_marked = False
                if not self.matrix[j][i].marked:
                    column_marked = False
            if row_marked or column_marked:
                return True
        return False

    @property
    def sum(self):
        unmarked = 0
        for row in self.matrix:
            for seat in row:
                if not seat.marked:
                    unmarked += seat.number
        return unmarked


def bingo(data, winner='first'):
    work_data = data.copy()
    numbers = list(map(int, work_data.pop(0).split(',')))
    work_data.pop(0)

    cards = []
    while len(work_data):
        rows = []
        while len(rows) < 5:
            rows.append(work_data.pop(0))
        card = Card(rows)
        cards.append(card)
        if len(work_data):
            work_data.pop(0)

    for index in range(0, len(numbers)):
        number = numbers[index]
        for card in cards:
            card.update(number)
            if card.is_winner and not card.win_sum:
                card.win_at_index = index
                card.win_at_number = number
                card.win_sum = card.sum
                print(f'card {index} won at {number} with sum {card.sum}')

    winner_card = None
    for card in cards:
        if card.win_sum:
            if not winner_card:
                winner_card = card
            elif winner == 'first' and winner_card.win_at_index > card.win_at_index:
                winner_card = card
            elif winner == 'last' and winner_card.win_at_index < card.win_at_index:
                winner_card = card
    return winner_card.win_at_number * winner_card.win_sum


def test_part1():
    data = test_data
    result = bingo(data)
    print(f'test1 is {result}')
    assert result == 4512


def test_part2():
    data = test_data
    result = bingo(data, 'last')
    print(f'test2 is {result}')
    assert result == 1924


def part1():
    data = load_data()
    result = bingo(data)
    print(f'part1 is {result}')
    assert result == 11536


def part2():
    data = load_data()
    result = bingo(data, 'last')
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
