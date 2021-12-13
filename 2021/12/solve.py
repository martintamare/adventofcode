#!/usr/bin/env python
from collections import Counter

test_data = [
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end',
]

test_data_2 = [
    'dc-end',
    'HN-start',
    'start-kj',
    'dc-start',
    'dc-HN',
    'LN-dc',
    'HN-end',
    'kj-sa',
    'kj-HN',
    'kj-dc',
]

test_data_3 = [
    'fs-end',
    'he-DX',
    'fs-he',
    'start-DX',
    'pj-DX',
    'end-zg',
    'zg-sl',
    'zg-pj',
    'pj-he',
    'RW-he',
    'fs-DX',
    'pj-RW',
    'zg-RW',
    'start-pj',
    'he-WI',
    'zg-he',
    'pj-fs',
    'start-RW',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part_1(data):

    graph = {}

    for line in data:
        source = line.split('-')[0]
        destination = line.split('-')[1]
        if source not in graph:
            graph[source] = {}
        if destination not in graph:
            graph[destination] = {}

        graph[source][destination] = 1
        graph[destination][source] = 1

    print(f'graph is {graph}')



    paths = []
    def recurse_path(from_node, visited=[]):
        #print(f'node {from_node} visited {visited}')
        #print(f'paths {paths}')
        #input('pause')

        # Check validity
        if from_node == 'end':
            visited.append(from_node)
            return visited

        # small cave max 1
        if from_node.lower() == from_node:
            if from_node in visited:
                return []

        # no loop
        if len(visited):
            last_node = visited[-1]
            test_index = None
            for index in range(0, len(visited)):
                visited_node = visited[index]
                if visited_node == last_node:
                    test_index = index
                    break

            if test_index and test_index != len(visited) - 1:
                test_node = visited[test_index+1]
                if test_node == from_node:
                    return []

        visited.append(from_node)
        for neighbor in graph[from_node].keys():
            new_visited = visited.copy()
            path = recurse_path(neighbor, new_visited)
            if path:
                paths.append(path)

    start = 'start'
    recurse_path('start')
    return len(paths)


def solve_part_2(data):

    graph = {}

    for line in data:
        source = line.split('-')[0]
        destination = line.split('-')[1]
        if source not in graph:
            graph[source] = {}
        if destination not in graph:
            graph[destination] = {}

        graph[source][destination] = 1
        graph[destination][source] = 1

    print(f'graph is {graph}')



    paths = []
    def recurse_path(from_node, visited=[]):
        #print(f'node {from_node} visited {visited}')
        #print(f'paths {paths}')
        #input('pause')

        # Check validity
        if from_node == 'end':
            visited.append(from_node)
            str_visited = ','.join(visited)
            return visited

        if from_node == 'start':
            if from_node in visited:
                return []

        # small cave max 2 only one
        if from_node.lower() == from_node:
            if from_node in visited:
                counter = Counter(filter(lambda x: x.lower() == x, visited))
                already_have_2_small_caves = len(list(filter(lambda x: counter[x] == 2, counter.keys())))
                if already_have_2_small_caves == 1:
                    if from_node in visited:
                        return []

        visited.append(from_node)
        for neighbor in graph[from_node].keys():
            new_visited = visited.copy()
            path = recurse_path(neighbor, new_visited)
            if path:
                paths.append(path)

    start = 'start'
    recurse_path('start')

    return len(paths)



def test_part1():
    data = test_data
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 10

    data = test_data_2
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 19

    data = test_data_3
    result = solve_part_1(data)
    print(f'test1 is {result}')
    assert result == 226


def test_part2():
    data = test_data
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 36

    data = test_data_2
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 103

    data = test_data_3
    result = solve_part_2(data)
    print(f'test2 is {result}')
    assert result == 3509


def part1():
    data = load_data()
    result = solve_part_1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part_2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
