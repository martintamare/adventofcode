#!/usr/bin/env python

test_data = [
"3-5",
"10-14",
"16-20",
"12-18",
"",
"1",
"5",
"8",
"11",
"17",
"32",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Range:
    def __init__(self, _min, _max):
        self.min = _min
        self.max = _max

    def __repr__(self):
        return f"{self.min}-{self.max}"

    def contains(self, ingredient):
        if ingredient >= self.min and ingredient <= self.max:
            return True
        else:
            return False

    def match(self, other_range):
        if other_range.min > self.max:
            return False
        elif other_range.max < self.min:
            return False
        else:
            return True

    def update(self, other_range):
        new_min = min(self.min, other_range.min)
        new_max = max(self.max, other_range.max)
        self.min = new_min
        self.max = new_max

    @property
    def total(self):
        return self.max - self.min + 1


def solve_part1(data):
    ranges = []
    ingredients = []
    mode = "range"

    for line in data:
        if not line:
            mode = "ingredient"
            continue
        if mode == "range":
            _min = int(line.split('-')[0])
            _max = int(line.split('-')[1])
            _range = Range(_min, _max)
            ranges.append(_range)
        elif mode == "ingredient":
            ingredients.append(int(line))

    result = 0
    for ingredient in ingredients:
        fresh = False
        for _range in ranges:
            if _range.contains(ingredient):
                fresh = True
                break
        if fresh:
            print(f"{ingredient=} is fresh")
            result += 1
    return result


def solve_part2(data):
    ranges = []
    ingredients = []
    mode = "range"

    for line in data:
        if not line:
            mode = "ingredient"
            continue
        if mode == "range":
            _min = int(line.split('-')[0])
            _max = int(line.split('-')[1])
            _range = Range(_min, _max)
            ranges.append(_range)
        elif mode == "ingredient":
            ingredients.append(int(line))

    stop = False
    while not stop:
        final_ranges = []
        has_update = False
        for _range in ranges:
            if not final_ranges:
                final_ranges.append(_range)
            else:
                to_add = True
                for test_range in final_ranges:
                    print(f"testing {_range} vs {test_range}")
                    if test_range.match(_range):
                        print(f"Updating {test_range} with {_range}")
                        test_range.update(_range)
                        print(f"Updated {test_range}")
                        to_add = False
                        has_update = True
                        break
                if to_add:
                    print("Added")
                    final_ranges.append(_range)
        if not has_update:
            stop = True
        ranges = final_ranges

    result = 0
    for _range in ranges:
        print(f"Adding {_range} with {_range.total}")
        result += _range.total
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 3


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 14


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')
    assert result < 349584170223220


test_part1()
part1()
test_part2()
part2()
