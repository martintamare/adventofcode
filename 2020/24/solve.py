#!/usr/bin/env python
import collections

test_data = [
    'sesenwnenenewseeswwswswwnenewsewsw',
    'neeenesenwnwwswnenewnwwsewnenwseswesw',
    'seswneswswsenwwnwse',
    'nwnwneseeswswnenewneswwnewseswneseene',
    'swweswneswnenwsewnwneneseenw',
    'eesenwseswswnenwswnwnwsewwnwsene',
    'sewnenenenesenwsewnenwwwse',
    'wenwwweseeeweswwwnwwe',
    'wsweesenenewnwwnwsenewsenwwsesesenwne',
    'neeswseenwwswnwswswnw',
    'nenwswwsewswnenenewsenwsenwnesesenew',
    'enewnwewneswsewnwswenweswnenwsenwsw',
    'sweneswneswneneenwnewenewwneswswnese',
    'swwesenesewenwneswnwwneseswwne',
    'enesenwswwswneneswsenwnewswseenwsese',
    'wnwnesenesenenwwnenwsewesewsesesew',
    'nenewswnwewswnenesenwnesewesw',
    'eneswnwswnwsenenwnwnwwseeswneewsenese',
    'neswnwewnwnwseenwseesewsenwsweewe',
    'wseweeenwnesenwwwswnew',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Floor:
    def __init__(self, data):
        self.data = data
        self.tiles = collections.defaultdict(int)

    def setup(self):
        vectors = {
            'w': (-1, 0),
            'sw': (0, -1),
            'se': (1, -1),
            'e': (1, 0),
            'ne': (0, 1),
            'nw': (-1, 1),
        }

        for line in self.data:
            vector = (0, 0)

            while len(line):
                direction = None
                for test_direction in ['e', 'se', 'sw', 'w', 'nw', 'ne']:
                    if line.startswith(test_direction):
                        direction = test_direction
                        break
                vector_to_add = vectors[direction]
                vector = (vector[0] + vector_to_add[0], vector[1] + vector_to_add[1])
                line = line[len(direction):]

            self.tiles[vector] = (self.tiles[vector] + 1) % 2

        new_tiles = []
        for index, tile in self.tiles.items():
            vectors = [
                (-1, 0),
                (0, -1),
                (1, -1),
                (1, 0),
                (0, 1),
                (-1, 1),
            ]

            for vector in vectors:
                test_index = (index[0] + vector[0], index[1] + vector[1])
                if test_index not in self.tiles:
                    new_tiles.append(test_index)

        for vector in new_tiles:
            self.tiles[vector] = 0

    @property
    def black_tiles(self):
        return sum(filter(lambda x: x == 1, self.tiles.values()))

    def iterate(self):
        neighboors = collections.defaultdict(int)
        new_tiles = []

        for index, tile in self.tiles.items():
            vectors = [
                (-1, 0),
                (0, -1),
                (1, -1),
                (1, 0),
                (0, 1),
                (-1, 1),
            ]

            for vector in vectors:
                test_index = (index[0] + vector[0], index[1] + vector[1])
                if test_index in self.tiles:
                    neighboors[index] += self.tiles[test_index]
                else:
                    new_tiles.append(test_index)

        for vector in new_tiles:
            self.tiles[vector] = 0

        for index, tile in self.tiles.items():
            if tile == 1:
                if neighboors[index] == 0 or neighboors[index] > 2:
                    self.tiles[index] = 0
            elif tile == 0:
                if neighboors[index] == 2:
                    self.tiles[index] = 1
            else:
                print('WTF ?')


def compute_black_tiles(data):
    floor = Floor(data)
    floor.setup()
    return floor.black_tiles


def compute_black_tiles_iteration(data):
    floor = Floor(data)
    floor.setup()
    for i in range(100):
        floor.iterate()
        print(f'iteration {i+1} black {floor.black_tiles}')
    return floor.black_tiles


def test_part1():
    data = test_data.copy()
    result = compute_black_tiles(data)
    print(f'test1 is {result}')
    assert result == 10


def test_part2():
    data = test_data.copy()
    result = compute_black_tiles_iteration(data)
    print(f'test2 is {result}')
    assert result == 2208


def part1():
    data = load_data()
    result = compute_black_tiles(data)
    print(f'part1 is {result}')
    assert result == 521


def part2():
    data = load_data()
    result = compute_black_tiles_iteration(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
