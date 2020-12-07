#!/usr/bin/env python

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            data.append(line)
    return data

def compute_trees(step_line, step_column):
    data = load_data()
    lines = len(data)
    columns = len(data[0])

    stop = False
    index_line = 0
    index_column = 0
    trees = 0

    while not stop:
        if index_line >= lines:
            stop = True
            break
        if index_column >= columns:
            index_column = index_column % columns
        test = data[index_line][index_column]
        if test == '#':
            trees += 1
        index_line += step_line
        index_column += step_column

    return trees

def part1():
    trees = compute_trees(1, 3)
    print(f'we found {trees} trees')


def part2():
    trees = 1
    for step_line, step_column in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
        step_trees = compute_trees(step_line, step_column)
        print(f'we found {step_trees} trees for slop {step_column}:{step_line}' )
        trees = trees * step_trees
        
    print(f'we found {trees} trees')


part1()
part2()
