#!/usr/bin/env python

test_data = [
    '....#..',
    '..###.#',
    '#...#.#',
    '.#...##',
    '#.###..',
    '##.#.##',
    '.#..#..',
]

small_test = [
    '.....',
    '..##.',
    '..#..',
    '.....',
    '..##.',
    '.....',
]



def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Grid:
    def __init__(self, elves):
        self.elves = elves
        self.proposals = {}
        self.delta_to_test = [
            ([(0,-1), (1, -1), (-1, -1)], (0, -1)),
            ([(0,1), (1, 1), (-1, 1)], (0, 1)),
            ([(-1,1), (-1, 0), (-1, -1)], (-1, 0)),
            ([(1,1), (1, 0), (1, -1)], (1,0)),
        ]
        self.delta_index = 0


    @property
    def empty_tiles(self):
        min_x = min(map(lambda x: x[0], self.elves.keys()))
        max_x = max(map(lambda x: x[0], self.elves.keys()))
        min_y = min(map(lambda x: x[1], self.elves.keys()))
        max_y = max(map(lambda x: x[1], self.elves.keys()))
        x_length = max_x - min_x + 1
        y_length = max_y - min_y + 1
        print(f'x={x_length} ({max_x}-{min_x}) y={y_length} ({max_y}-{min_y}')
        total = x_length * y_length - len(self.elves.keys())
        return total

    def iterate(self):
        for position in self.elves.keys():
            has_neighbors = False
            x, y = position
            for x_delta in range(-1,2):
                for y_delta in range(-1,2):
                    test_position = (x + x_delta, y + y_delta)
                    if test_position == position:
                        continue
                    elif test_position in self.elves:
                        has_neighbors = True
                        break
            self.elves[position]['has_neighbors'] = has_neighbors

        self.proposals = {}

        for position in self.elves.keys():
            elve = self.elves[position]
            if not elve['has_neighbors']:
                continue

            proposal = None
            x, y = position

            for index in range(self.delta_index, self.delta_index + 4):
                index = index % len(self.delta_to_test)
                deltas, to_add  = self.delta_to_test[index]
                has_neighbors = False
                for delta in deltas:
                    x_delta = delta[0]
                    y_delta = delta[1]
                    test_position = (x + x_delta, y + y_delta)
                    if test_position in self.elves:
                        has_neighbors = True
                if not has_neighbors:
                    x_delta, y_delta = to_add
                    proposal = (x + x_delta, y + y_delta)
                    break


            if proposal is not None:
                self.elves[position]['proposal'] = proposal
                if proposal in self.proposals:
                    self.proposals[proposal] += 1
                else:
                    self.proposals[proposal] = 1

        new_elves = {}
        self.has_movement = False
        for position in self.elves.keys():
            elve = self.elves[position]
            if 'proposal' not in elve:
                new_elves[position] = {}
            else:
                proposal = elve['proposal']
                if self.proposals[proposal] > 1:
                    new_elves[position] = {}
                else:
                    new_elves[proposal] = {}
                    self.has_movement = True
        self.delta_index = (self.delta_index + 1) % len(self.delta_to_test)
        self.elves = new_elves


def solve_part1(data):
    elves = {}
    for y in range(len(data)):
        line = data[y]
        for x in range(len(line)):
            if line[x] == '#':
                elve = {}
                position = (x,y)
                elves[position] = elve
    grid = Grid(elves)

    for i in range(10):
        grid.iterate()

    return grid.empty_tiles


def solve_part2(data):
    elves = {}
    for y in range(len(data)):
        line = data[y]
        for x in range(len(line)):
            if line[x] == '#':
                elve = {}
                position = (x,y)
                elves[position] = elve
    grid = Grid(elves)

    grid.iterate()
    i = 1
    while grid.has_movement:
        if i % 100 == 0:
            print(f'iteration {i}')
        grid.iterate()
        i += 1

    return i



def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 110


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 20


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
