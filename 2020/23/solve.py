#!/usr/bin/env python
import itertools

test_data = '389125467'


def load_data():
    return '487912365'

class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self):
        return f'{self.value}'

class Game:
    def __init__(self, data, set_length):
        self.cups = {}
        last_node = None
        for c in data:
            c = int(c)
            node = Node(c)
            self.cups[c] = node
            if last_node is None:
                last_node = node
                self.current_node = node
            else:
                last_node.next = node
                last_node = node

        if set_length > len(data):
            for i in range(len(data)+1, set_length+1):
                node = Node(i)
                self.cups[i] = node
                last_node.next = node
                last_node = node

        last_node.next = self.current_node

    def iterate(self):
        next1 = self.current_node.next
        next2 = next1.next
        next3 = next2.next
        #print(f'{next1} {next2} {next3}')

        destination_found = False
        destination = self.current_node.value - 1
        while not destination_found:
            if destination not in [next1.value, next2.value, next3.value]:
                if destination in self.cups:
                    destination_found = True
                    break
            if destination < 2:
                destination = max(self.cups.keys())
            else:
                destination -= 1
        #print(f'found destination {destination}')
        destination_node = self.cups[destination]

        self.current_node.next = next3.next
        next3.next = destination_node.next
        destination_node.next = next1

        self.current_node = self.current_node.next

    @property
    def collected_string(self):
        result = ''
        i = 1
        node = self.cups[1].next
        while i < len(self.cups):
            result += f'{node}'
            node = node.next
            i += 1
        return int(result)



class Game2:
    def __init__(self, data, set_length):
        self.cups = [int(c) for c in data]
        if set_length > len(data):
            self.cups += list(range(len(data)+1, set_length+1))
        self.current_index = 0

    def iterate(self):
        self.current_cup = self.cups[self.current_index]

        cups = ' '.join(map(lambda x: f'({self.cups[x]})' if x == self.current_index else str(self.cups[x]), range(len(self.cups))))
        print(f'cups: {cups}')

        prev = self.cups[0:self.current_index]
        pop_index = (self.current_index + 1) % len(self.cups)
        picked_up = self.cups[pop_index:pop_index+3]
        remaining = self.cups[pop_index+3:]

        picked_up = []
        #print(f'pop_index is {pop_index}')
        for index in range(3):
            picked_up.append(self.cups.pop(pop_index))
            if pop_index == len(self.cups):
                pop_index = 0
        print(f'pick up {picked_up}')

        #print(f'current_index 1 is {self.current_index}')
        destination = self.current_cup - 1
        print(f'destination {destination} prev {prev} remaining {remaining}')
        destination_found = False
        found_index = None

        while not destination_found:
            print(f'testing {destination}')
            if destination < 2:
                max_prev = max(prev)
                max_remaining = max(remaining)
                if max_remaining > max_prev:
                    destination = max_remaining
                    found_index = remaining.index(max_remaining) + len(prev) + 1
                    destination_found = True
                else:
                    destination_found = max_prev
                    found_index = prev.index(max_prev)
                    destination_found = True
            elif destination in picked_up:
                destination -= 1
            elif destination in prev:
                found_index = prev.index(destination)
                destination_found = True
            elif destination in remaining:
                found_index = remaining.index(destination) + len(prev) + 1
                destination_found = True
            else:
                destination -= 1
        print(f'found destination {destination} at index {found_index}')

        #print(f'cups {self.cups}')
        for index in range(3):
            insert_index = index + found_index + 1
            cup_to_insert = picked_up[index]
            self.cups.insert(insert_index, cup_to_insert)

        self.current_index = (self.cups.index(self.current_cup) + 1) % len(self.cups)
        input()

    def iterate_raw(self):
        self.current_cup = self.cups[self.current_index]

        cups = ' '.join(map(lambda x: f'({self.cups[x]})' if x == self.current_index else str(self.cups[x]), range(len(self.cups))))
        print(f'cups: {cups}')

        picked_up = []
        pop_index = (self.current_index + 1) % len(self.cups)
        #print(f'pop_index is {pop_index}')
        for index in range(3):
            picked_up.append(self.cups.pop(pop_index))
            if pop_index == len(self.cups):
                pop_index = 0
        print(f'pick up {picked_up}')

        #print(f'current_index 1 is {self.current_index}')
        destination = self.current_cup - 1
        print(f'destination {destination}')
        destination_found = False
        found_index = None

        while not destination_found:
            print(f'testing {destination}')
            if destination in self.cups:
                found_index = self.cups.index(destination)
                destination_found = True
            elif destination < 2:
                destination = max(self.cups) 
            else:
                destination -= 1
        print(f'found destination {destination} at index {found_index}')

        #print(f'cups {self.cups}')
        for index in range(3):
            insert_index = index + found_index + 1
            cup_to_insert = picked_up[index]
            self.cups.insert(insert_index, cup_to_insert)

        self.current_index = (self.cups.index(self.current_cup) + 1) % len(self.cups)
    
    @property
    def collected_string(self):
        start_index = 0
        for index in range(len(self.cups)):
            if self.cups[index] == 1:
                start_index = index
                break

        result = ''
        for index in range(1, len(self.cups)):
            result += str(self.cups[(index+start_index)%len(self.cups)])
        return int(result)


def compute_result(data, iteration=10, set_length=9):
    game = Game(data, set_length)
    index = 0
    while index < iteration:
        game.iterate()
        index += 1
    return game.collected_string


def compute_result_star(data, iteration=10000000, set_length=1000000):
    game = Game(data, set_length)
    index = 0
    while index < iteration:
        game.iterate()
        index += 1
        if index % 100000 == 0:
            print(f'index {index}')
    star_1 = game.cups[1].next
    star_2 = star_1.next
    return star_1.value * star_2.value


def test_part1():
    data = test_data
    result = compute_result(data, 10, 9)
    print(f'test1 is {result}')
    assert result == 92658374

    result = compute_result(data, 100, 9)
    print(f'test1 is {result}')
    assert result == 67384529


def test_part2():
    data = test_data
    result = compute_result_star(data)
    print(f'test2 is {result}')
    assert result == 149245887792


def part1():
    data = load_data()
    result = compute_result(data, 100, 9)
    print(f'part1 is {result}')
    assert result == 89573246


def part2():
    data = load_data()
    result = compute_result_star(data)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
