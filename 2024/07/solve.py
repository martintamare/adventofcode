#!/usr/bin/env python

test_data = [
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20",
]

def recursion(current, wanted_result, number, remaining_numbers):
    print(f"{current=} {wanted_result=} {number=} {remaining_numbers=}")
    if not remaining_numbers:
        if current + number == wanted_result:
            return [True]
        elif current * number == wanted_result:
            return [True]
        else:
            return [False]
    else:
        to_return = []
        current_1 = current + number
        to_return += recursion(current_1, wanted_result, remaining_numbers[0], remaining_numbers[1:].copy())
        current_2 = current * number
        to_return += recursion(current_2, wanted_result, remaining_numbers[0], remaining_numbers[1:].copy())
        return to_return


def recursion_part2(current, wanted_result, number, remaining_numbers):
    print(f"{current=} {wanted_result=} {number=} {remaining_numbers=}")
    if current > wanted_result:
        return False

    if not remaining_numbers:
        concat = int(f"{current}{number}")
        if current + number == wanted_result:
            return True
        elif current * number == wanted_result:
            return True
        elif concat == wanted_result:
            return True
        else:
            return False
    else:
        to_return = []
        current_1 = current + number
        to_return.append(recursion_part2(current_1, wanted_result, remaining_numbers[0], remaining_numbers[1:].copy()))
        current_2 = current * number
        to_return.append(recursion_part2(current_2, wanted_result, remaining_numbers[0], remaining_numbers[1:].copy()))
        current_3 = int(f"{current}{number}")
        to_return.append(recursion_part2(current_3, wanted_result, remaining_numbers[0], remaining_numbers[1:].copy()))
        return any(to_return)
    



class Operation:
    def __init__(self, line):
        self.line = line
        self.result = int(line.split(':')[0].strip())
        self.numbers = list(map(int, line.split(':')[1].strip().split(' ')))

    @property
    def valid(self):
        result = recursion(self.numbers[0], self.result, self.numbers[1], self.numbers[2:])
        print(f"{self.line=} {result=}")
        return any(result)

    @property
    def valid_part2(self):
        result = recursion_part2(self.numbers[0], self.result, self.numbers[1], self.numbers[2:])
        print(f"{self.line=} {result=}")
        return result


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    result = 0
    for line in data:
        operation = Operation(line)
        if operation.valid:
            result += operation.result
    return result


def solve_part2(data):
    result = 0
    for line in data:
        operation = Operation(line)
        if operation.valid_part2:
            result += operation.result
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 3749


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 11387


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result > 248345859993584
    print(f'part2 maybe ok ?')


#test_part1()
#part1()
test_part2()
part2()
