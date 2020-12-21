#!/usr/bin/env python
import numpy as np

test_data = [
    'Tile 2311:',
    '..##.#..#.',
    '##..#.....',
    '#...##..#.',
    '####.#...#',
    '##.##.###.',
    '##...#.###',
    '.#.#.#..##',
    '..#....#..',
    '###...#.#.',
    '..###..###',
    '',
    'Tile 1951:',
    '#.##...##.',
    '#.####...#',
    '.....#..##',
    '#...######',
    '.##.#....#',
    '.###.#####',
    '###.##.##.',
    '.###....#.',
    '..#.#..#.#',
    '#...##.#..',
    '',
    'Tile 1171:',
    '####...##.',
    '#..##.#..#',
    '##.#..#.#.',
    '.###.####.',
    '..###.####',
    '.##....##.',
    '.#...####.',
    '#.##.####.',
    '####..#...',
    '.....##...',
    '',
    'Tile 1427:',
    '###.##.#..',
    '.#..#.##..',
    '.#.##.#..#',
    '#.#.#.##.#',
    '....#...##',
    '...##..##.',
    '...#.#####',
    '.#.####.#.',
    '..#..###.#',
    '..##.#..#.',
    '',
    'Tile 1489:',
    '##.#.#....',
    '..##...#..',
    '.##..##...',
    '..#...#...',
    '#####...#.',
    '#..#.#.#.#',
    '...#.#.#..',
    '##.#...##.',
    '..##.##.##',
    '###.##.#..',
    '',
    'Tile 2473:',
    '#....####.',
    '#..#.##...',
    '#.##..#...',
    '######.#.#',
    '.#...#.#.#',
    '.#########',
    '.###.#..#.',
    '########.#',
    '##...##.#.',
    '..###.#.#.',
    '',
    'Tile 2971:',
    '..#.#....#',
    '#...###...',
    '#.#.###...',
    '##.##..#..',
    '.#####..##',
    '.#..####.#',
    '#..#.#..#.',
    '..####.###',
    '..#.#.###.',
    '...#.#.#.#',
    '',
    'Tile 2729:',
    '...#.#.#.#',
    '####.#....',
    '..#.#.....',
    '....#..#.#',
    '.##..##.#.',
    '.#.####...',
    '####.#.#..',
    '##.####...',
    '##..#.##..',
    '#.##...##.',
    '',
    'Tile 3079:',
    '#.#.#####.',
    '.#..######',
    '..#.......',
    '######....',
    '####.#..#.',
    '.#...#.##.',
    '#.#####.##',
    '..#.###...',
    '..#.......',
    '..#.###...',
    '',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Tile:
    def __init__(self, index, data, tiles, size):
        self.index = index
        self.matrix = []
        self.tiles = tiles
        self.size = size
        matrix = []
        for row in data:
            row_data = []
            for char in row:
                row_data.append(char)
            matrix.append(row_data)
        self.matrix = np.array(matrix)
        self.working_matrix = None

    def print_matrix(self):
        for row in self.matrix:
            print(''.join(row))

    def print_working_matrix(self):
        for row in self.working_matrix:
            print(''.join(row))

    def is_valid(self, row, column, processed_data, processed_index):
        next_row, next_column = self.compute_next_position(row, column)
        must_match = self.what_should_i_inspect(row, column, next_row, next_column)
        already_tested = len(processed_index)
        total = len(self.tiles.keys())

        if already_tested == total:
            for row in processed_data:
                for item in row:
                    if item is None:
                        return False
            return True

        my_orientation = processed_index[self.index]
        self.set_orientation(my_orientation)

        candidates_with_orientation = self.find_possible_neighboors(must_match, processed_data, processed_index, next_row, next_column)

        is_ok = False
        for candidate, orientation in candidates_with_orientation:
            processed_data_copy = processed_data.copy()
            processed_index_copy = dict(processed_index)
            processed_data_copy[next_row][next_column] = candidate
            processed_index_copy[candidate.index] = orientation
            if candidate.is_valid(next_row, next_column, processed_data_copy, processed_index_copy):
                is_ok = True
                break
        if is_ok:
            return True
        else:
            return False

    def what_should_i_inspect(self, r, c, next_r, next_c):
        # Same line -> only right
        if r == next_r:
            if r == 0:
                return ['left']
            elif next_c == 0:
                return ['up']
            else:
                return ['up', 'left']
        else:
            if next_c == 0:
                return ['up']
            else:
                return ['up', 'left']

    def __repr__(self):
        return f'Tile {self.index}'

    @classmethod
    def orientations(cls):
        # 0, 90, 180, 270
        # flip or not
        orientations = []
        for rotate in [0, 90, 180, 270]:
            for flip in [0, 1]:
                orientations.append((rotate, flip))
        return orientations

    def set_orientation(self, orientation):
        rotate, flip = orientation
        k = rotate / 90
        if not k:
            working_matrix = self.matrix
        else:
            working_matrix = np.rot90(self.matrix, k)

        if flip == 0:
            self.working_matrix = working_matrix
        elif flip == 1:
            self.working_matrix = np.flipud(working_matrix)

    def match_left(self, processed_data, row, column, orientation):
        length = len(self.matrix)
        self.set_orientation(orientation)
        is_valid = True
        actual_tile = processed_data[row][column-1]
        for index in range(length):
            if self.working_matrix[index][0] != actual_tile.working_matrix[index][-1]:
                is_valid = False
                break
        return is_valid

    def match_up(self, processed_data, row, column, orientation):
        length = len(self.matrix)
        self.set_orientation(orientation)
        is_valid = True
        actual_tile = processed_data[row-1][column]
        for index in range(length):
            if self.working_matrix[0][index] != actual_tile.working_matrix[-1][index]:
                is_valid = False
                break
        return is_valid

    def find_possible_neighboors(self, must_match, processed_data, processed_index, row, column):
        candidates_with_orientation = []
        for index in self.tiles.keys():
            if index in processed_index:
                continue
            test_tile = self.tiles[index]
            for orientation in test_tile.orientations():
                is_matching = True
                for match in must_match:
                    if match == 'left':
                        if not test_tile.match_left(processed_data, row, column, orientation):
                            is_matching = False
                            break
                    elif match == 'up':
                        if not test_tile.match_up(processed_data, row, column, orientation):
                            is_matching = False
                            break

                if is_matching:
                    candidates_with_orientation.append((test_tile, orientation))
        return candidates_with_orientation

    def compute_next_position(self, row, column):
        next_column = (column + 1) % self.size
        next_row = row
        if next_column == 0:
            next_row = row + 1
        return next_row, next_column


def process_data(data, size):
    tile_index = None
    tile_data = []
    tiles = {}
    for line in data:
        if line.startswith('Tile'):
            tile_index = int(line.split(' ')[1].split(':')[0])
        elif line:
            tile_data.append(line)
        else:
            tile = Tile(tile_index, tile_data, tiles, size)
            tiles[tile_index] = tile
            tile_data = []
            tile_index = None
    return tiles


def compute_corner_tilt(data, size):
    tiles = process_data(data, size=size)
    print(tiles)
    assert len(tiles.keys()) == size * size

    for index in tiles.keys():
        tile = tiles[index]

        for orientation in tile.orientations():
            row = 0
            column = 0
            processed_data = [[None for i in range(size)] for j in range(size)]
            processed_data[row][column] = tile
            processed_index = {tile.index: orientation}

            if tile.is_valid(row, column, processed_data, processed_index):
                for row in processed_data:
                    print(row)
                return processed_data[0][0].index * processed_data[-1][0].index * processed_data[0][-1].index * processed_data[-1][-1].index


def test_part1():
    data = test_data
    result = compute_corner_tilt(data, size=3)
    print(f'test1 is {result}')
    assert result == 20899048083289


def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = load_data()
    result = compute_corner_tilt(data, size=12)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = None
    print(f'part2 is {result}')


test_part1()
part1()
#test_part3()
#part2()
