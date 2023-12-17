#!/usr/bin/env python

test_data = [
".|...\....",
"|.-.\.....",
".....|-...",
"........|.",
"..........",
".........\\",
"..../.\\\\..",
".-.-/..|..",
".|....-|.\\",
"..//.|....",
]


class Tile:
    def __init__(self, layout, value, row, col):
        self.layout = layout
        self.value = value
        self.row = row
        self.col = col
        self.energized = False
        self.beams = {}

    @property
    def representation(self):
        if self.value == '.':
            if self.beams.keys():
                vector = next(iter(self.beams.values()))
                if vector == (0, 1):
                    return '>'
                elif vector == (0, -1):
                    return '<'
                elif vector == (1, 0):
                    return 'v'
                elif vector == (-1, 0):
                    return '^'
                else:
                    print('WTF ?')
                    exit(0)
            else:
                return self.value
        else:
            return self.value

    def __repr__(self):
        return self.value

class Beam:
    def __init__(self, layout, cell, row_delta, col_delta, parent=None):
        self.layout = layout
        self.cells = [cell]
        self.vector = (row_delta, col_delta)
        self.parent = parent
        self.childrens = []
        self.ended = False

    @property
    def next_row(self):
        return self.vector[0] + self.cells[-1].row

    @property
    def next_col(self):
        return self.vector[1] + self.cells[-1].col

    def can_iterate(self):
        if self.ended:
            return False

        next_row = self.next_row
        next_col = self.next_col

        if next_row < 0 or next_row >= self.layout.rows:
            self.ended = True
            return False
        elif next_col < 0 or next_col >= self.layout.columns:
            self.ended = True
            return False
        else:
            return True

    def compute_new_vector(self, next_cell):
        current_row_vector = self.vector[0]
        current_col_vector = self.vector[1]

        new_vector = self.vector

        if next_cell.value == '/':
            # New vector
            if current_row_vector == 1 and current_col_vector == 0:
                new_vector = (0, -1)
            elif current_row_vector == -1 and current_col_vector == 0:
                new_vector = (0, 1)
            elif current_row_vector == 0 and current_col_vector == 1:
                new_vector = (-1, 0)
            elif current_row_vector == 0 and current_col_vector == -1:
                new_vector = (1, 0)
            else:
                print('CNjabnzhjfbazhjfbzajfza')
                exit(0)
        elif next_cell.value == '\\':
            if current_row_vector == 1 and current_col_vector == 0:
                new_vector = (0, 1)
            elif current_row_vector == -1 and current_col_vector == 0:
                new_vector = (0, -1)
            elif current_row_vector == 0 and current_col_vector == 1:
                new_vector = (1, 0)
            elif current_row_vector == 0 and current_col_vector == -1:
                new_vector = (-1, 0)
            else:
                print('dzanf,z ngezfazdaz')
                exit(0)
        elif next_cell.value == '-':
            if current_row_vector == 1 and current_col_vector == 0:
                beam = Beam(self.layout,
                            next_cell,
                            0,
                            -1,
                            self)
                self.childrens.append(beam)

                beam = Beam(self.layout,
                            next_cell,
                            0,
                            1,
                            self)
                self.childrens.append(beam)
                self.ended = True
                return None
            elif current_row_vector == -1 and current_col_vector == 0:
                beam = Beam(self.layout,
                            next_cell,
                            0,
                            -1,
                            self)
                self.childrens.append(beam)

                beam = Beam(self.layout,
                            next_cell,
                            0,
                            1,
                            self)
                self.childrens.append(beam)
                self.ended = True
                return None
            elif current_row_vector == 0 and current_col_vector == 1:
                pass
            elif current_row_vector == 0 and current_col_vector == -1:
                pass
            else:
                print('nfezjkfngzejkngezk')
                exit(0)
        elif next_cell.value == '|':
            if current_row_vector == 1 and current_col_vector == 0:
                pass
            elif current_row_vector == -1 and current_col_vector == 0:
                pass
            elif current_row_vector == 0 and current_col_vector == 1:
                beam = Beam(self.layout,
                            next_cell,
                            1,
                            0,
                            self)
                self.childrens.append(beam)

                beam = Beam(self.layout,
                            next_cell,
                            -1,
                            0,
                            self)
                self.childrens.append(beam)
                self.ended = True
                return None
            elif current_row_vector == 0 and current_col_vector == -1:
                beam = Beam(self.layout,
                            next_cell,
                            1,
                            0,
                            self)
                self.childrens.append(beam)

                beam = Beam(self.layout,
                            next_cell,
                            -1,
                            0,
                            self)
                self.childrens.append(beam)
                self.ended = True
                return None
            else:
                print('nfezjkfngzejkngezk')
                exit(0)
        return new_vector

    def iterate(self):
        next_row = self.next_row
        next_col = self.next_col
        next_cell = self.layout.matrix[next_row][next_col]

        # energized
        next_cell.energized = True
        if self not in next_cell.beams:
            next_cell.beams[self] = self.vector


        if next_cell.value == '.':
            self.cells.append(next_cell)
        else:
            new_vector = self.compute_new_vector(next_cell)
            if new_vector is not None:
                self.cells.append(next_cell)
                self.vector = new_vector
            else:
                # Split
                # new beams with parents
                for new_beam in self.childrens:
                    ok_to_add = True
                    for test_beam, test_vector in next_cell.beams.items():
                        if test_vector[0] == new_beam.vector[0] and test_vector[1] == new_beam.vector[1]:
                            ok_to_add = False
                            break
                    if ok_to_add:
                        self.layout.add_beam(new_beam)


class Layout:
    def __init__(self, data):
        self.data = data
        self.matrix = []
        self.beams = []

        for row, line in enumerate(data):
            row_data = []
            for col, value in enumerate(line):
                tile = Tile(self, value, row, col)
                row_data.append(tile)
            self.matrix.append(row_data)

    def __repr__(self):
        data = []
        for row in self.matrix:
            data.append(''.join(list(map(lambda x: x.representation, row))))
        return '\n'.join(data)

    def add_init_beam(self, row, col, vector_row, vector_col):
        cell = self.matrix[row][col]
        beam = Beam(self, cell, vector_row, vector_col)
        new_vector = beam.compute_new_vector(cell)
        beam.vector = new_vector
        self.add_beam(beam)

    def add_beam(self, beam):
        # cell energized
        cell = beam.cells[-1]
        cell.energized = True
        if beam not in cell.beams:
            cell.beams[beam] = beam.vector
        self.beams.append(beam)

    def iterate(self):
        for beam in self.beams:
            if beam.can_iterate():
                beam.iterate()

    @property
    def cache_key(self):
        data = []
        for row in self.matrix:
            data.append(''.join(list(map(lambda x: x.value, row))))
        return ''.join(data)

    @property
    def rows(self):
        return len(self.matrix)

    @property
    def columns(self):
        return len(self.matrix[0])

    @property
    def stable(self):
        result = True
        for beam in self.beams:
            if not beam.ended:
                result = False
                break
        return result



    @property
    def energized(self):
        result = 0
        for row in self.matrix:
            for tile in row:
                if tile.energized:
                    result += 1
        return result


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    layout = Layout(data)
    layout.add_init_beam(0, 0, 0, 1)
    last_energized = None
    while not layout.stable:
        layout.iterate()
        print(f"{layout.energized=}")
        print(len(layout.beams))
        if last_energized is None:
            last_energized = layout.energized
        elif last_energized != layout.energized:
            last_energized = layout.energized
    return layout.energized

def solve_part2(data):
    maximum = None

    rows = len(data)
    columns = len(data[0])

    for col in range(columns):
        # | 
        # v
        vector_row = 1
        vector_col = 0
        row = 0
        layout = Layout(data)
        layout.add_init_beam(row, col, vector_row, vector_col)
        while not layout.stable:
            layout.iterate()
        if maximum is None:
            maximum = layout.energized
            print(f"max={layout.energized}")
        elif layout.energized > maximum:
            maximum = layout.energized
            print(f"max={layout.energized}")

        # ^
        # |
        vector_row = -1
        vector_col = 0
        row = rows - 1
        layout = Layout(data)
        layout.add_init_beam(row, col, vector_row, vector_col)
        while not layout.stable:
            layout.iterate()
        if maximum is None:
            maximum = layout.energized
            print(f"max={layout.energized}")
        elif layout.energized > maximum:
            maximum = layout.energized
            print(f"max={layout.energized}")

    for row in range(rows):
        # ->
        vector_row = 0
        vector_col = 1
        col = 0
        layout = Layout(data)
        layout.add_init_beam(row, col, vector_row, vector_col)
        while not layout.stable:
            layout.iterate()
        if maximum is None:
            maximum = layout.energized
            print(f"max={layout.energized}")
        elif layout.energized > maximum:
            maximum = layout.energized
            print(f"max={layout.energized}")

        # <-
        vector_row = 0
        vector_col = -1
        col = columns-1
        layout = Layout(data)
        layout.add_init_beam(row, col, vector_row, vector_col)
        while not layout.stable:
            layout.iterate()
        if maximum is None:
            maximum = layout.energized
            print(f"max={layout.energized}")
        elif layout.energized > maximum:
            maximum = layout.energized
            print(f"max={layout.energized}")

    return maximum

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 46


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result > 120
    assert result == 6855


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 51


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
