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
                if position == self.me_position:
                    display_line.append('E')
                elif y == 0:
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
    while not stop:
        print(f'iteration {iteration}')
        new_grids = []
        for grid in grids:
            new_positions = grid.iterate()
            if end in new_positions:
                stop = True
                break
            if len(new_positions) == 1:
                grid.me_position = new_positions[0]
                new_grids.append(grid)
                caches[f'{grid}'] = 1
            else:
                for position in new_positions:
                    new_grid = deepcopy(grid)
                    new_grid.me_position = position
                    if f'{new_grid}' not in caches:
                        new_grids.append(new_grid)
                        caches[f'{new_grid}'] = 1


        grids = new_grids
        print(f'We now have {len(new_grids)} to check')
        iteration += 1
    return iteration


def solve_part2(data):
    pass


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
