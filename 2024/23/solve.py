#!/usr/bin/env python
from collections import Counter, defaultdict
from itertools import combinations

test_data = [
    "kh-tc",
    "qp-kh",
    "de-cg",
    "ka-co",
    "yn-aq",
    "qp-ub",
    "cg-tb",
    "vc-aq",
    "tb-ka",
    "wh-tc",
    "yn-cg",
    "kh-ub",
    "ta-co",
    "de-co",
    "tc-td",
    "tb-wq",
    "wh-td",
    "ta-ka",
    "td-qp",
    "aq-cg",
    "wq-ub",
    "ub-vc",
    "de-ta",
    "wq-aq",
    "wq-vc",
    "wh-yn",
    "ka-de",
    "kh-ta",
    "co-tc",
    "wh-qp",
    "tb-vc",
    "td-yn",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Edge:
    def __init__(self, data):
        self.data = data
        self.connexions = set()

    def add_next(self, edge):
        self.connexions.add(edge)
        edge.connexions.add(self)

    def __lt__(self, other):
        return self.data < other.data

    def __repr__(self):
        return f"{self.data}"

    def compute_path(self, length=3):
        q = [0, self, set()]
        while q:
            (cur_length, edge, path) = q.pop(0)
            path = [edge] + path

            for neighbor in edge.connexions:
                if neighbor in path:
                    continue
                
                q.append((cur_length+1, neighbor, path))


def solve_part1(data):
    edges = {}
    for line in data:
        edge1 = line.split('-')[0]
        edge2 = line.split('-')[1]
        if edge1 not in edges:
            edges[edge1] = Edge(edge1)
        if edge2 not in edges:
            edges[edge2] = Edge(edge2)

        edges[edge1].add_next(edges[edge2])

    final_set = defaultdict(int)
    for edge in edges.values():
        print(len(edge.connexions))
        for t1, t2 in combinations(edge.connexions, 2):
            final_set[(f"{sorted([t1, t2, edge])}")] += 1

    result = 0
    for item, values in final_set.items():
        ok_item = item[1:-1]
        if values == final_set:
            print(item)
            if len(list(filter(lambda x: x.startswith("t"), ok_item.split(', ')))):
                result += 1
    return result


def solve_part2(data):
    edges = {}

    for line in data:
        edge1 = line.split('-')[0]
        edge2 = line.split('-')[1]
        if edge1 not in edges:
            edges[edge1] = Edge(edge1)
        if edge2 not in edges:
            edges[edge2] = Edge(edge2)

        edges[edge1].add_next(edges[edge2])


    max_connexions = len(list(edges.values())[0].connexions)
    final_set = defaultdict(int)
    for edge in edges.values():
        print(len(edge.connexions))
        for test in combinations(edge.connexions, max_connexions - 1):
            to_sorted = list(test) + [edge]
            final_set[(f"{sorted(to_sorted)}")] += 1

    print(final_set)
    print(max_connexions)
    result = 0
    for item, values in final_set.items():
        ok_item = item[1:-1]
        if values == max_connexions:
            return ','.join(ok_item.split(', '))
            print(item)
            exit(0)
            if len(list(filter(lambda x: x.startswith("t"), ok_item.split(', ')))):
                result += 1
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 7


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result < 2544
    print(f'part1 maybe {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == "co,de,ka,ta"


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
