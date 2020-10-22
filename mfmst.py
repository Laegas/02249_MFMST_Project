# run from terminal as e.g. "python mfmst.py < test01.uwg"

### imports ###
from typing import Union, List
from operator import itemgetter
from itertools import combinations
import math
import sys
import collections
import random
import time
###############

# define graph classes
class Edge:
    def __init__(self, from_node: int, to_node: int, weight: int):
        self.from_node: int = from_node
        self.to_node: int = to_node
        self.weight: int = weight

    def other(self, vertex: int):
        if vertex == self.from_node:
            return self.to_node
        elif vertex == self.to_node:
            return self.from_node
        else:
            raise Exception("Error")

    def __str__(self):
        return "From " + str(self.from_node) + " to " + str(self.to_node) + "; Weight: " + str(self.weight)

    def __eq__(self, other):
        if type(other) != Edge:
            return False
        e: Edge = other
        return e.from_node == self.from_node and e.to_node == self.to_node and e.weight == self.weight

class Graph:
    def __init__(self, vertices_number: int):
        self.V: int = vertices_number
        # adjacency lists
        self.adj: List[List[Edge]] = [[] for _ in range(self.V)]
        # for edge order
        self.edges: List[Edge] = []

    # function to add an edge to graph
    def add_edge(self, from_node_or_edge: Union[int,Edge], to_node: int = None, weight: int = None):
        if to_node is None and weight is None and type(from_node_or_edge) is Edge:
            edge = from_node_or_edge
        elif to_node is not None and weight is not None and type(from_node_or_edge) is int:
            edge = Edge(from_node_or_edge-1, to_node-1, weight) # -1 as the nodes starts with 1 in the .uwg files
        else:
            raise Exception("Illegal arguments")
        self.edges.append(edge)
        self.adj[edge.from_node].append(edge)
        self.adj[edge.to_node].append(edge)

    def is_connected(self):
        # BFS approach
        visited = set()
        queue = collections.deque([0]) # start at node 0, does not matter where
        visited.add(0)

        while queue:
            v = queue.popleft()
            for e in self.adj[v]:
                w = e.other(v)
                if w not in visited:
                    visited.add(w)
                    if len(visited) == self.V:
                        return True
                    queue.append(w)
        return False

    def spans_tree(self, edges_idx: List[int], cut_edge_list = False):
        # must be at least |V|-1 edges
        if len(edges_idx) < self.V - 1:
            return False
        if len(edges_idx) > len(self.edges):
            raise Exception("List of indices is longer than number of edges in graph")

        # take only |V|-1 edges
        if cut_edge_list:
            edges_idx = edges_idx[0:self.V - 1]

        # construct new graph with only the given edges
        new_graph = Graph(self.V)
        for i in range(len(edges_idx)):
            new_graph.add_edge(self.edges[edges_idx[i] - 1])

        return new_graph.is_connected()

    def get_weight_sum_tuple(self, edges_idx: List[int], cut_edge_list = False):
        # # must be at least |V|-1 edges
        # if len(edges_idx) < self.V - 1:
        #     return False

        # take only |V|-1 edges
        if cut_edge_list:
            edges_idx = edges_idx[0:self.V - 1]

        weight_sum_unmirrored = 0
        weight_sum_mirrored = 0
        for i in range(len(edges_idx)):
            weight_sum_unmirrored += self.edges[edges_idx[i] - 1].weight
            weight_sum_mirrored += self.edges[len(self.edges) - edges_idx[i]].weight

        return weight_sum_unmirrored, weight_sum_mirrored

class MFMSTBruteForceSolver:
    def __init__(self, g: Graph):
        self.graph: Graph = g
        self.r_len = g.V - 1
        self.m = len(g.edges)

    def solve(self, max_runtime = 0.9):
        if not self.graph.is_connected():
            return "NO"

        start_time = time.time()
        i = 0
        edges_for_best_b = []
        best_b = sys.maxsize

        while time.time() - start_time < max_runtime:
            i += 1
            rand_edges = self.__generate_random_edges()
            if self.graph.spans_tree(rand_edges):
                temp_b = max(self.graph.get_weight_sum_tuple(rand_edges))
                if temp_b < best_b:
                    best_b = temp_b
                    edges_for_best_b = rand_edges

        return edges_for_best_b, best_b

    def __generate_random_edges(self):
        generated_edges = []

        i = 0
        while i < self.r_len:
            rand_idx = random.randint(1,self.m)
            if rand_idx not in generated_edges:
                generated_edges.append(rand_idx)
                i += 1

        return generated_edges

class MFMSTBetterSolver:
    def __init__(self, g: Graph):
        self.graph: Graph = g
        self.edges_in_spanning_tree = g.V - 1
        self.m = len(g.edges)

    def solve(self, max_runtime = 0.9):
        if not self.graph.is_connected():
            return "NO"

        start_time = time.time()
        best_b = sys.maxsize
        edges_for_best_b = []
        pairs = self.__get_ordered_edge_pairs()

        considered_edges = self.__get_considered_edges(pairs, self.m)
        for edges_idx in combinations(considered_edges, self.edges_in_spanning_tree):
            if time.time() - start_time >= max_runtime:
                return edges_for_best_b, best_b
            if self.graph.spans_tree(edges_idx):
                temp_b = max(self.graph.get_weight_sum_tuple(edges_idx))
                if temp_b < best_b:
                    best_b = temp_b
                    edges_for_best_b = edges_idx

        return edges_for_best_b, best_b

    def __get_ordered_edge_pairs(self):
        # get pairs
        pairs = []
        for i in range(math.ceil(self.m / 2)):
            pairs.append((i + 1, self.m - i, self.graph.edges[i].weight + self.graph.edges[self.m - i - 1].weight))

        # sort pairs by weight sum
        pairs.sort(key=itemgetter(2))
        return pairs

    def __get_considered_edges(self, pairs, edges_to_take):
        considered_edges = []
        pairs_to_take = math.ceil(edges_to_take / 2)
        for i in range(pairs_to_take):
            considered_edges.append(pairs[i][0])
            if pairs[i][1] not in considered_edges:
                considered_edges.append(pairs[i][1])
        return considered_edges


if __name__ == '__main__':
    vertex_no = int(sys.stdin.readline())
    graph = Graph(vertex_no)
    edge_no = int(sys.stdin.readline())

    for _ in range(edge_no):
        line = [int(s) for s in sys.stdin.readline().split()]
        graph.add_edge(line[0], line[1], line[2])

    solver = MFMSTBetterSolver(graph)
    edges, b = solver.solve()
    if type(edges) is str and type(b) is str:
        print("NO")
    else:
        for e in edges:
            print(e)
        print(b)
