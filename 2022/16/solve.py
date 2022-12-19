#!/usr/bin/env python
from collections import deque

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


class Valve:
    def __init__(self, name, flow_rate, valves, neighbors):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors = neighbors
        self.valves = valves
        self.open = False

    def __str__(self):
        return f'Valve {self.name} flow={self.flow_rate} neighbors={self.neighbors}'

    def __repr__(self):
        return str(self)


class Graph:
    # example of adjacency list (or rather map)
    # adjacency_list = {
    # 'A': [('B', 1), ('C', 3), ('D', 7)],
    # 'B': [('D', 5)],
    # 'C': [('D', 12)]
    # }

    def __init__(self, adjacency_list, valves, visited):
        self.adjacency_list = adjacency_list
        self.valves = valves
        self.visited = visited
        self.max_flow = max(map(lambda x: x.flow_rate, self.valves.values())) + 1

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    # heuristic function with equal values for all nodes
    def h(self, n):
        if n in self.visited:
            return 10
        else:
            return 1

    def a_star_algorithm(self, start_node, stop_node):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = set([start_node])
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v;

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all neighbors of the current node do
            for m in self.get_neighbors(n):
                weight = len(closed_list)
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None


def get_valves(data):
    valves = {}
    for line in data:
        splitted = line.split(' ')
        name = splitted[1]
        flow_rate = int(''.join(list(filter(lambda x: x.isdigit(), splitted[4]))))
        neighbors = []
        for neighbor in splitted[9:]:
            neighbors.append(neighbor[0:2])
        valve = Valve(name, flow_rate, valves, neighbors)
        valves[name] = valve
    return valves


def solve_part1(data):
    valves = get_valves(data)
    graph = {k: v.neighbors for k, v in valves.items()}

    current = 'AA'
    pressure = 0
    visited = []
    to_visit_in_priority = [x.name for x in sorted(valves.values(), key=lambda x: x.flow_rate, reverse=True)]

    real_graph = Graph(graph, valves, visited)

    def find_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in graph:
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath: return newpath
        return None

    i = 0
    while i < 30:
        print(f'== Minute {i+1} Valve {current} Total {pressure}==')
        valve = valves[current]
        i_pressure = sum(map(lambda x: x.flow_rate, filter(lambda x: x.open, valves.values())))
        pressure += i_pressure
        print(f'Current pressure is {i_pressure}')
        visited.append(current)

        action = 'open'
        if valve.flow_rate == 0 or valve.open:
            action = 'travel'

        if action == 'open':
            print(f'Opening {current}')
            valve.open = True
            i += 1
        elif action == 'travel':
            # Go to the next max ? 
            next_path = None
            next_path_reward = None

            calculated_path = {}
            for visit_index in range(0, len(to_visit_in_priority)):
                to_visit = to_visit_in_priority[visit_index]
                if to_visit == current:
                    continue
                if valves[to_visit].open:
                    continue

                path_to_next = real_graph.a_star_algorithm(current, to_visit)
                calculated_path[to_visit] = path_to_next

                path_reward = 0
                path_visited = []
                to_divided = 0
                for valve_i in range(1, len(path_to_next)):
                    valve = path_to_next[valve_i]
                    if valve in path_visited:
                        continue
                    if valves[valve].open:
                        continue
                    else:
                        path_visited.append(valve)
                        number_of_time = len(path_to_next) - valve_i
                        to_divided += number_of_time
                        path_reward += number_of_time * valves[valve].flow_rate

                if to_divided != 0:
                    path_reward /= to_divided
                path_reward = int(path_reward)

                if next_path_reward is None:
                    next_path = path_to_next
                    next_path_reward = path_reward
                elif next_path_reward == path_reward:
                    if len(path_to_next) < len(next_path):
                        next_path = path_to_next
                        next_path_reward = path_reward

                elif next_path_reward < path_reward:
                    next_path = path_to_next
                    next_path_reward = path_reward
                print(f'path to {to_visit} is {path_to_next} reward {path_reward}')

            print(f'Will go to {next_path}')

            # Now extraccheck
            smaller = None
            smaller_length = None
            #for valve, valve_path in calculated_path.items():
            #    if valve_path == next_path:
            #        continue

            #    if len(valve_path) >= len(next_path):
            #        continue

            #    is_subset = True
            #    for index in range(len(valve_path)):
            #        if valve_path[index] != next_path[index]:
            #            is_subset = False
            #            break

            #    if is_subset:
            #        print(f'Found a subset {valve_path}')
            #        if smaller is None:
            #            smaller = valve_path
            #            smaller_length = len(valve_path)
            #        elif smaller_length > len(valve_path):
            #            smaller = valve_path
            #            smaller_length = len(valve_path)

            if smaller is not None:
                print(f'But found a subset {valve_path} using it')
                next_path = smaller


            path_to_next = next_path
            print(f'Will go to {next_path}')

            if not path_to_next:
                print('WTF ?')
            elif len(path_to_next) == 1:
                print('Ended ??')
                i += 1
            else:
                for to_add in range(len(path_to_next) - 1):
                    i += 1
                    pressure += i_pressure
                pressure -= i_pressure
                
                current = path_to_next[-1]
                print(f'Move to {current} using {path_to_next} so jump in time of {len(path_to_next) - 1}')
        print('')
        if i < 5:
            input()


    return pressure


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
