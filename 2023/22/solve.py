#!/usr/bin/env python

test_data = [
    '1,0,1~1,2,1',
    '0,0,2~2,0,2',
    '0,2,3~2,2,3',
    '0,0,4~0,2,4',
    '2,0,5~2,2,5',
    '0,1,6~2,1,6',
    '1,1,8~1,1,9',
]


def compute_name(index):

    index += 65
    if index > 91:
        return '#'
        print("todo")
        exit(0)
    return chr(index)


class Brick:
    def __init__(self, index, data, space):
        self.index = index
        self.data = data
        start = data.split('~')[0]
        end = data.split('~')[1]
        self.start = list(map(int, start.split(',')))
        self.end = list(map(int, end.split(',')))
        self.name = compute_name(index)
        self.space = space
        self._neighbors = None

    def __repr__(self):
        return f"{self.name}"


    def neighbors(self):
        # Count every brick that touch up
        # Recurse until no brick ?
        bricks = []
        for position in self.positions():
            # z
            to_add = [0, 0, 1]
            test_position = [x + y for x, y in zip(position, to_add)]
            test_vector = (test_position[0], test_position[1], test_position[2])

            if test_vector in self.space.positions:
                test_brick = self.space.positions[test_vector]
                if test_brick == self:
                    continue
                if test_brick not in bricks:
                    bricks.append(test_brick)

        result = set()
        result.add(self)
        if not bricks:
            print(f"{self.name} no neighbors")
        else:
            print(f"{self.name} neighbors=")
            for brick in bricks:
                print(f"{brick.name}")
                result |= brick.neighbors()
        print(f"{self.name} neighbors total {result}")
        return result


    def positions(self):
        range_index = None
        if self.start[0] != self.end[0]:
            range_index = 0
        if self.start[1] != self.end[1]:
            if range_index is not None:
                print('fnezjkfnezkjfezf1')
                exit(0)
            else:
                range_index = 1
        if self.start[2] != self.end[2]:
            if range_index is not None:
                print('fnezjkfnezkjfezf2')
                exit(0)
            else:
                range_index = 2

        # single cube
        if range_index is None:
            result = [self.start]
            return result

        min_range = min(self.start[range_index], self.end[range_index])
        max_range = max(self.start[range_index], self.end[range_index])

        result = []
        for index in range(min_range, max_range+1):
            if range_index == 0:
                position = [index, self.start[1], self.start[2]]
            elif range_index == 1:
                position = [self.start[0], index, self.start[2]]
            else:
                position = [self.start[0], self.start[1], index]
            result.append(position)
        return result 

    def can_fall(self, to_skip=set()):
        for position in self.positions():
            # z
            if position[2] == 1:
                return False
            to_add = [0, 0, -1]
            test_position = [x + y for x, y in zip(position, to_add)]
            test_vector = (test_position[0], test_position[1], test_position[2])

            # another brick is here
            must_not_match = set()
            must_not_match.add(self)
            if to_skip:
                must_not_match |= to_skip

            if test_vector in self.space.positions and self.space.positions[test_vector] not in must_not_match:
                return False
        return True

    def can_be_removed(self):
        result = True
        count = 0
        counted = set()
        brick_removed = set()
        brick_removed.add(self)
        for brick in self.space.bricks:
            if brick == self:
                continue
            if brick.can_fall(brick_removed):
                return False
        return result


    def do_fall(self):
        # clean space positions
        for position in self.positions():
            x = position[0]
            y = position[1]
            z = position[2]
            vector = (x, y, z)
            del self.space.positions[vector]

        # update self positions
        to_add = [0, 0, -1]
        new_start = [x+y for x, y in zip(self.start, to_add)]
        new_end = [x+y for x, y in zip(self.end, to_add)]
        self.start = new_start
        self.end = new_end

        # update space positions
        self.space.add_brick(self)


class Space:
    def __init__(self):
        # x, y, z
        self.positions = {}
        self.bricks = []
        self.x = [None, None]
        self.y = [None, None]
        self.z = [0, None]

    def add_brick(self, brick):
        if brick not in self.bricks:
            self.bricks.append(brick)

        for position in brick.positions():
            x = position[0]
            y = position[1]
            z = position[2]

            # min_x
            if self.x[0] is None or x < self.x[0]:
                self.x[0] = x
            # max_x
            if self.x[1] is None or x > self.x[1]:
                self.x[1] = x

            # min_y
            if self.y[0] is None or y < self.y[0]:
                self.y[0] = y
            # max_y
            if self.y[1] is None or y > self.y[1]:
                self.y[1] = y

            # min_z
            if self.z[0] is None or z < self.z[0]:
                self.z[0] = z
            # max_z
            if self.z[1] is None or z > self.z[1]:
                self.z[1] = z

            vector = (x, y, z)
            self.positions[vector] = brick

    def __repr__(self):
        return f"{self.x} {self.y} {self.z}"


    def print(self):
        self.print_x()
        print("======================================")
        self.print_y()

    def print_x(self):
        print("x")
        for x in range(self.x[0], self.x[1]+1):
            print(x, end="")
        print("")
        for z in range(self.z[1], self.z[0]-1, -1):
            for x in range(self.x[0], self.x[1]+1):
                bricks = []
                if z == 0:
                    print('-', end="")
                else:
                    for y in range(self.y[0], self.y[1] + 1):
                        vector = (x, y, z)
                        if vector in self.positions and self.positions[vector] not in bricks:
                            bricks.append(self.positions[vector])
                    if len(bricks) == 1:
                        print(bricks[0].name, end="")
                    elif len(bricks) > 1:
                        print('?', end="")
                    else:
                        print('.', end="")
            print(f" {z}")

    def print_y(self):
        print("y")
        for y in range(self.y[0], self.y[1]+1):
            print(y, end="")
        print("")
        for z in range(self.z[1], self.z[0]-1, -1):
            for y in range(self.y[0], self.y[1]+1):
                bricks = []
                if z == 0:
                    print('-', end="")
                else:
                    for x in range(self.x[0], self.x[1] + 1):
                        vector = (x, y, z)
                        if vector in self.positions and self.positions[vector] not in bricks:
                            bricks.append(self.positions[vector])
                    if len(bricks) == 1:
                        print(bricks[0].name, end="")
                    elif len(bricks) > 1:
                        print('?', end="")
                    else:
                        print('.', end="")
            print(f" {z}")

    def iterate(self):
        has_move = False
        for brick in self.bricks:
            if brick.can_fall():
                has_move = True
                brick.do_fall()
        return has_move

    def count_move_when_remove(self, brick_removed):
        removed = set()
        removed.add(brick_removed)
        while True:
            count = 0
            for brick in self.bricks:
                if brick not in removed:
                    if brick.can_fall(removed):
                        count += 1
                        removed.add(brick)
            if not count:
                break
        print(f"removed {removed=}")
        return len(removed) - 1

    @property
    def disintegrate(self):
        count = 0
        for brick in self.bricks:
            if brick.can_be_removed():
                count += 1
        return count

    @property
    def part2(self):
        self.print()
        brick_to_search = []
        for brick in self.bricks:
            if not brick.can_be_removed():
                brick_to_search.append(brick)
        count = 0
        for brick in brick_to_search:
            print(f"{brick.name} {brick.start} {brick.end}")
            # how many brick move if this is removed ?
            brick_count = self.count_move_when_remove(brick)
            print(f"{brick_count=}")
            count += brick_count

        return count


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    space = Space()

    bricks = []
    for index, line in enumerate(data):
        brick = Brick(index, line, space)
        space.add_brick(brick)

    space.print()
    while True:
        result = space.iterate()
        space.print()
        if not result:
            break

    # now count bricks that can be removed
    return space.disintegrate


def solve_part2(data):
    space = Space()

    bricks = []
    for index, line in enumerate(data):
        brick = Brick(index, line, space)
        space.add_brick(brick)

    space.print()
    while True:
        result = space.iterate()
        space.print()
        if not result:
            break

    # now count bricks that can be removed
    return space.part2


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 5


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 7


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result < 82782
    assert result > 1828


#test_part1()
#part1()
test_part2()
part2()
