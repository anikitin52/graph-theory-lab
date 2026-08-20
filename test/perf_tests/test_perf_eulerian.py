import io
import pytest
from unittest.mock import patch
from graph.graph import Graph


# TODO: Добавить сохранение в файл
class TestEulerianPerformance:
    """Тесты производительности для Эйлерова цикла"""

    def test_eulerian_cycle_perf_100(self):
        """Эйлеров цикл в графе с 100 вершинами (цикл)"""
        n = 100
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_200(self):
        """Эйлеров цикл в графе с 200 вершинами (цикл)"""
        n = 200
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_500(self):
        """Эйлеров цикл в графе с 500 вершинами (цикл)"""
        n = 500
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_1000(self):
        """Эйлеров цикл в графе с 1000 вершинами (цикл)"""
        n = 1000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_2000(self):
        """Эйлеров цикл в графе с 2000 вершинами (цикл)"""
        n = 2000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_5000(self):
        """Эйлеров цикл в графе с 5000 вершинами (цикл)"""
        n = 5000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_10000(self):
        """Эйлеров цикл в графе с 10000 вершинами (цикл)"""
        n = 10000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_15000(self):
        """Эйлеров цикл в графе с 15000 вершинами (цикл)"""
        n = 15000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_20000(self):
        """Эйлеров цикл в графе с 20000 вершинами (цикл)"""
        n = 20000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]

    def test_eulerian_cycle_perf_25000(self):
        """Эйлеров цикл в графе с 25000 вершинами (цикл)"""
        n = 25000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
        graph._num_edges = n

        cycle = graph.find_eulerian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]


    def test_non_eulerian_perf_100(self):
        """Граф без эйлерова цикла с 100 вершинами (путь)"""
        n = 100
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_200(self):
        """Граф без эйлерова цикла с 200 вершинами (путь)"""
        n = 200
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_500(self):
        """Граф без эйлерова цикла с 500 вершинами (путь)"""
        n = 500
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_1000(self):
        """Граф без эйлерова цикла с 1000 вершинами (путь)"""
        n = 1000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_2000(self):
        """Граф без эйлерова цикла с 2000 вершинами (путь)"""
        n = 2000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_5000(self):
        """Граф без эйлерова цикла с 5000 вершинами (путь)"""
        n = 5000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_10000(self):
        """Граф без эйлерова цикла с 10000 вершинами (путь)"""
        n = 10000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_15000(self):
        """Граф без эйлерова цикла с 15000 вершинами (путь)"""
        n = 15000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_20000(self):
        """Граф без эйлерова цикла с 20000 вершинами (путь)"""
        n = 20000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None

    def test_non_eulerian_perf_25000(self):
        """Граф без эйлерова цикла с 25000 вершинами (путь)"""
        n = 25000
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < n - 1:
                neighbors.append(i + 1)
            graph._adj_lists[i] = neighbors
        graph._num_edges = n - 1

        cycle = graph.find_eulerian_cycle()
        assert cycle is None
