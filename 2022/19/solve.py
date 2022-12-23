#!/usr/bin/env python
import math

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

    ore = 0
    clay = 0
    obsidian = 0
    geode = 0
    ore_robot = 1
    clay_robot = 0
    obsidian_robot = 0
    geode_robot = 0
    data_max = {'geode': 0}
    geodes = list(map(lambda x: 0, range(25)))
    time_cache = {}
    cache = {}

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

        if geode > geodes[i]:
            geodes[i] = geode
        elif geode < geodes[i]:
            return geode

        # Iteration max
        if i == 24:
            if data_max['geode'] is None:
                data_max['geode'] = geode
                print(f'new_max is {geode}')
            elif geode > data_max['geode']:
                data_max['geode'] = geode
                print(f'new_max is {geode}')
            return geode

        # Add smart break according to iteration we can estimate creation or geode or not ?
        cache_index = f'{i}_{ore}_{clay}_{obsidian}_{geode}_{ore_robot}_{clay_robot}_{obsidian_robot}_{geode_robot}'
        time_to_build_new_geode_robot = None
        if cache_index in time_cache:
            time_to_build_new_geode_robot = time_cache[cache_index]
        else:
            current_items = {
                'ore': ore,
                'clay': clay,
                'obsidian': obsidian,
                'geode': geode,
            }
            robot_items = {
                'ore_robot': ore_robot,
                'clay_robot': clay_robot,
                'obsidian_robot': obsidian_robot,
                'geode_robot': geode_robot,
            }
            times = []
            time_to_build = {}
            for item in ['ore', 'clay', 'obsidian', 'geode']:
                time = 0
                for subitem in ['ore', 'clay', 'obsidian']:
                    if subitem in blueprint[item]:
                        needed = max(0, blueprint[item][subitem] - current_items[subitem])

                        if robot_items[f'{subitem}_robot'] == 0:
                            # We dont have any robot for this
                            # We will need time_to_build this robot + number of ressource needed
                            time_needed = needed + time_to_build[subitem]
                        else:
                            time_needed = math.ceil(needed / robot_items[f'{subitem}_robot'])
                        time = max(time, time_needed)
                times.append(time)
                time_to_build[item] = time

            time_to_build_new_geode_robot = max(times)
            time_cache[cache_index] = time_to_build_new_geode_robot

        if False:
        #if 24 - i < time_to_build_new_geode_robot:
            geode += (24 -i) * geode_robot
            if data_max['geode'] is None:
                data_max['geode'] = geode
                print(f'new_max is {geode}')
            elif geode > data_max['geode']:
                data_max['geode'] = geode
                print(f'new_max is {geode}')
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

                for x in range(24-i, 24+1):
                    geode += geode_robot
                    if geode > geodes[x]:
                        geodes[x] = geode

                if data_max['geode'] is None:
                    data_max['geode'] = geode
                    print(f'new_max is {geode}')
                elif geode > data_max['geode']:
                    data_max['geode'] = geode
                    print(f'new_max is {geode}')
                return geode
                # iterate(i+1, **new_items, **robot_items)
            else:
                cache_index = f'{i+1}_{ore+ore_robot}_{clay+clay_robot}_{obsidian+obsidian_robot}_{geode+geode_robot}_{ore_robot}_{clay_robot}_{obsidian_robot}_{geode_robot}'
                if cache_index in cache:
                    maximum = cache[cache_index]
                else:
                    res = None
                    maximum = None

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
                    cache_index = f'{i+1}_{ore+ore_robot}_{clay+clay_robot}_{obsidian+obsidian_robot}_{geode+geode_robot}_{ore_robot}_{clay_robot}_{obsidian_robot}_{geode_robot}_normal'
                    if cache_index in cache:
                        res = cache[cache_index]
                    else:
                        res = iterate(i+1, **new_items, **robot_items)
                    if maximum is None:
                        maximum = res
                    elif res > maximum:
                        maximum = res

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

                            cache_index = f'{i+1}_{new_items["ore"]}_{new_items["clay"]}_{new_items["obsidian"]}_{new_items["geode"]}_{robot_items["ore_robot"]}_{robot_items["clay_robot"]}_{robot_items["obsidian_robot"]}_{robot_items["geode_robot"]}_{robot_item}'
                            if cache_index in cache:
                                res = cache[cache_index]
                            else:
                                res = iterate(i+1, **new_items, **robot_items)
                            res = iterate(i+1, **new_items, **robot_items)
                            if maximum is None:
                                maximum = res
                            elif res > maximum:
                                maximum = res
                    cache[cache_index] = maximum
                return maximum

    test = iterate(0)
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
    assert result < 3085
    assert result > 706
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
