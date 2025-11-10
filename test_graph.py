import unittest
import time
import matplotlib.pyplot as plt
from graph import Graph
from graph_io import *


class TestGraph(unittest.TestCase):

    def test_graph_initialisation_vertices(self):
        graph = Graph(5)
        self.assertEqual(graph.num_vertices, 5)

    def test_graph_initialisation_edges(self):
        graph = Graph(5)
        self.assertEqual(graph.num_edges, 0)

    def test_graph_initialisation_directed(self):
        graph = Graph(5)
        self.assertFalse(graph.directed)

    def test_graph_initialisation_matrix(self):
        graph = Graph(5)
        self.assertEqual(len(graph.adj_matrix), 5)

    def test_graph_initialisation_lists(self):
        graph = Graph(5)
        self.assertEqual(len(graph.adj_lists), 5)

    def test_matrix_to_lists(self):
        graph = Graph(3)
        graph.adj_matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        graph._adj_matrix_to_adj_lists()

        res_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        self.assertEqual(graph.adj_lists, res_lists)

    def test_lists_to_martix(self):
        graph = Graph(3)
        graph.adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph._adj_lists_to_adj_matrix()

        res_matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        self.assertEqual(graph.adj_matrix, res_matrix)

    def test_eulerian_not_directed_graph_true(self):
        graph = Graph(3)
        graph.adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph.directed = False
        self.assertTrue(graph._is_eulerian())

    def test_eulerian_not_directed_graph_false(self):
        graph = Graph(3)
        graph.adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1]
        }
        graph.directed = False
        self.assertFalse(graph._is_eulerian())

    def test_eulerian_directed_graph_true(self):
        graph = Graph(3)
        graph.adj_lists = {
            0: [1],
            1: [2],
            2: [0]
        }
        graph.directed = True
        self.assertTrue(graph._is_eulerian())

    def test_eulerian_directed_graph_false(self):
        graph = Graph(3)
        graph.adj_lists = {
            0: [1],
            1: [2],
            2: [1]  # Нарушает баланс
        }
        graph.directed = True
        self.assertFalse(graph._is_eulerian())

    def test_eulerian_cycle_not_none(self):
        graph = Graph(3)
        graph.adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph.directed = False
        graph.num_edges = 3

        cycle = graph.find_eulerian_cycle()
        self.assertIsNotNone(cycle)

    def test_eulerian_cycle_length(self):
        graph = Graph(3)
        graph.adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph.directed = False
        graph.num_edges = 3

        cycle = graph.find_eulerian_cycle()
        self.assertEqual(len(cycle), 4)

    def test_eulerian_cycle_start_end(self):
        graph = Graph(3)
        graph.adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph.directed = False
        graph.num_edges = 3

        cycle = graph.find_eulerian_cycle()
        self.assertEqual(cycle[0], cycle[-1])

    def test_eulerian_cycle_directed(self):
        graph = Graph(4)
        graph.adj_lists = {
            0: [1],
            1: [2],
            2: [3],
            3: [0]
        }
        graph.directed = True
        graph.num_edges = 4

        cycle = graph.find_eulerian_cycle()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 5)

    # Особые случаи
    def test_empty_graph_zero_vertices(self):
        graph = Graph(0)
        self.assertEqual(graph.num_vertices, 0)

    def test_empty_graph_adj_matrix(self):
        graph = Graph(0)
        self.assertEqual(len(graph.adj_matrix), 0)

    def test_empty_graph_adj_lists(self):
        graph = Graph(0)
        self.assertEqual(len(graph.adj_lists), 0)

    def test_empty_graph_num_edges(self):
        graph = Graph(0)
        self.assertEqual(graph.num_edges, 0)

    def test_single_vertex_graph(self):
        graph = Graph(1)
        self.assertEqual(graph.num_vertices, 1)

    def test_single_vertex_adj_matrix_size(self):
        graph = Graph(1)
        self.assertEqual(len(graph.adj_matrix[0]), 1)

    def test_single_vertex_adj_lists_size(self):
        graph = Graph(1)
        self.assertEqual(len(graph.adj_lists[0]), 0)

    def test_single_vertex_with_loop(self):
        graph = Graph(1)
        graph.adj_matrix[0][0] = 1
        graph._adj_matrix_to_adj_lists()
        self.assertEqual(graph.adj_lists[0], [0])

    def test_single_vertex_eulerian_check(self):
        graph = Graph(1)
        graph.adj_lists[0] = []
        self.assertTrue(graph._is_eulerian())

    def test_single_vertex_with_loop_eulerian(self):
        graph = Graph(1)
        graph.adj_lists[0] = [0]
        graph.directed = False
        self.assertTrue(graph._is_eulerian())

    def test_isolated_vertices_graph(self):
        graph = Graph(5)
        for i in range(5):
            graph.adj_lists[i] = []
        self.assertTrue(graph._is_eulerian())

    def test_complete_graph_k2(self):
        graph = Graph(2)
        graph.adj_lists = {0: [1], 1: [0]}
        graph.directed = False
        self.assertFalse(graph._is_eulerian())

    def test_complete_graph_k3(self):
        graph = Graph(3)
        graph.adj_lists = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        graph.directed = False
        self.assertTrue(graph._is_eulerian())

    def test_star_graph_center_degree(self):
        graph = Graph(4)
        graph.adj_lists = {0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}
        graph.directed = False
        self.assertFalse(graph._is_eulerian())

    def test_path_graph_three_vertices(self):
        graph = Graph(3)
        graph.adj_lists = {0: [1], 1: [0, 2], 2: [1]}
        graph.directed = False
        self.assertFalse(graph._is_eulerian())

    def test_cycle_graph_four_vertices(self):
        graph = Graph(4)
        graph.adj_lists = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
        graph.directed = False
        self.assertTrue(graph._is_eulerian())

    def test_disconnected_components(self):
        graph = Graph(6)
        graph.adj_lists = {
            0: [1, 2], 1: [0, 2], 2: [0, 1],  # Компонента 1 - треугольник
            3: [4, 5], 4: [3, 5], 5: [3, 4]  # Компонента 2 - треугольник
        }
        graph.directed = False
        self.assertTrue(graph._is_eulerian())

    def test_graph_with_multiple_loops(self):
        graph = Graph(2)
        graph.adj_lists = {0: [0, 1], 1: [0, 1, 1]}  # Петли: 0->0, 1->1, 1->1
        graph.directed = False
        graph.num_edges = 3  # Ребра: (0,0), (0,1), (1,1)

        self.assertFalse(graph._is_eulerian())  # ✅ Должен быть False

    def test_directed_cycle_eulerian(self):
        graph = Graph(3)
        graph.adj_lists = {0: [1], 1: [2], 2: [0]}
        graph.directed = True
        self.assertTrue(graph._is_eulerian())

    def test_directed_non_eulerian_imbalance(self):
        graph = Graph(3)
        graph.adj_lists = {0: [1, 2], 1: [0], 2: [1]}
        graph.directed = True
        self.assertFalse(graph._is_eulerian())

    def test_large_graph_initialization(self):
        large_number = 1000
        graph = Graph(large_number)
        self.assertEqual(graph.num_vertices, large_number)

    def test_large_graph_adj_matrix_dimensions(self):
        large_number = 1000
        graph = Graph(large_number)
        self.assertEqual(len(graph.adj_matrix), large_number)
        self.assertEqual(len(graph.adj_matrix[0]), large_number)

    def test_large_graph_adj_lists_size(self):
        large_number = 1000
        graph = Graph(large_number)
        self.assertEqual(len(graph.adj_lists), large_number)

    def test_complete_graph_large_eulerian(self):
        graph = Graph(5)
        graph.adj_lists = {
            0: [1, 2, 3, 4],
            1: [0, 2, 3, 4],
            2: [0, 1, 3, 4],
            3: [0, 1, 2, 4],
            4: [0, 1, 2, 3]
        }
        graph.directed = False
        graph.num_edges = 10  # n*(n-1)/2 = 5*4/2 = 10
        self.assertTrue(graph._is_eulerian())  # ✅ Должен быть True

    def test_complete_graph_large_eulerian_even(self):
        graph = Graph(4)
        graph.adj_lists = {
            0: [1, 2, 3],
            1: [0, 2, 3],
            2: [0, 1, 3],
            3: [0, 1, 2]
        }
        graph.directed = False
        graph.num_edges = 6  # 4*3/2 = 6
        self.assertFalse(graph._is_eulerian())


class TestGraphIO(unittest.TestCase):

    def test_is_directed_by_matrix_symmetric(self):
        matrix = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        self.assertFalse(is_directed_by_matrix(matrix))

    def test_is_directed_by_matrix_asymmetric(self):
        matrix = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
        self.assertTrue(is_directed_by_matrix(matrix))

    def test_is_directed_by_matrix_diagonal(self):
        matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertFalse(is_directed_by_matrix(matrix))

    def test_is_directed_by_lists_symmetric(self):
        lists = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        self.assertFalse(is_directed_by_lists(lists))

    def test_is_directed_by_lists_asymmetric(self):
        lists = {0: [1], 1: [2], 2: [0]}
        self.assertTrue(is_directed_by_lists(lists))

    def test_is_directed_by_lists_empty(self):
        lists = {0: [], 1: [], 2: []}
        self.assertFalse(is_directed_by_lists(lists))

    def test_count_edges_from_matrix_undirected(self):
        matrix = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        self.assertEqual(count_edges_from_matrix(matrix, False), 3)

    def test_count_edges_from_matrix_directed(self):
        matrix = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        self.assertEqual(count_edges_from_matrix(matrix, True), 6)

    def test_count_edges_from_matrix_empty(self):
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(count_edges_from_matrix(matrix, False), 0)

    def test_count_edges_from_lists_undirected(self):
        lists = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        self.assertEqual(count_edges_from_lists(lists, False), 3)

    def test_count_edges_from_lists_directed(self):
        lists = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        self.assertEqual(count_edges_from_lists(lists, True), 6)

    def test_count_edges_from_lists_empty(self):
        lists = {0: [], 1: [], 2: []}
        self.assertEqual(count_edges_from_lists(lists, False), 0)

    def test_count_edges_from_lists_isolated_vertices(self):
        lists = {0: [1], 1: [0], 2: []}
        self.assertEqual(count_edges_from_lists(lists, False), 1)

    def test_count_edges_from_matrix_with_loops_undirected(self):
        matrix = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
        self.assertEqual(count_edges_from_matrix(matrix, False), 4)

    def test_count_edges_from_matrix_with_loops_directed(self):
        matrix = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
        self.assertEqual(count_edges_from_matrix(matrix, True), 6)


import time
import matplotlib.pyplot as plt


class TestPerformance(unittest.TestCase):

    def test_eulerian_cycle_performance(self):
        """Тест производительности алгоритма поиска Эйлерова цикла"""
        print("\n--- Тестирование производительности ---")

        sizes = [100, 200, 500, 1000, 2000, 5000, 10000, 15000, 20000]
        times = []

        for size in sizes:
            graph = Graph(size)
            graph.directed = False

            # Создаем циклический граф
            for i in range(size):
                prev_vertex = (i - 1) % size
                next_vertex = (i + 1) % size
                graph.adj_lists[i] = [prev_vertex, next_vertex]

            graph.num_edges = size

            start_time = time.time()
            cycle = graph.find_eulerian_cycle()
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000
            times.append(execution_time)

            print(f"Граф с {size} вершинами: {execution_time:.2f} мс")

            self.assertIsNotNone(cycle)
            self.assertEqual(cycle[0], cycle[-1])

        # Строим график
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8)
        plt.xlabel('Количество вершин')
        plt.ylabel('Время выполнения (мс)')
        plt.title('Зависимость времени поиска Эйлерова цикла от размера графа')
        plt.grid(True, alpha=0.3)
        plt.savefig('performance_graph.png', dpi=300, bbox_inches='tight')
        plt.close()