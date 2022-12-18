#!/usr/bin/env python

test_data = [
    '2,2,2',
    '1,2,2',
    '3,2,2',
    '2,1,2',
    '2,3,2',
    '2,2,1',
    '2,2,3',
    '2,2,4',
    '2,2,6',
    '1,2,5',
    '3,2,5',
    '2,1,5',
    '2,3,5',
]

test_data_2 = [
    '1,1,1',
    '2,1,1'
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.neigbors = set()


class Graph:
    # example of adjacency list (or rather map)
    # adjacency_list = {
    # 'A': [('B', 1), ('C', 3), ('D', 7)],
    # 'B': [('D', 5)],
    # 'C': [('D', 12)]
    # }

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def get_neighbors(self, v):
        if v in self.adjacency_list:
            return self.adjacency_list[v]
        else:
            return []

    # heuristic function with equal values for all nodes
    def h(self, n):
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

                #print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all neighbors of the current node do
            for m in self.get_neighbors(n):
                weight = 1
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

def solve_part1(data, part=1):
    coordinates = {}
    for line in data:
        coordinate = list(map(int, line.split(',')))
        x = coordinate[0]
        y = coordinate[1]
        z = coordinate[2]
        coordinates[line] = Point(x,y,z)

    for coordinate, point in coordinates.items():
        for x in range(max(0, point.x - 1), point.x + 2):
            if x == point.x:
                continue

            test_index = f'{x},{point.y},{point.z}'
            if test_index in coordinates:
                if test_index not in point.neigbors:
                    point.neigbors.add(test_index)
                if coordinate not in coordinates[test_index].neigbors:
                    coordinates[test_index].neigbors.add(coordinate)

        for y in range(max(0, point.y - 1), point.y + 2):
            if y == point.y:
                continue

            test_index = f'{point.x},{y},{point.z}'
            if test_index in coordinates:
                if test_index not in point.neigbors:
                    point.neigbors.add(test_index)
                if coordinate not in coordinates[test_index].neigbors:
                    coordinates[test_index].neigbors.add(coordinate)

        for z in range(max(0, point.z - 1), point.z + 2):
            if z == point.z:
                continue

            test_index = f'{point.x},{point.y},{z}'
            if test_index in coordinates:
                if test_index not in point.neigbors:
                    point.neigbors.add(test_index)
                if coordinate not in coordinates[test_index].neigbors:
                    coordinates[test_index].neigbors.add(coordinate)

    min_x = min(map(int, map(lambda x: x.split(',')[0], coordinates.keys())))
    max_x = max(map(int, map(lambda x: x.split(',')[0], coordinates.keys())))
    min_y = min(map(int, map(lambda x: x.split(',')[1], coordinates.keys())))
    max_y = max(map(int, map(lambda x: x.split(',')[1], coordinates.keys())))
    min_z = min(map(int, map(lambda x: x.split(',')[2], coordinates.keys())))
    max_z = max(map(int, map(lambda x: x.split(',')[2], coordinates.keys())))

    graph = {}
    for x in range(-1, max_x + 2):
        for y in range(-1, max_y + 2):
            for z in range(-1, max_z + 2):
                index = f'{x},{y},{z}'
                neighbors = []

                for test_x in range(x-1, x+2):
                    if test_x == x:
                        continue
                    test_index = f'{test_x},{y},{z}'
                    if test_index not in coordinates:
                        neighbors.append(test_index)
                    else:
                        continue
                for test_y in range(y-1, y+2):
                    if test_y == y:
                        continue
                    test_index = f'{x},{test_y},{z}'
                    if test_index not in coordinates:
                        neighbors.append(test_index)
                    else:
                        continue
                for test_z in range(z-1, z+2):
                    if test_z == z:
                        continue
                    test_index = f'{x},{y},{test_z}'
                    if test_index not in coordinates:
                        neighbors.append(test_index)
                    else:
                        continue
                graph[index] = neighbors
    real_graph = Graph(graph)

    # Get ok coordinates
    ok_coordinates = []
    blocked = []

    def check_if_point_can_reach_water(test_index):
        path_to_next = real_graph.a_star_algorithm(test_index, '0,0,0')
        return path_to_next != None

        x = int(test_index.split(',')[0])
        y = int(test_index.split(',')[1])
        z = int(test_index.split(',')[2])

        found_blocker = 0

        # X
        for block_x in range(min(min_x, x), max(min_x, x)+2):
            block_index = f'{block_x},{y},{z}'
            if test_index == block_index:
                continue
            if block_index in coordinates:
                print(f'Is block at {block_index}')
                found_blocker += 1
                break
        if found_blocker != 1:
            return True

        for block_x in range(min(max_x, x), max(max_x, x)+2):
            block_index = f'{block_x},{y},{z}'
            if test_index == block_index:
                continue
            if block_index in coordinates:
                print(f'Is block at {block_index}')
                found_blocker += 1
                break
        if found_blocker != 2:
            return True

        # Y
        for block_y in range(min(min_y, y), max(min_y, y) + 2):
            block_index = f'{x},{block_y},{z}'
            if test_index == block_index:
                continue
            if block_index in coordinates:
                found_blocker += 1
                print(f'Is block at {block_index}')
                break
        if found_blocker != 3:
            return True

        for block_y in range(min(max_y, y), max(max_y, y) + 2):
            block_index = f'{x},{block_y},{z}'
            if test_index == block_index:
                continue
            if block_index in coordinates:
                found_blocker += 1
                print(f'Is block at {block_index}')
                break
        if found_blocker != 4:
            return True

        # Z
        for block_z in range(min(min_z, z), max(min_z, z)+2):
            block_index = f'{x},{y},{block_z}'
            if test_index == block_index:
                continue
            if block_index in coordinates:
                found_blocker += 1
                print(f'Is block at {block_index}')
                break
        if found_blocker != 5:
            return True

        for block_z in range(min(max_z, z), max(max_z, z)+2):
            block_index = f'{x},{y},{block_z}'
            if test_index == block_index:
                continue
            if block_index in coordinates:
                found_blocker += 1
                print(f'Is block at {block_index}')
                break
        if found_blocker != 6:
            return True
        else:
            print(f'index {test_index} is blocked {found_blocker}')
            return False

    total_coordinates = len(coordinates.keys())
    current = 0
    for coordinate, point in coordinates.items():
        current += 1
        print(f'==== {coordinate} {current}/{total_coordinates}=====')
        if part == 1:
            for x in range(point.x - 1, point.x + 2):
                if x == point.x:
                    continue
                test_index = f'{x},{point.y},{point.z}'
                if test_index not in point.neigbors:
                    ok_coordinates.append(test_index)

            for y in range(point.y - 1, point.y + 2):
                if y == point.y:
                    continue
                test_index = f'{point.x},{y},{point.z}'
                if test_index not in point.neigbors:
                    ok_coordinates.append(test_index)

            for z in range(point.z - 1, point.z + 2):
                if z == point.z:
                    continue
                test_index = f'{point.x},{point.y},{z}'
                if test_index not in point.neigbors:
                    ok_coordinates.append(test_index)
        else:
            for x in range(point.x - 1, point.x + 2):
                if x == point.x:
                    continue
                test_index = f'{x},{point.y},{point.z}'
                if test_index not in point.neigbors:
                    if check_if_point_can_reach_water(test_index):
                        ok_coordinates.append(test_index)

            for y in range(point.y - 1, point.y + 2):
                if y == point.y:
                    continue
                test_index = f'{point.x},{y},{point.z}'
                if test_index not in point.neigbors:
                    if check_if_point_can_reach_water(test_index):
                        ok_coordinates.append(test_index)

            for z in range(point.z - 1, point.z + 2):
                if z == point.z:
                    continue
                test_index = f'{point.x},{point.y},{z}'
                if test_index not in point.neigbors:
                    if check_if_point_can_reach_water(test_index):
                        ok_coordinates.append(test_index)

    return len(ok_coordinates)




def solve_part2(data):
    pass


def test_part1():
    data = test_data_2
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 10
    data = test_data
    result = solve_part1(data, 1)
    print(f'test1 is {result}')
    assert result == 64


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part1(data, 2)
    print(f'test2 is {result}')
    assert result == 58


def part2():
    data = load_data()
    result = solve_part1(data, 2)
    print(f'part2 is {result}')


test_part1()
part1()
print('===================================part2=============================')
test_part2()
part2()
