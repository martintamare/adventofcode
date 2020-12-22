#!/usr/bin/env python

test_data = [
    'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
    'trh fvjkl sbzzf mxmxvkd (contains dairy)',
    'sqjhc fvjkl (contains soy)',
    'sqjhc mxmxvkd sbzzf (contains fish)',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

def count_allergens(data):
    allergens_set = {}
    all_ingredients = set()

    for line in data:
        test = line.split('(contains')
        if len(test) > 1:
            ingredients = set([x.strip() for x in test[0].strip().split(' ')])
            all_ingredients = all_ingredients.union(ingredients)
            allergens = set([x.strip() for x in test[1].split(')')[0].split(',')])
            for allergen in allergens:
                if allergen in allergens_set:
                    new_set = allergens_set[allergen].intersection(ingredients)
                    allergens_set[allergen] = new_set
                else:
                    allergens_set[allergen] = ingredients

    ingredients_with_allergens = set()
    for allergen, allergen_set in allergens_set.items():
        ingredients_with_allergens = ingredients_with_allergens.union(allergen_set)
    print(all_ingredients)
    print(ingredients_with_allergens)
    ingredients_with_no_allergens = all_ingredients - ingredients_with_allergens
    total = 0
    for line in data:
        ingredients = set([x.strip() for x in line.split('(contains')[0].strip().split(' ')])
        for ingredient in ingredients:
            if ingredient in ingredients_with_no_allergens:
                total += 1
    return total


def find_canonical(data):
    allergens_set = {}
    all_ingredients = set()

    for line in data:
        test = line.split('(contains')
        if len(test) > 1:
            ingredients = set([x.strip() for x in test[0].strip().split(' ')])
            all_ingredients = all_ingredients.union(ingredients)
            allergens = set([x.strip() for x in test[1].split(')')[0].split(',')])
            for allergen in allergens:
                if allergen in allergens_set:
                    new_set = allergens_set[allergen].intersection(ingredients)
                    allergens_set[allergen] = new_set
                else:
                    allergens_set[allergen] = ingredients

    print(allergens_set)
    final_allergens = {}
    stop = False
    while not stop:
        changes = 0
        for allergen, allergen_set in allergens_set.items():
            if len(allergen_set) == 1:
                item = allergen_set.pop()
                print(f'found {item}')
                final_allergens[item] = allergen
                changes += 1
            else:
                for found_allergen in final_allergens.keys():
                    if found_allergen in allergen_set:
                        allergen_set.remove(found_allergen)
                        changes += 1
        if changes == 0:
            stop = True
        else:
            changes = 0

    test = sorted(final_allergens.items(), key=lambda kv: kv[1])
    data = []
    for key, value in test:
        data.append(key)
    return ','.join(data)


def test_part1():
    data = test_data
    result = count_allergens(data)
    print(f'test1 is {result}')
    assert result == 5


def test_part2():
    data = test_data
    result = find_canonical(data)
    print(f'test2 is {result}')
    assert result == 'mxmxvkd,sqjhc,fvjkl'


def part1():
    data = load_data()
    result = count_allergens(data)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = find_canonical(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
