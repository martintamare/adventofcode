#!/usr/bin/env python
import re

test_data = [
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


class Light:
    def __init__(self, x, y, matrix):
        self.x = x
        self.y = y
        self.matrix = matrix
        self.status = False
        self.brightness = 0

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False

    def toggle(self):
        self.status = not self.status

    def turn_on_2(self):
        self.brightness += 1

    def turn_off_2(self):
        self.brightness = max(0, self.brightness-1)

    def toggle_2(self):
        self.brightness += 2


class Grid:
    def __init__(self, rows=1000, columns=1000):
        self.matrix = []
        for row in range(rows):
            lights = []
            for column in range(columns):
                light = Light(row, column, self)
                lights.append(light)
            self.matrix.append(lights)
        self.regex = re.compile(r'^(.*) (\d+),(\d+) through (\d+),(\d+)')

    def process_instruction(self, instruction):
        match = self.regex.match(instruction)
        if not match:
            print(f'WTF ? {instruction}')
            exit(1)
        action, start_row, start_column, end_row, end_colum = match.groups()
        for row in range(int(start_row), int(end_row)+1):
            for column in range(int(start_column), int(end_colum)+1):
                light = self.matrix[row][column]
                if action == 'turn on':
                    light.turn_on()
                elif action == 'turn off':
                    light.turn_off()
                else:
                    light.toggle()

    def process_instruction_part_2(self, instruction):
        match = self.regex.match(instruction)
        if not match:
            print(f'WTF ? {instruction}')
            exit(1)
        action, start_row, start_column, end_row, end_colum = match.groups()
        for row in range(int(start_row), int(end_row)+1):
            for column in range(int(start_column), int(end_colum)+1):
                light = self.matrix[row][column]
                if action == 'turn on':
                    light.turn_on_2()
                elif action == 'turn off':
                    light.turn_off_2()
                else:
                    light.toggle_2()

    @property
    def lights_on(self):
        total = 0
        for row in self.matrix:
            for light in row:
                if light.status:
                    total += 1
        return total

    @property
    def total_brightness(self):
        total = 0
        for row in self.matrix:
            for light in row:
                total += light.brightness
        return total



def part1():
    data = load_data()
    grid = Grid()
    for line in data:
        grid.process_instruction(line)

    result = grid.lights_on
    print(f'part1 is {result}')


def part2():
    data = load_data()
    grid = Grid()
    for line in data:
        grid.process_instruction_part_2(line)

    result = grid.total_brightness
    print(f'part2 is {result}')


part1()
part2()
