#!/usr/bin/env python
from collection import Counter

test_data = {
    1: 4,
    2: 8
}

prod_data = {
    1: 8,
    2: 3
}

class Game:
    def __init__(self, p1, p2, win_score=1000, scores=None, parent=None, current_player=1):
        self.position = {
                1: p1,
                2: p2,
        }
        if scores is None:
            scores = {
                1: 0,
                2: 0,
            }
        self.scores = scores
        self.win_score = win_score
        self.rolls = 0
        self.gameover = False
        self.parent = None
        self.current_player = current_player

    def quantum_play(self):
        # Roll 1 2 and 3 (recursive ?)
        scores = Counter()

        current_player = self.current_player
        while not self.gameover:
            for total_roll in range(1,4):
                position = (self.position[current_player] + total_roll) % 10
                if position == 0:
                    position = 10
                self.position[current_player] = position
                new_score = self.scores[current_player] + position

                if new_score >= self.win_score:
                    scores.update([current_player])
                else:
                    if current_player == 1:
                        current_player = 2
                    else:
                        current_player = 1
                    new_game
                    recurse = Game(position, self.position[current_player], scores=score


        return

    def play(self):
        start_index = 1
        current_player = self.current_player

        while not self.gameover:
            for roll in range(1,32):
                total_roll = 3 * start_index + 3
                start_index = start_index + 3

                position = (self.position[current_player] + total_roll) % 10
                if position == 0:
                    position = 10
                self.position[current_player] = position

                new_score = self.scores[current_player] + position
                self.scores[current_player] = new_score

                if current_player == 1:
                    current_player = 2
                else:
                    current_player = 1

                self.rolls += 3
                if new_score >= self.win_score:
                    self.gameover = True
                    self.loser = current_player
                    break

def solve_part_1(data):
    game = Game(data[1], data[2])
    game.play()
    return game.scores[game.loser] * game.rolls

def solve_part_2(data):
    game = Game(data[1], data[2], win_score=21)
    game.quantum_play()


def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 739785


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 444356092776315


def part1():
    data = prod_data
    result = solve_part_1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = None
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
#part2()
