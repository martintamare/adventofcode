#!/usr/bin/env python

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
        if pulse.state == 'low':
            self.ok = True
        return []

class Broadcaster(Module):
    def __init__(self, name, destinations, modules):
        super().__init__(name, 'broadcaster', destinations, modules)

    def process(self, pulse):
        pulses = []
        for destination in self.destinations:
            module = self.modules[destination]
            pulse = Pulse(pulse.state, self, module, self.modules)
            pulses.append(pulse)
        return pulses


class FlipFlopModule(Module):
    def __init__(self, name, destinations, modules):
        self.state = 'low'
        super().__init__(name, 'flipflop', destinations, modules)

    def toggle(self):
        if self.state:
            self.state = False
        else:
            self.state = True

    def process(self, pulse):
        pulses = []

        if pulse.state == 'high':
            return pulses


        if self.state == 'high':
            self.state = 'low'
        else:
            self.state = 'high'

        for destination in self.destinations:
            module = self.modules[destination]
            pulse = Pulse(self.state, self, module, self.modules)
            pulses.append(pulse)

        return pulses



class ConjuctionModule(Module):
    def __init__(self, name, destinations, modules):
        self.sources = {}
        self.source_states = {}
        super().__init__(name, 'conjunction', destinations, modules)

    def add_source(self, module):
        if module.name not in self.sources:
            self.sources[module.name] = module
            self.source_states[module.name] = 'low'

    def process(self, pulse):
        pulses = []

        # When a pulse is received, the conjunction module first updates its memory for that input
        source_states = []
        for source in self.source_states.keys():
            if pulse.source.name == source:
                self.source_states[source] = pulse.state
                source_states.append(pulse.state)
            else:
                last_state = self.source_states[source]
                source_states.append(last_state)
            

        if not len(source_states):
            print(f"{source_states=} {pulse.state=} {self}")

        if len(set(source_states)) == 1 and source_states[0] == 'high':
            new_pulse_state = 'low'
        else:
            new_pulse_state = 'high'

        for destination in self.destinations:
            module = self.modules[destination]
            pulse = Pulse(new_pulse_state, self, module, self.modules)
            pulses.append(pulse)
        return pulses


class Button(Module):
    def __init__(self, name, modules):
        super().__init__(name, 'button', ['broadcaster'], modules)

    def process(self, pulse):
        pulses = []
        for destination in self.destinations:
            module = self.modules[destination]
            pulse = Pulse(pulse.state, self, module, self.modules)
            pulses.append(pulse)
        return pulses


class Pulse:
    def __init__(self, state, source, destination, modules):
        self.state = state
        self.modules = modules
        self.source = source
        self.destination = destination

    def __repr__(self):
        return f"{self.source.name} -{self.state} -> {self.destination.name}"

    def launch(self):
        pulses = self.destination.process(self)
        return pulses



def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def solve_part1(data):
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

    button = Button('button', modules)
    modules['button'] = button
    init_pulse = Pulse('low', button, broadcaster, modules)

    def process():
        pulses = [init_pulse]
        low_count = 1
        high_count = 0
        while True:
            new_pulses = []
            for pulse in pulses:
                next_pulses = pulse.launch()
                new_pulses += next_pulses
                for p in next_pulses:
                    if p.state == 'high':
                        high_count += 1
                    else:
                        low_count += 1
            pulses = new_pulses
            if not pulses:
                break
        return low_count, high_count

    total_low = 0
    total_high = 0
    for i in range(1000):
        low, high = process()
        total_low += low
        total_high += high
    print(f"{total_low=} {total_high=}")
    return total_low * total_high



def solve_part2(data):
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



    button = Button('button', modules)
    modules['button'] = button
    init_pulse = Pulse('low', button, broadcaster, modules)

    def process():
        pulses = [init_pulse]
        while True:
            new_pulses = []
            for pulse in pulses:
                next_pulses = pulse.launch()
                new_pulses += next_pulses
            pulses = new_pulses
            if not pulses:
                break

    index = 1
    rx = modules['rx']
    while not rx.ok:
        if index % 1000 == 0:
            print(index)
        process()
        index += 1
    return index


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test_data is {result}')
    assert result == 32000000

    data = test_data_2
    result = solve_part1(data)
    print(f'test_data_2 is {result}')
    assert result == 11687500


def part1():
    data = load_data()
    result = solve_part1(data)
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
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
part2()
