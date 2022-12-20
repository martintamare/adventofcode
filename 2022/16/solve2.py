#!/usr/bin/env python
from copy import deepcopy

test_data = [
    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
    'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
    'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
    'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
    'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
    'Valve HH has flow rate=22; tunnel leads to valve GG',
    'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
    'Valve JJ has flow rate=21; tunnel leads to valve II',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def get_valves(data):
    valves = {}
    for line in data:
        splitted = line.split(' ')
        name = splitted[1]
        flow_rate = int(''.join(list(filter(lambda x: x.isdigit(), splitted[4]))))
        neighbors = []
        for neighbor in splitted[9:]:
            neighbors.append(neighbor[0:2])
        valve = {
            'flow_rate': flow_rate,
            'neighbors': neighbors,
            'open': False,
        }
        valves[name] = valve
    return valves


def solve_part1(data):
    valves = get_valves(data)
    current = 'AA'
    pressure = 0
    data_max = list(map(lambda x: 0, range(30)))
    data_max[25] = 1

    def iterate(time=0, current='AA', valves={}, pressure=0, parents=[]):
        print(f'{current} - {parents}')
        if time == 30:
            print(f'found pressure {pressure}')
            return

        i_pressure = sum(map(lambda x: x['flow_rate'], filter(lambda x: x['open'], valves.values())))
        pressure += i_pressure
        if pressure < data_max[time]:
            return
        else:
            data_max[time] = pressure
        valve = valves[current]
        if valve['flow_rate'] > 0 and not valve['open']:
            new_valves = deepcopy(valves)
            new_valves[current]['open'] = True
            new_parents = parents.copy()
            iterate(time+1, current, valves, pressure, new_parents)

        did_i_went_somehere = False
        for neighbor in valve['neighbors']:
            if neighbor in parents:
                continue
            else:
                new_parents = parents.copy()
                new_parents.append(current)
                did_i_went_somehere = True
                iterate(time+1, neighbor, valves, pressure, new_parents)
        if not did_i_went_somehere:
                new_parents = parents.copy()
                new_parents.append(current)
                iterate(time+1, neighbor, valves, pressure, new_parents)


    iterate(0, 'AA', valves, 0)



def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 1651


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
