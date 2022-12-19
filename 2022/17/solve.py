#!/usr/bin/env python

test_data = [
    '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

# Rocks
#    ####
#    
#    .#.
#    ###
#    .#.
#    
#    ..#
#    ..#
#    ###
#    
#    #
#    #
#    #
#    #
#    
#    ##
#    ##

rocks = [
    [
        [-1,0,1,2],
    ],
    [
        [0],
        [-1,0,1],
        [0],
    ],
    [
        [1],
        [1],
        [-1,0,1],
    ],
    [
        [-1],
        [-1],
        [-1],
        [-1],
    ],
    [
        [-1,0],
        [-1,0],
    ],
]

class Grid:
    def __init__(self):
        self.occupied = set()
        self.current_rock_set = None
        self.current_rock_placed = False
        self.rocks_added = 0

    @property
    def get_tower_hash(self):
        line_to_check = 50
        hash_data = [0,0,0,0,0,0,0]
        for y in range(min(0, self.height - line_to_check), self.height):
            for x in range(-3,4):
                if (x, y) in self.occupied:
                    hash_data[x] = y - self.height
        return f'{hash_data}'



    @property
    def height(self):
        max_y = 0
        if len(self.occupied):
            max_y = max(map(lambda x: x[1], self.occupied))
        return max_y

    def add_rock(self, rock):
        self.rocks_added += 1
        y_to_add = self.height + 3
        rock_set = set()
        rock_height = len(rock)
        for y in range(rock_height):
            rock_line = rock[y]
            final_y_to_add = rock_height - y + y_to_add
            for x in rock_line:
                rock_set.add((x, final_y_to_add))
        self.current_rock_set = rock_set
        self.current_rock_placed = False

    def move_current_rock(self, action):
        if action == '>':
            move_x = 1
            # Max Length
            can_move_x = max(map(lambda x: x[0] + move_x, self.current_rock_set)) <= 3
        else:
            move_x = -1
            # Max Length
            can_move_x = min(map(lambda x: x[0] + move_x, self.current_rock_set)) >= -3

        # Move
        if can_move_x:
            # Check if occupied is blocking
            can_move_x_2 = True
            for elem in self.current_rock_set:
                new_elem = (elem[0] + move_x, elem[1])
                if new_elem in self.occupied:
                    can_move_x_2 = False
                    break
            
            if can_move_x_2:
                new_set = set()
                for elem in self.current_rock_set:
                    new_elem = (elem[0] + move_x, elem[1])
                    new_set.add(new_elem)
                self.current_rock_set = new_set

        # Going down
        can_move_down = min(map(lambda x: x[1] - 1, self.current_rock_set)) > 0
        if can_move_down:
            can_move_down_2 = True
            for elem in self.current_rock_set:
                new_elem = (elem[0], elem[1] -1)
                if new_elem in self.occupied:
                    can_move_down_2 = False
                    break
            can_move_down = can_move_down_2

        if can_move_down:
            new_set = set()
            for elem in self.current_rock_set:
                new_elem = (elem[0], elem[1] -1)
                new_set.add(new_elem)
            self.current_rock_set = new_set
        else:
            for elem in self.current_rock_set:
                self.occupied.add(elem)
            self.current_rock_placed = True


def solve_part1(data, wanted_iteration):
    grid = Grid()
    actions = data[0]

    cache = {}

    rock_i = 0
    rocks_added = 0
    action_i = 0
    height_to_add = 0
    backup_height = 0
    apply_smart = False
    while rocks_added < wanted_iteration:
        rock_to_add_index = rock_i % len(rocks)
        rock_to_add = rocks[rock_to_add_index]
        grid.add_rock(rock_to_add)
        rocks_added += 1
        rock_i += 1
        if rocks_added % 100 == 0:
            print(f'added {rocks_added}')

        while not grid.current_rock_placed:
            action_index = action_i % len(actions)
            action = actions[action_index]
            grid.move_current_rock(action)
            action_i += 1

        if not apply_smart:
            if rock_i > len(rocks):
                if action_i > len(actions):
                    tower_index = grid.get_tower_hash
                    cache_index = f'{rock_to_add_index}_{action_index}_{tower_index}'
                    if cache_index in cache:
                        print(f'Do something smart at {rock_to_add_index}_{action_index}_{tower_index} {grid.height} {cache[cache_index]} {rocks_added}')
                        delta_rocks = rocks_added - cache[cache_index]['rocks']
                        print(delta_rocks)
                        factor = ((wanted_iteration -rocks_added) // delta_rocks)
                        rocks_added += factor * delta_rocks
                        backup_height = factor * (grid.height - cache[cache_index]['height'])
                        apply_smart = True
                    else:
                        cache[cache_index] = {'rocks': rocks_added, 'height': grid.height}


    print(f'{height_to_add} and backup {backup_height}')
    return grid.height + backup_height


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data, 2022)
    print(f'test1 is {result}')
    assert result == 3068


def part1():
    data = load_data()
    result = solve_part1(data, 2022)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part1(data, 1000000000000)
    print(f'test2 is {result}')
    assert result == 1514285714288


def part2():
    data = load_data()
    result = solve_part1(data, 1000000000000)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
