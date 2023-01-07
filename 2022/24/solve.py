#!/usr/bin/env python
from collections import Counter
from copy import deepcopy

test_data = [
    '#.#####',
    '#.....#',
    '#>....#',
    '#.....#',
    '#...v.#',
    '#.....#',
    '#####.#',
]

test_data_2 = [
    '#.######',
    '#>>.<^<#',
    '#.<..<<#',
    '#>v.><>#',
    '#<^v^^>#',
    '######.#',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


blizzard_mapping = {
    '>': (1,0),
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1,0),
}

vector_mapping = {
    (1,0): '>',
    (-1,0): '<',
    (0,1): 'v',
    (0,-1): '^',
}


class Grid:
    def __init__(self, data):
        self.data = data
        self.blizzards = []
        self.blizzard_positions = set()
        self.start_position = None
        self.end_position = None
        self.x_length = len(data[0])
        self.y_length = len(data)

        for y in range(len(data)):
            line = data[y]
            for x in range(len(line)):
                if x == 0 or x == len(line) - 1:
                    continue
                if y == 0:
                    if line[x] == '.':
                        self.start_position = (x,y)
                elif y == len(data) - 1:
                    if line[x] == '.':
                        self.end_position = (x,y)
                else:
                    blizzard = line[x]
                    if blizzard in blizzard_mapping:
                        vector = blizzard_mapping[blizzard]
                        position = (x,y)
                        self.blizzards.append((position, vector))
                        self.blizzard_positions.add(position)
        self.me_position = self.start_position

    def get_possible_move_start(self, me_position):
        possible_moves = set()
        for vector in [(1,0), (-1,0), (0, 1), (0, -1)]:
            x_me, y_me = me_position
            x_delta, y_delta = vector
            x_me += x_delta
            y_me += y_delta
            new_position = (x_me, y_me)
            if new_position == self.start_position:
                return [new_position]
            elif new_position == self.end_position:
                possible_moves.add(new_position)
            elif x_me <= 0:
                continue
            elif x_me >= self.x_length - 1:
                continue
            elif y_me <= 0:
                continue
            elif y_me >= self.y_length - 1:
                continue
            elif new_position in self.blizzard_positions:
                continue
            else:
                possible_moves.add(new_position)
        if me_position not in self.blizzard_positions:
            possible_moves.add(me_position)

        return possible_moves

    def get_possible_move(self, me_position):
        possible_moves = set()
        for vector in [(1,0), (-1,0), (0, 1), (0, -1)]:
            x_me, y_me = me_position
            x_delta, y_delta = vector
            x_me += x_delta
            y_me += y_delta
            new_position = (x_me, y_me)
            if new_position == self.end_position:
                return [new_position]
            elif new_position == self.start_position:
                possible_moves.add(new_position)
            elif x_me <= 0:
                continue
            elif x_me >= self.x_length - 1:
                continue
            elif y_me <= 0:
                continue
            elif y_me >= self.y_length - 1:
                continue
            elif new_position in self.blizzard_positions:
                continue
            else:
                possible_moves.add(new_position)
        if me_position not in self.blizzard_positions:
            possible_moves.add(me_position)

        return possible_moves

    def iterate(self):
        new_blizzards = []
        new_positions = set()
        for item in self.blizzards:
            blizzard, vector = item
            x, y = blizzard
            x_delta, y_delta = vector
            x += x_delta
            y += y_delta

            if x == 0:
                x = self.x_length - 2
            elif x == self.x_length - 1:
                x = 1
            elif y == 0:
                y = self.y_length - 2
            elif y == self.y_length - 1:
                y = 1

            new_position = (x,y)
            new_blizzards.append((new_position, vector))
            new_positions.add(new_position)
        self.blizzards = new_blizzards
        self.blizzard_positions = new_positions
        return

        possible_moves = []
        for vector in [(1,0), (-1,0), (0, 1), (0, -1)]:
            x_me, y_me = self.me_position
            x_delta, y_delta = vector
            x_me += x_delta
            y_me += y_delta
            new_position = (x_me, y_me)
            if new_position == self.end_position:
                possible_moves = [new_position]
                break
            elif new_position == self.start_position:
                possible_moves.append(new_position)
            elif x_me <= 0:
                continue
            elif x_me >= self.x_length - 1:
                continue
            elif y_me <= 0:
                continue
            elif y_me >= self.y_length - 1:
                continue
            elif new_position in self.blizzard_positions:
                continue
            else:
                possible_moves.append(new_position)
        if self.me_position not in self.blizzard_positions:
            possible_moves.append(self.me_position)

        return possible_moves

        print(f'I can move to {possible_moves}')
        # Compute distance to end using manha
        new_move = None
        min_distance = None
        x,y = self.end_position
        for position in possible_moves:
            x1, y1 = position
            distance = abs(x1-x) + abs(y1-y)
            if min_distance is None:
                min_distance = distance
                new_move = position
                print(f'New move {new_move} because distance={min_distance}')
            elif distance < min_distance:
                new_move = position
                min_distance = distance
                print(f'New move {new_move} because distance={min_distance}')
            elif distance == min_distance:
                print(f'Tie between {new_move} and {position}')
                new_move = position
                min_distance = distance
        print(f'Will choose {new_move}')
        self.me_position = new_move


    def __str__(self):
        display = []
        positions = Counter(map(lambda x: x[0], self.blizzards))
        for y in range(self.y_length):
            line = self.data[y]
            display_line = []
            for x in range(self.x_length):
                position = (x, y)
                if y == 0:
                    display_line.append(line[x])
                elif y == self.y_length - 1:
                    display_line.append(line[x])
                elif x == 0:
                    display_line.append(line[x])
                elif x == self.x_length - 1:
                    display_line.append(line[x])
                else:
                    if position in positions:
                        number = positions[position]
                        if number > 1:
                            to_display = f'{number}'
                        else:
                            vector = None
                            for blizzard in self.blizzards:
                                test_position, test_vector = blizzard
                                if position == test_position:
                                    vector = test_vector
                                    break
                            if vector is None:
                                print('fnzajfnzajkfnazkjfnka')
                                exit(0)
                            else:
                                to_display = vector_mapping[vector]
                        display_line.append(to_display)
                    else:
                        display_line.append('.')
            display.append(''.join(display_line))
        return '\n'.join(display)



def solve_part1(data):
    grid = Grid(data)
    end = grid.end_position
    iteration = 0
    grids = [grid]
    caches = {}

    stop = False
    print('Building cache')
    while not stop:
        print(f'iteration {iteration}')
        iteration += 1
        grid.iterate()
        new_grid = deepcopy(grid)
        grid_str = f'{grid}'
        if grid_str in caches:
            stop = True
        else:
            caches[grid_str] = 1
            grids.append(new_grid)

    number_of_grids = len(grids)
    print(f'We build {number_of_grids} grids')

    iteration = 0
    stop = False
    positions_to_test = {}
    positions_to_test[0] = set()
    positions_to_test[0].add(grid.start_position)
    positions_tested = {}

    while not stop:
        print(f'iteration {iteration}')
        index = iteration % number_of_grids
        current_grid = grids[index]
        next_index = (iteration + 1) % number_of_grids
        print(f'index={index} next={next_index}')

        to_test_next = set()
        for position in positions_to_test[index]:
            current_grid.me_position = position
            if index in positions_tested:
                if position in positions_tested[index]:
                    continue

            can_move_to = current_grid.get_possible_move(position)
            if grid.end_position in can_move_to:
                print('EXITTTTTTTTTTTTTTT')
                return iteration
            if index in positions_tested:
                positions_tested[index].add(position)
            else:
                positions_tested[index] = set()
                positions_tested[index].add(position)
            for t in can_move_to:
                to_test_next.add(t)

        positions_to_test[next_index] = to_test_next
        positions_to_test[index] = set()
        iteration += 1
    return iteration


def solve_part2(data):
    grid = Grid(data)
    end = grid.end_position
    iteration = 0
    grids = [grid]
    caches = {}

    stop = False
    print('Building cache')
    while not stop:
        print(f'iteration {iteration}')
        iteration += 1
        grid.iterate()
        new_grid = deepcopy(grid)
        grid_str = f'{grid}'
        if grid_str in caches:
            stop = True
        else:
            caches[grid_str] = 1
            grids.append(new_grid)

    number_of_grids = len(grids)
    print(f'We build {number_of_grids} grids')

    iteration = 0
    first_trip = 0
    second_trip = 0
    last_trip = 0

    positions_to_test = {}
    positions_to_test[0] = set()
    positions_to_test[0].add(grid.start_position)
    positions_tested = {}

    stop = False
    while not stop:
        index = iteration % number_of_grids
        current_grid = grids[index]
        next_index = (iteration + 1) % number_of_grids
        print(f'index={index} next={next_index}')

        to_test_next = set()
        for position in positions_to_test[index]:
            current_grid.me_position = position
            #if index in positions_tested:
            #    if position in positions_tested[index]:
            #        continue

            can_move_to = current_grid.get_possible_move(position)
            if grid.end_position in can_move_to:
                print(f'End reach at {iteration} index={index} next={next_index}')
                first_trip = iteration
                stop = True
                break
            if index in positions_tested:
                positions_tested[index].add(position)
            else:
                positions_tested[index] = set()
                positions_tested[index].add(position)
            for t in can_move_to:
                to_test_next.add(t)

        if stop:
            iteration += 1
            break

        positions_to_test[next_index] = to_test_next
        positions_to_test[index] = set()
        iteration += 1

    index = iteration % number_of_grids

    positions_to_test = {}
    positions_to_test[index] = set()
    positions_to_test[index].add(grid.end_position)
    positions_tested = {}

    stop = False
    while not stop:
        index = iteration % number_of_grids
        next_index = (iteration + 1) % number_of_grids
        print(f'index={index} next={next_index}')
        current_grid = grids[index]
        to_test_next = set()
        for position in positions_to_test[index]:
            current_grid.me_position = position
            if index in positions_tested:
                if position in positions_tested[index]:
                    continue

            can_move_to = current_grid.get_possible_move_start(position)
            if grid.start_position in can_move_to:
                print(f'Start reach at {iteration} index={index} next={next_index}')
                second_trip = iteration
                stop = True
                break
            if index in positions_tested:
                positions_tested[index].add(position)
            else:
                positions_tested[index] = set()
                positions_tested[index].add(position)
            for t in can_move_to:
                to_test_next.add(t)

        if stop:
            iteration += 1
            break

        positions_to_test[next_index] = to_test_next
        positions_to_test[index] = set()
        iteration += 1

    second_time = second_trip - first_trip
    positions_to_test = {}

    index = iteration % number_of_grids
    positions_to_test[index] = set()
    positions_to_test[index].add(grid.start_position)
    positions_tested = {}

    stop = False
    while not stop:
        index = iteration % number_of_grids
        current_grid = grids[index]
        next_index = (iteration + 1) % number_of_grids
        print(f'index={index} next={next_index}')

        to_test_next = set()
        for position in positions_to_test[index]:
            current_grid.me_position = position
            if index in positions_tested:
                if position in positions_tested[index]:
                    continue

            can_move_to = current_grid.get_possible_move(position)
            if grid.end_position in can_move_to:
                print(f'End2 reach at {iteration}')
                last_trip = iteration
                stop = True
                break
            if index in positions_tested:
                positions_tested[index].add(position)
            else:
                positions_tested[index] = set()
                positions_tested[index].add(position)
            for t in can_move_to:
                to_test_next.add(t)

        if stop:
            break

        positions_to_test[next_index] = to_test_next
        positions_to_test[index] = set()
        iteration += 1

    last_time = last_trip - second_trip
    print(f'First {first_trip} second {second_time} last {last_time}')
    return first_trip + second_time + last_time




def test_part1():
    data = test_data_2
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 18


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data_2
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 54


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result > 733


test_part1()
#part1()
test_part2()
part2()
