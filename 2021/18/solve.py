#!/usr/bin/env python

test_data = [
    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
    '[7,[5,[[3,8],[1,4]]]]',
    '[[2,[2,2]],[8,[8,1]]]',
    '[2,9]',
    '[1,[[[9,3],9],[[9,0],[0,7]]]]',
    '[[[5,[7,4]],7],1]',
    '[[[[4,2],2],6],[8,7]]',
]

class SnailfishNumber:
    def __init__(self, parent=None):
        self.left = None
        self.right = None
        self.parent = parent

    def __repr__(self):
        return f'[{self.left},{self.right}]'

    def add(self, value):
        if self.left is None:
            self.left = value
        elif self.right is None:
            self.right = value
        else:
            raise Exception('Add but already full ?!')

    def __add__(self, other):
        new = SnailfishNumber()
        new.left = self
        self.parent = new
        new.right = other
        other.parent = new
        return new.reduce()

    def __eq__(self, other):
        left_ok = False
        right_ok = False

        if isinstance(self, int) and isinstance(other, int):
            return self == other
        elif isinstance(self, int):
            return False
        elif isinstance(other, int):
            return False

        if (isinstance(self.left, SnailfishNumber) and isinstance(other.left, SnailfishNumber)) \
            or (isinstance(self.left, int) and isinstance(other.left, int)):
            left_ok = self.left == other.left
            if not left_ok:
                return left_ok

        if (isinstance(self.right, SnailfishNumber) and isinstance(other.right, SnailfishNumber)) \
            or (isinstance(self.right, int) and isinstance(other.right, int)):
            right_ok = self.right == other.right
            if not right_ok:
                return right_ok

        return left_ok and right_ok

    @property
    def parents(self):
        ret = []
        current = self
        while True:
            if current.parent:
                ret.append(current.parent)
                current = current.parent
            else:
                break
        return ret

    def explosion(self):
        if isinstance(self.left, int) and \
            isinstance(self.right, int):
            if len(self.parents) > 3:
                return self
        else:
            if isinstance(self.left, SnailfishNumber):
                left_explosion = self.left.explosion()
                if left_explosion:
                    return left_explosion
            if isinstance(self.right, SnailfishNumber):
                right_explosion = self.right.explosion()
                if right_explosion:
                    return right_explosion
            return None


    def splitted(self):
        if isinstance(self.left, SnailfishNumber):
            splitted = self.left.splitted()
            if splitted:
                return splitted
        elif self.left > 9:
            return self

        if isinstance(self.right, SnailfishNumber):
            splitted = self.right.splitted()
            if splitted:
                return splitted
        elif self.right > 9:
            return self

        return None

    @property
    def first_left_regular_number(self):
        return self._first_regular_number('left')

    @property
    def first_right_regular_number(self):
        return self._first_regular_number('right')

    def _first_regular_number(self, side):

        # Find first parent with value
        first_parent_with_side_value = None

        current = self
        while True:
            if current.parent is None:
                break

            test_node = getattr(current.parent, side)
            #print(f'testing for {side} : {current} left: {current.left} right: {current.right} parent: {current.parent} test_node {test_node}')


            if isinstance(test_node, int):
                first_parent_with_side_value = current.parent
                break

            elif isinstance(test_node, SnailfishNumber):
                if test_node != current:
                    first_parent_with_side_value = current.parent
                    break
                else:
                    if current.parent:
                        current = current.parent
                    else:
                        break

        # Now find first right value
        if first_parent_with_side_value is None:
            return None

        # Now start to look for the other side
        other_side = 'left'
        if side == 'left':
            other_side = 'right'

        # A int on right -> return
        if isinstance(getattr(first_parent_with_side_value, side), int):
            return first_parent_with_side_value

        # Else, go other_side until find a valid value
        start_parent_to_look_for_other_side = getattr(first_parent_with_side_value, side)
        result = None
        while True:
            test_node = getattr(start_parent_to_look_for_other_side, other_side)
            if isinstance(test_node, SnailfishNumber):
                start_parent_to_look_for_other_side = test_node
            else:
                result = start_parent_to_look_for_other_side
                break
        return result


    def split(self):
        """
        To split a regular number, replace it with a pair; the left element of the pair should be the regular 
        number divided by two and rounded down, while the right element of the pair should be the regular number 
        divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
        """
        to_split_branch = None
        to_split_value = None
        if isinstance(self.left, int) and self.left > 9:
            to_split_branch = 'left'
            to_split_value = self.left
        elif isinstance(self.right, int) and self.right > 9:
            to_split_branch = 'right'
            to_split_value = self.right
        else:
            raise Exception('You not split here ??')

        new_left = int(to_split_value/2)
        new_right = to_split_value - new_left
        new_number = SnailfishNumber(parent=self)
        new_number.add(new_left)
        new_number.add(new_right)

        if to_split_branch == 'left':
            self.left = new_number
        else:
            self.right = new_number

        





    def explode(self):
        """
        To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any),
        and the pair's right value is added to the first regular number to the right of the exploding pair (if any).

        Exploding pairs will always consist of two regular numbers.
        Then, the entire exploding pair is replaced with the regular number 0.
        """
        first_left_regular_number = self.first_left_regular_number
        print(f'first_left_regular_number {first_left_regular_number}')
        first_right_regular_number = self.first_right_regular_number
        print(f'first_right_regular_number {first_right_regular_number}')

        left_value = self.left
        right_value = self.right

        if first_left_regular_number:
            if isinstance(first_left_regular_number.left, SnailfishNumber):
                print(f'left found -> {first_left_regular_number.right} + {left_value}')
                first_left_regular_number.right = first_left_regular_number.right + left_value
            else:
                print(f'left found -> {first_left_regular_number.left} + {left_value}')
                first_left_regular_number.left = first_left_regular_number.left + left_value
        if first_right_regular_number:
            if isinstance(first_right_regular_number.left, SnailfishNumber):
                print(f'right found -> {first_right_regular_number.right} + {right_value}')
                first_right_regular_number.right = first_right_regular_number.right + right_value
            else:
                print(f'right found -> {first_right_regular_number.left} + {right_value}')
                first_right_regular_number.left = first_right_regular_number.left + right_value

        if self.parent.left == self:
            self.parent.left = 0
        else:
            self.parent.right = 0

    def explosions_candidates(self):
        canditates = []

        if isinstance(self.left, SnailfishNumber):
            canditates += self.left.explosions_candidates()

        if isinstance(self.right, SnailfishNumber):
            canditates += self.right.explosions_candidates()

        if isinstance(self.left, int) and \
            isinstance(self.right, int):
            if len(self.parents) > 3:
                canditates.append(self)
        return canditates


    def reduce(self):

        while True:
            print(f'reducing {self}')
            # Test explosion
            explosion = None

            # List all explosions
            # Take most left
            explosions = self.explosions_candidates()
            print(f'canditates are {explosions}')

            if isinstance(self.left, SnailfishNumber):
                explosion = self.left.explosion()

            if explosion is None:
                if isinstance(self.right, SnailfishNumber):
                    explosion = self.right.explosion()

            if explosion is not None:
                print(f'explosion {explosion}')
                explosion.explode()
                print(f'now is {self}')
                continue

            splitted = None
            if isinstance(self.left, SnailfishNumber):
                splitted = self.left.splitted()
            elif self.left > 9:
                splitted = self

            if splitted is None:
                if isinstance(self.right, SnailfishNumber):
                    splitted = self.right.splitted()
                elif self.right > 9:
                    splitted = self

            if splitted is not None:
                print(f'split {splitted}')
                splitted.split()
                print(f'now is {self}')

            if splitted is None and explosion is None:
                break
                
        return self



class RawNumber:
    def __init__(self, value):
        self.value = value
        self.root = None
        self.snailfished()

    def __add__(self, other):
        return self.root + other.root

    def reduce(self):
        return self.root.reduce()

    def snailfished(self):
        graph = []
        current = None
        so_far = ''

        for char in self.value:
            so_far += char
            if char == '[':
                new = SnailfishNumber(parent=current)
                if current is not None:
                    current.add(new)
                else:
                    self.root = new
                current = new
            elif char == ']':
                current = current.parent
            elif char == ',':
                pass
            else:
                current.add(int(char))


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


def test_part1():
    test = '[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]'
    number = RawNumber(test)
    assert f'{number.root}' == test

    test = '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]'
    number = RawNumber(test)
    assert f'{number.root}' == test

    left = '[1,2]'
    right = '[[3,4],5]'
    left_number = RawNumber(left)
    right_number = RawNumber(right)
    addition_number = left_number + right_number
    assert f'{addition_number}' == '[[1,2],[[3,4],5]]'

    test = '[[[[[9,8],1],2],3],4]'
    number = RawNumber(test)
    reduced_number = number.reduce() 
    print(f'reduced_number is {reduced_number}')
    assert f'{reduced_number}' == '[[[[0,9],2],3],4]'

    test = '[7,[6,[5,[4,[3,2]]]]]'
    number = RawNumber(test)
    reduced_number = number.reduce() 
    print(f'reduced_number is {reduced_number}')
    assert f'{reduced_number}' == '[7,[6,[5,[7,0]]]]'

    test = '[[6,[5,[4,[3,2]]]],1]'
    number = RawNumber(test)
    reduced_number = number.reduce() 
    print(f'reduced_number is {reduced_number}')
    assert f'{reduced_number}' == '[[6,[5,[7,0]]],3]'

    test = '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'
    number = RawNumber(test)
    reduced_number = number.reduce() 
    print(f'reduced_number is {reduced_number}')
    assert f'{reduced_number}' == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'

    left = '[[[[4,3],4],4],[7,[[8,4],9]]]'
    right = '[1,1]'
    left_number = RawNumber(left)
    right_number = RawNumber(right)
    addition_number = left_number + right_number
    print(f'addition_number is {addition_number}')

    array = [
        '[1,1]',
        '[2,2]',
        '[3,3]',
        '[4,4]',
    ]
    current = None
    for number in array:
        if current is None:
            current = RawNumber(number).root
        else:
            new = RawNumber(number).root
            current = current + new
    assert f'{current}' == '[[[[1,1],[2,2]],[3,3]],[4,4]]'

    array = [
        '[1,1]',
        '[2,2]',
        '[3,3]',
        '[4,4]',
        '[5,5]',
    ]
    current = None
    for number in array:
        if current is None:
            current = RawNumber(number).root
        else:
            new = RawNumber(number).root
            current = current + new
    assert f'{current}' == '[[[[3,0],[5,3]],[4,4]],[5,5]]'

    array = [
        '[1,1]',
        '[2,2]',
        '[3,3]',
        '[4,4]',
        '[5,5]',
        '[6,6]',
    ]
    current = None
    for number in array:
        if current is None:
            current = RawNumber(number).root
        else:
            new = RawNumber(number).root
            current = current + new
    assert f'{current}' == '[[[[5,0],[7,4]],[5,5]],[6,6]]'

    print('================================================')
    print('================================================')
    print('================================================')
    print('================================================')


    array = test_data
    current = None
    for number in array:
        if current is None:
            current = RawNumber(number).root
        else:
            new = RawNumber(number).root
            current = current + new
            print(f'{current}')
            input()
    assert f'{current}' == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
    exit(0)
    result = None
    print(f'test1 is {result}')
    assert result == 25


def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = load_data()
    result = None
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = None
    print(f'part2 is {result}')


test_part1()
#part1()
#test_part2()
#part2()
