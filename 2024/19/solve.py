#!/usr/bin/env python
import re
from collections import Counter, defaultdict
from heapq import heappop, heappush

test_data = [
    "r, wr, b, g, bwu, rb, gb, br",
    "",
    "brwrr",
    "bggr",
    "gbbr",
    "rrbgbr",
    "ubwu",
    "bwurrg",
    "brgr",
    "bbrgwb",
]


CACHE={}
INVALID_CACHE={}

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Design:
    def __init__(self, data, regex, patterns):
        self.data = data
        self.regex = regex
        self.patterns = patterns

    def __repr__(self):
        return f"Design {self.data}"

    @property
    def length(self):
        return len(self.data)

    @property
    def possible_but_too_long(self):
        return self.regex.match(self.data)

    @property
    def ways(self):
        impossible = set()
        seen = {}

        def smart_search(line):
            if line == "":
                return 1
            elif line in seen:
                return seen[line]
            elif line in impossible:
                return 0

            match = list(filter(lambda x: line.startswith(x), self.patterns))
            if not len(match):
                return 0

            result = 0
            for pattern in match:
                new_line = line[len(pattern):]
                new_search = smart_search(new_line)
                if new_search == 0:
                    impossible.add(new_line)
                else:
                    result += new_search
            seen[line] = result
            return result

        return smart_search(self.data)


    @property
    def possible(self):
        """
        Compute a path from start to end using patterns.

        Move the index toward the end to get a match.

        Be smart about what to cache
        Use only the biggest design (biggest pattern size)
        1) Invalid design cache ?
        2) Valid design with a step forward

        """

        q = [
                # start_index, patterns
                (0, [])
        ]

        seen = defaultdict(Counter)

        while q:
            (current_index, patterns)  = heappop(q)

            #print(f"{current_index=} current_data={self.data[0:current_index]} remaining_data={self.data[current_index:]}")
            if current_index == self.length:
                return True
                continue

            # Skipping if we already tested current_index
            if current_index in seen:
                coming_from_index = current_index - len(patterns[0])
                if coming_from_index in seen[current_index]:
                    seen[current_index][coming_from_index] += 1
                    continue

            # Build the list of next items to test
            if len(patterns):
                coming_from_index = current_index - len(patterns[0])
                seen[current_index][coming_from_index] += 1

            next_q = []
            for pattern in self.patterns:
                len_pattern = len(pattern)
                final_index = current_index+len_pattern
                if final_index > self.length:
                    continue

                to_test = self.data[current_index:final_index]
                #print(f"{to_test} == {pattern} : {to_test == pattern}")
                if to_test == pattern:
                    new_index = current_index + len_pattern
                    new_patterns = [pattern] + patterns
                    next_q.append((new_index, new_patterns))


            if next_q:
                for to_append in next_q:
                    heappush(q, to_append)

        return False

        print(self)
        print(f"{seen=}")
        
        def compute_pattern_possibilities(current_index):
            if current_index == 0:
                return 1
            elif current_index in seen:
                coming_from_keys = seen[current_index].keys()
                coming_from_length = len(coming_from_keys)
                print(f"{current_index=} {seen[current_index]=} {coming_from_length=}")

                result = 0
                for key in coming_from_keys:
                    key_result = seen[current_index][key] * compute_pattern_possibilities(key)
                    print(f"{key_result=}")
                    result += key_result
                return result

        total = 0
        #result = compute_pattern_possibilities(len(self.data) - 1)
        #print(f"{result=}")
        #total += result
        self.ways = total
        return True


def solve_part1(data):
    patterns = list(map(lambda x: x.strip(), data[0].split(',')))
    sorted_patterns = sorted(patterns, key=len, reverse=True)
    # Big pattern first
    regex_pattern = "|".join(sorted_patterns)
    pattern_str = f"^(?:{regex_pattern})+$"
    regex = re.compile(pattern_str)

    designs = list(map(lambda x: Design(x, regex, sorted_patterns), data[2:]))

    print(f"We have {len(designs)} designs to test")
    result = 0
    for index, design in enumerate(designs):
        if design.possible:
            print(f"{design=} OK")
            result += 1
        else:
            print(f"{design=} KO")
    return result


def solve_part2(data):
    patterns = list(map(lambda x: x.strip(), data[0].split(',')))
    sorted_patterns = sorted(patterns, key=len, reverse=True)
    # Big pattern first
    regex_pattern = "|".join(sorted_patterns)
    pattern_str = f"^(?:{regex_pattern})+$"
    regex = re.compile(pattern_str)

    designs = list(map(lambda x: Design(x, regex, sorted_patterns), data[2:]))

    print(f"We have {len(designs)} designs to test")
    result = 0
    for index, design in enumerate(designs):
        if design.ways:
            print(f"{design=} OK ways={design.ways}")
            result += design.ways
        else:
            print(f"{design=} KO")
    return result


def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 6


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')
    assert result == 278


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 16


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
