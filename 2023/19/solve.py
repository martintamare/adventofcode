#!/usr/bin/env python
import operator

test_data = [
    'px{a<2006:qkq,m>2090:A,rfg}',
    'pv{a>1716:R,A}',
    'lnx{m>1548:A,A}',
    'rfg{s<537:gd,x>2440:R,A}',
    'qs{s>3448:A,lnx}',
    'qkq{x<1416:A,crn}',
    'crn{x>2662:A,R}',
    'in{s<1351:px,qqz}',
    'qqz{s>2770:qs,m<1801:hdj,R}',
    'gd{a>3333:R,R}',
    'hdj{m>838:A,pv}',
    '',
    '{x=787,m=2655,a=1222,s=2876}',
    '{x=1679,m=44,a=2067,s=496}',
    '{x=2036,m=264,a=79,s=2244}',
    '{x=2461,m=1339,a=466,s=291}',
    '{x=2127,m=1623,a=2188,s=1013}',
]

class Instruction:
    def __init__(self, instruction, workflow):
        self.instruction = instruction
        self.operator = None
        self.source_attr = None
        self.condition = None
        self.workflow = workflow
        self.workflows = workflow.workflows

        if ':' in self.instruction:
            condition = self.instruction.split(':')[0]
            destination = self.instruction.split(':')[1]
            source_attr = condition[0]
            source_operator = condition[1]
            source_value = int(condition[2:])
            if source_operator == '>':
                source_operator = operator.gt
            elif source_operator == '<':
                source_operator = operator.lt
            else:
                print(f"TODO {source_operator=}")
                exit(0)
            self.source_attr = source_attr
            self.operator = source_operator
            self.condition_value = source_value
            self.destination = destination
        else:
            self.destination = self.instruction

    def __repr__(self):
        return f"{self.instruction}"

    def match(self, rating):
        self.next_workflow = None
        if self.operator is None:
            self.next_workflow = self.instruction
            return True
            if self.instruction == 'A':
                print(f"TODO {self.operator=} {self.instruction=}")
                print(self.instruction)
                exit(0)
        else:
            rating_attr = getattr(rating, self.source_attr)
            result = self.operator(rating_attr, self.condition_value)
            if result:
                self.next_workflow = self.destination
            return result

class Workflow:
    def __init__(self, name, instructions, workflows):
        self.workflows = workflows
        self.instructions = []
        for instruction in instructions:
            self.instructions.append(Instruction(instruction, self))
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class Rating:
    def __init__(self, x, m, a, s, workflows):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.workflows = workflows
        self.current_workflow = workflows['in']
        self.valid = False

    @property
    def total(self):
        return self.x + self.m + self.a + self.s

    def __repr__(self):
        return f"x={self.x} m={self.m} a={self.a} s={self.s}"

    def iterate(self):
        next_workflow = None
        for instruction in self.current_workflow.instructions:
            print(f"testing {instruction}")
            if instruction.match(self):
                print(f"{instruction} match {self}")
                next_workflow = instruction.next_workflow
                if next_workflow in self.workflows:
                    self.current_workflow = self.workflows[next_workflow]
                    return True
                elif next_workflow == 'A':
                    self.valid = True
                return False
        return False


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

def get_data(data):
    workflows = {}
    ratings = []

    mode = 'workflow'
    for line in data:
        if not line:
            mode = 'ratings'
            continue
        if mode == 'workflow':
            name, workflow_data = line.split('{')
            workflow_data = workflow_data[:-1].split(',')
            workflow = Workflow(name, workflow_data, workflows)
            workflows[name] = workflow
        else:
            line = line[1:-1]
            items = line.split(',')
            creation_params = {'workflows': workflows}
            for item in items:
                name, value = item.split('=')
                value = int(value)
                creation_params[name] = value
            rating = Rating(**creation_params)
            ratings.append(rating)
    return workflows, ratings


def solve_part1(data):
    workflows, ratings = get_data(data)

    result = 0
    for rating in ratings:
        print(f"iterate {rating}")
        while rating.iterate():
            pass
        if rating.valid:
            print(f"VALID {rating}")
            result += rating.total
        else:
            print(f"INVALID {rating}")
    return result
    pass


def solve_part2(data):
    workflows, ratings = get_data(data)
    source = workflows['in']

    valid_path = []

    def compute_path(node, current_path):
        false_instructions = []
        for instruction in node.instructions:
            if instruction.destination == 'A':
                new_valid_path = current_path.copy()
                new_valid_path.append((node, instruction, false_instructions.copy()))
                valid_path.append(new_valid_path)
            elif instruction.destination == 'R':
                pass
            else:
                new_path = current_path.copy()
                new_path.append((node, instruction, false_instructions.copy()))
                new_node = workflows[instruction.destination]
                compute_path(new_node, new_path)
            false_instructions.append(instruction)

    current_path = []
    compute_path(source, [])

    
    total = 0
    final_ranges = []
    for path in valid_path:
        ranges = {
            'x': [1, 4000],
            'm': [1, 4000],
            'a': [1, 4000],
            's': [1, 4000],
        }
        print("========================")
        print(f"{path=}")
        for node, instruction, false_instructions in path:
            l = instruction.source_attr
            if l:
                current_min = ranges[l][0]
                current_max = ranges[l][1]
                new_current_min = current_min
                new_current_max = current_max
                if instruction.operator == operator.gt:
                    new_current_min = instruction.condition_value + 1
                elif instruction.operator == operator.lt:
                    new_current_max = instruction.condition_value - 1
                ranges[l] = [max(current_min, new_current_min), min(new_current_max, current_max)]
                print(f"must {ranges=}")

            for false_instruction in false_instructions:
                l = false_instruction.source_attr
                if l:
                    current_min = ranges[l][0]
                    current_max = ranges[l][1]
                    new_current_min = current_min
                    new_current_max = current_max
                    if false_instruction.operator == operator.gt:
                        new_current_max = false_instruction.condition_value
                    elif false_instruction.operator == operator.lt:
                        new_current_min = false_instruction.condition_value
                    ranges[l] = [max(current_min, new_current_min), min(current_max, new_current_max)]
            print(f"must not {ranges=}")
        valid = True
        for item, data in ranges.items():
            min_item = data[0]
            max_item = data[1]
            if min_item > max_item:
                valid = False
                print(f"range {ranges} not valid")
                break
        if valid:
            final_ranges.append(ranges)

    added_ranges = []
    for ranges in final_ranges:
        if not added_ranges:
            added_ranges.append(ranges)
        else:
            global_overlap = False
            for test_ranges in added_ranges:
                overlap_with = []
                for char in ['x', 'm', 'a', 's']:
                    overlap = False
                    test = test_ranges[char]
                    current = ranges[char]
                    #print(f"comparing {char=} {test} vs {current}")
                    real_test = max(test[0], current[0]) < min(test[1], current[1])
                    print(f"{real_test=} {test} vs {current}")
                    if real_test:
                        overlap = True
                        overlap_with.append(char)
                    else:
                        pass
                print(f"{ranges=}")
                print(f"{test_ranges=}")
                print(f"{overlap_with=}")
                if len(overlap_with) == 4:
                    # une range overlap pas -> pas overlap
                    global_overlap = True
                    overlap_with.append(test_ranges)
                    input("")
            if not global_overlap:
                added_ranges.append(ranges)
            else:
                print(f"overlapping {ranges} with {overlap_with=}")
                for t in added_ranges:
                    print(f"{t}")
                exit(0)
    print("no")
    for ranges in added_ranges:
        print(f"{ranges}")
    total = 0
    for ranges in added_ranges:
        path_total = 1
        valid = True
        for item, data in ranges.items():
            min_item = data[0]
            max_item = data[1]
            current_possibility = data[1] - data[0] + 1
            path_total *= current_possibility
        total += path_total
    return total
    exit(0)

    added_ranges = []
    for ranges in final_ranges:
        if not added_ranges:
            added_ranges.append(ranges)
        else:
            global_overlap = True
            overlap_with = []
            for char in ['x', 'm', 'a', 's']:
                overlap = False
                for test_ranges in added_ranges:
                    test = test_ranges[char]
                    current = ranges[char]
                    #print(f"comparing {char=} {test} vs {current}")
                    if range(max(test[0], current[0]), min(test[1], current[1])):
                        overlap = True
                        overlap_with.append(char)
                    else:
                        pass
                if not overlap:
                    global_overlap = False
                    break
            if not global_overlap:
                print(f"non overlapping {ranges} with")
                for t in added_ranges:
                    print(f"{t}")
                added_ranges.append(ranges)
                continue
            else:
                # need to find intersection
                print(f"overlapping {ranges} with {overlap_with=}")
                for t in added_ranges:
                    print(f"{t}")
                exit(0)
                print(ranges)
                print(added_ranges)
                exit(0)

    exit(0)
    return total




def test_part1():
    data = test_data.copy()
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 19114


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 332145


def test_part2():
    data = test_data
    result = solve_part2(data)
    wanted_result = 167409079868000
    print(f'test2 is {result} diff={result-wanted_result}')
    assert result == 167409079868000


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
