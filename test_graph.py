import random
import unittest
import time
import matplotlib.pyplot as plt
from graph import Graph
from graph_io import *
from sys import setrecursionlimit

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

        self.assertFalse(graph._is_eulerian())

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
        self.assertTrue(graph._is_eulerian())

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

    def test_is_tournament_true(self):
        """Турнир из трёх вершин (цикл)"""
        graph = Graph(3)
        graph.directed = True
        graph.adj_matrix = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0]
        ]
        graph._adj_matrix_to_adj_lists()
        self.assertTrue(graph.is_tournament())

    def test_is_tournament_directed_not_tournament(self):
        """Ориентированный граф, но не турнир: есть два встречных ребра и изолированная вершина"""
        graph = Graph(3)
        graph.directed = True
        graph.adj_matrix = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ]
        graph._adj_matrix_to_adj_lists()
        self.assertFalse(graph.is_tournament())

    def test_is_tournament_undirected(self):
        """Неориентированный граф не может быть турниром"""
        graph = Graph(3)
        graph.directed = False
        graph.adj_matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        graph._adj_matrix_to_adj_lists()
        self.assertFalse(graph.is_tournament())

    def test_is_tournament_K33_oriented(self):
        """Ориентированный K_{3,3} (все рёбра из доли 0..2 в 3..5) — не турнир"""
        n = 6
        graph = Graph(n)
        graph.directed = True
        matrix = [[0] * n for _ in range(n)]
        for i in range(3):
            for j in range(3, 6):
                matrix[i][j] = 1
        graph.adj_matrix = matrix
        graph._adj_matrix_to_adj_lists()
        self.assertFalse(graph.is_tournament())

    def test_is_tournament_K5_tournament(self):
        """K5, ориентированный как турнир (i -> j при i < j)"""
        n = 5
        graph = Graph(n)
        graph.directed = True
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i < j:
                    matrix[i][j] = 1
        graph.adj_matrix = matrix
        graph._adj_matrix_to_adj_lists()
        self.assertTrue(graph.is_tournament())

    def test_is_tournament_large_tournament_100(self):
        """Большой турнир на 100 вершинах (i -> j при i < j)"""
        n = 100
        graph = Graph(n)
        graph.directed = True
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i < j:
                    matrix[i][j] = 1
        graph.adj_matrix = matrix
        graph._adj_matrix_to_adj_lists()
        self.assertTrue(graph.is_tournament())

    def test_hamiltonian_cycle_exists(self):
        """Граф C4 (цикл из 4 вершин) — гамильтонов цикл существует"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1, 3],
            1: [0, 2],
            2: [1, 3],
            3: [0, 2]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 5)
        self.assertEqual(cycle[0], cycle[-1])
        self.assertEqual(sorted(cycle[:-1]), [0, 1, 2, 3])

    def test_hamiltonian_cycle_path_no_cycle(self):
        """Путь P4 (0-1-2-3) — гамильтонов путь есть, цикла нет"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_no_path_no_cycle(self):
        """Две компоненты (0-1 и 2-3) — ни пути, ни цикла"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_bipartite(self):
        """Двудольный граф K_{2,3} — цикла нет (доли разного размера)"""
        graph = Graph(5)
        graph.directed = False
        # доли: {0,1} и {2,3,4}, все рёбра между долями
        graph.adj_lists = {
            0: [2, 3, 4],
            1: [2, 3, 4],
            2: [0, 1],
            3: [0, 1],
            4: [0, 1]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_split_graph(self):
        """Расщепляемый граф без гамильтонова цикла"""
        graph = Graph(4)
        graph.directed = False
        # Клика {0,1}, независимое множество {2,3}; 0 соединена с 2 и 3, 1 соединена только с 2
        graph.adj_lists = {
            0: [1, 2, 3],
            1: [0, 2],
            2: [0, 1],
            3: [0]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_co_bipartite(self):
        """Дополнение двудольного графа — две несвязные клики, цикла нет"""
        graph = Graph(4)
        graph.directed = False
        # Клика {0,1}, клика {2,3}, рёбер между ними нет
        graph.adj_lists = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_chordal(self):
        """Хордальный граф (P4) — нет цикла"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_directed(self):
        """Ориентированный цикл 0->1->2->0 — гамильтонов цикл существует"""
        graph = Graph(3)
        graph.directed = True
        graph.adj_lists = {
            0: [1],
            1: [2],
            2: [0]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 4)
        self.assertEqual(cycle[0], cycle[-1])

    def test_hamiltonian_cycle_multiple_edges(self):
        """Граф с кратными рёбрами (K3 с дубликатами) — цикл должен найтись"""
        graph = Graph(3)
        graph.directed = False
        graph.adj_lists = {
            0: [1, 1, 2],
            1: [0, 0, 2],
            2: [0, 1]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 4)
        self.assertEqual(cycle[0], cycle[-1])

    def test_hamiltonian_cycle_with_loop(self):
        """Граф с петлёй (K3 с петлёй у вершины 0) — цикл сохраняется"""
        graph = Graph(3)
        graph.directed = False
        graph.adj_lists = {
            0: [0, 1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        cycle = graph.find_hamiltonian_cycle()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 4)
        self.assertEqual(cycle[0], cycle[-1])

    def test_hamiltonian_path_graph_with_cycle(self):
        """Граф C4 (цикл) — гамильтонов путь существует"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1, 3],
            1: [0, 2],
            2: [1, 3],
            3: [0, 2]
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 4)
        self.assertEqual(sorted(path), [0, 1, 2, 3])

    def test_hamiltonian_path_path_no_cycle(self):
        """Путь P4 (0-1-2-3) — гамильтонов путь есть"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 4)
        self.assertTrue(set(path) == {0, 1, 2, 3})

    def test_hamiltonian_path_no_path_no_cycle(self):
        """Две компоненты (0-1 и 2-3) — ни пути, ни цикла"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNone(path)

    def test_hamiltonian_path_split_graph(self):
        """Расщепляемый граф (клика {0,1}, независимое {2,3}, рёбра 0-2,0-3,1-2) — путь есть"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1, 2, 3],
            1: [0, 2],
            2: [0, 1],
            3: [0]
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 4)
        self.assertEqual(set(path), {0, 1, 2, 3})

    def test_hamiltonian_path_co_bipartite(self):
        """Дополнение двудольного графа — две несвязные клики, пути нет"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNone(path)

    def test_hamiltonian_path_chordal(self):
        """Хордальный граф P4 — путь есть"""
        graph = Graph(4)
        graph.directed = False
        graph.adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 4)

    def test_hamiltonian_path_directed(self):
        """Ориентированный путь 0->1->2 — гамильтонов путь существует"""
        graph = Graph(3)
        graph.directed = True
        graph.adj_lists = {
            0: [1],
            1: [2],
            2: []
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 3)
        self.assertEqual(set(path), {0, 1, 2})

    def test_hamiltonian_path_multiple_edges(self):
        """Граф с кратными рёбрами (K3 с дубликатами) — путь есть"""
        graph = Graph(3)
        graph.directed = False
        graph.adj_lists = {
            0: [1, 1, 2],
            1: [0, 0, 2],
            2: [0, 1]
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 3)
        self.assertEqual(set(path), {0, 1, 2})

    def test_hamiltonian_path_with_loop(self):
        """Граф с петлёй (K3 с петлёй у вершины 0) — путь существует"""
        graph = Graph(3)
        graph.directed = False
        graph.adj_lists = {
            0: [0, 1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        path = graph.find_hamiltonian_path()
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 3)
        self.assertEqual(set(path), {0, 1, 2})

    def test_hamiltonian_cycle_tournament_small_3(self):
        """Турнир на 3 вершинах (цикл 0->1->2->0) — цикл существует"""
        graph = Graph(3)
        graph.directed = True
        graph.adj_lists = {
            0: [1],
            1: [2],
            2: [0]
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 4)  # n+1
        self.assertEqual(cycle[0], cycle[-1])
        self.assertEqual(sorted(cycle[:-1]), [0, 1, 2])

    def test_hamiltonian_cycle_tournament_strongly_connected_4(self):
        """Сильно связный турнир на 4 вершинах (содержит цикл)"""
        graph = Graph(4)
        graph.directed = True
        # Базовый цикл 0->1->2->3->0, остальные рёбра добавлены до турнира:
        # 0->2, 1->3
        graph.adj_lists = {
            0: [1, 2],
            1: [2, 3],
            2: [3],
            3: [0]
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 5)
        self.assertEqual(cycle[0], cycle[-1])
        self.assertEqual(set(cycle[:-1]), {0, 1, 2, 3})

    def test_hamiltonian_cycle_tournament_not_strongly_connected_4(self):
        """Турнир с источником (0) — не сильно связный, цикла нет"""
        graph = Graph(4)
        graph.directed = True
        # Транзитивный турнир: все рёбра от меньшего к большему
        graph.adj_lists = {
            0: [1, 2, 3],
            1: [2, 3],
            2: [3],
            3: []
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_tournament_strongly_connected_5(self):
        """Сильно связный турнир на 5 вершинах (содержит цикл)"""
        graph = Graph(5)
        graph.directed = True
        # Цикл 0->1->2->3->4->0, доп. рёбра: 0->2, 3->0, 1->3, 1->4, 2->4
        graph.adj_lists = {
            0: [1, 2],
            1: [2, 3, 4],
            2: [3, 4],
            3: [4, 0],
            4: [0]
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 6)
        self.assertEqual(cycle[0], cycle[-1])
        self.assertEqual(set(cycle[:-1]), {0, 1, 2, 3, 4})

    def test_hamiltonian_cycle_tournament_single_vertex(self):
        """Турнир из одной вершины — гамильтонова цикла нет"""
        graph = Graph(1)
        graph.directed = True
        graph.adj_lists = {0: []}
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_tournament_two_vertices(self):
        """Турнир на 2 вершинах (0->1) — цикла нет"""
        graph = Graph(2)
        graph.directed = True
        graph.adj_lists = {
            0: [1],
            1: []
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_tournament_transitive_5(self):
        """Транзитивный турнир на 5 вершинах — не сильно связный, цикла нет"""
        graph = Graph(5)
        graph.directed = True
        graph.adj_lists = {
            0: [1, 2, 3, 4],
            1: [2, 3, 4],
            2: [3, 4],
            3: [4],
            4: []
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        self.assertIsNone(cycle)

    def test_hamiltonian_cycle_tournament_zero_vertices(self):
        """Пустой турнир (0 вершин) — цикла нет"""
        graph = Graph(0)
        graph.directed = True
        graph.adj_lists = {}
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        self.assertIsNone(cycle)


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

    def _plot_performance(self, sizes, times, title, filename):
        """Вспомогательный метод для построения графика производительности"""
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, times, 'b-', linewidth=2)
        plt.xlabel('Количество вершин')
        plt.ylabel('Время выполнения (мс)')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

    # ==================== Эйлеров цикл ====================

    def test_eulerian_cycle_performance(self):
        """Тест производительности алгоритма поиска Эйлерова цикла"""
        print("\n--- Тестирование производительности: Эйлеров цикл ---")

        sizes = [100, 200, 500, 1000, 2000, 5000, 10000, 15000, 20000]
        times = []

        for size in sizes:
            graph = Graph(size)
            graph.directed = False

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

        self._plot_performance(
            sizes, times,
            'Зависимость времени поиска Эйлерова цикла от размера графа',
            'performance_eulerian_cycle.png'
        )

    # ==================== Гамильтонов цикл: случайные графы ====================

    def test_hamiltonian_cycle_random_performance(self):
        """Тест производительности поиска гамильтонова цикла на случайных графах"""
        print("\n--- Тестирование производительности: Гамильтонов цикл (случайные графы) ---")
        setrecursionlimit(100000)
        sizes = [i for i in range(1, 2000, 50)]
        times = []

        for size in sizes:
            graph = Graph(size)
            graph.directed = False

            for i in range(size):
                neighbors = [(i - 1) % size, (i + 1) % size]
                for j in range(size):
                    if j != i and j not in neighbors and random.random() < 0.3:
                        neighbors.append(j)
                graph.adj_lists[i] = neighbors

            start_time = time.time()
            cycle = graph.find_hamiltonian_cycle()
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000
            times.append(execution_time)

            print(f"Граф с {size} вершинами: {execution_time:.4f} мс")

        self._plot_performance(
            sizes, times,
            'Поиск гамильтонова цикла на случайных графах',
            'performance_hamiltonian_random.png'
        )

    # ==================== Гамильтонов цикл: двудольные графы ====================

    def test_hamiltonian_cycle_bipartite_performance(self):
        """Тест производительности поиска гамильтонова цикла на полных двудольных графах"""
        print("\n--- Тестирование производительности: Гамильтонов цикл (полные двудольные графы) ---")
        setrecursionlimit(10000)
        sizes = [i for i in range(2, 1000, 10)]
        times = []

        for size in sizes:
            graph = Graph(size)
            graph.directed = False

            half = size // 2
            for i in range(size):
                neighbors = []
                if i < half:
                    for j in range(half, size):
                        neighbors.append(j)
                else:
                    for j in range(half):
                        neighbors.append(j)
                graph.adj_lists[i] = neighbors
            graph._adj_lists_to_adj_matrix()

            start_time = time.time()
            cycle = graph.find_hamiltonian_cycle()
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000
            times.append(execution_time)

            print(f"Граф с {size} вершинами: {execution_time:.4f} мс")

        self._plot_performance(
            sizes, times,
            'Поиск гамильтонова цикла на полных двудольных графах',
            'performance_hamiltonian_bipartite.png'
        )

    # ==================== Гамильтонов цикл: расщепляемые графы ====================

    def test_hamiltonian_cycle_split_performance(self):
        """Тест производительности поиска гамильтонова цикла на расщепляемых графах"""
        print("\n--- Тестирование производительности: Гамильтонов цикл (расщепляемые графы) ---")

        sizes = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        times = []

        for size in sizes:
            graph = Graph(size)
            graph.directed = False

            clique_size = size // 2
            for i in range(size):
                neighbors = []
                if i < clique_size:
                    for j in range(clique_size):
                        if i != j:
                            neighbors.append(j)
                    for j in range(clique_size, size - 1):
                        neighbors.append(j)
                else:
                    for j in range(clique_size - 1):
                        neighbors.append(j)
                graph.adj_lists[i] = neighbors
            graph._adj_lists_to_adj_matrix()

            start_time = time.time()
            cycle = graph.find_hamiltonian_cycle()
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000
            times.append(execution_time)

            print(f"Граф с {size} вершинами: {execution_time:.4f} мс")

        self._plot_performance(
            sizes, times,
            'Поиск гамильтонова цикла на расщепляемых графах',
            'performance_hamiltonian_split.png'
        )

    # ==================== Гамильтонов цикл: дополнения двудольных ====================

    def test_hamiltonian_cycle_cobipartite_performance(self):
        """Тест производительности поиска гамильтонова цикла на дополнениях двудольных графов"""
        print("\n--- Тестирование производительности: Гамильтонов цикл (дополнения двудольных) ---")

        sizes = [6, 8, 10, 12, 14, 16, 18, 20, 22]
        times = []

        for size in sizes:
            graph = Graph(size)
            graph.directed = False

            half = size // 2
            for i in range(size):
                neighbors = []
                if i < half:
                    for j in range(half):
                        if i != j:
                            neighbors.append(j)
                    for j in range(half, size):
                        if j != half:
                            neighbors.append(j)
                else:
                    for j in range(half, size):
                        if i != j:
                            neighbors.append(j)
                    for j in range(half):
                        if j != 0:
                            neighbors.append(j)
                graph.adj_lists[i] = neighbors
            graph._adj_lists_to_adj_matrix()

            start_time = time.time()
            cycle = graph.find_hamiltonian_cycle()
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000
            times.append(execution_time)

            print(f"Граф с {size} вершинами: {execution_time:.4f} мс")

        self._plot_performance(
            sizes, times,
            'Поиск гамильтонова цикла на дополнениях двудольных графов',
            'performance_hamiltonian_cobipartite.png'
        )

    # ==================== Гамильтонов цикл: триангулированные графы ====================

    def test_hamiltonian_cycle_triangular_performance(self):
        """Тест производительности поиска гамильтонова цикла на триангулированных графах"""
        print("\n--- Тестирование производительности: Гамильтонов цикл (триангулированные графы) ---")

        sizes = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        times = []

        for size in sizes:
            graph = Graph(size)
            graph.directed = False

            for i in range(size):
                neighbors = []
                for j in range(size):
                    if i != j:
                        if abs(i - j) <= 2:
                            neighbors.append(j)
                        elif abs(i - j) == size - 1:
                            neighbors.append(j)
                graph.adj_lists[i] = neighbors
            graph._adj_lists_to_adj_matrix()

            start_time = time.time()
            cycle = graph.find_hamiltonian_cycle()
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000
            times.append(execution_time)

            print(f"Граф с {size} вершинами: {execution_time:.4f} мс")

        self._plot_performance(
            sizes, times,
            'Поиск гамильтонова цикла на триангулированных графах',
            'performance_hamiltonian_chordal.png'
        )

