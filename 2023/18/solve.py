#!/usr/bin/env python
test_data = [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Direction:
    def __init__(self, direction, amount):
        self.direction = direction
        self.amount = amount
        self.next = None
        self.previous = None

    def __repr__(self):
        return f"{self.direction} {self.amount}"


class Terrain:
    def __init__(self):
        self.matrix = {}
        self.array = []

    def add_trench(self, row, col, direction):
        if row not in self.matrix:
            self.matrix[row] = {}
        self.matrix[row][col] = direction

    def smart_count(self):
        min_row = self.min_row
        max_row = self.max_row
        min_col = self.min_col
        max_col = self.max_col

        count = 0
        row = min_row
        col = min_col
        total_count = 0
        state = 'out'
        cols = sorted(self.matrix[row].keys())
        while True:
            if row in self.matrix:
                if col in self.matrix[row]:
                    obj = self.matrix[row][col]
                    direction = obj.direction
                    _previous = obj.previous
                    _next = obj.next
                    amount = obj.amount

                    if direction in ['R', 'L']:
                        #print(f"RL {col=} count + {amount}")
                        count += amount
                        col += amount
                        if _previous.direction != _next.direction:
                            if state == 'out':
                                state = 'in'
                            else:
                                state = 'out'

                    elif direction in ['U', 'D']:
                        if state == 'out':
                            #print(f"UD {col=} count + 1 {state=}->in")
                            state = 'in'
                            count += 1
                        elif state == 'in':
                            #print(f"UD {col=} count + 0 {state=}->out")
                            state = 'out'
                            count += 1
                        col += 1
                else:
                    old_col = col
                    for next_col in cols:
                        if col > next_col:
                            continue
                        if state == 'in':
                            #print(f"{col=} {next_col=} {previous_col=} {cols=}")
                            #print(f"count + {next_col - col}")
                            count += next_col - col
                        col = next_col
                        break
                    if old_col == col:
                        col = max_col + 1
            if col > max_col:
                #self.print_row(row)
                row % 10000 == 0 and print(f"{row=} {count=}")
                total_count += count
                count = 0
                row += 1
                if row > max_row:
                    break
                col = min_col
                cols = sorted(self.matrix[row].keys())
                state = 'out'

        return total_count
        exit(0)

    def print_row(self, row):
        line = ''
        for col in range(self.min_col, self.max_col+1):
            if row in self.matrix:
                if col in self.matrix[row]:
                    line += '#'
                else:
                    line += '.'
            else:
                line += '.'
        print("============")
        print(line)
        print("============")

    @property
    def min_row(self):
        return min(self.matrix.keys())

    @property
    def max_row(self):
        return max(self.matrix.keys())

    @property
    def min_col(self):
        min_col = None
        max_col = None
        for row, col_data in self.matrix.items():
            test_min_col = min(col_data.keys())
            test_max_col = max(col_data.keys())
            if min_col is None:
                min_col = test_min_col
            elif test_min_col < min_col:
                min_col = test_min_col
            if max_col is None:
                max_col = test_max_col
            elif test_max_col > max_col:
                max_col = test_max_col
        return min_col

    @property
    def max_col(self):
        min_col = None
        max_col = None
        for row, col_data in self.matrix.items():
            test_min_col = min(col_data.keys())
            test_max_col = max(col_data.keys())
            if min_col is None:
                min_col = test_min_col
            elif test_min_col < min_col:
                min_col = test_min_col
            if max_col is None:
                max_col = test_max_col
            elif test_max_col > max_col:
                max_col = test_max_col
        return max_col

    def __repr__(self):
        lines = []
        for row in range(self.min_row, self.max_row+1):
            line = ''
            for col in range(self.min_col, self.max_col+1):
                if row in self.matrix:
                    if col in self.matrix[row]:
                        line += '#'
                    else:
                        line += '.'
                else:
                    line += '.'
            lines.append(line)

        return '\n'.join(lines)


def solve_part1(data):

    terrain = Terrain()

    current_row = None
    current_col = None

    start_direction = None
    previous_direction = None
    for instruction in data:
        direction, amount, color = instruction.split(' ')
        amount = int(amount)
        if direction == 'R':
            delta_row = 0
            delta_col = 1
        elif direction == 'L':
            delta_row = 0
            delta_col = -1
        elif direction == 'U':
            delta_row = -1
            delta_col = 0
        elif direction == 'D':
            delta_row = 1
            delta_col = 0
        else:
            print('WTF')
            exit(0)

        obj = Direction(direction, amount)

        for a in range(amount):
            if current_row is None:
                current_row = delta_row
                current_col = delta_col
            else:
                test_row = current_row + delta_row
                test_col = current_col + delta_col
                current_row = test_row
                current_col = test_col
            terrain.add_trench(current_row, current_col, obj)
        if start_direction is None:
            start_direction = obj
        if previous_direction is None:
            previous_direction = obj
        else:
            previous_direction.next = obj
            obj.previous = previous_direction
            previous_direction = obj

    previous_direction.next = start_direction
    start_direction.previous = previous_direction

    return terrain.smart_count()


def solve_part2(data):
    terrain = Terrain()

    current_row = None
    current_col = None

    mapping_direction = {
        0: 'R',
        1: 'D',
        2: 'L',
        3: 'U',
    }

    start_direction = None
    previous_direction = None
    total_instructions = len(data)
    index = 1
    for instruction in data:
        print(f"loading {index}/{total_instructions}")
        index += 1

        direction, amount, color = instruction.split(' ')
        amount = int(color[2:7], 16)
        real_direction = int(color[-2])
        if real_direction not in mapping_direction:
            print('njfkgezngkjzengkez')
            exit(0)
        direction = mapping_direction[real_direction]

        if direction == 'R':
            delta_row = 0
            delta_col = 1
        elif direction == 'L':
            delta_row = 0
            delta_col = -1
        elif direction == 'U':
            delta_row = -1
            delta_col = 0
        elif direction == 'D':
            delta_row = 1
            delta_col = 0

        obj = Direction(direction, amount)

        for a in range(amount):
            if current_row is None:
                current_row = delta_row
                current_col = delta_col
            else:
                test_row = current_row + delta_row
                test_col = current_col + delta_col
                current_row = test_row
                current_col = test_col
            terrain.add_trench(current_row, current_col, obj)

        if start_direction is None:
            start_direction = obj
        if previous_direction is None:
            previous_direction = obj
        else:
            previous_direction.next = obj
            obj.previous = previous_direction
            previous_direction = obj

    previous_direction.next = start_direction
    start_direction.previous = previous_direction

    print("smart way !")

    return terrain.smart_count()


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 62


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 33491


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 952408144115


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
