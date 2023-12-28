#!/usr/bin/env python
import networkx as nx
from networkx.algorithms.connectivity import minimum_st_edge_cut


test_data = [
    'jqt: rhn xhk nvd',
    'rsh: frs pzl lsr',
    'xhk: hfx',
    'cmg: qnr nvd lhk bvb',
    'rhn: xhk bvb hfx',
    'bvb: xhk hfx',
    'pzl: lsr hfx nvd',
    'qnr: nvd',
    'ntq: jqt hfx bvb xhk',
    'nvd: lhk',
    'lsr: lhk',
    'rzs: qnr cmg lsr rsh',
    'frs: qnr lhk lsr',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Link:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b or self.a == other.b and self.b == other.a

    def __hash__(self):
        if self.a.name < self.b.name:
            return hash(f"{self.a.name}_{self.b.name}")
        else:
            return hash(f"{self.b.name}_{self.a.name}")


class Node:
    def __init__(self, name, graph):
        self.name = name
        self.graph = graph
        self.links = set()

    def add_link(self, other):
        link = Link(self, other)
        self.graph.links.add(link)
        self.links.add(link)
        other.links.add(link)


class Graph:
    def __init__(self, data):
        self.nodes = {}
        self.links = set()

        for line in data:
            source = line.split(': ')[0]
            destinations = line.split(': ')[1].split(' ')

            if source not in self.nodes:
                node = Node(source, self)
                self.nodes[source] = node

            source_node = self.nodes[source]

            for destination in destinations:
                if destination not in self.nodes: 
                    node = Node(destination, self)
                    self.nodes[destination] = node
                destination_node = self.nodes[destination]

                source_node.add_link(destination_node)



def solve_part1(data):
    graph = nx.Graph()

    for line in data:
        source = line.split(': ')[0]
        destinations = line.split(': ')[1].split(' ')

        if source not in graph.nodes:
            graph.add_node(source)

        for destination in destinations:
            if destination not in graph.nodes: 
                graph.add_node(destination)
            graph.add_edge(source, destination)


    test = nx.minimum_edge_cut(graph)
    result, groups = nx.stoer_wagner(graph)
    group_1, group_2 = groups
    return len(group_1) * len(group_2)


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 54


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
