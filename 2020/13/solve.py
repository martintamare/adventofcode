#!/usr/bin/env python

test_data = [
    '939',
    '7,13,x,x,59,x,31,19',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = find_result(data)
    print(f'test1 is {result}')
    assert result == 295


def find_result(data):
    min_minutes_to_wait = int(data[0])
    bus_ids = []
    for bus_id in data[1].split(','):
        try:
            bus_id = int(bus_id)
            bus_ids.append(bus_id)
        except ValueError:
            continue

    def get_min_minutes_to_start(bus_id):
        start_minutes = bus_id
        while start_minutes < min_minutes_to_wait:
            start_minutes += bus_id
        return start_minutes - min_minutes_to_wait

    wait_bus_minutes = list(map(get_min_minutes_to_start, bus_ids))
    min_minutes = min(wait_bus_minutes)
    min_minutes_index = wait_bus_minutes.index(min_minutes)
    bus_id = bus_ids[min_minutes_index]
    return bus_id * min_minutes


def find_min_timestamp(data):
    timestamp = 1
    stop = False
    while not stop:
        if timestamp % 1000 == 0:
            print(f'current timestamp {timestamp}')
        all_match_is_ok = True
        last_ok_index = None
        for index in range(len(data)):
            bus_id = data[index]
            try:
                bus_id = int(bus_id)
            except ValueError:
                continue
            if (timestamp + index) % bus_id == 0:
                last_ok_index = index
                continue
            else:
                all_match_is_ok = False
                break
        if all_match_is_ok:
            stop = True
            print(f'timestamp is {timestamp}')
            return timestamp
        else:
            if last_ok_index is not None:
                # print(f'current timestamp {timestamp}')
                # print(f'last_ok_index {last_ok_index}')
                # print(data[0:last_ok_index+1])
                timestamp_to_add = 1
                for add_index in range(last_ok_index+1):
                    elem = data[add_index]
                    try:
                        elem = int(elem)
                    except ValueError:
                        continue
                    timestamp_to_add = timestamp_to_add * elem
                timestamp += timestamp_to_add
            else:
                timestamp += 1


def test_part2():
    data = ['17','x','13','19']
    result = find_min_timestamp(data)
    print(f'test2 is {result}')
    assert result == 3417

    data = ['67','7','59','61']
    result = find_min_timestamp(data)
    print(f'test2 is {result}')
    assert result == 754018

    data = ['67','x', '7','59','61']
    result = find_min_timestamp(data)
    print(f'test2 is {result}')
    assert result == 779210

    data = ['67','7', 'x','59','61']
    result = find_min_timestamp(data)
    print(f'test2 is {result}')
    assert result == 1261476

    data = ['1789','37','47','1889']
    result = find_min_timestamp(data)
    print(f'test2 is {result}')
    assert result == 1202161486


def part1():
    data = load_data()
    result = find_result(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = find_min_timestamp(data[1].split(','))
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
