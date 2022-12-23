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
        self.current_face = 0
        self.current_vector = (1,0)
        self.len_x = len_x
        self.len_y = len_y
        self.cube_length = cube_length

        # Holy crap test is not the same cube ...
        if cube_length == 4:
            self.cube_padding = [
                (2,0),
                (0,1),
                (1,1),
                (2,1),
                (2,2),
                (3,2),
            ]

        else:
            self.cube_padding = [
                (1,0),
                (2,0),
                (1,1),
                (0,2),
                (1,2),
                (0,3),
            ]
        self.cube_ranges = list(map(lambda x: (range(x[0]*cube_length, (x[0]+1)*cube_length), range(x[1]*cube_length, (x[1]+1)*cube_length)), self.cube_padding))

        for i in range(len(self.cube_ranges)):
            r = self.cube_ranges[i]
            y_range = r[1]
            x_range = r[0]
            cube_face = []
            for y in y_range:
                line = data[y]
                grid_line = []
                for x in x_range:
                    if self.current_point is None:
                        if line[x] == '.':
                            self.current_point = (x-2*self.cube_length,y)
                    grid_line.append(line[x])
                cube_face.append(grid_line)
            self.faces.append(cube_face)
        self.path = deepcopy(self.faces)


    def __str__(self):
        return self.draw(self.faces)

    def draw(self, to_print):
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
                    char = to_print[face_index][y][padded_x]
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
                    char = to_print[face_index][padded_y][padded_x]
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
                    char = to_print[face_index][padded_y][padded_x]
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
                    char = to_print[face_index][padded_y][padded_x]
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
                    char = to_print[face_index][padded_y][padded_x]
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
                    char = to_print[face_index][padded_y][padded_x]
                else:
                    char = ' '
                line.append(char)
            data.append(''.join(line))

        return '\n'.join(data)

    @property
    def paths(self):
        return self.draw(self.path)

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
            return 3

    def next_point(self):
        move_x, move_y = self.current_vector
        x, y = self.current_point
        cur_face = self.current_face
        max_index = self.cube_length - 1

        cur_x = x + move_x
        cur_y = y + move_y

        if self.cube_length == 4:
            if cur_x >= self.cube_length:
                # x+
                if cur_face == 0:
                    return ((5, (-1, 0)), (max_index, max_index-y))
                elif cur_face == 1:
                    return ((2, (1, 0)), (0, y))
                elif cur_face == 2:
                    return ((3, (1, 0)), (0, y))
                elif cur_face == 3:
                    return ((5, (0, 1)), (max_index-y, 0))
                elif cur_face == 4:
                    return ((5, (1, 0)), (0, y))
                elif cur_face == 5:
                    return ((0, (-1, 0)), (max_index, max_index-y))
            elif cur_x < 0:
                # x-
                if cur_face == 0:
                    return ((2, (0, 1)), (y, 0))
                elif cur_face == 1:
                    return ((5, (0, 1)), (max_index-y, max_index))
                elif cur_face == 2:
                    return ((1, (-1, 0)), (max_index, y))
                elif cur_face == 3:
                    return ((2, (-1, 0)), (max_index, y))
                elif cur_face == 4:
                    return ((2, (0, -1)), (max_index-y, max_index))
                elif cur_face == 5:
                    return ((4, (-1, 0)), (max_index, y))
            elif cur_y >= self.cube_length:
                # y+
                if cur_face == 0:
                    return ((3, (0, 1)), (x, 0))
                elif cur_face == 1:
                    return ((4, (0, -1)), (max_index-x, max_index))
                elif cur_face == 2:
                    return ((4, (1, 0)), (0, max_index-x))
                elif cur_face == 3:
                    return ((4, (0, 1)), (x, 0))
                elif cur_face == 4:
                    return ((1, (0, -1)), (max_index-x, max_index))
                elif cur_face == 5:
                    return ((1, (1, 0)), (0, max_index-x))
            elif cur_y < 0:
                # y-
                if cur_face == 0:
                    return ((1, (0, 1)), (max_index-x, 0))
                elif cur_face == 1:
                    return ((0, (0, 1)), (max_index-x, 0))
                elif cur_face == 2:
                    return ((0, (1, 0)), (0, x))
                elif cur_face == 3:
                    return ((0, (0, -1)), (x, max_index))
                elif cur_face == 4:
                    return ((3, (0, -1)), (x, max_index))
                elif cur_face == 5:
                    return ((3, (-1, 0)), (max_index, max_index-x))
            else:
                return ((cur_face, self.current_vector), (cur_x, cur_y))
        else:
            if cur_x >= self.cube_length:
                # x+
                if cur_face == 0:
                    return ((1, (1, 0)), (x, 0))
                elif cur_face == 1:
                    return ((4, (-1, 0)), (max_index, max_index-y))
                elif cur_face == 2:
                    return ((1, (0, -1)), (y, max_index))
                elif cur_face == 3:
                    return ((4, (1, 0)), (x, 0))
                elif cur_face == 4:
                    return ((1, (-1, 0)), (max_index, max_index-y))
                elif cur_face == 5:
                    return ((4, (0, -1)), (y, max_index))
            elif cur_x < 0:
                # x-
                if cur_face == 0:
                    return ((3, (1, 0)), (0, max_index-y))
                elif cur_face == 1:
                    return ((0, (-1, 0)), (max_index, y))
                elif cur_face == 2:
                    return ((3, (0, 1)), (y, 0))
                elif cur_face == 3:
                    return ((0, (1, 0)), (0, max_index-y))
                elif cur_face == 4:
                    return ((3, (-1, 0)), (max_index, y))
                elif cur_face == 5:
                    return ((0, (0, 1)), (y, 0))
            elif cur_y >= self.cube_length:
                # y+
                if cur_face == 0:
                    return ((2, (0, 1)), (x, 0))
                elif cur_face == 1:
                    return ((2, (-1, 0)), (max_index, x))
                elif cur_face == 2:
                    return ((4, (0, 1)), (x, 0))
                elif cur_face == 3:
                    return ((5, (0, 1)), (x, 0))
                elif cur_face == 4:
                    return ((5, (-1, 0)), (max_index, x))
                elif cur_face == 5:
                    return ((1, (0, 1)), (x ,0))
            elif cur_y < 0:
                # y-
                if cur_face == 0:
                    return ((5, (1, 0)), (0, x))
                elif cur_face == 1:
                    return ((5, (0, -1)), (x, max_index))
                elif cur_face == 2:
                    return ((0, (0, -1)), (x, max_index))
                elif cur_face == 3:
                    return ((2, (1, 0)), (0, x))
                elif cur_face == 4:
                    return ((2, (0, -1)), (x, max_index))
                elif cur_face == 5:
                    return ((3, (0, -1)), (x, max_index))
            else:
                return ((cur_face, self.current_vector), (cur_x, cur_y))


    def move(self, instruction):
        mode = instruction[0]
        data = instruction[1]
        if mode == 'move':
            for l in range(data):
                cur_x, cur_y = self.current_point
                cur_face = self.current_face
                self.path[cur_face][cur_y][cur_x] = self.current_move

                new_point = self.next_point()
                if new_point is None:
                    break
                else:
                    new_point_face, new_point_vector = new_point[0]
                    new_point_x, new_point_y = new_point[1]

                    test = self.faces[new_point_face][new_point_y][new_point_x]
                    if test == '.':
                        self.current_point = (new_point_x, new_point_y)
                        self.current_face = new_point_face
                        self.current_vector = new_point_vector
                    elif test == '#':
                        break
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
    print(grid.paths)

    result_x, result_y = grid.current_point
    face_index = grid.current_face
    x_to_pad, y_to_pad = grid.cube_padding[face_index]
    result_x += 1 + x_to_pad * cube_length
    result_y += 1 + y_to_pad * cube_length
    facing_score = grid.facing_score
    print(f'Point is at {result_x},{result_y} and facing is {facing_score}')
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
    result = solve_part2(data, 4)
    print(f'test2 is {result}')
    assert result == 5031


def part2():
    data = load_data()
    result = solve_part2(data, 50)
    print(f'part2 is {result}')
    assert result != 79247
    assert result != 119371


#test_part1()
#part1()
test_part2()
part2()
