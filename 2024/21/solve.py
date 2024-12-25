#!/usr/bin/env python
from itertools import pairwise
from functools import lru_cache

test_data = [
    "029A",
    "980A",
    "179A",
    "456A",
    "379A",
]

test_data_dict = {
    "029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
    "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
    "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
    "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
    "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
}

def calculate_difference(path):
    previous = None
    result = 0
    for char in path:
        if previous is None:
            previous = char
        else:
            if char != previous:
                result += 1
            previous = char
    return result


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    numeric = NumericKeypad()
    direction = DirectionalKeypad()

    result = 0
    for c in data:
        code = Code(c, numeric, direction)
        code.compute_shortest_path()
        path = len(code.shortest_path)
        result += path * code.value
    return result


def solve_part2(data):
    numeric = NumericKeypad()
    direction = DirectionalKeypad()

    result = 0
    for c in data:
        code = Code(c, numeric, direction, robot=25)
        code.compute_shortest_path()
        path = len(code.shortest_path)
        result += path * code.value
    return result
    pass

class Keypad:
    def __init__(self):
        self.data = {}

    @lru_cache
    def compute_path(self, start, end):
        q = [(0, start, [])]
        min_path = None
        mins = { start: 0 }
        ok_paths = []
        best_path = None

        while q:
            (cost, cell, path) = q.pop(0)
            if min_path is not None and min_path < cost:
                continue

            path = [cell] + path
            if cell == end:
                final_path = list(reversed(path))
                ok_paths.append(final_path)

                if min_path is None:
                    min_path = cost
                    best_path = final_path
                elif min_path > cost:
                    min_path = cost
                    best_path = final_path
            else:
                for neighbor in self.data[cell].keys():
                    if neighbor in path:
                        continue
                    prev_cost = mins.get(neighbor, None)
                    next_cost = cost + 1

                    if prev_cost is None or next_cost <= prev_cost:
                        mins[neighbor] = next_cost
                        q.append((next_cost, neighbor, path))

        return list(filter(lambda x: len(x) == min_path+1, ok_paths))

    @lru_cache
    def compute_paths_for_code(self, code):
        current = "A"
        results = []
        for char in code:
            test = self.compute_path(current, char)
            paths = []
            for path in test:
                ok_path = ""
                for source, destination in pairwise(path):
                    ok_path += self.data[source][destination]
                ok_path += "A"
                paths.append(ok_path)
            if not results:
                results = paths
            else:
                new_results = []
                for result in results:
                    for path in paths:
                        new_results.append(result+path)
                results = new_results
            current = char

        min_difference = None
        ok_path = None
        for path in results:
            differences = calculate_difference(path)
            if min_difference is None:
                min_difference = differences
                ok_path = path
            elif differences < min_difference:
                min_difference = differences
                ok_path = path

        return list(filter(lambda x: calculate_difference(x) == min_difference, results))

class NumericKeypad(Keypad):
    def __init__(self):
        self.data = {
            "0": {
                "A": ">",
                "2": "^",
            },
            "1": {
                "2": ">",
                "4": "^",
            },
            "2": {
                "3": ">",
                "5": "^",
                "0": "v",
                "1": "<",
            },
            "3": {
                "6": "^",
                "A": "v",
                "2": "<",
            },
            "4": {
                "5": ">",
                "7": "^",
                "1": "v",
            },
            "5": {
                "6": ">",
                "8": "^",
                "2": "v",
                "4": "<",
            },
            "6": {
                "9": "^",
                "3": "v",
                "5": "<",
            },
            "7": {
                "8": ">",
                "4": "v",
            },
            "8": {
                "9": ">",
                "5": "v",
                "7": "<",
            },
            "9": {
                "6": "v",
                "8": "<",
            },
            "A": {
                "3": "^",
                "0": "<",
            },
        }




class DirectionalKeypad(Keypad):
    def __init__(self):
        self.data = {
            "A": {
                ">": "v",
                "^": "<",
            },
            "<": {
                "v": ">",
            },
            ">": {
                "A": "^",
                "v": "<",
            },
            "^": {
                "A": ">",
                "v": "v",
            },
            "v": {
                ">": ">",
                "^": "^",
                "<": "<",
            },
        }
        pass


class Code:
    def __init__(self, code, numeric, direction, robot=2):
        self.code = code
        self.shortest_path = []
        self.numeric = numeric
        self.direction = direction
        self.robot = robot

    def __repr__(self):
        return self.code

    @property
    def value(self):
        return int(self.code[0:-1])

    def compute_shortest_path(self):
        results1 = self.numeric.compute_paths_for_code(self.code)

        current_result = results1
        for index in range(self.robot):
            print(f"{index=} parsing {len(current_result)} results")
            new_current = []
            for r in current_result:
                new_r = self.direction.compute_paths_for_code(r)
                new_current += new_r
            current_result = new_current

        paths_length = map(len, current_result)
        min_path = min(paths_length)
        print(f"{min_path=}")
        self.shortest_path = list(filter(lambda x: len(x) == min_path, current_result))[0]

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 126384


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
test_part2()
#part2()
