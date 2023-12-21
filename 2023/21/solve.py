#!/usr/bin/env python
from collections import Counter

test_data = [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........',
]


class Plot:
    def __init__(self, garden, value, row, col):
        self.garden = garden
        self.row = row
        self.col = col
        self.value = value
        self.visited = False
        self._neighbors = None
        self.gardens = set()
        current_garden = (0, 0)
        self.gardens.add(current_garden)

    @property
    def is_rock(self):
        return self.value == '#'

    @property
    def neighbors(self):
        if self._neighbors is not None:
            return self._neighbors

        result = []

        to_check = []
        # down
        row = self.row - 1
        col = self.col
        if row >= 0:
            neighbor = self.garden.matrix[row][col]
            to_check.append(neighbor)

        # up
        row = self.row + 1
        col = self.col
        if row < self.garden.rows:
            neighbor = self.garden.matrix[row][col]
            to_check.append(neighbor)

        # left
        row = self.row
        col = self.col - 1
        if col >= 0:
            neighbor = self.garden.matrix[row][col]
            to_check.append(neighbor)

        # right
        row = self.row
        col = self.col + 1
        if col < self.garden.cols:
            neighbor = self.garden.matrix[row][col]
            to_check.append(neighbor)

        for neighbor in to_check:
            if neighbor.is_rock:
                pass
            else:
                result.append(neighbor)

        self._neighbors = result
        return result


    def __repr__(self):
        if self.visited:
            return 'O'
        else:
            return f"{self.value}"

    @property
    def position(self):
        return f"{self.row},{self.col}"


class Garden:
    def __init__(self, data, version=1):
        # Build 2x2 matrix : line and cols
        self.matrix = []
        self.start = None
        self.visited = {}
        self._neighbors = {}

        initial_rows = len(data)
        initial_cols = len(data[0])

        for row, line in enumerate(data):
            matrix_row = []

            for col, char in enumerate(line):
                plot = Plot(self, char, row, col)
                matrix_row.append(plot)
                if char == 'S':
                    self.start = plot
                vector = (row, col)
                self.visited[vector] = False

            self.matrix.append(matrix_row)

    # reset
    def set_visited(self, row, col, value):
        vector = (row, col)
        self.visited[vector] = value

    # be smart about existing neighbors
    def delta_neighbors(self, wanted_vector, existing_vector):
        #print(f"{wanted_vector=} {existing_vector=}")
        wanted_row, wanted_col = wanted_vector
        ok_row, ok_col = existing_vector
        neighbors = self._neighbors[existing_vector]
        delta_row = (wanted_row // self.rows) * self.rows
        delta_col = (wanted_col // self.cols) * self.cols
        new_set = {(x+delta_row, y+delta_col) for x, y in neighbors}
        return new_set

    def get_plot(self, source_row, source_col):
        return self.matrix[source_row % self.rows][source_col % self.cols]

    # get neighbors over infinite map
    def get_neighbors(self, source_row, source_col):
        init_vector = (source_row, source_col)
        fake_vector = (source_row % self.rows, source_col % self.cols)

        if fake_vector in self._neighbors:
            if fake_vector == init_vector:
                return self._neighbors[fake_vector]
            else:
                return self.delta_neighbors(init_vector, fake_vector)

        neighbors = set()

        to_check = set()

        # down
        row = source_row - 1
        col = source_col
        vector = (row, col)
        to_check.add(vector)

        row = source_row + 1
        col = source_col
        vector = (row, col)
        to_check.add(vector)

        row = source_row
        col = source_col - 1
        vector = (row, col)
        to_check.add(vector)

        row = source_row
        col = source_col + 1
        vector = (row, col)
        to_check.add(vector)

        for row, col in to_check:
            fake_row = row % self.rows
            fake_col = col % self.cols

            neighbor = self.matrix[fake_row][fake_col]
            if not neighbor.is_rock:
                vector = (row, col)
                neighbors.add(vector)

        self._neighbors[init_vector] = neighbors
        return neighbors




    def __repr__(self):
        display = []
        for row, row_data in enumerate(self.matrix):
            line = ''
            for col, char in enumerate(row_data):
                if (row, col) in self.visited and self.visited[(row, col)]:
                    line += 'O'
                else:
                    line += char.value
            display.append(line)
        return '\n'.join(display)


    @property
    def rows(self):
        return len(self.matrix)

    @property
    def cols(self):
        return len(self.matrix[0])


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve(data, iteration):
    garden = Garden(data)

    start_row = garden.start.row
    start_col = garden.start.col

    start = (start_row, start_col, 0, 0)
    current_plots = set()
    plots_counter = {}
    current_plots.add(start)
    extra_plots = {}
    for i in range(iteration):


        # compute les voisins
        next_plots = set()

        for row, col, garden_row, garden_col in current_plots:
            current_vector = (row, col)
            garden.set_visited(row, col, False)
            plot = garden.get_plot(row, col)
            neighbors = garden.get_neighbors(row, col)
            for neighbor_row, neighbor_col in neighbors:
                init_vector = (neighbor_row, neighbor_col)
                final_row = neighbor_row % garden.rows
                final_col = neighbor_col % garden.cols
                final_vector = (final_row, final_col)

                final_garden_row = garden_row
                final_garden_col = garden_col

                if init_vector == final_vector:
                    # same garden
                    pass
                else:
                    # compute next item garden
                    #print(f"self {row=} {col=} {garden_row=} {garden_col=} {garden.rows=} {garden.cols=}")
                    #print(f"neighbor {neighbor_row=} {neighbor_col=}")
                    delta_garden_col = neighbor_col // garden.cols
                    delta_garden_row = neighbor_row // garden.rows
                    #print(f"{delta_garden_row=} {delta_garden_col=}")
                    final_garden_col += delta_garden_col
                    final_garden_row += delta_garden_row

                garden.set_visited(final_row, final_col, True)
                #print(f"final_plot {final_row=} {final_col=} {final_garden_row=} {final_garden_col=}")
                final_plot = (final_row, final_col, final_garden_row, final_garden_col)
                next_plots.add(final_plot)

        current_plots = set(next_plots)
        #print(garden)
        #print(next_plots)
        current_sum = len(next_plots)
        print(f"{i+1} {current_sum=}")


        continue
        # si voisin déjà existant mais que source extérieur
        # compter
        # si voisin déjà existant mais que pas source extérieur
        # pas compter

    return len(current_plots)
    pass


def test_part1():
    data = test_data
    result = solve(data, 6)
    print(f'test1 is {result}')
    assert result == 16


def part1():
    data = load_data()
    result = solve(data, 64)
    print(f'part1 is {result}')
    assert result == 3795


def test_part2():
    data = test_data
    to_check = {
            8: 30,
            9: 41,
            10: 50,
            11: 63,
            50: 1594,
            100: 6536,
            500: 167004,
            1000: 668697,
            5000: 16733044,
    }
    for step, wanted_result in to_check.items():
        result = solve(data, step)
        print(f'test2 at {step=} {result=} {wanted_result=}')
        assert result == wanted_result


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
#part2()
