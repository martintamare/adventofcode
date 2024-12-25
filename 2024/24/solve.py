#!/usr/bin/env python
from itertools import combinations
import copy

test_data = [
    "x00: 1",
    "x01: 1",
    "x02: 1",
    "y00: 0",
    "y01: 1",
    "y02: 0",
    "",
    "x00 AND y00 -> z00",
    "x01 XOR y01 -> z01",
    "x02 OR y02 -> z02",
]

test_data_2 = [
    "x00: 1",
    "x01: 0",
    "x02: 1",
    "x03: 1",
    "x04: 0",
    "y00: 1",
    "y01: 1",
    "y02: 1",
    "y03: 1",
    "y04: 1",
    "",
    "ntg XOR fgs -> mjb",
    "y02 OR x01 -> tnw",
    "kwq OR kpj -> z05",
    "x00 OR x03 -> fst",
    "tgd XOR rvg -> z01",
    "vdt OR tnw -> bfw",
    "bfw AND frj -> z10",
    "ffh OR nrd -> bqk",
    "y00 AND y03 -> djm",
    "y03 OR y00 -> psh",
    "bqk OR frj -> z08",
    "tnw OR fst -> frj",
    "gnj AND tgd -> z11",
    "bfw XOR mjb -> z00",
    "x03 OR x00 -> vdt",
    "gnj AND wpb -> z02",
    "x04 AND y00 -> kjc",
    "djm OR pbm -> qhw",
    "nrd AND vdt -> hwm",
    "kjc AND fst -> rvg",
    "y04 OR y02 -> fgs",
    "y01 AND x02 -> pbm",
    "ntg OR kjc -> kwq",
    "psh XOR fgs -> tgd",
    "qhw XOR tgd -> z09",
    "pbm OR djm -> kpj",
    "x03 XOR y03 -> ffh",
    "x00 XOR y04 -> ntg",
    "bfw OR bqk -> z06",
    "nrd XOR fgs -> wpb",
    "frj XOR qhw -> z04",
    "bqk OR frj -> z07",
    "y03 OR x01 -> nrd",
    "hwm AND bqk -> z03",
    "tgd XOR rvg -> z12",
    "tnw OR pbm -> gnj",
]

test_data_3 = [
    "x00: 0",
    "x01: 1",
    "x02: 0",
    "x03: 1",
    "x04: 0",
    "x05: 1",
    "y00: 0",
    "y01: 0",
    "y02: 1",
    "y03: 1",
    "y04: 0",
    "y05: 1",
    "",
    "x00 AND y00 -> z05",
    "x01 AND y01 -> z02",
    "x02 AND y02 -> z01",
    "x03 AND y03 -> z03",
    "x04 AND y04 -> z04",
    "x05 AND y05 -> z00",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class System:
    def __init__(self, data, lenght):
        self.data = data
        self.lenght = lenght
        self.operations = []
        for line in data:
            splitted = line.split(' ')
            w1 = splitted[0].strip()
            operation = splitted[1].strip()
            w2 = splitted[2].strip()
            destination = splitted[-1].strip()
            self.operations.append([w1, operation, w2, destination])


    def __repr__(self):
        return f"{self.lenght=} {self.data=}"

    def test(self, index, swapped=[]):
        x_index = f"x{index:02}"
        y_index = f"y{index:02}"
        z_index = f"z{index:02}"

        to_test = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]

        def test_permutations(operations):
            is_ok = True
            for combinaison in to_test:
                x_value = combinaison[0]
                y_value = combinaison[1]
                wanted_z_value = combinaison[2]

                wires = {}
                wires[x_index] = x_value
                wires[y_index] = y_value

                stop = False
                while not stop:
                    new_operations = []
                    has_changes = False
                    for operation in operations:
                        w1 = operation[0]
                        operand = operation[1]
                        w2 = operation[2]
                        destination = operation[3]
                        if w1 in wires and w2 in wires:
                            has_changes = True
                            if operand == "AND":
                                wires[destination] = wires[w1] & wires[w2]
                            elif operand == "OR":
                                wires[destination] = wires[w1] | wires[w2]
                            elif operand == "XOR":
                                wires[destination] = wires[w1] ^ wires[w2]
                            else:
                                raise Exception("fazif,nazfaz")
                        else:
                            new_operations.append(operation)

                    if not has_changes or z_index in wires:
                        stop = True
                    else:
                        operations = new_operations

                z_computed = wires.get(z_index, None)
                if z_computed is None or z_computed != wanted_z_value:
                    #print(f"{combinaison=} is not valid {z_computed=} {wanted_z_value=}")
                    is_ok = False
                    break
                else:
                    #print(f"{combinaison=} is valid {z_computed=} wanted={combinaison[2]}")
                    pass
            return is_ok


        # No changes
        test = test_permutations(self.operations)
        if test:
            print("OK without changes")
            return []

        new_swapped = []
        for swap in combinations(self.operations, 2):
            t1, t2 = swap
            old_destination_1 = t1[3]
            old_destination_2 = t2[3]
            #print(f"Swapping {old_destination_1} and {old_destination_2}")
            t1[3] = old_destination_2
            t2[3] = old_destination_1
            test = test_permutations(self.operations)
            if test:
                new_swapped.append(swap)
            else:
                pass
            t1[3] = old_destination_1
            t2[3] = old_destination_2

        return new_swapped


def solve_part1(data):
    wires = {}
    mode = "init"
    data = data.copy()

    while data: 
        line = data.pop(0)
        if line == "":
            mode = "operations"
            continue
        elif mode == "init":
            wire = line.split(':')[0].strip()
            value = int(line.split(':')[1].strip())
            wires[wire] = value
        elif mode == "operations":
            splitted = line.split(' ')
            w1 = splitted[0].strip()
            operation = splitted[1].strip()
            w2 = splitted[2].strip()
            destination = splitted[-1].strip()
            if w1 in wires and w2 in wires:
                if operation == "AND":
                    wires[destination] = wires[w1] & wires[w2]
                elif operation == "OR":
                    wires[destination] = wires[w1] | wires[w2]
                elif operation == "XOR":
                    wires[destination] = wires[w1] ^ wires[w2]
                else:
                    raise Exception("fazif,nazfaz")
            else:
                data.append(line)

    result = ''
    for key in sorted(list(filter(lambda x: x.startswith("z"), wires.keys())), reverse=True):
        result += f"{wires[key]}"
    print(result)
    return int(result, 2)


def solve_part2(data):
    mode = "init"

    lenght = 0
    operations = []
    for line in data:
        if line == "":
            mode = "operations"
        elif mode == "operations":
            operations.append(line)
        elif mode == "init":
            lenght += 1
        else:
            pass

    ok_length = int(lenght/2)
    system = System(operations, ok_length)
    swapped = {}
    for index in range(ok_length):
        print(f"Testing {index=}")
        swapped[index] = system.test(index)
        print(f"{len(swapped[index])} OK")
        print(swapped[index])
    final_set = set()
    for swaps in swapped.values():
        for swap in swaps:
            t1, t2 = swap
            final_set.add(t1[-1])
            final_set.add(t2[-1])
    print(final_set)
    return ','.join(sorted(list(final_set)))


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 4

    data = test_data_2
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 2024


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')


def test_part2():
    data = test_data_3
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 'z00,z01,z02,z05'


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
