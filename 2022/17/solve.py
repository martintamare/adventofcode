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
        [2,3,4,5],
    ],
    [
        [3],
        [2,3,4],
        [3],
    ],
    [
        [4],
        [4],
        [2,3,4],
    ],
    [
        [2],
        [2],
        [2],
        [2],
    ],
    [
        [2,3],
        [2,3],
    ],
]

class Grid:
    def __init__(self):
        self.occupied = [[True, True, True, True, True, True, True]]
        self.current_rock_set = None
        self.current_rock_placed = False
        self.rocks_added = 0

    @property
    def get_tower_hash(self):
        line_to_check = 50
        hash_data = [0,0,0,0,0,0,0]
        for y in range(max(0, self.height - line_to_check), self.height):
            for x in range(7):
                if self.occupied[y][x]:
                    hash_data[x] = y - self.height
        return f'{hash_data}'


    def print_tower(self):
        print(self)

    def print_current_rocks(self):
        for y in reversed(range(len(self.current_rock_positions))):
            line = self.current_rock_positions[y]
            print_line = []
            for x in range(len(line)):
                if line[x]:
                    print_line.append('#')
                else:
                    print_line.append(' ')
            print(print_line)

    def __repr__(self):
        return str(self)

    def __str__(self):
        data = []
        max_y = self.height - 1
        if self.current_rock_set:
            max_y = max(max_y, max(map(lambda x: x[1], self.current_rock_set)))

        for y in reversed(range(max_y+1)):
            print_line = []
            # If rocks
            if y >= len(self.occupied):
                for x in range(0, 7):
                    if (x, y) in self.current_rock_set:
                        print_line.append('@')
                    else:
                        print_line.append(' ')
            else:
                line = self.occupied[y]
                for x in range(len(line)):
                    if self.current_rock_set and (x, y) in self.current_rock_set:
                        print_line.append('@')
                    elif line[x]:
                        print_line.append('#')
                    else:
                        print_line.append(' ')
            data.append(f'{print_line}')
        return '\n'.join(data)


    @property
    def height(self):
        return len(self.occupied)

    @property
    def result(self):
        line_to_remove = 0
        for y in reversed(range(max(self.height-3,0), self.height)):
            line_to_test = self.occupied[y]
            empty_line = sum(map(lambda x: 1 if x else 0, line_to_test)) == 0
            if empty_line:
                line_to_remove += 1

        return self.height - 1 - line_to_remove


    def add_rock(self, rock):
        self.rocks_added += 1
        rock_positions = []

        # Add new_line
        line_to_add = 3
        for y in reversed(range(max(self.height-3,0), self.height)):
            line_to_test = self.occupied[y]
            empty_line = sum(map(lambda x: 1 if x else 0, line_to_test)) == 0
            if empty_line:
                line_to_add -= 1

        for y in range(line_to_add):
            rock_data = []
            for i in range(7):
                rock_data.append(False)
            self.occupied.append(rock_data)

        # Add new rock
        rock_set = set()
        rock_height = len(rock)
        for y in range(rock_height):
            rock_line = rock[y]
            final_y_to_add = rock_height - y + self.height - 1
            for x in rock_line:
                rock_set.add((x, final_y_to_add))
        self.current_rock_y = self.height - 1
        self.current_rock_set = rock_set
        self.current_rock_placed = False

    def move_current_rock(self, action):
        if action == '>':
            move_x = 1
            # Max Length
            can_move_x = max(map(lambda x: x[0] + move_x, self.current_rock_set)) <= 6
        else:
            move_x = -1
            # Max Length
            can_move_x = min(map(lambda x: x[0] + move_x, self.current_rock_set)) >= 0

        # Move
        if can_move_x:
            # Check if occupied is blocking
            can_move_x_2 = True
            for elem in self.current_rock_set:
                x = elem[0] + move_x
                y = elem[1]
                if y < len(self.occupied):
                    if x >= 0 and x < 7:
                        if self.occupied[y][x]:
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
                x = elem[0]
                y = elem[1] -1
                if y < len(self.occupied):
                    if self.occupied[y][x]:
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
            min_y = min(map(lambda x: x[1], self.current_rock_set))
            max_y = max(map(lambda x: x[1], self.current_rock_set))
            for y in range(min_y, max_y + 1):
                if y >= len(self.occupied):
                    self.occupied.append([False, False, False, False, False, False, False])

            for elem in self.current_rock_set:
                x = elem[0]
                y = elem[1]
                self.occupied[y][x] = True
            self.current_rock_placed = True


    def move_current_rock_old(self, action):

        # Jet move
        if action == '>':
            move_x = 1
            # Max Length
            test_x = list(filter(lambda x: x[6] == True, self.current_rock_positions))
            can_move_x = len(test_x) == 0
        else:
            move_x = -1
            # Max Length
            test_x = list(filter(lambda x: x[0] == True, self.current_rock_positions))
            can_move_x = len(test_x) == 0

        # If Jet move test current grid
        if can_move_x:
            # Check if occupied is blocking
            can_move_x_2 = True
            for y_delta in range(len(self.current_rock_positions)):
                line = self.current_rock_positions[y_delta]
                y = self.height - y_delta
                if y not in self.occupied:
                    continue
                for x in range(len(line)):
                    if line[x] == True:
                        if self.occupied[y][x+move_x] == True:
                            can_move_x_2 = False
                            break

                if not can_move_x_2:
                    break
            
            if can_move_x_2:
                new_positions = []
                print(f'Will move x {move_x}')
                print('before')
                self.print_current_rocks()
                for line in self.current_rock_positions:
                    new_line = []
                    for x in range(7):
                        old_char_index = x - move_x
                        old_char = False
                        if old_char_index >= 0 and old_char_index < len(line):
                            old_char = line[old_char_index]

                        new_line.append(old_char)
                    new_positions.append(new_line)
                self.current_rock_positions = new_positions
                print('after')
                self.print_current_rocks()

        # Going down
        can_move_down = True
        for y_delta in range(len(self.current_rock_positions)):
            line = self.current_rock_positions[y_delta]
            y = self.height - y_delta - 1
            print(f'testing at y={y} current height={self.height}')
            if y >= self.height:
                print('Not yet in grid')
                continue
            for x in range(len(line)):
                if line[x]:
                    print(f'testing at {y},{x}')
                    if self.occupied[y][x]:
                        can_move_down = False
                        break

            if not can_move_down:
                break
        
        if can_move_down:
            print('will move y-1')
            print('before')
            self.print_current_rocks()
            print('after')
            self.current_rock_positions.insert(0, [False, False, False, False, False, False, False])
            self.print_current_rocks()
            print('tower')
            self.print_tower()
        else:
            print('TODO')
            self.print_current_rocks()
            self.print_tower()
            for y_delta in range(len(self.current_rock_positions)):
                real_y = self.height - y_delta
                print(f'real_y={real_y}')
                if real_y > self.height - 1:
                    self.occupied.append([False, False, False, False, False, False, False])
                line_to_add = self.current_rock_positions[y_delta]
                empty_line = sum(map(lambda x: 1 if x else 0, line_to_add)) == 0
                if empty_line:
                    continue
                for x in range(len(line_to_add)):
                    if line_to_add[x]:
                        self.occupied[real_y][x] = True
            print('After')
            self.print_tower()
            self.current_rock_placed = True


def solve_part1(data, wanted_iteration, part=1):
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

        #print(f'====Tower after {rocks_added} rocks added =====')
        #grid.print_tower()
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
    return grid.result + backup_height


def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = solve_part1(data, 2022, 1)
    print(f'test1 is {result}')
    assert result == 3068


def part1():
    data = load_data()
    result = solve_part1(data, 2022, 1)
    print(f'part1 is {result}')
    assert result == 3181


def test_part2():
    data = test_data
    result = solve_part1(data, 1000000000000, 2)
    print(f'test2 is {result}')
    assert result == 1514285714288


def part2():
    data = load_data()
    result = solve_part1(data, 1000000000000, 2)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
