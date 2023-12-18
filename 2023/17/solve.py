#!/usr/bin/env python
from math import inf as infinity
from functools import cache
from collections import namedtuple
from functools import lru_cache
import functools
import json

Serialized = namedtuple('Serialized', 'json')

test_data = [
    '2413432311323',
    '3215453535623',
    '3255245654254',
    '3446585845452',
    '4546657867536',
    '1438598798454',
    '4457876987766',
    '3637877979653',
    '4654967986887',
    '4564679986453',
    '1224686865563',
    '2546548887735',
    '4322674655533',
]

DEBUG = False




class City:
    def __init__(self, citymap, value, row, col):
        self._neighbors_for_astar = None
        self.citymap = citymap
        self.row = row
        self.col = col
        self.value = int(value)
        self.init_for_astar()

    def init_for_astar(self):
        self.gscore = infinity
        self.fscore = infinity
        self.closed = False
        self.in_openset = False
        self.came_from = None

    def __repr__(self):
        return f"{self.value}"


    @property
    def position(self):
        return f"{self.row},{self.col}"

    @property
    def neighbors_for_graph(self):
        neighbors = []
        neighbors.append('left')
        neighbors.append('up')
        neighbors.append('down')
        neighbors.append('right')

        real_neigbhors = []
        for neighbor in neighbors:
            if neighbor == 'right':
                row = self.row
                col = self.col + 1
            elif neighbor == 'down':
                row = self.row + 1
                col = self.col
            elif neighbor == 'left':
                row = self.row
                col = self.col - 1
            elif neighbor == 'up':
                row = self.row - 1
                col = self.col

            if col < 0 or col >= self.citymap.columns:
                continue
            if row < 0 or row >= self.citymap.rows:
                continue
            real_neigbhor = self.citymap.matrix[row][col]
            real_neigbhors.append(real_neigbhor)

        return real_neigbhors

    def neighbors_for_astar(self, current_path):
        neighbors = []

        if not current_path:
            # on est au début
            neighbors.append('down')
            neighbors.append('right')
        else:
            neighbors.append('down')
            neighbors.append('right')
            neighbors.append('left')
            neighbors.append('up')
            vector_row = None
            vector_col = None
            delta_row = None
            delta_col = None
            current = None
            for item in reversed(current_path):
                if item == self:
                    continue
                if vector_row is None:
                    vector_row = self.row - item.row
                    vector_col = self.col - item.col
                    delta_row = vector_row
                    delta_col = vector_col 
                    current = item
                else:
                    test_vector_row = current.row - item.row
                    test_vector_col = current.col - item.col
                    current = item
                    if test_vector_row == vector_row:
                        delta_row += vector_row
                    elif test_vector_col == vector_col:
                        delta_col += delta_col
                    else:
                        break

            min_row = max(0, self.row - 1)
            max_row = min(self.row + 2, len(self.citymap.matrix))

            min_col = max(0, self.col -1)
            max_col = min(self.col + 2, len(self.citymap.matrix[0]))
            if delta_row > 0:
                neighbors.remove('up')
                if delta_row == 3:
                    neighbors.remove('down')
            elif delta_row < 0:
                neighbors.remove('down')
                if delta_row == -3:
                    neighbors.remove('up')
            elif delta_col > 0:
                neighbors.remove('left')
                if delta_col == 3:
                    neighbors.remove('right')
            elif delta_col < 0:
                neighbors.remove('right')
                if delta_col == -3:
                    neighbors.remove('left')


        real_neigbhors = []
        for neighbor in neighbors:
            if neighbor == 'right':
                row = self.row
                col = self.col + 1
            elif neighbor == 'down':
                row = self.row + 1
                col = self.col
            elif neighbor == 'left':
                row = self.row
                col = self.col - 1
            elif neighbor == 'up':
                row = self.row - 1
                col = self.col

            if col < 0 or col >= self.citymap.columns:
                continue
            if row < 0 or row >= self.citymap.rows:
                continue
            real_neigbhor = self.citymap.matrix[row][col]
            real_neigbhors.append(real_neigbhor)

        return real_neigbhors

class Citymap:
    def __init__(self, data, version=1):
        # Build 2x2 matrix : line and columns
        self.matrix = []

        initial_rows = len(data)
        initial_columns = len(data[0])
        self.min_at_node = {}
        self.current_min = None

        for row, line in enumerate(data):
            matrix_row = []

            for col, char in enumerate(line):
                city = City(self, char, row, col)
                matrix_row.append(city)

            self.matrix.append(matrix_row)

        for row in self.matrix:
            for node in row:
                self.min_at_node[node] = infinity

    def __repr__(self):
        display = []
        for row in self.matrix:
            line_repr = ''.join(list(map(str, row)))
            display.append(line_repr)
        return '\n'.join(display)


    def cost_estimate(self, current, goal):
        return abs(current.row-goal.row) * 9 + abs(current.col-goal.col) * 9


    def find_best_path(self, start, end, current_path=[]):
        current_value = 0
        for test in current_path:
            current_value += test.value
        if self.current_min is not None:
            if current_value > self.current_min:
                return None

        if start == end:
            return current_path
        else:
            current_path_value = None
            current_sum_value = None
            for neighbor in start.neighbors_for_astar(current_path):
                if neighbor in current_path:
                    continue
                current_path_neighbor = current_path.copy()
                current_path_neighbor.append(start)
                final_path = self.find_best_path(neighbor, end, current_path_neighbor)
                if final_path is None:
                    continue
                current_value = 0
                for test in final_path:
                    current_value += test.value
                if self.current_min is not None and self.current_min < current_value:
                    continue
                if current_path_value is None:
                    current_path_value = final_path
                    current_sum_value = current_value
                    print(f"min {current_value}")
                    self.current_min = current_value
                elif current_value < current_sum_value:
                    current_path_value = final_path
                    current_sum_value = current_value
                    self.current_min = current_value
                    print(f"new min {current_value}")
            return current_path_value


    @property
    def part1(self):
        start = self.matrix[0][0]
        end = self.matrix[-1][-1]

        best_path = self.find_best_path(start, end)
        print("{best_path=}")
        min_item = 0
        for item in best_path:
            min_item += item.value
        return min_item + end.value



    @property
    def part1_astar_ko(self):
        start = self.matrix[0][0]
        end = self.matrix[-1][-1]
        test = self.astar(start, end)
        result = 0
        current = None
        print("================")
        for item in self.valid_path:
            print(f"path {item}@{item.position}")
            if current is None:
                result += item.value
                current = item
            else:
                distance = self.distance_between(current, item)
                result += distance
                current = item
        return result

    @property
    def rows(self):
        return len(self.matrix)

    @property
    def columns(self):
        return len(self.matrix[0])

    def distance_between(self, current, goal):
        return goal.value

    def neighbors(self, current):
        return current.neighbors_for_astar

    def is_goal_reached(self, current, goal):
        return current == goal

    def reconstruct_path(self, last):
        def _gen():
            current = last
            while current:
                yield current
                current = current.came_from

        return _gen()


    def astar(self, start, goal):
        for row in self.matrix:
            for city in row:
                city.init_for_astar()

        self.valid_path = []
        if self.is_goal_reached(start, goal):
            self.valid_path = [start]
            return True

        open_set = []
        search_nodes = {}
        start_node = start
        start_node.gscore = 0.0
        start_node.fscore = self.cost_estimate(start_node, goal)

        open_set.append(start_node)

        while open_set:
            current = open_set.pop(0)

            if self.is_goal_reached(current, goal):
                self.valid_path = self.reconstruct_path(current)
                return True

            current.closed = True
            for neighbor in current.neighbors_for_astar:
                if neighbor.closed:
                    continue

                tentative_gscore = current.gscore + self.distance_between(current, neighbor)

                if tentative_gscore >= neighbor.gscore:
                    continue

                if neighbor.in_openset:
                    open_set.remove(neighbor)

                neighbor.came_from = current
                neighbor.gscore = tentative_gscore
                neighbor.fscore = tentative_gscore + self.cost_estimate(neighbor, goal)
                open_set.append(neighbor)
        return False


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    citymap = Citymap(data)
    return citymap.part1


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 102


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result < 964
    assert result > 810


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
part1()
#test_part2()
#part2()
