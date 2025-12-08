#!/usr/bin/env python
import math
import heapq
from itertools import combinations, count


test_data = [
    "162,817,812",
    "57,618,57",
    "906,360,560",
    "592,479,940",
    "352,342,300",
    "466,668,158",
    "542,29,236",
    "431,825,988",
    "739,650,466",
    "52,470,668",
    "216,146,977",
    "819,987,18",
    "117,168,530",
    "805,96,715",
    "346,949,466",
    "970,615,88",
    "941,993,340",
    "862,61,35",
    "984,92,344",
    "425,690,689",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Box:
    def __init__(self, index):
        self.index = index
        splitted = index.split(',')
        self.x = int(splitted[0])
        self.y = int(splitted[1])
        self.z = int(splitted[2])
        self.circuit = set()
        self.circuit.add(self)

    def __repr__(self):
        return self.index

    def distance_to(self, other):
        delta_x = math.pow(self.x - other.x, 2)
        delta_y = math.pow(self.y - other.y, 2)
        delta_z = math.pow(self.z - other.z, 2)
        return delta_x + delta_y + delta_z


def solve_part1(data, wanted_connections=10):
    boxes = []
    for line in data:
        box = Box(line)
        boxes.append(box)

    print(f"We have {len(boxes)} boxes")

    circuits = []
    heap = []
    for b1, b2 in combinations(boxes, 2):
        distance = b1.distance_to(b2)
        heapq.heappush(heap, (distance, (b1, b2)))

    connection = 0
    stop = False
    while not stop:
        distance, (b1, b2) = heapq.heappop(heap) 
        print(f"{connection=} {b1=} {b2=}")
        if b1.circuit == b2.circuit:
            pass
        else:
            b1_circuit = b1.circuit
            b2_circuit = b2.circuit
            len_b1_circuit = len(b1_circuit)
            len_b2_circuit = len(b2_circuit)
            print("before")
            print(f"{len_b1_circuit=}")
            print(f"{len_b2_circuit=}")
            b1_circuit.update(b2_circuit)
            b2.circuit = b1_circuit
            b1.circuit = b1_circuit
            for box in b1_circuit:
                box.circuit = b1_circuit
            print("after")
            new_len_b1_circuit = len(b1_circuit)
            print(f"{new_len_b1_circuit=}")
            assert new_len_b1_circuit == len_b1_circuit + len_b2_circuit

        connection += 1
        if connection == wanted_connections:
            break


    circuits = {}
    for box in boxes:
        if box.circuit:
            string = " ".join(map(str,box.circuit))
            if string not in circuits:
                circuits[string] = box.circuit

    for circuit in circuits.values():
        print(len(circuit))

    circuits = sorted(list(circuits.values()), key=len, reverse=True)
    result = 1
    circuit = circuits.pop(0)
    size = len(circuit)
    #print(f"{size=} {circuit=}")
    result *=size

    circuit = circuits.pop(0)
    size = len(circuit)
    #print(f"{size=} {circuit=}")
    result *=size

    circuit = circuits.pop(0)
    size = len(circuit)
    #print(f"{size=} {circuit=}")
    result *=size
    return result


def solve_part2(data):
    boxes = []
    for line in data:
        box = Box(line)
        boxes.append(box)

    print(f"We have {len(boxes)} boxes")

    circuits = []
    heap = []
    for b1, b2 in combinations(boxes, 2):
        distance = b1.distance_to(b2)
        heapq.heappush(heap, (distance, (b1, b2)))

    connection = 0
    stop = False
    while not stop:
        distance, (b1, b2) = heapq.heappop(heap) 
        print(f"{connection=} {b1=} {b2=}")
        if b1.circuit == b2.circuit:
            pass
        else:
            b1_circuit = b1.circuit
            b2_circuit = b2.circuit
            len_b1_circuit = len(b1_circuit)
            len_b2_circuit = len(b2_circuit)
            print("before")
            print(f"{len_b1_circuit=}")
            print(f"{len_b2_circuit=}")
            b1_circuit.update(b2_circuit)
            b2.circuit = b1_circuit
            b1.circuit = b1_circuit
            for box in b1_circuit:
                box.circuit = b1_circuit
            print("after")
            new_len_b1_circuit = len(b1_circuit)
            if new_len_b1_circuit == len(boxes):
                return b1.x * b2.x
            print(f"{new_len_b1_circuit=}")
            assert new_len_b1_circuit == len_b1_circuit + len_b2_circuit

        connection += 1

    circuits = {}
    for box in boxes:
        if box.circuit:
            string = " ".join(map(str,box.circuit))
            if string not in circuits:
                circuits[string] = box.circuit

    for circuit in circuits.values():
        print(len(circuit))

    circuits = sorted(list(circuits.values()), key=len, reverse=True)
    result = 1
    circuit = circuits.pop(0)
    size = len(circuit)
    #print(f"{size=} {circuit=}")
    result *=size

    circuit = circuits.pop(0)
    size = len(circuit)
    #print(f"{size=} {circuit=}")
    result *=size

    circuit = circuits.pop(0)
    size = len(circuit)
    #print(f"{size=} {circuit=}")
    result *=size
    return result



def test_part1():
    data = test_data
    result = solve_part1(data, 10)
    print(f'test1 is {result}')
    assert result == 40


def part1():
    data = load_data()
    result = solve_part1(data, 1000)
    print(f'part1 is {result}')
    assert result > 9639
    assert result > 12474
    assert result > 82984
    assert result == 175440


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 25272


def part2():
    data = load_data()
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
