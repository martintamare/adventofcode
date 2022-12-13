#!/usr/bin/env python
from itertools import product
from collections import Counter
import copy


test_data = [
    'Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8',
    'Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name


def solve_part1(data):
    ingredients = []

    for line in data:
        splitted = line.replace(',', '').replace(':', '').split(' ')
        name = splitted[0]
        capacity = int(splitted[2])
        durability = int(splitted[4])
        flavor = int(splitted[6])
        texture = int(splitted[8])
        calories = int(splitted[10])
        ingredient = Ingredient(name, capacity, durability, flavor, texture, calories)
        ingredients.append(ingredient)

    maximum = 0
    iteration = 0
    ok_configurations = []
    best_configuration = None
    for combination in product(ingredients, repeat=10):
        iteration += 1
        is_ok = True
        for attr in ['capacity', 'durability', 'flavor', 'texture']:
            attr_sum = sum(map(lambda x: getattr(x, attr), combination))
            if attr_sum <= 0:
                is_ok = False
                break
        if is_ok:
            ok_configurations.append(combination)
            result = 1
            for attr in ['capacity', 'durability', 'flavor', 'texture']:
                result *= sum(map(lambda x: getattr(x, attr), combination))
            if result > maximum:
                maximum = result
                best_configuration = combination
    best_configuration = Counter(best_configuration)

    # Now compute range to look
    ranges = {}
    for ingredient in ingredients:
        number = best_configuration[ingredient]
        ranges[ingredient] = {'min': (number*10)-5, 'max': (number*10)+5}

    counters = []
    for ingredient in ingredients:
        ingredient_counter = []
        for ingredient_number in range(ranges[ingredient]['min'], ranges[ingredient]['max']+1):
            if ingredient_number == 0:
                continue
            if not counters:
                c = Counter()
                c[ingredient] = ingredient_number
                ingredient_counter.append(c)
            else:
                for c in counters:
                    new_counter = copy.copy(c)
                    current_counter = len(list(c.elements()))
                    if ingredient.name == ingredients[-1].name:
                        if current_counter + ingredient_number != 100:
                            continue
                    else:
                        if current_counter >= 100:
                            continue
                        elif current_counter + ingredient_number > 100:
                            continue
                    new_counter[ingredient] = ingredient_number
                    ingredient_counter.append(new_counter)
        counters = ingredient_counter
        print(f'We now have {len(counters)} counters after ingredient {ingredient}')

    maximum = 0
    for c in counters:
        if len(c) != len(ingredients):
            continue
        current_counter = len(list(c.elements()))
        if current_counter != 100:
            continue

        result = 1
        for attr in ['capacity', 'durability', 'flavor', 'texture']:
            attr_result = 0
            for ingredient in c:
                if ingredient in c:
                    number = c[ingredient]
                    attr_result += number * getattr(ingredient, attr)
            if attr_result < 0:
                attr_result = 0
            result *= attr_result
            if result == 0:
                break

        if result > maximum:
            print(f'combination is new_max ! {c}')
            maximum = result
    return maximum


def solve_part2(data):
    ingredients = []

    for line in data:
        splitted = line.replace(',', '').replace(':', '').split(' ')
        name = splitted[0]
        capacity = int(splitted[2])
        durability = int(splitted[4])
        flavor = int(splitted[6])
        texture = int(splitted[8])
        calories = int(splitted[10])
        ingredient = Ingredient(name, capacity, durability, flavor, texture, calories)
        ingredients.append(ingredient)

    maximum = 0
    iteration = 0
    ok_configurations = []
    best_configuration = None
    for combination in product(ingredients, repeat=10):
        is_ok = True
        for attr in ['capacity', 'durability', 'flavor', 'texture']:
            attr_sum = sum(map(lambda x: getattr(x, attr), combination))
            if attr_sum <= 0:
                is_ok = False
                break
        if is_ok:
            ok_configurations.append(combination)
            result = 1
            for attr in ['capacity', 'durability', 'flavor', 'texture']:
                result *= sum(map(lambda x: getattr(x, attr), combination))
            if result > maximum:
                maximum = result
                best_configuration = combination
    best_configuration = Counter(best_configuration)

    # Now compute range to look

    # Now compute range to look
    ranges = {}
    for ingredient in ingredients:
        number = best_configuration[ingredient]
        ranges[ingredient] = {'min': (number-1)*10, 'max': (number+1)*10}

    counters = []
    for ingredient in ingredients:
        ingredient_counter = []
        for ingredient_number in range(ranges[ingredient]['min'], ranges[ingredient]['max']+1):
            if ingredient_number == 0:
                continue
            if not counters:
                c = Counter()
                c[ingredient] = ingredient_number
                ingredient_counter.append(c)
            else:
                for c in counters:
                    new_counter = copy.copy(c)
                    current_counter = len(list(c.elements()))
                    if ingredient.name == ingredients[-1].name:
                        if current_counter + ingredient_number != 100:
                            continue
                    else:
                        if current_counter >= 100:
                            continue
                        elif current_counter + ingredient_number > 100:
                            continue
                    new_counter[ingredient] = ingredient_number
                    ingredient_counter.append(new_counter)
        counters = ingredient_counter
        print(f'We now have {len(counters)} counters after ingredient {ingredient}')

    print(f'We have {len(counters)} configuration to test {counters}')
    maximum = 0
    for c in counters:
        if len(c) != len(ingredients):
            continue
        current_counter = len(list(c.elements()))
        if current_counter != 100:
            continue

        calories = 0
        for ingredient in c:
            number = c[ingredient]
            calories += ingredient.calories * number
        if calories != 500:
            continue

        result = 1
        for attr in ['capacity', 'durability', 'flavor', 'texture']:
            attr_result = 0
            for ingredient in c:
                if ingredient in c:
                    number = c[ingredient]
                    attr_result += number * getattr(ingredient, attr)
            if attr_result < 0:
                attr_result = 0
            result *= attr_result
            if result == 0:
                break

        if result > maximum:
            print(f'combination is new_max ! {c}')
            maximum = result
    return maximum


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 62842880


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 57600000


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
