#!/usr/bin/env python
import re

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    result = handle_seat('FBFBBFFRLR')
    assert result == 357


def part1():
    seats = load_data()
    max_id = 0
    for seat in seats:
        id = handle_seat(seat)
        max_id = max(id, max_id)
    print(f'Max id is {max_id}')


def handle_seat(seat):
    row = seat[0:7]
    row_bin = ['0' if x == 'F' else '1' for x in row]
    column = seat[7:10]
    column_bin = ['1' if x == 'R' else '0' for x in column]
    row = int(''.join(row_bin), 2)
    column = int(''.join(column_bin), 2)
    return row * 8 + column


def gen_seat(key):
    row = key // 8
    column = key % 8
    str_row = str(bin(row))
    str_row = ['F' if x == '0' else 'B' for x in str_row[2:]]
    while(len(str_row) != 7):
            str_row.insert(0, 'F')
    str_column = str(bin(column))
    str_column = ['L' if x == '0' else 'R' for x in str_column[2:]]
    return '{0}{1}'.format(''.join(str_row), ''.join(str_column))


def test_part2():
    assert gen_seat(119) == 'FFFBBBFRRR'
    assert gen_seat(820) == 'BBFFBBFRLL'
    assert gen_seat(567) == 'BFFFBBFRRR'


def part2():
    seats = load_data()
    seat_dict = {}
    for seat in seats:
        seat_id = handle_seat(seat)
        seat_dict[seat_id] = seat

    for row in range(0, 127):
        for column in range(0, 7):
            key = row * 8 + column
            if key in seat_dict:
                continue
            if key - 1 in seat_dict and key + 1 in seat_dict:
                seat = gen_seat(key)
                print(f'{key} == {seat}')
                if seat.startswith('FFFFFFF'):
                    continue
                if seat.startswith('BBBBBBB'):
                    continue
                print(key)
    


test_part2()
test_part1()
part1()
part2()
