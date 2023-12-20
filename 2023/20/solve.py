#!/usr/bin/env python
from collections import Counter
from math import lcm

test_data = [
    'broadcaster -> a, b, c',
    '%a -> b',
    '%b -> c',
    '%c -> inv',
    '&inv -> a',
]


test_data_2 = [
    'broadcaster -> a',
    '%a -> inv, con',
    '&inv -> b',
    '%b -> con',
    '&con -> output',
]

class Module:
    def __init__(self, name, _type, destinations, modules):
        self.name = name
        self.destinations = destinations
        self.modules = modules
        self.type = _type
        self.ok = False

    def __repr__(self):
        return self.name

    def process(self, pulse):
        if pulse.state == 0:
            self.ok = True
        return []

class Broadcaster(Module):
    def __init__(self, name, destinations, modules):
        super().__init__(name, 'broadcaster', destinations, modules)

    def process(self, pulse, source):
        pulses = []
        for destination in self.destinations:
            module = self.modules[destination]
            pulse = (pulse, self, module)
            pulses.append(pulse)
        return pulses


class FlipFlopModule(Module):
    def __init__(self, name, destinations, modules):
        self.state = 0
        super().__init__(name, 'flipflop', destinations, modules)

    def toggle(self):
        if self.state:
            self.state = False
        else:
            self.state = True

    def process(self, pulse, source):
        pulses = []

        if pulse:
            return pulses


        if self.state == 1:
            self.state = 0
        else:
            self.state = 1

        for destination in self.destinations:
            module = self.modules[destination]
            pulse = (self.state, self, module)
            pulses.append(pulse)

        return pulses



class ConjuctionModule(Module):
    def __init__(self, name, destinations, modules):
        self.source_states = {}
        super().__init__(name, 'conjunction', destinations, modules)

    def add_source(self, module):
        if module.name not in self.source_states:
            self.source_states[module.name] = 0

    def process(self, pulse, source):
        pulses = []

        # When a pulse is received, the conjunction module first updates its memory for that input
        source_states = []
        for source_module in self.source_states.keys():
            if source_module == source:
                self.source_states[source] = pulse.state
                source_states.append(pulse.state)
            else:
                last_state = self.source_states[source_module]
                source_states.append(last_state)
            

        print(f"{source_states=} {pulse=} {self}")

        if len(set(source_states)) == 1 and source_states[0] == 1:
            new_pulse_state = 0
        else:
            new_pulse_state = 1

        for destination in self.destinations:
            module = self.modules[destination]
            pulse = (new_pulse_state, self, module)
            pulses.append(pulse)
        return pulses



def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve(data, part=1):
    modules = {}
    broadcaster = None
    for line in data:
        source, destination = line.split(' -> ')
        destinations = destination.split(', ')
        if source == 'broadcaster':
            module = Broadcaster(source, destinations, modules)
            broadcaster = module
        elif source[0] == '&':
            module = ConjuctionModule(source[1:], destinations, modules)
        elif source[0] == '%':
            module = FlipFlopModule(source[1:], destinations, modules)
        else:
            print('fnajgaznfgjkazr')
            exit(0)
        modules[module.name] = module

    module_to_add = {}
    for module in modules.values():
        for destination in module.destinations:
            if destination not in modules:
                if destination not in module_to_add:
                    print(f"{destination=} has no module adding a dummy one")
                    new_module = Module(destination, 'dummy', [], modules)
                    module_to_add[destination] = new_module
    for module in module_to_add.values():
        modules[module.name] = module

    for module in modules.values():
        for destination in module.destinations:
            destination_module = modules[destination]
            if destination_module.type == 'conjunction':
                destination_module.add_source(module)

    init_pulse = (0, None, broadcaster)

    def process(press=None, needed_sources=None):
        queue = [init_pulse]
        low_count = 0
        high_count = 0
        while queue:
            pulse_in, source_module, destination_module = queue.pop(0)

            if pulse_in:
                high_count += 1
            else:
                low_count += 1

            pulse_out = None
            if destination_module.type == 'broadcaster':
                pulse_out = pulse_in
            elif destination_module.type == 'flipflop':
                if pulse_in:
                    continue
                elif destination_module.state:
                    pulse_out = 0
                    destination_module.state = 0
                else:
                    pulse_out = 1
                    destination_module.state = 1
            elif destination_module.type == 'conjunction':
                # When a pulse is received, the conjunction module first updates its memory for that input
                destination_module.source_states[source_module.name] = pulse_in
                # if it remembers high pulses for all inputs, it sends a low pulse
                if all(destination_module.source_states.values()):
                    pulse_out = 0
                else:
                    pulse_out = 1

                if needed_sources is not None:
                    if 'rx' in destination_module.destinations:
                        for source, state in destination_module.source_states.items():
                            if state:
                                needed_sources[source] = press
            else:
                continue

            if pulse_out is None:
                continue

            for destination in destination_module.destinations:
                next_destination = modules[destination]
                queue.append((pulse_out, destination_module, next_destination))

        if needed_sources is not None:
            if all(needed_sources.values()):
                modules['rx'].ok = True
                return

        return low_count, high_count

    if part == 1:
        total_low = 0
        total_high = 0
        for i in range(1000):
            low, high = process()
            total_low += low
            total_high += high
        print(f"{total_low=} {total_high=}")
        return total_low * total_high
    else:

        rx_conjunction = None
        for module in modules.values():
            if 'rx' in module.destinations:
                rx_conjunction = module
                break
        needed_sources = {}
        for source in rx_conjunction.source_states.keys():
            needed_sources[source] = 0

        index = 1
        while True:
            process(index, needed_sources)
            if modules['rx'].ok:
                return lcm(*list(needed_sources.values()))


            index += 1
        return index





def test_part1():
    data = test_data
    result = solve(data)
    print(f'test_data is {result}')
    assert result == 32000000

    data = test_data_2
    result = solve(data)
    print(f'test_data_2 is {result}')
    assert result == 11687500


def part1():
    data = load_data()
    result = solve(data)
    print(f'part1 is {result}')
    assert result > 519509025
    assert result == 670984704


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25


def part2():
    data = load_data()
    result = solve(data, part=2)
    print(f'part2 is {result}')
    assert result == 262775362119547


test_part1()
part1()
#test_part2()
part2()
