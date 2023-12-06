#!/usr/bin/env python

test_data = [
    'Time:      7  15   30',
    'Distance:  9  40  200',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data



def solve(times, distances):
    score = 1
    for race in range(len(times)):
        race_total = 0
        time = times[race]
        distance = distances[race]
        #print(f"{time=} {distance=}")
        for hold_time in range(1, time):
            iteration = time-hold_time
            boat_distance = hold_time * iteration
            if boat_distance > distance:
                race_total += 1
            #print(f"{hold_time=} {iteration=} {boat_distance=}")
        #print(f"{race_total=}")
        score *= race_total
    return score

def solve_part1(data):
    times = list(map(int, filter(lambda x: x, data[0].split(':')[1].strip().split(' '))))
    distances = list(map(int, filter(lambda x: x, data[1].split(':')[1].strip().split(' '))))
    print(times)
    print(distances)
    return solve(times, distances)


def solve_part2(data):
    time = int(''.join(list(filter(lambda x: x, data[0].split(':')[1].strip().replace(' ', '')))))
    distance = int(''.join(list(filter(lambda x: x, data[1].split(':')[1].strip().replace(' ', '')))))
    return solve([time],[distance])

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 288


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 71503


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
