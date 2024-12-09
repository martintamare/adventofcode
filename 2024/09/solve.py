#!/usr/bin/env python

test_data = [
    "2333133121414131402",
    "12345",
]


def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data

class Block:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.free_size = 0
        self.processed = False
        self.inserted = False
        self.free_block_inside = []

    def __repr__(self):
        result = ''
        for index in range(self.size):
            result += f"{self.id}"
        if self.free_size:
            for index in range(self.free_size):
                result += f"."
        return result

    def add_block(self, block):
        self.free_block_inside.append(block)
        block.processed = True
        block.inserted = True
        self.free_size -= block.size
        if self.free_size < 0:
            raise Exception("ndzajkdnazjkdnazkjd")
        elif self.free_size == 0:
            self.processed = True



def solve_part1(data):
    disk_id = 0
    blocks = []

    current_block = None

    for index, char in enumerate(data):
        size = int(char)
        if index % 2 == 0:
            file = True
            free = False
        else:
            file = False
            free = True

        if file:
            print(f"dealing with file {index=} {disk_id=} {size=}")
            block = Block(disk_id, size)
            blocks.append(block)
            disk_id += 1
            current_block = block
        elif free:
            current_block.free_size = size

    # First representation
    print(''.join(list(map(str, blocks))))

    # Now rearrange
    final_data = []
    free_block_index = 0
    current_free_block = blocks[free_block_index]

    def process_block(block):
        for to_insert in range(block.size):
            final_data.append(block.id)
        block.processed = True

    process_block(current_free_block)

    print("final_data")
    print(''.join(map(str, final_data)))
    for block in reversed(blocks):
        print(f"We have to insert {block.size} {block.id} {current_free_block=}")
        if block.processed:
            break
        block_size = block.size
        inserted = 0
        while True:
            if current_free_block == block:
                final_data.append(block.id)
                inserted += 1
            elif current_free_block.free_size > 0:
                final_data.append(block.id)
                inserted += 1
                current_free_block.free_size -= 1
            else:
                free_block_index += 1
                current_free_block = blocks[free_block_index]
                if current_free_block != block:
                    process_block(current_free_block)
            if inserted == block_size:
                break

    result = 0
    for index, char in enumerate(final_data):
        result += index * char

    return result


def solve_part2(data):
    disk_id = 0
    blocks = []

    current_block = None

    for index, char in enumerate(data):
        size = int(char)
        if index % 2 == 0:
            file = True
            free = False
        else:
            file = False
            free = True

        if file:
            print(f"dealing with file {index=} {disk_id=} {size=}")
            block = Block(disk_id, size)
            blocks.append(block)
            disk_id += 1
            current_block = block
        elif free:
            current_block.free_size = size

    # First representation
    print(''.join(list(map(str, blocks))))

    # Now rearrange
    final_data = []
    free_block_index = 0

    for block in reversed(blocks):
        print(f"We have to insert {block.size} {block.id}")
        for free_block in filter(lambda x: x.free_size >= block.size and not x.processed, blocks):
            print(f"Adding {block.id} to {free_block.id}")
            free_block.add_block(block)
            break

    index = 0
    result = 0
    for block in blocks:
        for _ in range(block.size):
            if not block.inserted:
                result += block.id * index
            index += 1
        for inserted_block in block.free_block_inside:
            for _ in range(inserted_block.size):
                result += inserted_block.id * index
                index += 1
        for _ in range(block.free_size):
            index += 1
    return result


def test_part1():
    data = test_data
    result = solve_part1(data[0])
    print(f'test1 is {result}')
    assert result == 1928


def part1():
    data = load_data()
    result = solve_part1(data[0])
    print(f'part1 is {result}')
    assert result < 6280871190126
    print(f'part1 maybe {result}')


def test_part2():
    data = test_data
    result = solve_part2(data[0])
    print(f'test2 is {result}')
    assert result == 2858


def part2():
    data = load_data()
    result = solve_part2(data[0])
    print(f'part2 is {result}')
    assert result < 8460423284794
    assert result < 6309955910883
    print(f'part2 maybe {result}')


#test_part1()
#part1()
test_part2()
part2()
