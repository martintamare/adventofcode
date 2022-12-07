#!/usr/bin/env python

test_data = [
    '$ cd /',
    '$ ls',
    'dir a',
    '14848514 b.txt',
    '8504156 c.dat',
    'dir d',
    '$ cd a',
    '$ ls',
    'dir e',
    '29116 f',
    '2557 g',
    '62596 h.lst',
    '$ cd e',
    '$ ls',
    '584 i',
    '$ cd ..',
    '$ cd ..',
    '$ cd d',
    '$ ls',
    '4060174 j',
    '8033020 d.log',
    '5626152 d.ext',
    '7214296 k',
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data


class Node:
    def __init__(self, name, parent=None, size=0):
        self.name = name
        self.parent = parent
        self.size = size
        self.children = []

    @property
    def is_dir(self):
        return self.size == 0

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        if self.parent:
            return f'{self.parent}/{self.name}'
        else:
            return self.name

    def __repr__(self):
        return str(self)

    @property
    def total_size(self):
        size = 0
        for child in self.children:
            if child.is_dir:
                size += child.total_size
            else:
                size += child.size
        return size


def solve(data, part):
    data = data.copy()

    nodes = {}

    # Root
    data.pop(0)
    root = Node('/')
    nodes[str(root)] = root

    current_node = root
    current_mode = None

    for line in data:
        print(f'current:{current_node} mode:{current_mode} line:{line}')
        splitted_line = line.split(' ')
        if line.startswith('$'):
            # LS
            if line == '$ ls':
                current_mode = 'ls'
                continue
            # cd somewhere
            elif len(splitted_line) == 3:
                change_directory = splitted_line[2]
                if change_directory == '..':
                    current_node = current_node.parent
                else:
                    wanted_node = f'{current_node}/{splitted_line[2]}'
                    current_node = nodes[wanted_node]
        elif line.startswith('dir'):
            dir_name = splitted_line[1]
            node = Node(dir_name, current_node)
            nodes[str(node)] = node
            current_node.add_child(node)
        elif len(splitted_line) == 2:
            file_name = splitted_line[1]
            size = int(splitted_line[0])
            node = Node(file_name, current_node, size)
            nodes[str(node)] = node
            current_node.add_child(node)
        else:
            print('what todo ?')
            exit(0)
            pass

    if part == 1:
        size = 0
        for node in nodes.values():
            node_size = node.total_size
            if node_size <= 100000:
                size += node_size
        return size
    else:
        root_size = root.total_size
        current_free_size = 70000000 - root_size
        wanted_free_size = 30000000 - current_free_size
        print(f'{root_size} need {wanted_free_size}')

        child_to_delete = None
        for child in nodes.values():
            if child.total_size >= wanted_free_size:
                if child_to_delete is None:
                    child_to_delete = child
                elif child_to_delete.total_size > child.total_size:
                    child_to_delete = child
        return child_to_delete.total_size


def test_part1():
    data = test_data
    result = solve(data, part=1)
    print(f'test1 is {result}')
    assert result == 95437


def test_part2():
    data = test_data
    result = solve(data, part=2)
    print(f'test2 is {result}')
    assert result == 24933642


def part1():
    data = load_data()
    result = solve(data, part=1)
    print(f'part1 is {result}')


def part2():
    data = load_data()
    result = solve(data, part=2)
    print(f'part2 is {result}')


test_part1()
part1()
test_part2()
part2()
