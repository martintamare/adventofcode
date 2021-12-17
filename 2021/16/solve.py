#!/usr/bin/env python

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
    def valid(self):
        cache_index = self.translated
        if cache_index in cache:
            return cache[cache_index]

        if len(self) < 11:
            DEBUG_VALID and print('VALID=length to small')
            cache[cache_index] = False
            return False

        if self.is_literal:
            try:
                test = self.literal_value
                cache[cache_index] = True
                return True
            except Exception:
                DEBUG_VALID and print('VALID=is_literal but no literal_value')
                cache[cache_index] = False
                return False
        elif self.is_operator:
            if self.length_type == 0:
                try:
                    self.subpacket_length
                except Exception:
                    DEBUG_VALID and print('VALID=is_operator 0 but no subpacket_length')
                    cache[cache_index] = False
                    return False
                if not self.subpacket_length:
                    cache[cache_index] = False
                    return False

                if len(self) < self.subpacket_length + 15 + 7:
                    DEBUG_VALID and print('VALID=is_operator 0 but length too small')
                    cache[cache_index] = False
                    return False
            elif self.length_type == 1:
                try:
                    self.subpacket_number
                except Exception:
                    DEBUG_VALID and print('VALID=is_operator 1 but no subpacket_number')
                    cache[cache_index] = False
                    return False
                if not self.subpacket_number:
                    cache[cache_index] = False
                    return False

                if len(self) < 7 + 11 + self.subpacket_number * 7:
                    DEBUG_VALID and print('VALID=is_operator 1 but length too small')
                    cache[cache_index] = False
                    return False
                try:
                    assert len(self.subpackets) == self.subpacket_number
                except Exception:
                    DEBUG_VALID and print('VALID=is_operator 1 but not enought subpackets')
                    cache[cache_index] = False
                    return False
            else:
                cache[cache_index] = False
                return False
            try:
                self.subpackets
                cache[cache_index] = True
                return True
            except Exception:
                DEBUG_VALID and print('VALID=is_operator but no subpackets')
                cache[cache_index] = False
                return False

        else:
            # Todo
            print('VALID=todo')
            input('TODO')
            input()


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
        packets = []
        packets_length = 0
        start_index = 22
        min_length = 7
        packet_length = min_length

        while True:
            value = self.translated[start_index:start_index+packet_length]
            DEBUG_SUBPACKET and print(f'SUBPACKET=testing {value}')
            packet = Packet(binary=value)
            if packet.valid:
                DEBUG_SUBPACKET and print(f'SUBPACKET=value {value} is valid : start {start_index} length {packet_length} vs {len(self)}')
                packets.append(packet)
                start_index += len(packet)
                packets_length+= len(packet)
                if packets_length > self.subpacket_length:
                    break

            else:
                DEBUG_SUBPACKET and print(f'SUBPACKET=value {value} is invalid')
                if not value:
                    break
                elif start_index + packet_length > len(self) - 1:
                    if int(value, 2) == 0:
                        break
                    else:
                        raise Exception('No No No subpackets')
                else:
                    packet_length += 1
        return packets

    def subpackets_1(self):
        packets = []
        start_index = 18
        min_length = 7
        packet_length = min_length
        DEBUG_SUBPACKET_OPERATOR and print(f'SUBPACKET_OPERATOR=we want {self.subpacket_number} subpackets in {self}')

        while True:
            if self.subpacket_number == 1:
                value = self.translated[start_index:]
            else:
                value = self.translated[start_index:start_index+packet_length]
            DEBUG_SUBPACKET_OPERATOR and print(f'SUBPACKET_OPERATOR=testing {value} [{start_index}:{start_index+packet_length}]')
            packet = Packet(binary=value)
            if packet.valid:
                DEBUG_SUBPACKET_OPERATOR and print(f'SUBPACKET_OPERATOR=value {value} is valid : start {start_index} length {packet_length} vs {len(self)}')
                packets.append(packet)
                start_index += len(value)
                packet_length = min_length
                DEBUG_SUBPACKET_OPERATOR and print(f'SUBPACKET_OPERATOR=we have {len(packets)} and want {self.subpacket_number}')
                if len(packets) == self.subpacket_number:
                    break
            else:
                DEBUG_SUBPACKET_OPERATOR and print(f'SUBPACKET_OPERATOR=value {value} is invalid')
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
    assert packet.version_sum == 16
    packet = Packet('620080001611562C8802118E34')
    assert packet.version_sum == 12
    packet = Packet('C0015000016115A2E0802F182340')
    assert packet.version_sum == 23
    packet = Packet('A0016C880162017C3686B18A3D4780')
    assert packet.version_sum == 31


def test_part2():
    data = test_data
    result = None
    print(f'test2 is {result}')
    assert result == 25


def part1():
    data = load_data()
    packet = Packet(data[0])
    result = packet.version_sum
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = None
    print(f'part2 is {result}')


test_part1()
part1()
#test_part2()
#part2()
