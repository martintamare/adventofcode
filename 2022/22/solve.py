#!/usr/bin/env python
from copy import deepcopy

test_data = [
    '        ...#',
    '        .#..',
    '        #...',
    '        ....',
    '...#.......#',
    '........#...',
    '..#....#....',
    '..........#.',
    '        ...#....',
    '        .....#..',
    '        .#......',
    '        ......#.',
    '',
    '10R5L5R10L4R5L5',

]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.rstrip())
    return data


class Cube:
    def __init__(self, len_x, len_y, data, cube_length):
        self.faces = []
        self.current_point = None
        self.current_face = 1
        self.current_vector = (1,0)
        self.len_x = len_x
        self.len_y = len_y
        self.cube_length = cube_length
        self.cube_padding = [
            (2,0),
            (0,1),
            (1,1),
            (2,1),
            (2,2),
            (3,2),
        ]

        self.cube_ranges = [
                (range(2*cube_length, 3*cube_length), range(0*cube_length, 1*cube_length)),
                (range(0*cube_length, 1*cube_length), range(1*cube_length, 2*cube_length)),
                (range(1*cube_length, 2*cube_length), range(1*cube_length, 2*cube_length)),
                (range(2*cube_length, 3*cube_length), range(1*cube_length, 2*cube_length)),
                (range(2*cube_length, 3*cube_length), range(2*cube_length, 3*cube_length)),
                (range(3*cube_length, 4*cube_length), range(2*cube_length, 3*cube_length)),
        ]

        for r in self.cube_ranges:
            y_range = r[1]
            x_range = r[0]

            cube_face = []
            for y in y_range:
                line = data[y]
                grid_line = []
                for x in x_range:
                    if self.current_point is None:
                        if line[x] == '.':
                            self.current_point = (x,y)
                    grid_line.append(line[x])
                cube_face.append(grid_line)
            self.faces.append(cube_face)
        self.path = deepcopy(self.faces)


    def __str__(self):
        data = []
        for y in range(0, self.cube_length):
            line = []
            for x in range(0, 4*self.cube_length):
                face_index = 0
                x_to_pad, y_to_pad = self.cube_padding[face_index]

                x_to_pad = x_to_pad * self.cube_length
                x_cube_range = self.cube_ranges[face_index][0]
                if x in x_cube_range:
                    padded_x = x - x_to_pad
                    char = self.faces[face_index][y][padded_x]
                else:
                    char = ' '
                line.append(char)
            data.append(''.join(line))
        for y in range(self.cube_length, 2*self.cube_length):
            line = []
            for x in range(0, self.cube_length):
                face_index = 1
                x_to_pad, y_to_pad = self.cube_padding[face_index]

                x_to_pad = x_to_pad * self.cube_length
                y_to_pad = y_to_pad * self.cube_length

                x_cube_range = self.cube_ranges[face_index][0]

                if x in x_cube_range:
                    padded_x = x - x_to_pad
                    padded_y = y - y_to_pad
                    char = self.faces[face_index][padded_y][padded_x]
                else:
                    char = ' '
                line.append(char)
            for x in range(1*self.cube_length, 2*self.cube_length):
                face_index = 2
                x_to_pad, y_to_pad = self.cube_padding[face_index]

                x_to_pad = x_to_pad * self.cube_length
                y_to_pad = y_to_pad * self.cube_length
                x_cube_range = self.cube_ranges[face_index][0]
                if x in x_cube_range:
                    padded_x = x - x_to_pad
                    padded_y = y - y_to_pad
                    char = self.faces[face_index][padded_y][padded_x]
                else:
                    char = ' '
                line.append(char)
            for x in range(2*self.cube_length, 3*self.cube_length):
                face_index = 3
                x_to_pad, y_to_pad = self.cube_padding[face_index]

                x_to_pad = x_to_pad * self.cube_length
                y_to_pad = y_to_pad * self.cube_length
                x_cube_range = self.cube_ranges[face_index][0]
                if x in x_cube_range:
                    padded_x = x - x_to_pad
                    padded_y = y - y_to_pad
                    char = self.faces[face_index][padded_y][padded_x]
                else:
                    char = ' '
                line.append(char)
            for x in range(self.cube_length):
                line.append(' ')
            data.append(''.join(line))
        for y in range(2*self.cube_length, 3*self.cube_length):
            line = []
            for x in range(0, 2*self.cube_length):
                line.append(' ')
            for x in range(2*self.cube_length, 3*self.cube_length):
                face_index = 4
                x_to_pad, y_to_pad = self.cube_padding[face_index]

                x_to_pad = x_to_pad * self.cube_length
                y_to_pad = y_to_pad * self.cube_length
                x_cube_range = self.cube_ranges[face_index][0]
                if x in x_cube_range:
                    padded_x = x - x_to_pad
                    padded_y = y - y_to_pad
                    char = self.faces[face_index][padded_y][padded_x]
                else:
                    char = ' '
                line.append(char)
            for x in range(3*self.cube_length, 4*self.cube_length):
                face_index = 5
                x_to_pad, y_to_pad = self.cube_padding[face_index]

                x_to_pad = x_to_pad * self.cube_length
                y_to_pad = y_to_pad * self.cube_length
                x_cube_range = self.cube_ranges[face_index][0]
                if x in x_cube_range:
                    padded_x = x - x_to_pad
                    padded_y = y - y_to_pad
                    char = self.faces[face_index][padded_y][padded_x]
                else:
                    char = ' '
                line.append(char)
            data.append(''.join(line))

        return '\n'.join(data)

    @property
    def paths(self):
        data = []
        for line in self.path:
            data.append(''.join(line))
        return '\n'.join(data)

    @property
    def current_move(self):
        if self.current_vector == (1,0):
            return '>'
        elif self.current_vector == (-1,0):
            return '<'
        elif self.current_vector == (0,1):
            return 'v'
        elif self.current_vector == (0,-1):
            return '^'

    @property
    def facing_score(self):
        if self.current_vector == (1,0):
            return 0
        elif self.current_vector == (-1,0):
            return 2
        elif self.current_vector == (0,1):
            return 1
        elif self.current_vector == (0,-1):
            return 4

    def next_point(self, cur_x, cur_y):
        while True:
            move_x, move_y = self.current_vector
            cur_x = (cur_x + move_x) % self.len_x
            cur_y = (cur_y + move_y) % self.len_y
            test = self.grid[cur_y][cur_x]
            if test == ' ':
                continue
            elif test == '#':
                return None
            elif test == '.':
                return (cur_x, cur_y)


    def move(self, instruction):
        mode = instruction[0]
        data = instruction[1]
        if mode == 'move':
            for l in range(data):
                cur_x, cur_y = self.current_point
                self.path[cur_y][cur_x] = self.current_move
                move_x, move_y = self.current_vector
                test_x = (cur_x + move_x) % self.len_x
                test_y = (cur_y + move_y) % self.len_y

                test = self.grid[test_y][test_x]
                if test == '.':
                    self.current_point = (test_x, test_y)
                elif test == '#':
                    break
                elif test == ' ':
                    new_point = self.next_point(cur_x, cur_y)
                    if new_point is None:
                        break
                    else:
                        self.current_point = new_point
        else:
            if self.current_vector == (1,0):
                # '>'
                if data == 'R':
                    self.current_vector = (0,1)
                elif data == 'L':
                    self.current_vector = (0,-1)
            elif self.current_vector == (-1,0):
                # '<'
                if data == 'R':
                    self.current_vector = (0,-1)
                elif data == 'L':
                    self.current_vector = (0,1)
            elif self.current_vector == (0,1):
                # 'v'
                if data == 'R':
                    self.current_vector = (-1,0)
                elif data == 'L':
                    self.current_vector = (1,0)
            elif self.current_vector == (0,-1):
                # '^'
                if data == 'R':
                    self.current_vector = (1,0)
                elif data == 'L':
                    self.current_vector = (-1,0)


class Grid:
    def __init__(self, len_x, len_y, data):
        self.grid = []
        self.current_point = None
        self.current_vector = (1,0)
        self.len_x = len_x
        self.len_y = len_y

        for y in range(len(data)):
            line = data[y]
            grid_line = []
            for x in range(len_x):
                if y == 0:
                    if self.current_point is None:
                        if line[x] == '.':
                            self.current_point = (x,y)
                if x < len(line):
                    grid_line.append(line[x])
                else:
                    grid_line.append(' ')
            self.grid.append(grid_line)
        self.path = deepcopy(self.grid)

    def __str__(self):
        data = []
        for line in self.grid:
            data.append(''.join(line))
        return '\n'.join(data)

    @property
    def paths(self):
        data = []
        for line in self.path:
            data.append(''.join(line))
        return '\n'.join(data)

    @property
    def current_move(self):
        if self.current_vector == (1,0):
            return '>'
        elif self.current_vector == (-1,0):
            return '<'
        elif self.current_vector == (0,1):
            return 'v'
        elif self.current_vector == (0,-1):
            return '^'

    @property
    def facing_score(self):
        if self.current_vector == (1,0):
            return 0
        elif self.current_vector == (-1,0):
            return 2
        elif self.current_vector == (0,1):
            return 1
        elif self.current_vector == (0,-1):
            return 4

    def next_point(self, cur_x, cur_y):
        while True:
            move_x, move_y = self.current_vector
            cur_x = (cur_x + move_x) % self.len_x
            cur_y = (cur_y + move_y) % self.len_y
            test = self.grid[cur_y][cur_x]
            if test == ' ':
                continue
            elif test == '#':
                return None
            elif test == '.':
                return (cur_x, cur_y)


    def move(self, instruction):
        mode = instruction[0]
        data = instruction[1]
        if mode == 'move':
            for l in range(data):
                cur_x, cur_y = self.current_point
                self.path[cur_y][cur_x] = self.current_move
                move_x, move_y = self.current_vector
                test_x = (cur_x + move_x) % self.len_x
                test_y = (cur_y + move_y) % self.len_y

                test = self.grid[test_y][test_x]
                if test == '.':
                    self.current_point = (test_x, test_y)
                elif test == '#':
                    break
                elif test == ' ':
                    new_point = self.next_point(cur_x, cur_y)
                    if new_point is None:
                        break
                    else:
                        self.current_point = new_point
        else:
            if self.current_vector == (1,0):
                # '>'
                if data == 'R':
                    self.current_vector = (0,1)
                elif data == 'L':
                    self.current_vector = (0,-1)
            elif self.current_vector == (-1,0):
                # '<'
                if data == 'R':
                    self.current_vector = (0,-1)
                elif data == 'L':
                    self.current_vector = (0,1)
            elif self.current_vector == (0,1):
                # 'v'
                if data == 'R':
                    self.current_vector = (-1,0)
                elif data == 'L':
                    self.current_vector = (1,0)
            elif self.current_vector == (0,-1):
                # '^'
                if data == 'R':
                    self.current_vector = (1,0)
                elif data == 'L':
                    self.current_vector = (-1,0)


def solve_part1(data):
    grid_data = []
    passphrase = None
    do_pass = False
    for line in data:
        if not line:
            do_pass = True
        elif do_pass:
            passphrase = line
        else:
            grid_data.append(line)

    grid_x = max(map(lambda x: len(x), grid_data))
    grid_y = len(grid_data)
    grid = Grid(grid_x, grid_y, grid_data)

    instructions = []
    current_instruction = ''
    current_mode = 'int'
    
    index = 0
    while True:
        if index >= len(passphrase):
            instructions.append(('move', int(current_instruction)))
            break

        char = passphrase[index]
        try:
            int(char)
            current_instruction += char
            index += 1
        except ValueError:
            current_instruction = int(current_instruction)
            instructions.append(('move', current_instruction))
            instructions.append(('rotate', char))
            index += 1
            current_instruction = ''

    for instruction in instructions:
        grid.move(instruction)

    result_x, result_y = grid.current_point
    result_x += 1
    result_y += 1
    facing_score = grid.facing_score
    return 1000 * result_y + 4 * result_x + facing_score


def solve_part2(data, cube_length=4):
    grid_data = []
    passphrase = None
    do_pass = False
    for line in data:
        if not line:
            do_pass = True
        elif do_pass:
            passphrase = line
        else:
            grid_data.append(line)

    grid_x = max(map(lambda x: len(x), grid_data))
    grid_y = len(grid_data)
    grid = Cube(grid_x, grid_y, grid_data, cube_length)
    print(grid)
    exit(0)

    instructions = []
    current_instruction = ''
    current_mode = 'int'
    
    index = 0
    while True:
        if index >= len(passphrase):
            instructions.append(('move', int(current_instruction)))
            break

        char = passphrase[index]
        try:
            int(char)
            current_instruction += char
            index += 1
        except ValueError:
            current_instruction = int(current_instruction)
            instructions.append(('move', current_instruction))
            instructions.append(('rotate', char))
            index += 1
            current_instruction = ''

    for instruction in instructions:
        grid.move(instruction)

    result_x, result_y = grid.current_point
    result_x += 1
    result_y += 1
    facing_score = grid.facing_score
    return 1000 * result_y + 4 * result_x + facing_score
    pass


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 6032


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result < 48312


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 5031


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
#part2()
