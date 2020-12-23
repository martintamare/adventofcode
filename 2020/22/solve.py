#!/usr/bin/env python

test_data = [
    'Player 1:',
    '9',
    '2',
    '6',
    '3',
    '1',
    '',
    'Player 2:',
    '5',
    '8',
    '4',
    '7',
    '10',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Game:
    def __init__(self, deck1, deck2, game=1, parent=None):
        self.deck1 = deck1
        self.deck2 = deck2
        self.round = 0
        self.rounds = set()
        self.game = game
        self.recurse_stop = None
        self.parent = None

    @property
    def over(self):
        if self.recurse_stop is not None:
            return True
        if len(self.deck1) == 0:
            return True
        if len(self.deck2) == 0:
            return True
        return False

    @property
    def winner(self):
        if self.recurse_stop is not None:
            return 1
        if len(self.deck1) == 0:
            return 2
        elif len(self.deck2) == 0:
            return 1
        raise Exception('fnazjkfnazjkfaz')

    @property
    def over_with_recursion(self):
        return self.over

    @property
    def winner_score(self):
        if len(self.deck1) == 0:
            len_winner = len(self.deck2)
            score = 0
            for elem in self.deck2:
                score += elem*len_winner
                len_winner -= 1
            return score
        else:
            len_winner = len(self.deck1)
            score = 0
            for elem in self.deck1:
                score += elem*len_winner
                len_winner -= 1
            return score

    def iterate(self):
        self.round += 1
        print(f'round {self.round}')
        card1 = self.deck1.pop(0)
        card2 = self.deck2.pop(0)
        if card1 > card2:
            self.deck1.append(card1)
            self.deck1.append(card2)
        elif card2 > card1:
            self.deck2.append(card2)
            self.deck2.append(card1)
        else:
            print('fzajklfnazklfnaz')
            exit(0)

    @property
    def deck_index(self):
        deck1 = '-'.join([str(x) for x in self.deck1])
        deck2 = '-'.join([str(x) for x in self.deck2])
        return f'{deck1}_{deck2}'

    def iterate_recursion(self):
        self.round += 1
        print(f'Game {self.game} Round {self.round}')
        #print(f'deck1 {self.deck1}')
        #print(f'deck2 {self.deck2}')
        #print(f'{self.deck_index}')

        if self.deck_index in self.rounds:
            self.recurse_stop = 1
            return

        self.rounds.add(self.deck_index)

        card1 = self.deck1.pop(0)
        card2 = self.deck2.pop(0)
        #print(f'p1 plays {card1}')
        #print(f'p2 plays {card2}')

        if len(self.deck1) >= card1 and len(self.deck2) >= card2:
            deck1 = [self.deck1[x] for x in range(card1)]
            deck2 = [self.deck2[x] for x in range(card2)]
            subgame = Game(deck1, deck2, self.game+1, self)
            while not subgame.over_with_recursion:
                subgame.iterate_recursion()

            winner = subgame.winner
            if winner == 1:
                self.deck1.append(card1)
                self.deck1.append(card2)
            elif winner == 2:
                self.deck2.append(card2)
                self.deck2.append(card1)
        elif card1 > card2:
            self.deck1.append(card1)
            self.deck1.append(card2)
        else:
            self.deck2.append(card2)
            self.deck2.append(card1)


def get_deck(data):
    assert data[0] == 'Player 1:'
    data.pop(0)
    line = data.pop(0)
    deck_1 = []
    while line != 'Player 2:':
        if line == '':
            line = data.pop(0)
            continue
        deck_1.append(int(line))
        line = data.pop(0)
    print(deck_1)

    deck_2 = []
    for line in data:
        deck_2.append(int(line))
    print(deck_2)
    return deck_1, deck_2


def compute_winner_score(data):
    deck_1, deck_2 = get_deck(data.copy())
    game = Game(deck_1, deck_2)
    while not game.over:
        game.iterate()
    return game.winner_score


def compute_winner_score_using_awesome_recursion(data):
    deck_1, deck_2 = get_deck(data.copy())
    game = Game(deck_1, deck_2)
    while not game.over_with_recursion:
        game.iterate_recursion()
    return game.winner_score


def test_part1():
    data = test_data
    result = compute_winner_score(data)
    print(f'test1 is {result}')
    assert result == 306


def test_part2():
    data = test_data
    result = compute_winner_score_using_awesome_recursion(data)
    print(f'test2 is {result}')
    assert result == 291


def part1():
    data = load_data()
    result = compute_winner_score(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = compute_winner_score_using_awesome_recursion(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
