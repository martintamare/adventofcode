#!/usr/bin/env python

test_data = [
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def get_invalid_ids(t):
    first_id_txt = t.split("-")[0]
    last_id_txt = t.split("-")[1]

    first_id_range = len(first_id_txt)
    last_id_range = len(last_id_txt)

    first_id = int(first_id_txt)
    last_id = int(last_id_txt)

    ok_ids = set()

    for r in range(first_id_range, last_id_range+1):
        if r % 2:
            continue

        # Test a = b 
        test_size = int(r / 2)
        for t in range(10**test_size):
            a = ""
            a += f"{t}{t}"
            print(f"{t=} {a=}")
            a = int(a)
            if a >= first_id and a <= last_id:
                ok_ids.add(int(a))
    return list(ok_ids)


def get_invalid_ids_part2(t):
    first_id_txt = t.split("-")[0]
    last_id_txt = t.split("-")[1]

    first_id_range = len(first_id_txt)
    last_id_range = len(last_id_txt)

    first_id = int(first_id_txt)
    last_id = int(last_id_txt)

    ok_ids = set()

    for r in range(first_id_range, last_id_range+1):
        # Test a = b 
        test_size = int(r / 2)
        for t in range(10**test_size):
            a = ""
            while len(a) < r:
                a += f"{t}"
            if len(a) > r:
                continue
            print(f"{t=} {a=}")

            a = int(a)
            if a >= first_id and a <= last_id:
                ok_ids.add(int(a))
    return list(ok_ids)


def solve_part1(data):
    data = data[0]
    data = data.split(",")
    result = 0
    for t in data:
        invalid_ids = get_invalid_ids(t)
        print(f"{t=} {invalid_ids=}")
        for id in invalid_ids:
            result += int(id)
    return result


def solve_part2(data):
    data = data[0]
    data = data.split(",")
    result = 0
    for t in data:
        invalid_ids = get_invalid_ids_part2(t)
        print(f"{t=} {invalid_ids=}")
        for id in invalid_ids:
            result += int(id)
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 1227775554


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 4174379265


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
