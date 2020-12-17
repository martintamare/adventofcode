#!/usr/bin/env python

test_data = [
    '.#.',
    '..#',
    '###',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part2():
    data = test_data
    pocket = Pocket(data)
    for index in range(6):
        pocket.iterate(display=False)
        print(f'index {index} total {pocket.active_cubes}')
    result = pocket.active_cubes
    print(f'test1 is {result}')
    assert result == 848


class Cube:
    def __init__(self, x, y, z, w, pocket, status="."):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.pocket = pocket
        if status == '#':
            self.active = True
        elif status == '.':
            self.active = False
        else:
            raise Exception(f'WTF status ? {status}')
        self.next_status = None

    def update(self):
        if self.next_status is not None:
            self.active = self.next_status
            self.next_status = None

    def get_active_neightboors(self):
        active_neighboors = []
        #print(f'cube {self.x},{self.y},{self.z}')
        for x_index in range(self.x-1, self.x+2):
            for y_index in range(self.y-1, self.y+2):
                for z_index in range(self.z-1, self.z+2):
                    for w_index in range(self.w-1, self.w+2):
                        if x_index == self.x and \
                            y_index == self.y and \
                            z_index == self.z and \
                            w_index == self.w:
                            continue
                        pocket_index = self.pocket.build_index(x_index, y_index, z_index, w_index)
                        if pocket_index in self.pocket.cubes:
                            neighboor = self.pocket.cubes[pocket_index]
                            if neighboor.active:
                                #print('exist and active')
                                active_neighboors.append(neighboor)
                            else:
                                #print('exist and inactive')
                                pass
                        else:
                            #print('create')
                            new_cube = Cube(x_index, y_index, z_index, w_index, self.pocket)
                            self.pocket.cubes_to_add.append(new_cube)
        return active_neighboors


    def iterate(self):
        active_neighboors = self.get_active_neightboors()
        if self.active:
            if len(active_neighboors) not in [2,3]:
                self.next_status = False
            else:
               #print(f'cube z={self.z} {self.x},{self.y} has {len(active_neighboors)} neighboors : staying ALIVE')
               pass
        else:
            if len(active_neighboors) == 3:
                #print(f'cube z={self.z} {self.x},{self.y} has {len(active_neighboors)} neighboors : WAKING UP')
                self.next_status = True

    def __repr__(self):
        if self.active:
            return '#'
        else:
            return '.'


    
class Pocket:
    def __init__(self, data):
        self.length = len(data)
        self.cubes = {}
        self.cubes_to_add = []

        for x_index in range(self.length):
            row_data = []
            row = data[x_index]
            for y_index in range(self.length):
                status = row[y_index]
                cube = Cube(x_index, y_index, 0, 0, self, status)
                cube_index = self.build_index(x_index, y_index, 0, 0)
                self.cubes[cube_index] = cube

    def build_index(self, x, y, z, w):
        return f'{z}_{x}_{y}_{w}'

    def coordinates_from_index(self, index):
        coordinates = list(map(int, index.split('_')))
        return coordinates

    def iterate(self, display=False):
        # Find next step
        for cube in self.cubes.values():
            cube.get_active_neightboors()

        # Add new neighboors
        for cube in self.cubes_to_add:
            cube_index = self.build_index(cube.x, cube.y, cube.z, cube.w)
            self.cubes[cube_index] = cube

        # Apply next step
        for cube in self.cubes.values():
            cube.iterate()

        for cube in self.cubes.values():
            cube.update()
        
        self.cubes_to_add = []
        if display:
            print(self)


    def __repr__(self):
        return 'madness'

    @property
    def active_cubes(self):
        total = 0
        for cube in self.cubes.values():
            if cube.active:
                total += 1
        return total




def part2():
    data = load_data()
    pocket = Pocket(data)
    for index in range(6):
        pocket.iterate(display=False)
        print(f'index {index} total {pocket.active_cubes}')
    result = pocket.active_cubes
    print(f'part2 is {result}')


test_part2()
part2()