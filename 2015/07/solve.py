#!/usr/bin/env python

test_data = [
    '123 -> x',
    '456 -> y',
    'x AND y -> d',
    'x OR y -> e',
    'x LSHIFT 2 -> f',
    'y RSHIFT 2 -> g',
    'NOT x -> h',
    'NOT y -> i',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Wire:
    def __init__(self, line, circuit):
        destination = line.split(' -> ')[1]
        source = line.split(' -> ')[0]
        self.id = destination
        self.input_a = None
        self.input_b = None
        self.gate = None
        self.circuit = circuit
        self._signal = None

        args = source.split(' ')
        if len(args) == 1:
            self.input_a = source
        elif len(args) == 2:
            self.gate = args[0]
            self.input_a = args[1]
        elif len(args) == 3:
            self.gate = args[1]
            self.input_a = args[0]
            self.input_b = args[2]
        else:
            raise Exception()

    def get_input_a(self):
        try:
            input_a = int(self.input_a)
            return input_a
        except ValueError:
            if self.input_a in self.circuit:
                return self.circuit[self.input_a]._signal
            else:
                return None

    def get_input_b(self):
        try:
            input_b = int(self.input_b)
            return input_b
        except ValueError:
            if self.input_b in self.circuit:
                return self.circuit[self.input_b]._signal
            else:
                return None

    @property
    def signal(self):
        if self.gate is None:
            return self.get_input_a()
        elif self.gate == 'NOT':
            if self.get_input_a() is None:
                return None
            else:
                return ~ self.get_input_a() & 0xFFFF
        elif self.gate == 'AND':
            if self.get_input_a() is None:
                return None
            elif self.get_input_b() is None:
                return None
            else:
                return (self.get_input_a() & self.get_input_b()) & 0xFFFF
        elif self.gate == 'OR':
            if self.get_input_a() is None:
                return None
            elif self.get_input_b() is None:
                return None
            else:
                return (self.get_input_a() | self.get_input_b()) & 0xFFFF
        elif self.gate == 'RSHIFT':
            if self.get_input_a() is None:
                return None
            elif self.get_input_b() is None:
                return None
            else:
                return (self.get_input_a() >> self.get_input_b()) & 0xFFFF
        elif self.gate == 'LSHIFT':
            if self.get_input_a() is None:
                return None
            elif self.get_input_b() is None:
                return None
            else:
                return (self.get_input_a() << self.get_input_b()) & 0xFFFF
        else:
            raise Exception('fnazjkfnazkjfnazkf')

    def __str__(self):
        if self.gate is not None:
            return f'{self.id} {self.signal} from {self.input_a} {self.gate} {self.input_b}'
        else:
            return f'{self.id} {self.signal} from {self.input_a}'
             

def compute_circuit(data):
    circuit = {}
    for line in data:
        wire = Wire(line, circuit)
        circuit[wire.id] = wire

    while True:
        has_some_change = 0
        for wire_id in sorted(circuit.keys()):
            print(f'tesing {wire_id}')
            wire = circuit[wire_id]
            new_signal = wire.signal
            if new_signal is None:
                continue
            if new_signal != wire._signal:
                has_some_change += 1
                wire._signal = new_signal
                print(f'{wire} updated')
        if not has_some_change:
            print(f'Finished')
            return circuit
        else:
            print(f'We did {has_some_change} changes')
            has_some_change = 0


def test_part1():
    test_results = {
        'd': 72,
        'e': 507,
        'f': 492,
        'g': 114,
        'h': 65412,
        'i': 65079,
        'x': 123,
        'y': 456,
    }
    results = compute_circuit(test_data)
    print(f'{results}')
    for key, value in test_results.items():
        assert key in results
        assert results[key]._signal == value


def test_part2():
    data = test_data
    cur= None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = load_data()
    results = compute_circuit(data)
    print(f'part1 is {results["a"]._signal}')


def part2():
    data = load_data()
    circuit = compute_circuit(data)
    a_value = circuit['a']._signal
    circuit['b'].input_a = a_value
    circuit['b'].gate = None
    for wire_id in sorted(circuit.keys()):
        circuit[wire_id]._signal = None

    while True:
        has_some_change = 0
        for wire_id in sorted(circuit.keys()):
            wire = circuit[wire_id]
            new_signal = wire.signal
            if new_signal is None:
                continue
            if new_signal != wire._signal:
                has_some_change += 1
                wire._signal = new_signal
                print(f'{wire} updated')
        if not has_some_change:
            print(f'Finished')
            break
        else:
            print(f'We did {has_some_change} changes')
            has_some_change = 0

    print(f'part2 is {circuit["a"]._signal}')


test_part1()
part1()
#test_part2()
part2()
