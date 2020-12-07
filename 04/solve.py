#!/usr/bin/env python
import re

class Passport(object):

    def __init__(self,
            byr=None,
            iyr=None,
            eyr=None,
            hgt=None,
            hcl=None,
            ecl=None,
            pid=None,
            cid=None,
            ):
        self.byr = byr
        self.iyr = iyr
        self.eyr = eyr
        self.hgt = hgt
        self.hcl = hcl
        self.ecl = ecl
        self.pid = pid
        self.cid = cid

    def __repr__(self):
        return f'byr: {self.byr} iyr: {self.iyr} eyr: {self.eyr} hgt: {self.hgt} hcl: {self.hcl} ecl: {self.ecl} pid: {self.pid} cid: {self.cid}'

    def is_valid(self):
        if self.byr is None:
            return False
        if len(self.byr) != 4:
            return False
        self.byr = int(self.byr)
        if self.byr < 1920:
            return False
        if self.byr > 2002:
            return False

        if self.iyr is None:
            return False
        if len(self.iyr) != 4:
            return False
        self.iyr = int(self.iyr)
        if self.iyr < 2010:
            return False
        if self.iyr > 2020:
            return False

        if self.eyr is None:
            return False
        if len(self.eyr) != 4:
            return False
        self.eyr = int(self.eyr)
        if self.eyr < 2020:
            return False
        if self.eyr > 2030:
            return False

        if self.hgt is None:
            return False
        if not (self.hgt.endswith('cm') or self.hgt.endswith('in')):
                return False
        hgt = int(self.hgt[:-2])
        if self.hgt.endswith('cm'):
            if hgt < 150:
                return False
            if hgt > 193:
                return False
        if self.hgt.endswith('in'):
            if hgt < 59:
                return False
            if hgt > 76:
                return False

        if self.hcl is None:
            return False
        if not re.search(r'^#[0-9,a-f]{6}$', self.hcl):
            print(f'hcl not ok {self.hcl}')
            return False

        if self.ecl is None:
            return False
        if self.ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False

        if self.pid is None:
            return False
        if not re.search(r'^[0-9]{9}$', self.pid):
            print(f'pid not ok {self.pid}')
            return False

        return True






def load_data():
    data = []
    with open('input.txt', 'r') as f:
        data = f.readlines()
    return extract_data(data)

def extract_data(data):
    passport_data = []
    passport = {}
    for line in data:
        line = line.rstrip()
        if line == '':
            passport_data.append(passport)
            passport = {}
            continue
        else:
            line_data = line.split(' ')
            for raw_line in line_data:
                raw_data = raw_line.split(':')
                if len(raw_data) != 2:
                    print('djazidf,azdaz')
                    exit(1)
                key = raw_data[0]
                value = raw_data[1]
                passport[key] = value
    passport_data.append(passport)
    return passport_data


def test_data():
    data = [
        'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
        'byr:1937 iyr:2017 cid:147 hgt:183cm',
        '',
        'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
        'hcl:#cfa07d byr:1929',
        '',
        'hcl:#ae17e1 iyr:2013',
        'eyr:2024',
        'ecl:brn pid:760753108 byr:1931',
        'hgt:179cm',
        '',
        'hcl:#cfa07d eyr:2025 pid:166559648',
        'iyr:2011 ecl:brn hgt:59in',
    ]
    return extract_data(data)



def part1():
    passports = load_data()
    mandatory_keys = [
            'byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid',
    ]
    valid_passports = 0
    for passport in passports:
        is_valid = True
        for key in mandatory_keys:
            if key not in passport:
                is_valid = False
                break
        if is_valid:
            valid_passports += 1
    print(f'We have {valid_passports} valid passports')



def part2():
    passports = load_data()
    valid_passports = 0
    for passport in passports:
        test = Passport(**passport)
        if test.is_valid():
            valid_passports += 1
    print(f'We have {valid_passports} valid passports')



part1()
part2()
