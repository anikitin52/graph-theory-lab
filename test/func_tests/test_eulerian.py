import io
import pytest
from unittest.mock import patch
from graph.graph import Graph


class TestEulerianCycle:
    """Тесты для Эйлерова цикла"""

    def test_eulerian_not_directed_graph_true(self):
        """Неориентированный граф с эйлеровым циклом"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph._directed = False
        assert graph._is_eulerian() is True

    def test_eulerian_not_directed_graph_false(self):
        """Неориентированный граф без эйлерова цикла"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1]
        }
        graph._directed = False
        assert graph._is_eulerian() is False

    def test_eulerian_directed_graph_true(self):
        """Ориентированный граф с эйлеровым циклом"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1],
            1: [2],
            2: [0]
        }
        graph._directed = True
        assert graph._is_eulerian() is True

    def test_eulerian_directed_graph_false(self):
        """Ориентированный граф без эйлерова цикла"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1],
            1: [2],
            2: [1]
        }
        graph._directed = True
        assert graph._is_eulerian() is False

    def test_eulerian_cycle_not_none(self):
        """Поиск эйлерова цикла - результат не None"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph._directed = False
        graph._num_edges = 3

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None

    def test_eulerian_cycle_length(self):
        """Проверка длины эйлерова цикла"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph._directed = False
        graph._num_edges = 3

        cycle = graph.find_eulerian_cycle()
        assert len(cycle) == 4

    def test_eulerian_cycle_start_end(self):
        """Проверка что цикл начинается и заканчивается в одной вершине"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph._directed = False
        graph._num_edges = 3

        cycle = graph.find_eulerian_cycle()
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_directed(self):
        """Эйлеров цикл в ориентированном графе"""
        graph = Graph(4)
        graph._adj_lists = {
            0: [1],
            1: [2],
            2: [3],
            3: [0]
        }
        graph._directed = True
        graph._num_edges = 4

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == 5

    def test_single_vertex_eulerian_check(self):
        """Граф с одной вершиной без ребер - эйлеров"""
        graph = Graph(1)
        graph._adj_lists[0] = []
        assert graph._is_eulerian() is True

    def test_single_vertex_with_loop_eulerian(self):
        """Граф с одной вершиной и петлей - эйлеров"""
        graph = Graph(1)
        graph._adj_lists[0] = [0]
        graph._directed = False
        assert graph._is_eulerian() is True

    def test_isolated_vertices_graph(self):
        """Граф с изолированными вершинами - эйлеров"""
        graph = Graph(5)
        for i in range(5):
            graph._adj_lists[i] = []
        assert graph._is_eulerian() is True

    def test_complete_graph_k2(self):
        """Полный граф K2 - не эйлеров"""
        graph = Graph(2)
        graph._adj_lists = {0: [1], 1: [0]}
        graph._directed = False
        assert graph._is_eulerian() is False

    def test_complete_graph_k3(self):
        """Полный граф K3 - эйлеров"""
        graph = Graph(3)
        graph._adj_lists = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        graph._directed = False
        assert graph._is_eulerian() is True

    def test_star_graph_center_degree(self):
        """Звездный граф - не эйлеров"""
        graph = Graph(4)
        graph._adj_lists = {0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}
        graph._directed = False
        assert graph._is_eulerian() is False

    def test_path_graph_three_vertices(self):
        """Путь из 3 вершин - не эйлеров"""
        graph = Graph(3)
        graph._adj_lists = {0: [1], 1: [0, 2], 2: [1]}
        graph._directed = False
        assert graph._is_eulerian() is False

    def test_cycle_graph_four_vertices(self):
        """Цикл из 4 вершин - эйлеров"""
        graph = Graph(4)
        graph._adj_lists = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
        graph._directed = False
        assert graph._is_eulerian() is True

    def test_disconnected_components(self):
        """Две несвязные компоненты - эйлеров"""
        graph = Graph(6)
        graph._adj_lists = {
            0: [1, 2], 1: [0, 2], 2: [0, 1],
            3: [4, 5], 4: [3, 5], 5: [3, 4]
        }
        graph._directed = False
        assert graph._is_eulerian() is False

    def test_graph_with_multiple_loops(self):
        """Граф с несколькими петлями - не эйлеров"""
        graph = Graph(2)
        graph._adj_lists = {0: [0, 1], 1: [0, 1, 1]}
        graph._directed = False
        graph._num_edges = 3
        assert graph._is_eulerian() is False

    def test_directed_cycle_eulerian(self):
        """Ориентированный цикл - эйлеров"""
        graph = Graph(3)
        graph._adj_lists = {0: [1], 1: [2], 2: [0]}
        graph._directed = True
        assert graph._is_eulerian() is True

    def test_directed_non_eulerian_imbalance(self):
        """Ориентированный граф с дисбалансом степеней - не эйлеров"""
        graph = Graph(3)
        graph._adj_lists = {0: [1, 2], 1: [0], 2: [1]}
        graph._directed = True
        assert graph._is_eulerian() is False

    def test_complete_graph_large_eulerian(self):
        """Полный граф K5 - эйлеров"""
        graph = Graph(5)
        graph._adj_lists = {
            0: [1, 2, 3, 4],
            1: [0, 2, 3, 4],
            2: [0, 1, 3, 4],
            3: [0, 1, 2, 4],
            4: [0, 1, 2, 3]
        }
        graph._directed = False
        graph._num_edges = 10
        assert graph._is_eulerian() is True

    def test_complete_graph_large_eulerian_even(self):
        """Полный граф K4 - не эйлеров"""
        graph = Graph(4)
        graph._adj_lists = {
            0: [1, 2, 3],
            1: [0, 2, 3],
            2: [0, 1, 3],
            3: [0, 1, 2]
        }
        graph._directed = False
        graph._num_edges = 6
        assert graph._is_eulerian() is False

    def test_eulerian_cycle_returns_1based(self):
        """Проверка что эйлеров цикл возвращается в 1-based"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        graph._directed = False
        graph._num_edges = 3

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        # Все вершины в цикле должны быть >= 1 (1-based)
        assert all(v >= 1 for v in cycle)
        # Должны быть все вершины от 1 до 3
        assert set(cycle[:-1]) == {1, 2, 3}

    def test_empty_graph_zero_vertices_eulerian(self):
        """Пустой граф с 0 вершинами - эйлеров"""
        graph = Graph(0)
        assert graph._is_eulerian() is False

    def test_eulerian_cycle_no_cycle_print(self):
        """Поиск эйлерова цикла в графе без цикла - возвращает None"""
        graph = Graph(3)
        graph._adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1]
        }
        graph._directed = False
        graph._num_edges = 2

        cycle = graph.find_eulerian_cycle()
        assert cycle is None