#!/usr/bin/env python

test_data = [
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Password:
    def __init__(self, value):
        self.value = value

    def next(self):
        test_password = Password(self.iterate())
        iteration = 1
        while not test_password.valid:
            test_password = Password(test_password.iterate())
            iteration += 1
            if iteration % 100 == 0:
                print(f'Tested {iteration} password')
        return test_password.value

    def iterate(self):
        self.update_value(len(self.value) - 1)
        return self.value

    def update_value(self, index):
        if self.value[index] == 'z':
            self.value = self.value[:index] + 'a' + self.value[index + 1:]
            self.update_value(index-1)
        else:
            wanted_ord = ord(self.value[index]) + 1
            replace_char = chr(wanted_ord)
            self.value = self.value[:index] + replace_char + self.value[index + 1:]  # noqa

    @property
    def valid(self):
        # Invalid letter
        for letter in ['i', 'o', 'l']:
            if letter in self.value:
                return False

        # Duplicate letter we want to different
        double_letters = set()
        for index in range(1, len(self.value)):
            if self.value[index-1] == self.value[index]:
                double_letters.add(self.value[index])
        if len(double_letters) < 2:
            return False

        # increasing letters should be present
        increasing_letters_are_present = False
        for index in range(2, len(self.value)):
            first = ord(self.value[index-2])
            second = ord(self.value[index-1])
            third = ord(self.value[index])
            if first + 1 != second:
                continue
            if second + 1 != third:
                continue
            increasing_letters_are_present = True
            break
        if not increasing_letters_are_present:
            return False

        return True


def test_part1():
    assert not Password('hijklmmn').valid
    assert not Password('abbceffg').valid
    assert not Password('abbcegjk').valid
    assert Password('abcdefgh').next() == 'abcdffaa'
    assert Password('ghijklmn').next() == 'ghjaabcc'


def part1():
    result = Password('hxbxwxba').next()
    print(f'part1 is {result}')
    assert result == 'hxbxxyzz'


def part2():
    result = Password('hxbxxyzz').next()
    print(f'part2 is {result}')


test_part1()
part1()
part2()
