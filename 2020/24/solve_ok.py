#!/usr/bin/env python

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
        self.tiles = {}
        self.to_add = []
        self._max_x = None
        self._max_y = None
        self._min_x = None
        self._min_y = None


    def setup(self):
        x = 0
        y = 0
        current_tile = Tile(x, y, self)
        tiles = {}

        for line in self.data:
            x = 0
            y = 0
            while len(line):
                direction = None
                for test_direction in ['e', 'se', 'sw', 'w', 'nw', 'ne']:
                    if line.startswith(test_direction):
                        direction = test_direction
                        break
                if direction == 'w':
                    x = x - 1
                    y = y
                elif direction == 'sw':
                    x = x
                    y = y - 1
                elif direction == 'se':
                    x = x + 1
                    y = y - 1
                elif direction == 'e':
                    x = x + 1
                    y = y
                elif direction == 'ne':
                    x = x 
                    y = y + 1
                elif direction == 'nw':
                    x = x - 1
                    y = y + 1
                else:
                    raise Exception('NFJznajFNJ')

                index = f'{x}_{y}'
                if index in tiles:
                    current_tile = tiles[index]
                else:
                    current_tile = Tile(x, y, self)
                    tiles[index] = current_tile

                line = line[len(direction):]

            current_tile.flip()
            self.tiles[current_tile.index] = current_tile
        print(f'We have {len(self.tiles)} tiles and {len(self.data)} lines')

    @property
    def max_x(self):
        if self._max_x is not None:
            return self._max_x

        max_x = 0
        for i, tile in self.tiles.items():
            max_x = max(tile.x, max_x)
        self._max_x = max_x
        return max_x

    @property
    def min_x(self):
        if self._min_x is not None:
            return self._min_x

        min_x = 0
        for i, tile in self.tiles.items():
            min_x = min(tile.x, min_x)
        self._min_x = min_x
        return min_x

    @property
    def max_y(self):
        if self._max_y is not None:
            return self._max_y

        max_y = 0
        for i, tile in self.tiles.items():
            max_y = max(tile.y, max_y)
        self._max_y = max_y
        return max_y

    @property
    def min_y(self):
        if self._min_y is not None:
            return self._min_y

        min_y = 0
        for i, tile in self.tiles.items():
            min_y = min(tile.y, min_y)
        self._min_y = min_y
        return min_y

    def set_neighboors(self):

        tiles_to_add = []
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for i, tile in self.tiles.items():
            x = tile.x
            y = tile.y
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):

                index = f'{x}_{y}'
                if index in self.tiles:
                    continue
                else:
                    new_tile = Tile(x, y, self)
                    tiles_to_add.append(new_tile)
        for tile in tiles_to_add:
            self.tiles[tile.index] = tile


    def set_neighboors_2(self):
        neighboors = []
        for i, tile in self.tiles.items():
            for index in [
                    f'{tile.x-1}_{tile.y}',
                    f'{tile.x}_{tile.y-1}',
                    f'{tile.x+1}_{tile.y-1}',
                    f'{tile.x+1}_{tile.y}',
                    f'{tile.x}_{tile.y+1}',
                    f'{tile.x-1}_{tile.y+1}']:
                if index not in self.tiles:
                    x = int(index.split('_')[0])
                    y = int(index.split('_')[1])
                    new_tile = Tile(x, y, self)
                    neighboors.append(new_tile)
        for neighboor in neighboors:
            self.tiles[neighboor.index] = neighboor

    @property
    def black_tiles(self):
        total = 0
        for index, tile in self.tiles.items():
            if tile.black:
                total += 1
        return total


    def iterate(self):
        for index, tile in self.tiles.items():
            black_neighboors = tile.black_neighboors()

        for tile in self.to_add:
            index = tile.index
            self.tiles[index] = tile

        for index, tile in self.tiles.items():
            black_neighboors = tile.black_neighboors()
            if tile.black:
                if black_neighboors == 0 or black_neighboors > 2:
                    tile.will_flip()
            elif tile.white:
                if black_neighboors == 2:
                    tile.will_flip()

        #for tile in self.to_add:
        #    tile.neighboors(add_missing=False)
        #    black_neighboors = tile.black_neighboors()
        #    if tile.black:
        #        if black_neighboors == 0 or black_neighboors > 2:
        #            tile.will_flip()
        #    elif tile.white:
        #        if black_neighboors == 2:
        #            tile.will_flip()

        self.to_add = []

        for index, tile in self.tiles.items():
            tile.update()



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


def part2():
    data = load_data()
    result = None
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
#part2()
