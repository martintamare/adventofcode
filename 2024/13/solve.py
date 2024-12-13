#!/usr/bin/env python
from functools import cached_property

test_data = [
    "Button A: X+94, Y+34",
    "Button B: X+22, Y+67",
    "Prize: X=8400, Y=5400",
    "",
    "Button A: X+26, Y+66",
    "Button B: X+67, Y+21",
    "Prize: X=12748, Y=12176",
    "",
    "Button A: X+17, Y+86",
    "Button B: X+84, Y+37",
    "Prize: X=7870, Y=6450",
    "",
    "Button A: X+69, Y+23",
    "Button B: X+27, Y+71",
    "Prize: X=18641, Y=10279",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def parse_prize(button):
    parsed = button.split(':')[1].strip().split(',')
    x_parsed = int(parsed[0].split('=')[1])
    y_parsed = int(parsed[1].split('=')[1])
    vector = (x_parsed, y_parsed)
    return vector

def parse_button(button):
    parsed = button.split(':')[1].strip().split(',')
    x_parsed = int(parsed[0].split('+')[1])
    y_parsed = int(parsed[1].split('+')[1])
    vector = (x_parsed, y_parsed)
    return vector


def gcd(a, b):
    if a == 0:
        return b
    # recursively calculating the gcd.
    return gcd(b % a, a)


def lcm(a, b):
    return (a / gcd(a, b)) * b


class Machine:
    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = prize
        self.a_win = None
        self.b_win = None

    def __repr__(self):
        return f"{self.a=} {self.b=} {self.prize=}"

    @cached_property
    def win(self):
        has_win = False
        for a_press in range(1, 101):
            for b_press in range(1, 101):
                final_x = a_press * self.a[0] + b_press * self.b[0]
                final_y = a_press * self.a[1] + b_press * self.b[1]
                if final_x == self.prize[0] and final_y == self.prize[1]:
                    has_win = True
                    self.a_win = a_press
                    self.b_win = b_press
                    break

        return has_win

    @property
    def tokens(self):
        if not self.win:
            return 0
        else:
            return self.a_win * 3 + self.b_win 

    @property
    def smart_tokens(self):
        """
        a_press * self.a[0] + b_press * self.b[0] = self.prize[0]
        a_press * self.a[1] + b_press * self.b[1] = self.prize[1]

        a_press = x
        b_press = y
        """
        d = self.a[0] * self.b[1] - self.a[1] * self.b[0]
        if d == 0:
            return False
            
        a_press = (self.prize[0] * self.b[1] - self.prize[1] * self.b[0]) / d
        b_press = (self.a[0] * self.prize[1] - self.a[1] * self.prize[0]) / d

        if a_press < 0 or b_press < 0:
            return False

        if not a_press.is_integer():
            return False
        if not b_press.is_integer():
            return False

        return a_press * 3 + b_press

def solve_part1(data):
    result = 0
    while len(data):
        a = parse_button(data.pop(0))
        b = parse_button(data.pop(0))
        prize = parse_prize(data.pop(0))
        if len(data):
            data.pop(0)
        machine = Machine(a, b, prize)
        if machine.win:
            print(f"a_press={machine.a_win} b_press={machine.b_win}")
            tokens = machine.tokens
            assert tokens == machine.smart_tokens
            result += tokens
    return result


def solve_part2(data):
    result = 0
    while len(data):
        a = parse_button(data.pop(0))
        b = parse_button(data.pop(0))
        prize = parse_prize(data.pop(0))
        prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
        if len(data):
            data.pop(0)
        machine = Machine(a, b, prize)
        print(machine)
        tokens = machine.smart_tokens
        if isinstance(tokens, bool):
            print("Unable to compute")
        else:
            print("ok")
            result += machine.smart_tokens
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 480


def part1():
    data = load_data().copy()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 31761


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result < 157687857400714
    assert result < 153466466662074


#test_part1()
#part1()
test_part2()
part2()
