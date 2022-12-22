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
            print(f'Will move {self.current_move} for {data}')
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
            print(f'Will rotate {data}')
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
            print(f'Next direction is {self.current_move}')
        print(f'Now at {self.current_point}')


def solve_part1(data):
    grid_data = []
    passphrase = None
    do_pass = False
    for line in data:
        print(f"line is '{line}'")
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


def solve_part2(data):
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
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
part1()
#test_part2()
#part2()
