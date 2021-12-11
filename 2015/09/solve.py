#!/usr/bin/env python
from itertools import permutations

test_data = [
    'London to Dublin = 464',
    'London to Belfast = 518',
    'Dublin to Belfast = 141',
]

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def compute_shortest_path(data):
    graph = {}
    for line in data:
        city_a = line.split(' ')[0]
        city_b = line.split(' ')[2]
        distance = int(line.split(' ')[4])

        if city_a not in graph:
            graph[city_a] = {}
        graph[city_a][city_b] = distance

        if city_b not in graph:
            graph[city_b] = {}
        graph[city_b][city_a] = distance
    
    cities = graph.keys()
    shortest_distance = None
    longest_distance = None
    for combination in permutations(cities, len(cities)):
        distance = 0
        last_city = None
        for city in combination:
            if last_city is not None:
                distance += graph[last_city][city]
            last_city = city
        if shortest_distance is None:
            shortest_distance = distance
        elif distance < shortest_distance:
            shortest_distance = distance

        if longest_distance is None:
            longest_distance = distance
        elif distance > longest_distance:
            longest_distance = distance
    return shortest_distance, longest_distance


def test_part1():
    data = test_data
    result, fake = compute_shortest_path(data)
    print(f'test1 is {result}')
    assert result == 605


def test_part2():
    data = test_data
    fake, result = compute_shortest_path(data)
    print(f'test2 is {result}')
    assert result == 982


def part1():
    data = load_data()
    result, fake = compute_shortest_path(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    fake, result = compute_shortest_path(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
