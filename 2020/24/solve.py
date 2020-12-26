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


class Tile:
    def __init__(self, x, y, floor):
        self.x = x
        self.y = y
        self.floor = floor
        self.color = True
        self._neighboors = None
        self.to_flip = False

    @property
    def index(self):
        return f'{self.x}_{self.y}'

    def flip(self):
        self.color = not self.color

    @property
    def black(self):
        return not self.color

    @property
    def white(self):
        return self.color

    @property
    def white_neighboors(self):
        total = 0
        for neighboor in self.neighboors():
            if neighboor.white:
                total += 1
        return total

    def black_neighboors(self):
        total = 0
        for neighboor in self.neighboors():
            if neighboor.black:
                total += 1
        return total

    def will_flip(self):
        self.to_flip = True

    def update(self):
        if self.to_flip:
            self.color = not self.color
            self.to_flip = False
    
    def neighboors(self, add_missing=True):
        if self._neighboors is not None:
            return self._neighboors

        neighboors = []
        for index in [
                f'{self.x-1}_{self.y}',
                f'{self.x}_{self.y-1}',
                f'{self.x+1}_{self.y-1}',
                f'{self.x+1}_{self.y}',
                f'{self.x}_{self.y+1}',
                f'{self.x-1}_{self.y+1}']:
            if index in self.floor.tiles:
                neighboors.append(self.floor.tiles[index])
            else:
                if add_missing:
                    x = int(index.split('_')[0])
                    y = int(index.split('_')[1])
                    new_tile = Tile(x, y, self.floor)
                    self.floor.to_add.append(new_tile)
                    neighboors.append(new_tile)
        self._neighboors = neighboors
        return neighboors


class Floor:
    def __init__(self, data):
        self.data = data
        self.tiles = collections.defaultdict(int)

    def setup(self):
        x = 0
        y = 0

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
        print(f'We have {len(self.tiles)} tiles and {len(self.data)} lines')


    @property
    def black_tiles(self):
        return sum(filter(lambda x: x == 1, self.tiles.values()))


    def iterate(self):
        neighboors = collections.defaultdict(int)
        new_tiles = self.tiles.copy()

        for index, tile in new_tiles.items():
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
                neighboors[index] += self.tiles[test_index]

        for index, tile in new_tiles.items():
            if tile:
                if neighboors[index] == 0 or neighboors[index] > 2:
                    self.tiles[index] = 0
            else:
                if neighboors[index] == 2:
                    self.tiles[index] = 1



def compute_black_tiles(data):
    floor = Floor(data)
    floor.setup()
    return floor.black_tiles

def compute_black_tiles_iteration(data):
    floor = Floor(data)
    floor.setup()
    for i in range(100):
        floor.iterate()
        input(f'iteration {i+1} black {floor.black_tiles}')
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
    result = None
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
#part2()
