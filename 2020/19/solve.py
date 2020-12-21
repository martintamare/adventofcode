#!/usr/bin/env python
import re
import itertools

test_data = [
    '0: 4 1 5',
    '1: 2 3 | 3 2',
    '2: 4 4 | 5 5',
    '3: 4 5 | 5 4',
    '4: "a"',
    '5: "b"',
    '',
    'ababbb',
    'bababa',
    'abbbab',
    'aaabbb',
    'aaaabbb',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def process_data(data):
    rule_regex = re.compile(r'^(\d+): (.*)$')
    rules = {}
    messages = []

    for line in data:
        m = rule_regex.search(line)
        if m:
            index, rule_data = m.groups()
            index = int(index)
            rules[index] = rule_data
        elif line:
            messages.append(line)
    return rules, messages


def process_data_2(data):
    rule_regex = re.compile(r'^(\d+): (.*)$')
    rules = {}
    messages = []

    for line in data:
        m = rule_regex.search(line)
        if m:
            index, rule_data = m.groups()
            index = int(index)
            if index == 8:
                rules[index] = '42 | 42 8'
            elif index == 11:
                rules[index] = '42 31 | 42 11 31'
            else:
                rules[index] = rule_data
        elif line:
            messages.append(line)
    return rules, messages


class Rule:
    def __init__(self, rule, index, ruleset):
        self.ruleset = ruleset
        self.index = index
        self.groups = []
        self._len = None
        self.valid_data = {}

        if re.search('"."', rule):
            self.value = rule[1]
        else:
            self.value = None
            rules = rule.split('|')
            for r in rules:
                group = []
                for char in r.split(' '):
                    try:
                        char = int(char.strip())
                        group.append(char)
                    except ValueError:
                        continue

                self.groups.append(group)

    def __len__(self):
        if self._len is not None:
            return self._len

        if self.value is not None:
            self._len = len(self.value)
            return self._len
        else:
            total = 0
            for rule_index in self.groups[0]:
                total += len(self.ruleset.rules[rule_index])
            self._len = total
            return total

    def match(self, message):
        if len(message) != len(self):
            return False

        if self.groups:
            for group in self.groups:
                is_match = True
                group_index = 0
                for index in group:
                    rule = self.ruleset.rules[index]
                    if rule.match(message[group_index:group_index+len(rule)]):
                        group_index += len(rule)
                        continue
                    else:
                        is_match = False
                        break
                if is_match:
                    return True
            return False
        else:
            return message == self.value

    def get_valid_data(self, index):
        if index not in self.valid_data:
            rule = self.ruleset.rules[index]
            index_length = len(rule)
            valid_data = set()
            for to_test in itertools.product('ab', repeat=index_length):
                to_test = ''.join(to_test)
                if re.fullmatch(rule.pattern, to_test):
                    valid_data.add(to_test)
            self.valid_data[index] = valid_data
        return self.valid_data[index]

    def match_part_2(self, message):
        """
        Match 8 and 11.
        This 42* the 31*
        """
        init_message = message
        valid_data_42 = self.get_valid_data(42)
        valid_data_31 = self.get_valid_data(31)

        # Keep finding 42 pattern
        pattern_42 = r'^({0})'.format('|'.join(list(valid_data_42)))
        matches_42 = []
        m_42 = re.match(pattern_42, message)
        while m_42:
            len_42 = len(m_42.group(0))
            matches_42.append(m_42.group(0))
            message = message[len_42:]
            m_42 = re.match(pattern_42, message)

        # Now keep finding 31 pattern
        pattern_31 = r'^({0})'.format('|'.join(list(valid_data_31)))
        matches_31 = []
        m_31 = re.match(pattern_31, message)
        while m_31:
            len_31 = len(m_31.group(0))
            matches_31.append(m_31.group(0))
            message = message[len_31:]
            m_31 = re.match(pattern_31, message)

        # Message must be empty at this point
        if message:
            return False

        len_42 = len(matches_42)
        len_31 = len(matches_31)

        # At least one 42
        if not len_42:
            return False

        # At least one 31
        if not len_31:
            return False

        # At least 42 > 31
        if len(matches_42) > len(matches_31):
            print(f'message {init_message} valid !')
            return True
        else:
            return False

    @property
    def pattern(self):
        if self.value is not None:
            return self.value
        else:
            patterns = []
            for group in self.groups:
                pattern = ''
                for index in group:
                    if index == self.index:
                        pattern += '({0})+'.format(patterns[0])
                        continue
                    else:
                        rule = self.ruleset.rules[index]
                        pattern += rule.pattern
                if self.index in group:
                    patterns.append(f'({pattern})+')
                else:
                    patterns.append(pattern)
            return '({0})'.format('|'.join(patterns))


class RuleSet:
    def __init__(self, rules):
        self.rules = {}
        for index, rule in rules.items():
            self.rules[index] = Rule(rule, index, self)

    def match(self, message):
        if self.rules[0].match(message):
            return True
        else:
            return False

    def match_part_2(self, message):
        if self.rules[0].match_part_2(message):
            return True
        else:
            return False


def find_message_that_match(rules, messages):
    ruleset = RuleSet(rules)
    total = 0
    for message in messages:
        if ruleset.match(message):
            total += 1
    return total


def find_message_that_match_part_2(rules, messages):
    ruleset = RuleSet(rules)
    total = 0
    for message in messages:
        if ruleset.match_part_2(message):
            total += 1
    return total


def test_part1():
    data = test_data
    rules, messages = process_data(data)
    result = find_message_that_match(rules, messages)
    print(f'test1 is {result}')
    assert result == 2


def test_part2():
    data = [
        '42: 9 14 | 10 1',
        '9: 14 27 | 1 26',
        '10: 23 14 | 28 1',
        '1: "a"',
        '11: 42 31',
        '5: 1 14 | 15 1',
        '19: 14 1 | 14 14',
        '12: 24 14 | 19 1',
        '16: 15 1 | 14 14',
        '31: 14 17 | 1 13',
        '6: 14 14 | 1 14',
        '2: 1 24 | 14 4',
        '0: 8 11',
        '13: 14 3 | 1 12',
        '15: 1 | 14',
        '17: 14 2 | 1 7',
        '23: 25 1 | 22 14',
        '28: 16 1',
        '4: 1 1',
        '20: 14 14 | 1 15',
        '3: 5 14 | 16 1',
        '27: 1 6 | 14 18',
        '14: "b"',
        '21: 14 1 | 1 14',
        '25: 1 1 | 1 14',
        '22: 14 14',
        '8: 42',
        '26: 14 22 | 1 20',
        '18: 15 15',
        '7: 14 5 | 1 21',
        '24: 14 1',
        '',
        'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
        'bbabbbbaabaabba',
        'babbbbaabbbbbabbbbbbaabaaabaaa',
        'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
        'bbbbbbbaaaabbbbaaabbabaaa',
        'bbbababbbbaaaaaaaabbababaaababaabab',
        'ababaaaaaabaaab',
        'ababaaaaabbbaba',
        'baabbaaaabbaaaababbaababb',
        'abbbbabbbbaaaababbbbbbaaaababb',
        'aaaaabbaabaaaaababaa',
        'aaaabbaaaabbaaa',
        'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
        'babaaabbbaaabaababbaabababaaab',
        'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
    ]
    rules, messages = process_data(data)
    result = find_message_that_match(rules, messages)
    print(f'test2 normal is {result}')
    assert result == 3
    rules, messages = process_data_2(data)
    ruleset = RuleSet(rules)

    messages_to_test = {
        'aaaaabbaabaaaaababaa': True,
        'aaaabbaaaabbaaa': False,
        'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa': True,
        'aaabbbbbbaaaabaababaabababbabaaabbababababaaa': True,
        'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba': True,
        'ababaaaaaabaaab': True,
        'ababaaaaabbbaba': True,
        'abbbbabbbbaaaababbbbbbaaaababb': True,
        'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa': False,
        'baabbaaaabbaaaababbaababb': True,
        'babaaabbbaaabaababbaabababaaab': False,
        'babbbbaabbbbbabbbbbbaabaaabaaa': True,
        'bbabbbbaabaabba': True,
        'bbbababbbbaaaaaaaabbababaaababaabab': True,
        'bbbbbbbaaaabbbbaaabbabaaa': True,
    }
    for message, wanted_result in messages_to_test.items():
        result = ruleset.match_part_2(message)
        print(f'testing message {message} for {wanted_result}')
        assert result == wanted_result


def part1():
    data = load_data()
    rules, messages = process_data(data)
    result = find_message_that_match(rules, messages)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    rules, messages = process_data(data)
    result = find_message_that_match_part_2(rules, messages)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
