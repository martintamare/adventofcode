#!/usr/bin/env python

test_data = [
    'A Y',
    'B X',
    'C Z',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Round:
    def __init__(self, opponent, me):
        self.me = me
        self.opponent = opponent

    @property
    def result(self):
        if self.opponent == 'A' and self.me == 'Y':
            return 'win'
        if self.opponent == 'B' and self.me == 'Z':
            return 'win'
        if self.opponent == 'C' and self.me == 'X':
            return 'win'
        if self.opponent == 'A' and self.me == 'X':
            return 'tie'
        if self.opponent == 'B' and self.me == 'Y':
            return 'tie'
        if self.opponent == 'C' and self.me == 'Z':
            return 'tie'
        else:
            return 'lost'

    @property
    def score_shape(self):
        mapping = {
            'X': 1,
            'Y': 2,
            'Z': 3,
        }
        return mapping[self.me]

    @property
    def score_result(self):
        if self.result == 'win':
            return 6
        elif self.result == 'lost':
            return 0
        else:
            return 3

    @property
    def score(self):
        return self.score_shape + self.score_result

    @property
    def score_part2(self):
        # Loosing
        if self.me == 'X':
            if self.opponent == 'A':
                self.me = 'Z'
            elif self.opponent == 'B':
                self.me = 'X'
            elif self.opponent == 'C':
                self.me = 'Y'
        # Tie
        elif self.me == 'Y':
            if self.opponent == 'A':
                self.me = 'X'
            elif self.opponent == 'B':
                self.me = 'Y'
            elif self.opponent == 'C':
                self.me = 'Z'
        # Win
        elif self.me == 'Z':
            if self.opponent == 'A':
                self.me = 'Y'
            elif self.opponent == 'B':
                self.me = 'Z'
            elif self.opponent == 'C':
                self.me = 'X'

        return self.score


def compute_score(data):
    total = 0
    for _round in data:
        splitted = _round.split(' ')
        assert len(splitted) == 2
        opponent = splitted[0]
        me = splitted[1]
        _round = Round(opponent, me)
        total += _round.score
    return total


def compute_score_part2(data):
    total = 0
    for _round in data:
        splitted = _round.split(' ')
        assert len(splitted) == 2
        opponent = splitted[0]
        me = splitted[1]
        _round = Round(opponent, me)
        total += _round.score_part2
    return total


def test_part1():
    data = test_data
    result = compute_score(data)
    print(f'test1 is {result}')
    assert result == 15


def test_part2():
    data = test_data
    result = compute_score_part2(data)
    print(f'test2 is {result}')
    assert result == 12


def part1():
    data = load_data()
    result = compute_score(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = compute_score_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
