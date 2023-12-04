#!/usr/bin/env python

test_data = [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
]

class Gameset:
    def __init__(self, data):
        data = data.strip()
        self.count = {}
        for item in data.split(','):
            item_split = item.strip().split(' ')
            item_int = int(item_split[0])
            item_key = item_split[1]
            self.count[item_key] = item_int

    def is_possible_with(self, red, green, blue):
        data = {
            'red': red,
            'green': green,
            'blue': blue,
        }
        for key in data.keys():
            if key in self.count:
                game_value = self.count[key]
                possible_value = data[key]
                if game_value > possible_value:
                    return False
        return True




class Game:
    def __init__(self, line):
        self.line = line
        line_split = line.split(':')
        self.id = int(line_split[0].split(' ')[1])
        self.examples = line_split[1].strip()
        self.data_examples = []
        self.min_data = {}

        for example in self.examples.split(';'):
            subset = Gameset(example)
            self.data_examples.append(subset)

            for item in subset.count.keys():
                if item not in self.min_data:
                    self.min_data[item] = subset.count[item]
                elif self.min_data[item] < subset.count[item]:
                    self.min_data[item] = subset.count[item]


    def is_possible_with(self, red, green, blue):
        for gameset in self.data_examples:
            if not gameset.is_possible_with(red, green, blue):
                return False
        return True

    @property
    def power(self):
        result = 1
        for item in ['red', 'green', 'blue']:
            if item not in self.min_data:
                return 0
            else:
                result = result * self.min_data[item]
        return result

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    games = []
    for line in data:
        games.append(Game(line))

    ok_games = []
    for game in games:
        if game.is_possible_with(red=12, green=13, blue=14):
            ok_games.append(game.id)
    return sum(ok_games)

def solve_part2(data):
    games = []
    for line in data:
        game = Game(line)
        print(game.power)
        games.append(game.power)

    return sum(games)

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 8


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 2286


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
