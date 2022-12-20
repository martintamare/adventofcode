#!/usr/bin/env python

test_data = [
    'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.',
    'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
    splitted = data.split(':')[1].strip().split('.')
    blueprint = {}
    for line in splitted:
        line_splitted = line.strip().split(' ')
        if len(line_splitted) == 6:
            blueprint[line_splitted[1]] = {line_splitted[5]: int(line_splitted[4])}
        elif len(line_splitted) == 1:
            continue
        elif len(line_splitted) == 9:
            definition = {}
            i = 4
            while i < 9:
                to_map = line_splitted[i+1]
                n = int(line_splitted[i])
                definition[to_map] = n
                i += 3
            blueprint[line_splitted[1]] = definition

    # Build ore base for all
    for item in ['ore', 'clay', 'obsidian', 'geode']:
        print(f'Computing cost in ore for {item}')
        cost = 0
        for subitem in ['ore', 'clay', 'obsidian', 'geode']:
            if subitem in blueprint[item]:
                if subitem == 'ore':
                    cost += blueprint[item][subitem]
                else:
                    key = f'{subitem}_cost'
                    if key not in blueprint:
                        print('Jkdn,zkdn,azkdaz')
                    else:
                        cost += blueprint[key] * blueprint[item][subitem]
        blueprint[f'{item}_cost'] = cost

    print(blueprint)
    ore = 0
    clay = 0
    obsidian = 0
    geode = 0
    ore_robot = 1
    clay_robot = 0
    obsidian_robot = 0
    geode_robot = 0
    data_max = {'geode': None, 'time_for_geode': None}
    geodes = [0 for x in range(26)]
    escape = [0]

    ore_robot = 1
    ore = 0
    for index in range(25):
        ore += ore_robot
        if ore > blueprint['ore']['ore']:
            ore_robot += 1
            ore -= blueprint['ore']['ore']
        escape.append(ore)





    def can_build(robot, **kwargs):
        current_items = {
            'ore': kwargs['ore'],
            'clay': kwargs['clay'],
            'obsidian': kwargs['obsidian'],
            'geode': kwargs['geode'],
        }
        can_build = True
        for item in blueprint[robot].keys():
            if blueprint[robot][item] > current_items[item]:
                can_build = False
                break
        return can_build


    def iterate(i, ore=0, clay=0, obsidian=0, geode=0,
                ore_robot=1, clay_robot=0, obsidian_robot=0, geode_robot=0):

        print(i)
        # Smart out based on max
        if geode < geodes[i]:
            return geode
        elif geode > geodes[i]:
            geodes[i] = geode

        # Compute how much iteration to get a new geode
        # Base on others ?

        # Add smart break according to iteration we can estimate creation or geode or not ?
        #iteration_remaining = 24 - i
        current_ore = ore_robot + clay_robot * blueprint['clay_cost'] + obsidian_robot * blueprint['obsidian_cost'] + geode_robot * blueprint['geode_cost']
        print(f'{current_ore} vs {escape[i]}')
        if escape[i] > current_ore:
            return geode

        if i == 24:
            if data_max['geode'] is None:
                data_max['geode'] = geode
                print(f'ore={ore} (robot={ore_robot})')
                print(f'clay={clay} (robot={clay_robot})')
                print(f'obsidian={obsidian} (robot={obsidian_robot})')
                print(f'geode={geode} (robot={geode_robot})')
                print(f'found {geode}')
            elif geode > data_max['geode']:
                data_max['geode'] = geode
                print(f'ore={ore} (robot={ore_robot})')
                print(f'clay={clay} (robot={clay_robot})')
                print(f'obsidian={obsidian} (robot={obsidian_robot})')
                print(f'geode={geode} (robot={geode_robot})')
                print(f'found {geode}')
            return geode
        else:
            if can_build('geode', ore=ore, clay=clay, obsidian=obsidian, geode=geode):
                robot_item = 'geode'
                new_items = {
                    'ore': ore + ore_robot,
                    'clay': clay + clay_robot,
                    'obsidian': obsidian + obsidian_robot,
                    'geode': geode + geode_robot,
                }
                robot_items = {
                    'ore_robot': ore_robot,
                    'clay_robot': clay_robot,
                    'obsidian_robot': obsidian_robot,
                    'geode_robot': geode_robot,
                }
                robot_items[f'{robot_item}_robot'] += 1
                for item in ['ore', 'clay', 'obsidian', 'geode']:
                    if item in blueprint[robot_item]:
                        new_items[item] -= blueprint[robot_item][item]

                iterate(i+1, **new_items, **robot_items)
            else:
                new_items = {
                    'ore': ore + ore_robot,
                    'clay': clay + clay_robot,
                    'obsidian': obsidian + obsidian_robot,
                    'geode': geode + geode_robot,
                }
                robot_items = {
                    'ore_robot': ore_robot,
                    'clay_robot': clay_robot,
                    'obsidian_robot': obsidian_robot,
                    'geode_robot': geode_robot,
                }
                iterate(i+1, **new_items, **robot_items)

                for robot_item in ['obsidian', 'clay', 'ore']:
                    if can_build(robot_item, ore=ore, clay=clay, obsidian=obsidian, geode=geode):
                        new_items = {
                            'ore': ore + ore_robot,
                            'clay': clay + clay_robot,
                            'obsidian': obsidian + obsidian_robot,
                            'geode': geode + geode_robot,
                        }
                        robot_items = {
                            'ore_robot': ore_robot,
                            'clay_robot': clay_robot,
                            'obsidian_robot': obsidian_robot,
                            'geode_robot': geode_robot,
                        }
                        robot_items[f'{robot_item}_robot'] += 1
                        for item in ['ore', 'clay', 'obsidian', 'geode']:
                            if item in blueprint[robot_item]:
                                new_items[item] -= blueprint[robot_item][item]

                        iterate(i+1, **new_items, **robot_items)

    iterate(0)
    return data_max['geode']



def solve_part2(data):
    pass


def test_part1():
    data = test_data
    result = 0
    for index in range(len(data)):
        b_result = solve_part1(data[index])
        print(f'Blueprint {index+1} is {b_result}')
        if index ==  0:
            assert b_result == 9
        else:
            assert b_result == 12
        result += (index+1) * b_result
    assert result == 33


def part1():
    data = load_data()
    result = 0
    for index in range(len(data)):
        b_result = solve_part1(data[index])
        print(f'Blueprint {index+1} is {b_result}')
        result += (index+1) * b_result
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
