#!/usr/bin/env python
import math

test_data = [
    "Register A: 729",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 0,1,5,4,3,0",
]

test_data_2 = [
    "Register A: 2024",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 0,3,5,4,3,0",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Operand:
    def __init__(self, value, registers):
        self.data = value
        self.registers = registers

    @property
    def literal(self):
        return self.data

    @property
    def combo(self):
        if self.data <= 3:
            return self.data
        elif self.data == 4:
            return self.registers["a"]
        elif self.data == 5:
            return self.registers["b"]
        elif self.data == 6:
            return self.registers["c"]
        elif self.data == 7:
            raise Exception("Not a valid program")

    def __repr__(self):
        return f"Operand {self.literal=} {self.combo=}"

class Opcode:
    def __init__(self, instruction, value, operand, registers):
        self.instruction = instruction
        self.value = value
        self.operand = operand
        self.registers = registers
        self.next_instruction = None

    def __repr__(self):
        return f"{self.value=} {self.operand=}"

    def run(self):
        self.next_instruction = self.instruction + 2

        if self.value == 0:
            op = "adv"
            numerator = self.registers["a"]
            denominator = math.pow(2, self.operand.combo)
            result = int(numerator/denominator)
            self.registers["a"] = result
        elif self.value == 1:
            op = "bxl"
            x1 = self.registers["b"]
            x2 = self.operand.literal
            result = x1 ^ x2
            self.registers["b"] = result
        elif self.value == 2:
            op = "bst"
            result = self.operand.combo % 8
            self.registers["b"] = result
        elif self.value == 3:
            op = "jnz"
            if self.registers["a"] == 0:
                return
            else:
                self.next_instruction = self.operand.literal
        elif self.value == 4:
            op = "bxc"
            x1 = self.registers["b"]
            x2 = self.registers["c"]
            result = x1 ^ x2
            self.registers["b"] = result
        elif self.value == 5:
            op = "out"
            result = self.operand.combo % 8
            return result
        elif self.value == 6:
            op = "bdv"
            numerator = self.registers["a"]
            denominator = math.pow(2, self.operand.combo)
            result = int(numerator/denominator)
            self.registers["b"] = result
        elif self.value == 7:
            op = "cdv"
            numerator = self.registers["a"]
            denominator = math.pow(2, self.operand.combo)
            result = int(numerator/denominator)
            self.registers["c"] = result


class Program:
    def __init__(self, values, registers):
        self.values = values
        self.registers = registers
        self.wanted = ','.join(map(str, values))
        self.init_a = self.registers["a"]

    def run_smart(self):
        program = self.values
        instruction = 0
        values = []
        instructions = []
        printed = {}
        while instruction < len(program):
            instructions.append(instruction)
            operand = Operand(program[instruction+1], self.registers)
            opcode = Opcode(instruction, program[instruction], operand, self.registers)
            result = opcode.run()
            if result is not None:
                values.append(result)
                to_test = ','.join(map(str, values))
                if not self.wanted.startswith(to_test):
                    return to_test
            instruction = opcode.next_instruction
        return ','.join(map(str, values))

    def run(self):
        program = self.values
        instruction = 0
        values = []
        while instruction < len(program):
            operand = Operand(program[instruction+1], self.registers)
            opcode = Opcode(instruction, program[instruction], operand, self.registers)
            result = opcode.run()
            if result is not None:
                values.append(result)
            instruction = opcode.next_instruction
        return ','.join(map(str, values))


def solve_part1(data):
    a = int(data[0].split(':')[1].strip())
    b = int(data[1].split(':')[1].strip())
    c = int(data[2].split(':')[1].strip())
    registers = {
        "a": a,
        "b": b,
        "c": c,
    }
    program = Program(list(map(int, data[-1].split(':')[1].strip().split(','))), registers)
    return program.run()


def solve_part2(data):
    a = int(data[0].split(':')[1].strip())
    b = int(data[1].split(':')[1].strip())
    c = int(data[2].split(':')[1].strip())
    registers = {
        "a": a,
        "b": b,
        "c": c,
    }

    wanted = data[-1].split(':')[1].strip()
    # Find first out


    max_length = None
    max_a = None
    power_of_eight_to_apply = None
    delta_a = None
    current_a = 1
    a_to_test = [current_a]
    while True:
        a = a_to_test.pop(0)
        registers = {
            "a": a,
            "b": b,
            "c": c,
        }
        program = Program(list(map(int, wanted.split(','))), registers)
        result = program.run_smart()
        if result == wanted:
            return a

        len_result = len(result.split(','))
        if len_result:
            if max_length is None:
                max_length = len_result
            elif len_result > max_length:
                # a mod 8 need octal
                octal_str = oct(a)

                # We found a result of x digits -> we want to keep octal for this one
                to_keep = octal_str[-len_result:]
                octal_str = '0o' + octal_str[3:]

                # Next number will be 8** a specific power
                power_of_eight_to_apply = len(to_keep) - 2

                # Keep the delta
                delta_a = int(octal_str, 8)

                # If we have a delta, current_a is reseted
                if delta_a:
                    current_a = 1
                else:
                    pass
                max_length = len_result

        new_a_to_test = current_a + 1
        current_a += 1
        if power_of_eight_to_apply:
            new_a_to_test *= 8**power_of_eight_to_apply
        if delta_a:
            new_a_to_test += delta_a
        a_to_test.append(int(new_a_to_test))


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == "4,6,3,5,6,3,5,2,1,0"


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == "7,1,5,2,4,0,7,6,1"


def test_part2():
    data = test_data_2
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 117440


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
