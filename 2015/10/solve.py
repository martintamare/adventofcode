#!/usr/bin/env python

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Game:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'{self}'

    def iterate(self):
        current_digit = None
        number_of_current_digit = 0
        final_result = ''
        for char in self.value:
            if current_digit is None:
                current_digit = char
                number_of_current_digit += 1
            elif char == current_digit:
                number_of_current_digit += 1
            else:
                final_result += f'{number_of_current_digit}{current_digit}'
                current_digit = char
                number_of_current_digit = 1
        final_result += f'{number_of_current_digit}{current_digit}'
        self.value = final_result


def solve_game(data, iteration=40):
    game = Game(data)
    for i in range(0, iteration):
        game.iterate()
    return len(game.value)


def test_part1():
    result = solve_game('1')
    print(f'test1 is {result}')
    assert result == 25


def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = '3113322113'
    result = solve_game(data)
    print(f'part1 is {result}')


def part2():
    data = '3113322113'
    result = solve_game(data, 50)
    print(f'part2 is {result}')


#test_part1()
part1()
#test_part2()
part2()
