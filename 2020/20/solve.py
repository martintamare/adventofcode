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

test_final = [
    '.#.#..#.##...#.##..#####',
    '###....#.#....#..#......',
    '##.##.###.#.#..######...',
    '###.#####...#.#####.#..#',
    '##.#....#.##.####...#.##',
    '...########.#....#####.#',
    '....#..#...##..#.#.###..',
    '.####...#..#.....#......',
    '#..#.##..#..###.#.##....',
    '#.####..#.####.#.#.###..',
    '###.#.#...#.######.#..##',
    '#.####....##..########.#',
    '##..##.#...#...#.#.#.#..',
    '...#..#..#.#.##..###.###',
    '.#.#....#.##.#...###.##.',
    '###.#...#..#.##.######..',
    '.#.#.###.##.##.#..#.##..',
    '.####.###.#...###.#..#.#',
    '..#.#..#..#.#.#.####.###',
    '#..####...#.#.#.###.###.',
    '#####..#####...###....##',
    '#.##..#..#...#..####...#',
    '.#.###..##..##..####.##.',
    '...###...##...#...#..###',
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

        my_orientation = processed_index[self.index]
        self.set_orientation(my_orientation)

        if already_tested == total:
            for row in processed_data:
                for item in row:
                    if item is None:
                        return False
            return True

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


def compute_matrix(data, size):
    tiles = process_data(data, size=size)
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
                return processed_data


def compute_final_array(data):
    final_array = []
    for row in data:
        for r_index in range(1, len(row[0].working_matrix)-1):
            row_data = []
            for tile in row:
                for c_index in range(1, len(row[0].working_matrix)-1):
                    row_data.append(tile.working_matrix[r_index][c_index])
            final_array.append(row_data)
    return np.array(final_array)


def find_water_roughness(data):
    # Find see monsters
    orientations = []
    for rotate in [0, 90, 180, 270]:
        for flip in [0, 1]:
            orientations.append((rotate, flip))

    for rotate, flip in orientations:
        print(f'testing {rotate},{flip}')
        working_matrix = data.copy()
        k = rotate / 90
        if k:
            working_matrix = np.rot90(working_matrix, k)

        if flip == 1:
            working_matrix = np.flipud(working_matrix)

        sea = []
        for row in working_matrix:
            sea.append([1 if x == '#' else 0 for x in row])
        sea_monsters = find_sea_monsters(np.array(sea))
        if sea_monsters:
            return np.sum(sea) - len(sea_monsters)

            exit(0)


def find_sea_monsters(sea):
    pattern = [
        '..................#.',
        '#....##....##....###',
        '.#..#..#..#..#..#...',
    ]
    bool_pattern = []
    for row in pattern:
        bool_pattern.append([1 if x == '#' else 0 for x in row])
    bool_pattern = np.array(bool_pattern)

    sea_size = len(sea)
    sea_row = sea_size
    sea_col = sea_size
    pattern_col = len(pattern[0])
    pattern_row = len(pattern)

    print(f'sea : {sea_row}x{sea_col} pattern : {pattern_row}x{pattern_col}')
    pattern_sum = np.sum(bool_pattern)

    r_index = 0
    c_index = 0
    monster_present = set()
    while r_index < sea_row - pattern_row:
        while c_index < sea_col - pattern_col:
            part_of_sea = sea[r_index:r_index+pattern_row:1, c_index:c_index+pattern_col:1]
            result = np.sum((part_of_sea * bool_pattern))
            if result == pattern_sum:
                print(f'found at {r_index},{c_index}!')
                for r in range(pattern_row):
                    for c in range(pattern_col):
                        if bool_pattern[r][c]:
                            monster_present.add((r+r_index, c+c_index))
            c_index += 1
        r_index += 1
        c_index = 0

    return monster_present


def test_part1():
    data = test_data
    processed_data = compute_matrix(data, size=3)
    result = processed_data[0][0].index * processed_data[-1][0].index * processed_data[0][-1].index * processed_data[-1][-1].index
    print(f'test1 is {result}')
    assert result == 20899048083289

    final_array = []
    for row in test_final:
        row_data = []
        for char in row:
            row_data.append(char)
        final_array.append(row_data)
    test_array = np.array(final_array)
    final_array = compute_final_array(processed_data)
    assert np.array_equal(test_array, final_array)

    result = find_water_roughness(final_array)
    print(f'test water roughness is {result}')
    assert result == 273


def part1():
    data = load_data()
    processed_data = compute_matrix(data, size=12)
    result = processed_data[0][0].index * processed_data[-1][0].index * processed_data[0][-1].index * processed_data[-1][-1].index
    print(f'part1 is {result}')

    final_array = compute_final_array(processed_data)
    result = find_water_roughness(final_array)
    print(f'part2 water roughness is {result}')


test_part1()
part1()
