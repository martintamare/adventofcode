#!/usr/bin/env python


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = [
        'L.LL.LL.LL',
        'LLLLLLL.LL',
        'L.L.L..L..',
        'LLLL.LL.LL',
        'L.LL.LL.LL',
        'L.LLLLL.LL',
        '..L.L.....',
        'LLLLLLLLLL',
        'L.LLLLLL.L',
        'L.LLLLL.LL',
    ]
    plan = Plan(data)
    result = get_occupied_seats(plan)
    print(f'test1 is {result}')
    assert result == 37


def test_part2():
    data = [
        'L.LL.LL.LL',
        'LLLLLLL.LL',
        'L.L.L..L..',
        'LLLL.LL.LL',
        'L.LL.LL.LL',
        'L.LLLLL.LL',
        '..L.L.....',
        'LLLLLLLLLL',
        'L.LLLLLL.L',
        'L.LLLLL.LL',
    ]
    plan = Plan(data)
    result = get_occupied_seats_2(plan)
    print(f'test2 is {result}')
    assert result == 26


def get_occupied_seats(plan):
    changes = plan.iterate()
    print(f'changes {changes}')
    while changes:
        print(f'changes {changes}')
        changes = plan.iterate()
    return plan.occupied_seats


def get_occupied_seats_2(plan):
    changes = plan.iterate2()
    print(f'changes {changes}')
    while changes:
        print(f'changes {changes}')
        changes = plan.iterate2()
    return plan.occupied_seats


class Seat:
    def __init__(self, value, row, column, plan):
        self.value = value
        self.row = row
        self.column = column
        self.plan = plan
        self.futur_value = None

    def get_neighboors(self):
        neighboors = []

        if self.row == 0:
            row_to_look = [0, 1]
        elif self.row == self.plan.rows - 1:
            row_to_look = [self.row, self.row - 1]
        else:
            row_to_look = [self.row-1, self.row, self.row+1]

        if self.column == 0:
            column_to_look = [0, 1]
        elif self.column == self.plan.columns - 1:
            column_to_look = [self.column, self.column - 1]
        else:
            column_to_look = [self.column-1, self.column, self.column+1]
        
        for row in row_to_look:
            for column in column_to_look:
                if row == self.row and column == self.column:
                    continue
                neighboors.append(self.plan.matrix[row][column])
        return neighboors

    def get_neighboors_part2(self):
        neighboors = []

        directions = [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
        ]
        for row_delta, column_delta in directions:
            neighboor = False
            start_row = self.row
            start_column = self.column
            stop = False
            while not stop:
                row = start_row + row_delta
                column = start_column + column_delta
                if row not in range(0, self.plan.rows):
                    stop = True
                    continue
                elif column not in range(0, self.plan.columns):
                    stop = True
                    continue
                neighboor = self.plan.matrix[row][column]
                if neighboor.is_occupied() or neighboor.is_empty():
                    stop = True
                    neighboors.append(neighboor)
                    continue
                start_row = row
                start_column = column
        return neighboors

    def is_floor(self):
        return self.value == '.'

    def is_empty(self):
        return self.value == 'L'

    def is_occupied(self):
        return self.value == '#'

    def occupied(self):
        self.futur_value = '#'

    def empty(self):
        self.futur_value = 'L'

    def update(self):
        if self.futur_value is not None:
            self.value = self.futur_value
            self.futur_value = None

    def __repr__(self):
        return f'Seat {self.row}:{self.column} {self.value}'


class Plan:
    def __init__(self, data):
        self.rows = len(data)
        self.columns = len(data[0])
        self.matrix = []

        for row_index in range(0, self.rows):
            row = []
            for column_index in range(0, self.columns):
                value = data[row_index][column_index]
                seat = Seat(value, row_index, column_index, self)
                row.append(seat)
            self.matrix.append(row)

    def iterate2(self):
        changes = 0
        for row_index in range(0, self.rows):
            for column_index in range(0, self.columns):
                seat = self.matrix[row_index][column_index]
                neighboors = seat.get_neighboors_part2()
                #print(f'{seat} neighboors {neighboors}')
                all_neightboors_empty = True
                adjacent_occupied = 0
                for neighboor in neighboors:
                    if neighboor.is_floor():
                        continue
                    if neighboor.is_occupied():
                        all_neightboors_empty = False
                        adjacent_occupied += 1
                if seat.is_empty() and all_neightboors_empty:
                    seat.occupied()
                    changes += 1
                elif seat.is_occupied() and adjacent_occupied > 4:
                    seat.empty()
                    changes += 1

        for row in self.matrix:
            for seat in row:
                seat.update()
        return changes

    def __repr__(self):
        data_rows = []
        for row in self.matrix:
            data_row = []
            for seat in row:
                data_row.append(seat.value)
            data_rows.append(''.join(data_row))
        return '\n'.join(data_rows)

    def iterate(self):
        changes = 0
        for row_index in range(0, self.rows):
            for column_index in range(0, self.columns):
                seat = self.matrix[row_index][column_index]
                neighboors = seat.get_neighboors()
                all_neightboors_empty = True
                adjacent_occupied = 0
                for neighboor in neighboors:
                    if neighboor.is_floor():
                        continue
                    if neighboor.is_occupied():
                        all_neightboors_empty = False
                        adjacent_occupied += 1
                if seat.is_empty() and all_neightboors_empty:
                    seat.occupied()
                    changes += 1
                elif seat.is_occupied() and adjacent_occupied > 3:
                    seat.empty()
                    changes += 1

        for row in self.matrix:
            for seat in row:
                seat.update()
        return changes

    @property
    def occupied_seats(self):
        seats = 0
        for row in self.matrix:
            for seat in row:
                if seat.is_occupied():
                    seats += 1
        return seats


def part1():
    data = load_data()
    plan = Plan(data)
    result = get_occupied_seats(plan)
    print(f'result1 is {result}')


def part2():
    data = load_data()
    plan = Plan(data)
    result = get_occupied_seats_2(plan)
    print(f'result2 is {result}')


test_part1()
#part1()
test_part2()
part2()
