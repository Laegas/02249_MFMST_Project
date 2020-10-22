### imports ###
import unittest
import time
from mfmst import Edge, Graph, MFMSTBruteForceSolver, MFMSTBetterSolver

###############

def load_graph_from_test_file(filename: str):
    file_object = open(filename, "r")
    vertices = int(file_object.readline())
    edges = int(file_object.readline())
    graph = Graph(vertices)
    for _ in range(edges):
        line = [int(s) for s in file_object.readline().split()]
        graph.add_edge(line[0], line[1], line[2])
    return graph


class AgentTest(unittest.TestCase):
    def setUp(self):
        print("setup")

    def test_uwg_files_loading(self):
        g = load_graph_from_test_file("test01.uwg")
        self.assertEqual(3, g.V)
        self.assertEqual(3, len(g.edges))
        self.assertEqual(Edge(0, 1, 1), g.adj[0][0])
        self.assertEqual(Edge(0, 1, 1), g.adj[1][0])
        self.assertEqual(Edge(1, 2, 2), g.adj[1][1])
        self.assertEqual(Edge(1, 2, 2), g.adj[2][0])
        self.assertEqual(Edge(0, 2, 3), g.adj[2][1])
        self.assertEqual(Edge(0, 2, 3), g.adj[0][1])
        g = load_graph_from_test_file("test02_selected_edges_connected.uwg")
        self.assertEqual(5, g.V)
        self.assertEqual(4, len(g.edges))
        self.assertEqual(Edge(1, 2, 2), g.adj[1][0])
        self.assertEqual(Edge(1, 2, 2), g.adj[2][0])
        self.assertEqual(Edge(0, 2, 3), g.adj[0][0])
        self.assertEqual(Edge(0, 2, 3), g.adj[2][1])
        self.assertEqual(Edge(3, 4, 8), g.adj[3][0])
        self.assertEqual(Edge(3, 4, 8), g.adj[4][0])
        self.assertEqual(Edge(2, 3, 3), g.adj[2][2])
        self.assertEqual(Edge(2, 3, 3), g.adj[3][1])
        g = load_graph_from_test_file("test02.uwg")
        self.assertEqual(5, g.V)
        self.assertEqual(8, len(g.edges))
        g = load_graph_from_test_file("test03.uwg")
        self.assertEqual(30, g.V)
        self.assertEqual(35, len(g.edges))

    def test_is_connected(self):
        g = load_graph_from_test_file("test01.uwg")
        self.assertEqual(True, g.is_connected())
        g = load_graph_from_test_file("test02.uwg")
        self.assertEqual(True, g.is_connected())
        g = load_graph_from_test_file("test02_selected_edges_connected.uwg")
        self.assertEqual(True, g.is_connected())
        g = load_graph_from_test_file("test02_selected_edges_disconnected.uwg")
        self.assertEqual(False, g.is_connected())
        g = load_graph_from_test_file("test03.uwg")
        self.assertEqual(True, g.is_connected())

    def test_spans_tree(self):
        # exhaustive list of all combinations for test01.uwg
        g = load_graph_from_test_file("test01.uwg")
        self.assertEqual(False, g.spans_tree([1]))
        self.assertEqual(False, g.spans_tree([2]))
        self.assertEqual(False, g.spans_tree([3]))
        self.assertEqual(True, g.spans_tree([1,2]))
        self.assertEqual(True, g.spans_tree([2,1]))
        self.assertEqual(True, g.spans_tree([1,3]))
        self.assertEqual(True, g.spans_tree([3,1]))
        self.assertEqual(True, g.spans_tree([2,3]))
        self.assertEqual(True, g.spans_tree([3,2]))
        self.assertEqual(True, g.spans_tree([1,2,3]))
        self.assertEqual(True, g.spans_tree([1,3,2]))
        self.assertEqual(True, g.spans_tree([2,1,3]))
        self.assertEqual(True, g.spans_tree([2,3,1]))
        self.assertEqual(True, g.spans_tree([3,1,2]))
        self.assertEqual(True, g.spans_tree([3,2,1]))
        # selected combinations for test02.uwg only
        g = load_graph_from_test_file("test02.uwg")
        self.assertEqual(False, g.spans_tree([1,2,3]))
        self.assertEqual(False, g.spans_tree([1,2,3,4]))
        self.assertEqual(True, g.spans_tree([2,3,6,7]))
        self.assertEqual(True, g.spans_tree([1,2,3,6,7]))
        self.assertEqual(False, g.spans_tree([1,2,3,6,7], True))

    def test_get_weight_sum_tuple(self):
        g = load_graph_from_test_file("test01.uwg")
        self.assertEqual((1, 3), g.get_weight_sum_tuple([1]))
        self.assertEqual((2, 2), g.get_weight_sum_tuple([2]))
        self.assertEqual((3, 1), g.get_weight_sum_tuple([3]))
        self.assertEqual((3, 5), g.get_weight_sum_tuple([1,2]))
        self.assertEqual((4, 4), g.get_weight_sum_tuple([1,3]))
        self.assertEqual((3, 5), g.get_weight_sum_tuple([2,1]))
        self.assertEqual((5, 3), g.get_weight_sum_tuple([2,3]))
        self.assertEqual((4, 4), g.get_weight_sum_tuple([3,1]))
        self.assertEqual((5, 3), g.get_weight_sum_tuple([3,2]))
        self.assertEqual((6, 6), g.get_weight_sum_tuple([1,2,3]))
        self.assertEqual(5, max(g.get_weight_sum_tuple([2,3])))

        g = load_graph_from_test_file("test02.uwg")
        self.assertEqual((16, 16), g.get_weight_sum_tuple([2,3,6,7]))
        self.assertEqual((19, 41), g.get_weight_sum_tuple([1,2,3,4]))
        self.assertEqual(41, max(g.get_weight_sum_tuple([1,2,3,4])))

    def test_brute_force_solver_solve(self):
        g = load_graph_from_test_file("test01.uwg")
        solver = MFMSTBruteForceSolver(g)
        edges, b = solver.solve()
        self.assertEqual(4, b)
        self.assertEqual([1, 3], sorted(edges))

        g = load_graph_from_test_file("test02.uwg")
        solver = MFMSTBruteForceSolver(g)
        edges, b = solver.solve()
        self.assertEqual(16, b)
        self.assertEqual([2, 3, 6, 7], sorted(edges))

        g = load_graph_from_test_file("test02_selected_edges_connected.uwg")
        solver = MFMSTBruteForceSolver(g)
        edges, b = solver.solve()
        self.assertEqual(16, b)
        self.assertEqual([1, 2, 3, 4], sorted(edges))

        g = load_graph_from_test_file("test02_selected_edges_disconnected.uwg")
        solver = MFMSTBruteForceSolver(g)
        r = solver.solve()
        self.assertEqual("NO", r)

        # g = load_graph_from_test_file("test03.uwg")
        # solver = MFMSTBruteForceSolver(g)
        # print(solver.solve()) # 1128

    def test_brute_force_solver_string_generation(self):
        g = load_graph_from_test_file("test01.uwg")
        solver = MFMSTBruteForceSolver(g)
        r = solver._MFMSTBruteForceSolver__generate_random_edges()
        self.assertEqual(2, len(r))
        for item in r:
            self.assertTrue(item >= 1 and item <= 3)
        g = load_graph_from_test_file("test02.uwg")
        solver = MFMSTBruteForceSolver(g)
        r = solver._MFMSTBruteForceSolver__generate_random_edges()
        self.assertEqual(4, len(r))
        for item in r:
            self.assertTrue(item >= 1 and item <= 8)

    def test_better_solver_get_ordered_edge_pairs(self):
        g = load_graph_from_test_file("test01.uwg")
        solver = MFMSTBetterSolver(g)
        r = solver._MFMSTBetterSolver__get_ordered_edge_pairs()
        self.assertEqual(2, len(r))
        self.assertEqual((1,3,4), r[0])
        self.assertEqual((2,2,4), r[1])
        g = load_graph_from_test_file("test02.uwg")
        solver = MFMSTBetterSolver(g)
        r = solver._MFMSTBetterSolver__get_ordered_edge_pairs()
        self.assertEqual(4, len(r))
        self.assertEqual((2,7,5), r[0])
        self.assertEqual((3,6,11), r[1])
        self.assertEqual((4,5,19), r[2])
        self.assertEqual((1,8,25), r[3])
        g = load_graph_from_test_file("test03.uwg")
        solver = MFMSTBetterSolver(g)
        r = solver._MFMSTBetterSolver__get_ordered_edge_pairs()
        self.assertEqual(18, len(r))

    def test_better_solver_get_considered_edges(self):
        solver = MFMSTBetterSolver(Graph(1))
        pairs = [(1, 3, 4), (2, 2, 4)]
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 1)
        self.assertEqual([1, 3], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 2)
        self.assertEqual([1, 3], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 3)
        self.assertEqual([1, 3, 2], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 4)
        self.assertEqual([1, 3, 2], r)
        pairs = [(2, 7, 5), (3, 6, 11), (4, 5, 19), (1, 8, 25)]
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 1)
        self.assertEqual([2,7], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 2)
        self.assertEqual([2,7], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 3)
        self.assertEqual([2,7,3,6], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 4)
        self.assertEqual([2,7,3,6], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 5)
        self.assertEqual([2,7,3,6,4,5], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 6)
        self.assertEqual([2,7,3,6,4,5], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 7)
        self.assertEqual([2,7,3,6,4,5,1,8], r)
        r = solver._MFMSTBetterSolver__get_considered_edges(pairs, 8)
        self.assertEqual([2,7,3,6,4,5,1,8], r)

    def test_better_solver_solve(self):
        g = load_graph_from_test_file("test01.uwg")
        solver = MFMSTBetterSolver(g)
        edges, b = solver.solve()
        self.assertEqual(4, b)
        self.assertEqual([1, 3], sorted(edges))

        g = load_graph_from_test_file("test02.uwg")
        solver = MFMSTBetterSolver(g)
        edges, b = solver.solve()
        self.assertEqual(16, b)
        self.assertEqual([2, 3, 6, 7], sorted(edges))

        g = load_graph_from_test_file("test02_selected_edges_connected.uwg")
        solver = MFMSTBetterSolver(g)
        edges, b = solver.solve()
        self.assertEqual(16, b)
        self.assertEqual([1, 2, 3, 4], sorted(edges))

        g = load_graph_from_test_file("test02_selected_edges_disconnected.uwg")
        solver = MFMSTBetterSolver(g)
        r = solver.solve()
        self.assertEqual("NO", r)

        g = load_graph_from_test_file("test03.uwg")
        solver = MFMSTBetterSolver(g)
        edges, b = solver.solve()
        self.assertEqual(1128, b)
        self.assertEqual([1, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 34, 35], sorted(edges))


if __name__ == '__main__':
    # unittest.main()

    g = load_graph_from_test_file("test03.uwg")
    solver = MFMSTBetterSolver(g)
    print(solver.solve(1))  # 1128

