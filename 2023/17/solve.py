#!/usr/bin/env python
import itertools
from math import inf as infinity
from heapq import heappop, heappush
from collections import defaultdict

# row, col diff
# we can go 90% when iterating
directions = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}


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


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve(data):
    # https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    pq = []  # list of entries arranged in a heap
    entry_finder = {}  # mapping of tasks to entries
    REMOVED = '<removed-task>'  # placeholder for a removed task
    counter = itertools.count()  # unique sequence count

    def add_task(task, priority=0):
        if task in entry_finder:
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heappush(pq, entry)


    def remove_task(task):
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED


    def pop_task():
        while pq:
            priority, count, task = heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    heat_map = [[int(n) for n in line.strip()] for line in data]

    # build an action for all possible movement
    for row in range(len(heat_map)):
        for col in range(len(heat_map[0])):
            for direction in range(len(directions.keys())):
                for consecutive in range(1, 4):
                    add_task((row, col, direction, consecutive), infinity)

    # Start with 0,0 going right
    default_task = (0, 0, 1, 0)
    add_task(default_task)
    total_heat = defaultdict(lambda: infinity)
    total_heat[default_task] = 0
    last_task = None

    while True:
        current_task = pop_task()
        row, col, direction, consecutive = current_task

        # When we arrive to the task related to end -> stop
        # we did it all
        if col == len(heat_map[0]) - 1 and row == len(heat_map) - 1:
            last_task = current_task
            break

        # neighbors = next_direction 90°
        # with a consecutive of 1
        neighbors = [((direction + 1) % 4, 1), ((direction - 1) % 4, 1)]
        # if we can go further
        if consecutive < 3:
            neighbors.append((direction, consecutive + 1))

        # iterate
        for neighbor in neighbors:
            new_direction, new_consecutive = neighbor
            new_row, new_col = row + directions[new_direction][0], col + directions[new_direction][1]
            new_task = (new_row, new_col, new_direction, new_consecutive)

            if 0 <= new_row < len(heat_map) and 0 <= new_col < len(heat_map[0]):
                new_heat = total_heat[current_task] + heat_map[new_row][new_col]
                if new_heat < total_heat[new_task]:
                    total_heat[new_task] = new_heat
                    add_task(new_task, new_heat)

    return total_heat[last_task]


def solve_part2(data):
    # https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    pq = []  # list of entries arranged in a heap
    entry_finder = {}  # mapping of tasks to entries
    REMOVED = '<removed-task>'  # placeholder for a removed task
    counter = itertools.count()  # unique sequence count

    def add_task(task, priority=0):
        if task in entry_finder:
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heappush(pq, entry)


    def remove_task(task):
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED


    def pop_task():
        while pq:
            priority, count, task = heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    heat_map = [[int(n) for n in line.strip()] for line in data]

    # build an action for all possible movement
    for row in range(len(heat_map)):
        for col in range(len(heat_map[0])):
            for direction in range(len(directions.keys())):
                for consecutive in range(1, 12):
                    add_task((row, col, direction, consecutive), infinity)

    # Start with 0,0 going right
    default_task = (0, 0, 1, 0)
    add_task(default_task)
    total_heat = defaultdict(lambda: infinity)
    total_heat[default_task] = 0
    last_task = None

    while True:
        current_task = pop_task()
        row, col, direction, consecutive = current_task

        # When we arrive to the task related to end -> stop
        # we did it all
        if col == len(heat_map[0]) - 1 and row == len(heat_map) - 1:
            last_task = current_task
            break

        # neighbors = next_direction 90°
        # with a consecutive of 1
        neighbors = []
        if consecutive > 3:
            neighbors = [((direction + 1) % 4, 1), ((direction - 1) % 4, 1)]

        # if we can go further
        if consecutive < 10 :
            neighbors.append((direction, consecutive + 1))

        # iterate
        for neighbor in neighbors:
            new_direction, new_consecutive = neighbor
            new_row, new_col = row + directions[new_direction][0], col + directions[new_direction][1]
            new_task = (new_row, new_col, new_direction, new_consecutive)

            if 0 <= new_row < len(heat_map) and 0 <= new_col < len(heat_map[0]):
                new_heat = total_heat[current_task] + heat_map[new_row][new_col]
                if new_heat < total_heat[new_task]:
                    total_heat[new_task] = new_heat
                    add_task(new_task, new_heat)

    return total_heat[last_task]


def test_part1():
    data = test_data
    result = solve(data)
    print(f'test1 is {result}')
    assert result == 102

def part1():
    data = load_data()
    result = solve(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 94


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result > 979


#test_part1()
#part1()
test_part2()
part2()
