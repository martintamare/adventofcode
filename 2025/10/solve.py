#!/usr/bin/env python
from itertools import combinations, combinations_with_replacement
from collections import defaultdict, Counter
from z3 import *

test_data = [
    "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
    "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
    "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Machine:
    def __init__(self, line):
        self.line = line
        splitted = line.split(" ")
        indicators = splitted[0]
        self.wanted_indicators = []
        for indicator in indicators[1:-1]:
            if indicator == ".":
                self.wanted_indicators.append(False)
            elif indicator == "#":
                self.wanted_indicators.append(True)
            else:
                raise Exception(f"jdnzajkdnazkjd {indicator=}")
        self.indicators = list(map(lambda x: False, indicators[1:-1]))
        self.init_indicators = list(map(lambda x: False, indicators[1:-1]))
        joltage_requirements = splitted[-1]
        self.wanted_joltages = list(map(int, joltage_requirements[1:-1].split(',')))
        min_joltage = min(self.wanted_joltages)
        self.min_joltages = list(map(lambda x: x - min_joltage + 1, self.wanted_joltages))
        self.joltage_factor = min_joltage
        self.joltages = list(map(lambda x: 0, joltage_requirements[1:-1].split(',')))
        self.init_joltages = self.joltages.copy()
        self.buttons = []
        for data in splitted[1:-1]:
            button = list(map(int, data[1:-1].split(',')))
            self.buttons.append(button)

    def __repr__(self):
        return f"{self.indicators=} {self.wanted_indicators=} {self.joltage_requirements=} {self.buttons=}"

    def reset_indicators(self):
        self.indicators = self.init_indicators.copy()

    def reset_joltages(self):
        self.joltages = self.init_joltages.copy()

    def press(self, button):
        for b_index in button:
            real_index = b_index
            self.indicators[real_index] = not self.indicators[real_index]

    def press_part2(self, button):
        for b_index in button:
            real_index = b_index
            self.joltages[real_index] += 1

    def valid(self):
        return self.indicators == self.wanted_indicators

    def valid_part2(self):
        #print(f"{self.joltages=} {self.wanted_joltages=}")
        return self.joltages == self.wanted_joltages

    def part1(self):
        press = 1
        while True:
            buttons_combinations = combinations(self.buttons, press)
            for combination in buttons_combinations:
                self.reset_indicators()
                for button in combination:
                    self.press(button)
                if self.valid():
                    print(f"Valid ! {press=}")
                    return press
            press += 1

    def part2(self):
        result = 0


        # Using z3
        # Déclare variables
        variables = []
        for index, button in enumerate(self.buttons):
            name = f"Button_{index}"
            variable = Int(name)
            variables.append(variable)

        optimizer = Optimize()

        # Contraintes press > 0
        for press in variables:
            optimizer.add(press >= 0)

        # Contraintes pour les press
        for j_index, joltage in enumerate(self.wanted_joltages):
            press_variables = []
            # Extraire toutes les variables
            for b_index, button in enumerate(self.buttons):
                if j_index in button:
                    press_variables.append(variables[b_index])

            # La somme de toutes ces variable doit être egale au joltage
            optimizer.add(sum(press_variables) == joltage)

        # Solve
        optimizer.minimize(sum(variables))
        print(optimizer)
        print(optimizer.check())
        model = optimizer.model()

        result = 0
        for index, variable in enumerate(variables):
            variable_result = model[variable].as_long()
            print(f"{index=} {variable_result=}")
            result += variable_result
        print(f"{result=}")
        return result

    def part2_try(self):
        # Make an index link to buttons
        index_to_buttons = []
        for index in range(len(self.wanted_joltages)):
            joltage = self.wanted_joltages[index]
            index_buttons = []
            for button in self.buttons:
                if index in button:
                    index_buttons.append(button)
            index_to_buttons.append({
                "joltage": joltage,
                "buttons": sorted(index_buttons, key=len, reverse=True),
                "index": index,
                })
        index_to_buttons = sorted(index_to_buttons, key=lambda x: x["joltage"])
        print(f"{index_to_buttons=}")
        # On fixe les objectifs
        # On choisi intelligement le prochain button 
        # On sort de la boucle facilement
        # On utilise des structures légère car ça va bourriner
        min_press = None
        min_press_counter = None

        print(self.buttons)
        print(self.wanted_joltages)

        seen = set()
        ko = set()
        iteration = 0

        def choose_next_iteration_order(current):
            # Order by lowest joltages
            ok_indexes = get_ok_indexes(current)
            buttons = []
            if ok_indexes:
                for elem in index_to_buttons:
                    if elem["index"] not in ok_indexes:
                        continue
                    for button in elem["buttons"]:
                        if any(index not in ok_indexes for index in button):
                            continue
                        if button not in buttons:
                            buttons.append(button)
            if not buttons:
                #next_counter = Counter(tuple(x) for x in current)
                #hash_key = hashable_counter(next_counter)
                #ko.add(hash_key)
                pass
            return buttons

        def _compute_score(current):
            joltages = self.init_joltages.copy()
            for button in current:
                for index in button:
                    joltages[index] += 1
            results = [wanted - current for wanted, current in zip(self.wanted_joltages, joltages)]
            return results

        def get_ok_indexes(current):
            results = _compute_score(current)
            to_return = []
            for index in range(len(results)):
                if results[index] <= 0:
                    continue
                to_return.append(index)
            return to_return

        def compute_score(current):
            results = _compute_score(current)
            first = results[0]
            if all(r == first for r in results):
                if first == 0:
                    return 0
            # We did to much
            if any(v < 0 for v in results):
                return -1
            else:
                return 1

        def hashable_counter(counter: Counter) -> tuple:
            """
            Converts a Counter object into a hashable tuple representation.
            """
            # 1. Get items, 2. Sort by key, 3. Convert to a tuple
            return tuple(sorted(counter.items()))


        def recurse(current=[]):
            nonlocal min_press
            nonlocal min_press_counter
            nonlocal iteration
            iteration += 1
            if iteration % 100000 == 0:
                print(f"{iteration=}")

            iteration_buttons = choose_next_iteration_order(current)
            for button in iteration_buttons:
                next_current = current + [button]
                if min_press is not None and min_press <= len(next_current):
                    continue
                #next_counter = Counter(tuple(x) for x in next_current)
                #hash_key = hashable_counter(next_counter)
                #print(f"{hash_key=}")
                #if hash_key in seen:
                #    return False
                #if hash_key in ko:
                #    return False

                result = compute_score(next_current)
                if result < 0:
                    input("do this happen ?")
                    return False
                elif result == 0:
                    #seen.add(hash_key)
                    if min_press is None:
                        min_press = len(next_current)
                        min_press_counter = Counter(tuple(x) for x in next_current)
                        print(f"BINGO {min_press}")
                        return True
                    elif len(next_current) < min_press:
                        min_press = len(next_current)
                        min_press_counter = Counter(tuple(x) for x in next_current)
                        print(f"BINGO {min_press}")
                        return True
                    else:
                        return False
                else:
                    recurse(next_current)
                
        recurse()
        return min_press






def solve_part1(data):
    result = 0
    for line in data:
        machine = Machine(line)
        result += machine.part1()
    return result

def solve_part2(data):
    result = 0
    size = len(data)
    iteration = 0
    for line in data:
        print(f"=============== {iteration}/{size} ================")
        machine = Machine(line)
        result += machine.part2()
        iteration += 1
    return result


def test_part1():
    data = test_data
    r1 = solve_part1([data[0]])
    assert r1 == 2
    r2 = solve_part1([data[1]])
    assert r2 == 3
    r3 = solve_part1([data[2]])
    assert r3 == 2


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data
    r1 = solve_part2([data[0]])
    assert r1 == 10
    r2 = solve_part2([data[1]])
    assert r2 == 12
    r3 = solve_part2([data[2]])
    assert r3 == 11


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
