#!/usr/bin/env python

test_data = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    result = 0
    for line in data:
        test_line = line[:-1]
        digits = sorted(list(set(map(int, test_line))), reverse=True)
        max_digit = digits[0]
        max_index = line.find(f"{max_digit}")
        new_line = line[max_index+1:]
        new_digits = sorted(list(set(map(int, new_line))), reverse=True)
        second_digit = new_digits[0]
        to_add = f"{max_digit}{second_digit}"
        print(f"{line=} {to_add}")
        result += int(to_add)

    return result


def compute_line(line, bank_size):
    ok_result = ""
    line_size = len(line)
    current_line = line
    for size in range(bank_size):
        print(f"{current_line=} {size=}")
        if size == bank_size-1:
            test_line = current_line
        else:
            wanted_length = len(current_line) - bank_size + size + 1
            print(f"{len(current_line)=} {bank_size=} {size=} {wanted_length=}")
            test_line = current_line[0:wanted_length]
        print(f"{test_line=}")
        digits = sorted(list(set(map(int, test_line))), reverse=True)
        max_digit = digits[0]
        max_index = test_line.find(f"{max_digit}")
        print(f"{size=} {test_line=} {max_digit=} {max_index=} {ok_result=}")
        ok_result += f"{max_digit}"
        current_line = current_line[max_index+1:]
    print(f"{ok_result=}")
    return int(ok_result)



def solve_part2(data, bank_size=12):
    result = 0
    for line in data:
        to_add = compute_line(line, bank_size)
        result += to_add
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 357


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2_bis():
    data = {
        "987654321111111": 987654321111,
        "811111111111119": 811111111119,
        "234234234234278": 434234234278,
        "818181911112111": 888911112111,
    }
    for line, wanted_result in data.items():
        current_result = compute_line(line, 12)
        print(f"{line=} {current_result=} {wanted_result=}")
        assert current_result == wanted_result
    result = solve_part2(data)

def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 3121910778619


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2_bis()
test_part2()
part2()
