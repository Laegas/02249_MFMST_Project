### imports ###
import unittest
import time
from mfmst import Edge, Graph, MFMSTBruteForceSolver
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

    def test_solver_solve(self):
        g = load_graph_from_test_file("test01.uwg")
        solver = MFMSTBruteForceSolver(g)
        self.assertEqual(4, solver.solve())

        g = load_graph_from_test_file("test02.uwg")
        solver = MFMSTBruteForceSolver(g)
        self.assertEqual(16, solver.solve())

        g = load_graph_from_test_file("test03.uwg")
        solver = MFMSTBruteForceSolver(g)
        print(solver.solve(1000)) # 1128

    def test_solver_string_generation(self):
        g = load_graph_from_test_file("test01.uwg")
        solver = MFMSTBruteForceSolver(g)
        r = solver._MSMFMBruteForceSolver__generate_random_edges()
        self.assertEqual(2, len(r))
        for item in r:
            self.assertTrue(item >= 1 and item <= 3)
        g = load_graph_from_test_file("test02.uwg")
        solver = MFMSTBruteForceSolver(g)
        r = solver._MSMFMBruteForceSolver__generate_random_edges()
        self.assertEqual(4, len(r))
        for item in r:
            self.assertTrue(item >= 1 and item <= 8)


if __name__ == '__main__':
    unittest.main()

