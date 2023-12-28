
# Karger's algorithm to find Minimum Cut in an
# undirected, unweighted and connected graph.
import random

test_data = [
    'jqt: rhn xhk nvd',
    'rsh: frs pzl lsr',
    'xhk: hfx',
    'cmg: qnr nvd lhk bvb',
    'rhn: xhk bvb hfx',
    'bvb: xhk hfx',
    'pzl: lsr hfx nvd',
    'qnr: nvd',
    'ntq: jqt hfx bvb xhk',
    'nvd: lhk',
    'lsr: lhk',
    'rzs: qnr cmg lsr rsh',
    'frs: qnr lhk lsr',
]

def load_data():
    data = []
    with open('input.txt', 'r') as f:
        for r in f.readlines():
            data.append(r.strip())
    return data
 
# a class to represent a unweighted edge in graph
class Edge:
    def __init__(self, s, d):
        self.src = s
        self.dest = d
 
# a class to represent a connected, undirected
# and unweighted graph as a collection of edges.
class Graph:
   
    # V-> Number of vertices, E-> Number of edges
    def __init__(self, data):
        nodes = []
        edges = set()

        for line in data:
            source = line.split(': ')[0]
            destinations = line.split(': ')[1].split(' ')

            if source not in nodes:
                nodes.append(source)

            for destination in destinations:
                if destination not in nodes: 
                    nodes.append(destination)
                    edge = Edge(source, destination)
                    edges.add(edge)


        self.V = len(nodes)
        self.E = len(edges)
        self.nodes = nodes
         
        self.edge = []
        for edge in edges:
            self.edge.append(edge)
 
#A class to represent a subset for union-find
class subset:
    def __init__(self, p, r):
        self.parent = p
        self.rank = r
 
# A very basic implementation of Karger's randomized
# algorithm for finding the minimum cut. Please note
# that Karger's algorithm is a Monte Carlo Randomized algo
# and the cut returned by the algorithm may not be
# minimum always
def kargerMinCut(graph):
   
    # Get data of given graph
    V = graph.V
    E = graph.E
    edge = graph.edge
 
    # Allocate memory for creating V subsets.
    subsets = {}
 
    # Create V subsets with single elements
    for v in graph.nodes:
        subsets[v] = subset(v, 0)

 
    # Initially there are V vertices in
    # contracted graph
    vertices = V
 
    # Keep contracting vertices until there are
    # 2 vertices.
    while vertices > 2:
        # Pick a random edge
        i = int(10 * random.random()) % E
 
        # Find vertices (or sets) of two corners
        # of current edge
        subset1 = find(subsets, edge[i].src)
        subset2 = find(subsets, edge[i].dest)
 
        # If two corners belong to same subset,
        # then no point considering this edge
        if subset1 == subset2:
            continue
          
        # Else contract the edge (or combine the
        # corners of edge into one vertex)
        else:
            print("Contracting edge " + str(edge[i].src) + "-" + str(edge[i].dest))
            vertices -= 1
            Union(subsets, subset1, subset2)
 
    # Now we have two vertices (or subsets) left in
    # the contracted graph, so count the edges between
    # two components and return the count.
    cutedges = 0
    for i in range(E):
        subset1 = find(subsets, edge[i].src)
        subset2 = find(subsets, edge[i].dest)
        if subset1 != subset2:
            cutedges += 1
 
    return cutedges
 
# A utility function to find set of an element i
# (uses path compression technique)
def find(subsets, i):
   
    # find root and make root as parent of i
    # (path compression)
    print(f"{i=}")
    if subsets[i].parent != i:
        subsets[i].parent = find(subsets, subsets[i].parent)
 
    return subsets[i].parent
 
# A function that does union of two sets of x and y
# (uses union by rank)
def Union(subsets, x, y):
    xroot = find(subsets, x)
    yroot = find(subsets, y)
 
    # Attach smaller rank tree under root of high
    # rank tree (Union by Rank)
    if subsets[xroot].rank < subsets[yroot].rank:
        subsets[xroot].parent = yroot
    elif subsets[xroot].rank > subsets[yroot].rank:
        subsets[yroot].parent = xroot
         
    # If ranks are same, then make one as root and
    # increment its rank by one
    else:
        subsets[yroot].parent = xroot
        subsets[xroot].rank += 1
 
# Driver program to test above functions
def solve_part1(data):
    graph = Graph(data)

    r = random.random()
    res = kargerMinCut(graph)
    print("Cut found by Karger's randomized algo is", res)

def test_part1():
    data = test_data
    result = solve_part1(data)
    print(f'test1 is {result}')
    assert result == 54


def part1():
    data = load_data()
    result = solve_part1(data)
    print(f'part1 is {result}')

test_part1()
part1()
