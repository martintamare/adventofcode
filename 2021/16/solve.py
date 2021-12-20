#!/usr/bin/env python

import math

translation_dic = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

test_data = [
    'D2FE28',
]

DEBUG_VERSION = 0
DEBUG_VALID = 0
DEBUG_SUBPACKET = 0
DEBUG_SUBPACKET_OPERATOR = 0


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

cache = {}

class Packet:
    def __init__(self, raw=None, binary=None):
        self.raw = raw
        self._translated = None
        self._version = None
        self._type = None
        self._literal_value = None
        self._length_type = None
        self._subpacket_length = None
        self._subpacket_number = None
        self._subpackets = None

        if binary is not None:
            self._translated = binary


    def __len__(self):
        return len(self.translated)

    def __repr__(self):
        return self.translated

    def __str__(self):
        return self.translated

    @property
    def min_length(self):
        global_min_length = 11
        if self.is_literal:
            return global_min_length
        elif self.length_type == 0:
            return 6 + 15 + self.subpacket_length
        elif self.length_type == 1:
            return 6  + 11 + self.subpacket_number * global_min_length
        else:
            print('Should not arrived here ever')
            exit(0)

    @property
    def valid(self):
        cache_index = self.translated
        if cache_index in cache:
            return cache[cache_index]

        is_valid = True

        if self.is_literal:
            try:
                test = self.literal_value
                if not test:
                    DEBUG_VALID and print(f'{self}-VALID=is_literal but literal_value is 0')
            except Exception:
                DEBUG_VALID and print(f'{self}-VALID=is_literal but no literal_value')
                is_valid = False

        elif self.is_operator:
            if self.length_type == 0:
                try:
                    self.subpacket_length
                except Exception:
                    DEBUG_VALID and print(f'{self}-VALID=is_operator 0 but no subpacket_length')
                    is_valid = False

                if is_valid and not self.subpacket_length:
                    DEBUG_VALID and print(f'{self}-VALID=is_operator 0 but subpacket_length is 0')
                    is_valid = False

            elif self.length_type == 1:
                try:
                    self.subpacket_number
                except Exception:
                    DEBUG_VALID and print(f'{self}-VALID=is_operator 1 but no subpacket_number')
                    is_valid = False

                if is_valid and not self.subpacket_number:
                    DEBUG_VALID and print(f'{self}-VALID=is_operator 1 but subpacket_number is 0')
                    is_valid = False

                if is_valid:
                    try:
                        assert len(self.subpackets) == self.subpacket_number
                    except Exception:
                        DEBUG_VALID and print(f'{self}-VALID=is_operator 1 but not enought subpackets')
                        is_valid = False
            else:
                print('Should not arrived here')
                exit(0)

            try:
                self.subpackets
            except Exception:
                DEBUG_VALID and print(f'{self}-VALID=is_operator but no subpackets')
                is_valid = False
        else:
            print('Should not arrived here')
            exit(0)

        try:
            min_length = self.min_length
            if len(self) < min_length:
                DEBUG_VALID and print('{self}-VALID=length but length is {min_length}')
                is_valid = False
        except Exception:
            DEBUG_VALID and print('{self}-VALID=length but length exception')
            is_valid = False

        cache[cache_index] = is_valid
        return is_valid

    @property
    def value(self):
        if self.is_literal:
            return self.literal_value
        elif not self.is_operator:
            raise ('NDJZANBFJKAZNFKJZA')

        if self.type == 0:
            return sum(map(lambda x: x.value, self.subpackets))
        elif self.type == 1:
            return math.prod(map(lambda x: x.value, self.subpackets))
        elif self.type == 2:
            return min(map(lambda x: x.value, self.subpackets))
        elif self.type == 3:
            return max(map(lambda x: x.value, self.subpackets))
        elif self.type == 5:
            if self.subpackets[0].value > self.subpackets[1].value:
                return 1
            else:
                return 0
        elif self.type == 6:
            if self.subpackets[0].value < self.subpackets[1].value:
                return 1
            else:
                return 0
        elif self.type == 7:
            if self.subpackets[0].value == self.subpackets[1].value:
                return 1
            else:
                return 0


    @property
    def translated(self):
        if self._translated is not None:
            return self._translated
        out = ''
        for char in self.raw:
            out += translation_dic[char]
        self._translated = out
        return out

    @property
    def version(self):
        if self._version is not None:
            return self._version
        out = int(self.translated[0:3], 2)
        self._version = out
        return out

    @property
    def type(self):
        if self._type is not None:
            return self._type
        out = int(self.translated[3:6], 2)
        self._type = out
        return out

    @property
    def is_literal(self):
        return self.type == 4

    @property
    def is_operator(self):
        return not self.is_literal

    @property
    def literal_value(self):
        if self._literal_value is not None:
            return self._literal_value

        if not self.is_literal:
            raise Exception('No No No literal_value')
        
        out = ''
        start_index = 6
        while True:
            if len(self) < start_index + 5:
                raise Exception('No No No literal_value length')

            value = ''
            if self.translated[start_index] == '1':
                out += self.translated[start_index+1:start_index+5]
            else:
                out += self.translated[start_index+1:start_index+5]
                break
            start_index += 5
        out = int(out,2)
        self._literal_value = out
        return out

    @property
    def length_type(self):
        if self._length_type is not None:
            return self._length_type

        if not self.is_operator:
            raise Exception('No No No length_type')

        out = int(self.translated[6])
        self._length_type = out
        return out

    @property
    def subpacket_length(self):
        if self._subpacket_length is not None:
            return self._subpacket_length

        if self.length_type != 0:
            raise Exception('No No No subpacket_length')

        out = int(self.translated[7:22], 2)
        self._subpacket_length = out
        return out

    @property
    def subpacket_number(self):
        if self._subpacket_number is not None:
            return self._subpacket_number

        if self.length_type != 1:
            raise Exception('No No No subpacket_number')

        out = int(self.translated[7:18], 2)
        self._subpacket_number = out
        return out


    def subpackets_0(self):
        # the next 15 bits are a number that represents the total length in bits 
        # of the sub-packets contained by this packet.

        packets = []
        packets_length = 0
        start_index = 22
        min_length = 11
        packet_length = min_length

        while True:
            value = self.translated[start_index:start_index+packet_length]
            DEBUG_SUBPACKET and print(f'{self}-SUBPACKET=testing {value}')
            packet = Packet(binary=value)
            if packet.valid:
                DEBUG_SUBPACKET and print(f'{self}-SUBPACKET=value {value} is valid : start {start_index} length {packet_length} vs {len(self)}')
                packets.append(packet)
                start_index += len(packet)
                packet_length = min_length
                packets_length+= len(packet)
                if packets_length == self.subpacket_length:
                    break

            else:
                DEBUG_SUBPACKET and print(f'{self}-SUBPACKET=value {value} is invalid remaining {self.translated[start_index:]}')
                if not value:
                    break
                elif start_index + packet_length >= len(self):
                    if int(value, 2) == 0:
                        break
                    else:
                        raise Exception('No No No subpackets')
                else:
                    packet_length += 1
        return packets

    def subpackets_1(self):
        # the next 11 bits are a number that represents
        # the number of sub-packets immediately contained by this packet.

        packets = []
        start_index = 18
        min_length = 11
        packet_length = min_length
        DEBUG_SUBPACKET_OPERATOR and print(f'{self}-SUBPACKET_OPERATOR=we want {self.subpacket_number} subpackets in {self} length:{len(self)}')

        while True:
            value = self.translated[start_index:start_index+packet_length]
            DEBUG_SUBPACKET_OPERATOR and print(f'{self}-SUBPACKET_OPERATOR=testing {value} [{start_index}:{start_index+packet_length}]')
            packet = Packet(binary=value)
            if packet.valid:
                DEBUG_SUBPACKET_OPERATOR and print(f'{self}-SUBPACKET_OPERATOR=value {value} is valid : start {start_index} length {packet_length} vs {len(self)}')
                packets.append(packet)
                start_index += len(value)
                packet_length = min_length
                DEBUG_SUBPACKET_OPERATOR and print(f'{self}-SUBPACKET_OPERATOR=we have {len(packets)} and want {self.subpacket_number}')
                if len(packets) == self.subpacket_number:
                    break
            else:
                DEBUG_SUBPACKET_OPERATOR and print(f'{self}-SUBPACKET_OPERATOR=value {value} is invalid')
                if start_index + packet_length > len(self):
                    break
                else:
                    packet_length += 1
        return packets

    @property
    def subpackets(self):
        if self._subpackets is not None:
            return self._subpackets

        if self.length_type == 0:
            packets = self.subpackets_0()
        else:
            packets = self.subpackets_1()

        self._subpackets = packets
        return packets

    @property
    def version_sum(self):
        total = self.version
        DEBUG_VERSION and print(f'{self} has version {self.version}')
        if self.is_operator:
            for packet in self.subpackets:
                DEBUG_VERSION and print(f'{packet} has version_sum of {packet.version_sum}')
                total += packet.version_sum
        return total


def test_part1():
    data = test_data
    packet = Packet('D2FE28')
    assert packet.translated == '110100101111111000101000'
    assert packet.version == 6
    assert packet.type == 4
    assert packet.is_literal
    assert packet.literal_value == 2021

    packet = Packet('38006F45291200')
    assert packet.translated == '00111000000000000110111101000101001010010001001000000000'
    assert packet.is_operator
    assert packet.length_type == 0
    assert packet.subpacket_length == 27
    assert len(packet.subpackets) == 2
    assert packet.subpackets[0].literal_value == 10
    assert packet.subpackets[1].literal_value == 20

    packet = Packet('EE00D40C823060')
    assert packet.translated == '11101110000000001101010000001100100000100011000001100000'
    assert packet.is_operator
    assert packet.length_type == 1
    assert packet.subpacket_number == 3
    assert len(packet.subpackets) == 3
    assert packet.subpackets[0].literal_value == 1
    assert packet.subpackets[1].literal_value == 2
    assert packet.subpackets[2].literal_value == 3

    packet = Packet('8A004A801A8002F478')
    assert packet.is_operator
    assert packet.version == 4
    print(packet.subpackets)
    assert len(packet.subpackets) == 1

    subpacket = packet.subpackets[0]
    assert subpacket.is_operator
    assert subpacket.version == 1
    assert len(subpacket.subpackets) == 1

    subpacket = subpacket.subpackets[0]
    assert subpacket.is_operator
    assert subpacket.version == 5
    assert len(subpacket.subpackets) == 1

    subpacket = subpacket.subpackets[0]
    assert subpacket.is_literal
    assert subpacket.version == 6

    assert packet.version_sum == 16
    packet = Packet('620080001611562C8802118E34')
    assert packet.version_sum == 12
    packet = Packet('C0015000016115A2E0802F182340')
    assert packet.version_sum == 23
    packet = Packet('A0016C880162017C3686B18A3D4780')
    assert packet.version_sum == 31


def test_part2():
    packet = Packet('C200B40A82')
    assert packet.value == 3

    packet = Packet('04005AC33890')
    assert packet.value == 54

    packet = Packet('880086C3E88112')
    assert packet.value == 7

    packet = Packet('CE00C43D881120')
    assert packet.value == 9

    packet = Packet('D8005AC2A8F0')
    assert packet.value == 1

    packet = Packet('F600BC2D8F')
    assert packet.value == 0

    packet = Packet('9C005AC2F8F0')
    assert packet.value == 0

    packet = Packet('9C0141080250320F1802104A08')
    assert packet.value == 1


def part1():
    data = load_data()
    packet = Packet(data[0])
    result = packet.version_sum
    print(f'part1 is {result}')


def part2():
    data = load_data()
    packet = Packet(data[0])
    result = packet.value
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
