#!/usr/bin/env python
from itertools import combinations, permutations
from functools import cached_property
from collections import Counter, defaultdict
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

    @cached_property
    def all_indexes(self):
        data = []
        for i in range(45):
            data.append(f"x{i:02}")
            data.append(f"y{i:02}")
        return data

    @cached_property
    def operations_to_permute(self):
        # Result of guess_interesting_node
        test = [(['y05', 'AND', 'x05', 'mkq'], ['tsw', 'XOR', 'wwm', 'hdt']), (['y15', 'AND', 'x15', 'mht'], ['y15', 'XOR', 'x15', 'jgt']), (['tsw', 'XOR', 'wwm', 'hdt'], ['rnk', 'OR', 'mkq', 'z05']), (['x09', 'AND', 'y09', 'z09'], ['vkd', 'XOR', 'wqr', 'gbf']), (['x09', 'AND', 'y09', 'z09'], ['gbf', 'OR', 'ttm', 'pdk']), (['dpr', 'AND', 'nvv', 'z30'], ['dpr', 'XOR', 'nvv', 'nbf'])]
        to_test = set()
        for swap in test:
            t1, t2 = swap
            to_test.add(t1[3])
            to_test.add(t2[3])

        result = list(filter(lambda x: x[3] in to_test, self.operations))
        return result

    def test_interesting_node(self):
        result_index = defaultdict(list)
        max_index = None
        c_index = 1
        for c in combinations(self.operations_to_permute, 8):
            print(f"{c_index=}")
            p_index = 1
            for swap in permutations(list(c), 8):
                if p_index % 1000 == 0:
                    print(f"{c_index=} {p_index=}")
                p_index += 1

                t0, t1, t2, t3, t4, t5, t6, t7 = swap
                old_0 = t0[3]
                old_1 = t1[3]
                old_2 = t2[3]
                old_3 = t3[3]
                old_4 = t4[3]
                old_5 = t5[3]
                old_6 = t6[3]
                old_7 = t7[3]

                t0[3] = old_1
                t1[3] = old_0
                t2[3] = old_3
                t3[3] = old_2
                t4[3] = old_5
                t5[3] = old_4
                t6[3] = old_7
                t7[3] = old_6

                ok_index = 0
                missed = 0
                for index in range(self.lenght):
                    result = self.test_index(index)
                    if result:
                        ok_index += 1
                    else:
                        missed += 1
                    if missed > 2:
                        break

                if ok_index < 42:
                    pass
                elif max_index is None:
                    max_index = ok_index
                    print(f"{ok_index=}")
                    print(f"{swap=}")
                    result_index[ok_index].append(swap)
                elif ok_index > max_index:
                    max_index = ok_index
                    print(f"{ok_index=}")
                    print(f"{swap=}")
                    result_index[ok_index].append(swap)

                t0[3] = old_0
                t1[3] = old_1
                t2[3] = old_2
                t3[3] = old_3
                t4[3] = old_4
                t5[3] = old_5
                t6[3] = old_6
                t7[3] = old_7
            c_index += 1

        for index, value in result_index.items():
            print(f"{index=} {value=}")



    def guess_interesting_node(self):
        result_swap = {}
        result_index = defaultdict(list)
        max_index = None
        test = 1
        for swap in combinations(self.operations, 2):
            if test % 100 == 0:
                print(f"iteration {test}")
            test += 1

            t0, t1 = swap
            old_0 = t0[3]
            old_1 = t1[3]

            t0[3] = old_1
            t1[3] = old_0

            ok_index = 0
            missed = 0
            for index in range(self.lenght):
                result = self.test_index(index)
                if result:
                    ok_index += 1
                else:
                    missed += 1

                if missed > 3:
                    break

            result_swap[f"{swap}"] = ok_index
            result_index[ok_index].append(swap)

            if ok_index < 42:
                pass
            elif max_index is None:
                max_index = ok_index
                print(ok_index)
            elif ok_index > max_index:
                max_index = ok_index
                print(ok_index)
            elif ok_index == max_index:
                print(ok_index)
                print(f"swap={len(result_index[ok_index])}")

            t0[3] = old_0
            t1[3] = old_1
        print(result_index.get(42, None))
        print(result_index.get(43, None))
        exit(0)


    def test_index(self, index):
        x_index = f"x{index:02}"
        y_index = f"y{index:02}"
        z_index = f"z{index:02}"

        keys_to_set = []

        previous_index = False

        if index > 0:
            previous_index = True
            test_index = index
            while test_index > 0:
                test_index = test_index - 1
                previous_x_index = f"x{test_index:02}"
                previous_y_index = f"y{test_index:02}"
                keys_to_set.append(previous_x_index)
                keys_to_set.append(previous_y_index)

        def get_base_dict():
            base_dict = {}
            for key in self.all_indexes:
                base_dict[key] = 0
            return base_dict

        to_test = []
        if previous_index is False:
            base_dict = get_base_dict()
            base_dict[x_index] = 0
            base_dict[y_index] = 0
            to_test.append((base_dict, z_index, 0))

            base_dict = get_base_dict()
            base_dict[x_index] = 1
            base_dict[y_index] = 0
            to_test.append((base_dict, z_index, 1))

            base_dict = get_base_dict()
            base_dict[x_index] = 0
            base_dict[y_index] = 1
            to_test.append((base_dict, z_index, 1))

            base_dict = get_base_dict()
            base_dict[y_index] = 1
            base_dict[x_index] = 1
            to_test.append((base_dict, z_index, 0))
        else:
            base_dict = get_base_dict()
            base_dict[x_index] = 0
            base_dict[y_index] = 0
            to_test.append((base_dict, z_index, 0))

            base_dict = get_base_dict()
            base_dict[x_index] = 1
            base_dict[y_index] = 0
            to_test.append((base_dict, z_index, 1))

            base_dict = get_base_dict()
            base_dict[x_index] = 0
            base_dict[y_index] = 1
            to_test.append((base_dict, z_index, 1))

            base_dict = get_base_dict()
            base_dict[y_index] = 1
            base_dict[x_index] = 1
            to_test.append((base_dict, z_index, 0))

            base_dict = get_base_dict()
            base_dict[y_index] = 0
            base_dict[x_index] = 0
            for key in keys_to_set:
                base_dict[key] = 1
            to_test.append((base_dict, z_index, 1))

        if index == self.lenght - 1:
            base_dict = get_base_dict()
            base_dict[y_index] = 1
            base_dict[x_index] = 1
            for key in keys_to_set:
                base_dict[key] = 0
            next_z_index = f"z{index+1:02}"
            to_test.append((base_dict, next_z_index, 1))


        def test_permutations():

            is_ok = True
            to_return_path = None
            for combinaison in to_test:
                operations = self.operations
                data_to_set = combinaison[0]
                wanted_z_index = combinaison[1]
                wanted_z_value = combinaison[2]

                wires = {}
                for index, value in data_to_set.items():
                    wires[index] = value

                stop = False
                path = set()
                while not stop:
                    new_operations = []
                    has_changes = False
                    for operation in operations:
                        w1 = operation[0]
                        operand = operation[1]
                        w2 = operation[2]
                        destination = operation[3]
                        if w1 in wires and w2 in wires:
                            path.add(destination)
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

                    if not has_changes:
                        stop = True
                    elif wanted_z_index in wires:
                        stop = True
                    else:
                        operations = new_operations

                z_computed = wires.get(wanted_z_index, None)
                if z_computed is None or z_computed != wanted_z_value:
                    # print(f"{combinaison=} is not valid {z_computed=} {wanted_z_value=} {path=}")
                    is_ok = False
                    to_return_path = path
                    break
                else:
                    # print(f"{combinaison=} is valid {z_computed=} wanted={combinaison[1]}")
                    pass
            return is_ok, to_return_path


        # No changes
        test, path = test_permutations()
        return test



    def test(self, index, swapped):
        x_index = f"x{index:02}"
        y_index = f"y{index:02}"
        z_index = f"z{index:02}"

        keys_to_set = []

        previous_index = False

        if index > 0:
            previous_index = True
            test_index = index
            while test_index > 0:
                test_index = test_index - 1
                previous_x_index = f"x{test_index:02}"
                previous_y_index = f"y{test_index:02}"
                keys_to_set.append(previous_x_index)
                keys_to_set.append(previous_y_index)

        def get_base_dict():
            base_dict = {}
            return base_dict
            for key in self.all_indexes:
                base_dict[key] = 0
            return base_dict

        to_test = []
        if previous_index is False:
            base_dict = get_base_dict()
            base_dict[x_index] = 0
            base_dict[y_index] = 0
            to_test.append((base_dict, 0))

            base_dict = get_base_dict()
            base_dict[x_index] = 1
            base_dict[y_index] = 0
            to_test.append((base_dict, 1))

            base_dict = get_base_dict()
            base_dict[x_index] = 0
            base_dict[y_index] = 1
            to_test.append((base_dict, 1))

            base_dict = get_base_dict()
            base_dict[y_index] = 1
            base_dict[x_index] = 1
            to_test.append((base_dict, 0))
        else:
            base_dict = get_base_dict()
            base_dict[x_index] = 0
            base_dict[y_index] = 0
            to_test.append((base_dict, 0))

            base_dict = get_base_dict()
            base_dict[x_index] = 1
            base_dict[y_index] = 0
            to_test.append((base_dict, 1))

            base_dict = get_base_dict()
            base_dict[x_index] = 0
            base_dict[y_index] = 1
            to_test.append((base_dict, 1))

            base_dict = get_base_dict()
            base_dict[y_index] = 1
            base_dict[x_index] = 1
            to_test.append((base_dict, 0))

            base_dict = get_base_dict()
            base_dict[y_index] = 0
            base_dict[x_index] = 0
            for key in keys_to_set:
                base_dict[key] = 1
            to_test.append((base_dict, 1))

        def test_permutations():

            is_ok = True
            to_return_path = None
            for combinaison in to_test:
                operations = self.operations
                data_to_set = combinaison[0]
                wanted_z_value = combinaison[1]

                wires = {}
                for index, value in data_to_set.items():
                    wires[index] = value

                stop = False
                path = set()
                while not stop:
                    new_operations = []
                    has_changes = False
                    for operation in operations:
                        w1 = operation[0]
                        operand = operation[1]
                        w2 = operation[2]
                        destination = operation[3]
                        if w1 in wires and w2 in wires:
                            path.add(destination)
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

                    if not has_changes:
                        stop = True
                    elif z_index in wires:
                        stop = True
                    else:
                        operations = new_operations

                z_computed = wires.get(z_index, None)
                if z_computed is None or z_computed != wanted_z_value:
                    # print(f"{combinaison=} is not valid {z_computed=} {wanted_z_value=} {path=}")
                    is_ok = False
                    to_return_path = path
                    break
                else:
                    # print(f"{combinaison=} is valid {z_computed=} wanted={combinaison[1]}")
                    pass
            return is_ok, to_return_path


        # No changes
        test, path = test_permutations()
        if test:
            print("OK without changes")
            return swapped

        new_swapped = []
        current_c = 0
        for swap in combinations(self.operations, 2):
            if swapped is not None and swap not in swapped:
                continue

            t0, t1 = swap
            old_0 = t0[3]
            old_1 = t1[3]

            print(f"Swapping {old_0} and {old_1}")
            t0[3] = old_1
            t1[3] = old_0

            test = test_permutations()
            if test:
                new_swapped.append(swap)
            else:
                pass

            t0[3] = old_0
            t1[3] = old_1

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
    # system.guess_interesting_node()
    system.test_interesting_node()
    exit(0)
    print(system.operations_to_permute)
    swapped = None
    for index in range(ok_length):
        print(f"Testing {index=}")
        swapped  = system.test(index, swapped)
        if swapped is not None:
            print(f"{len(swapped)} OK")
        input(f"{index=} finished !")

    final_set = set()
    for swap in swapped:
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
#test_part2()
part2()
