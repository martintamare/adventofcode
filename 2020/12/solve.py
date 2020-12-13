#!/usr/bin/env python
import math

test_data = [
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    data = test_data
    result = get_manhattan_distance(data, 1, 0)
    print(f'test1 result is {result}')
    assert result == 25


def test_part2():
    data = test_data
    result = get_manhattan_distance_2(data, 1, 0, 10, 1)
    print(f'test2 result is {result}')
    assert result == 286


def part1():
    data = load_data()
    result = get_manhattan_distance(data, 1, 0)
    print(f'result1 is {result}')


def part2():
    data = load_data()
    result = get_manhattan_distance_2(data, 1, 0, 10, 1)
    print(f'result2 is {result}')

class Boat:
    def __init__(self, vector_x, vector_y, waypoint_x=None, waypoint_y=None):
        self.x = 0
        self.y = 0
        self.vector_x = vector_x
        self.vector_y = vector_y
        self.waypoint_x = waypoint_x
        self.waypoint_y = waypoint_y

    def move(self, instruction):
        letter = instruction[0]
        distance = int(instruction[1:])
        print(f'letter is {letter} distance is {distance}')

        if letter == 'F':
            self.move_forward(distance)
        elif letter in ['N', 'S', 'E', 'W']:
            self.move_direction(letter, distance)
        elif letter == 'L':
            print(f'rotating left {distance}')
            self.rotate(distance)
        elif letter == 'R':
            print(f'rotating right {distance}')
            self.rotate(-distance)
        else:
            print('WTF ?')
            exit(1)

    def move_forward(self, distance):
        self.x += self.vector_x * distance
        self.y += self.vector_y * distance
        self.print_position()

    def move_direction(self, direction, distance):
        if direction == 'N':
            self.y += distance
        elif direction == 'S':
            self.y -= distance
        elif direction == 'E':
            self.x += distance
        else:
            self.x -= distance
        self.print_position()

    def rotate(self, degree):
        current_radian = round(math.atan2(self.vector_y, self.vector_x), 2)
        current_degree = math.degrees(current_radian)
        new_degree = current_degree + degree
        radian = math.radians(new_degree)
        self.vector_x = round(math.cos(radian), 0)
        self.vector_y = round(math.sin(radian), 0)

    def move2(self, instruction):
        letter = instruction[0]
        distance = int(instruction[1:])
        print(f'letter is {letter} distance is {distance}')

        if letter == 'F':
            self.move_forward_waypoint(distance)
        elif letter in ['N', 'S', 'E', 'W']:
            self.move_waypoint(letter, distance)
        elif letter == 'L':
            print(f'rotating left {distance}')
            if distance == 270:
                self.rotate_waypoint_right()
            elif distance == 180:
                self.rotate_waypoint_inverse()
            else:
                self.rotate_waypoint_left()
        elif letter == 'R':
            print(f'rotating right {distance}')
            if distance == 270:
                self.rotate_waypoint_left()
            elif distance == 180:
                self.rotate_waypoint_inverse()
            else:
                self.rotate_waypoint_right()
        else:
            print('WTF ?')
            exit(1)

    def rotate_waypoint_inverse(self):
        self.waypoint_x = - self.waypoint_x
        self.waypoint_y = - self.waypoint_y

    def rotate_waypoint_left(self):
        waypoint_x = self.waypoint_x
        waypoint_y = self.waypoint_y
        self.waypoint_x = - waypoint_y
        self.waypoint_y = waypoint_x

    def rotate_waypoint_right(self):
        waypoint_x = self.waypoint_x
        waypoint_y = self.waypoint_y
        self.waypoint_x = waypoint_y
        self.waypoint_y = - waypoint_x

    def move_forward_waypoint(self, distance):
        self.x += self.waypoint_x * distance
        self.y += self.waypoint_y * distance
        self.print_position()

    def move_waypoint(self, direction, distance):
        if direction == 'N':
            self.waypoint_y += distance
        elif direction == 'S':
            self.waypoint_y -= distance
        elif direction == 'E':
            self.waypoint_x += distance
        else:
            self.waypoint_x -= distance
        self.print_position()

    def rotate_waypoint(self, degree):
        print(f'waypoint was {self.waypoint_x}:{self.waypoint_y} rotating {degree}')
        length = math.hypot(self.waypoint_x, self.waypoint_y)
        max_waypoint = max(abs(self.waypoint_y), abs(self.waypoint_x))
        min_waypoint = min(abs(self.waypoint_y), abs(self.waypoint_x))
        if self.waypoint_x > self.waypoint_y:
            radian = math.acos(min_waypoint/max_waypoint)
        else:
            radian = math.asin(min_waypoint/max_waypoint)
        new_radian = radian + math.radians(degree)
        self.waypoint_x = round(math.cos(new_radian) * length, 0)
        self.waypoint_y = round(math.sin(new_radian) * length, 0)
        print(f'waypoint is now {self.waypoint_x}:{self.waypoint_y}')

    def print_position(self):
        print(f'Boat is now at {self.x}:{self.y}')

    @property
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

def get_manhattan_distance(data, vector_x, vector_y):
    boat = Boat(vector_x, vector_y)
    for instruction in data:
        boat.move(instruction)
    return boat.manhattan_distance


def get_manhattan_distance_2(data, vector_x, vector_y, waypoint_x, waypoint_y):
    boat = Boat(vector_x, vector_y, waypoint_x, waypoint_y)
    for instruction in data:
        boat.move2(instruction)
    return boat.manhattan_distance


test_part1()
part1()
test_part2()
part2()
