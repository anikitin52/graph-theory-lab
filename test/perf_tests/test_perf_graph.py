import io
import pytest
from unittest.mock import patch
from graph.graph import Graph


class TestGraphPerformance:
    """Тесты производительности для Graph"""

    def test_perf_init_1000(self):
        """Создание графа с 1000 вершинами"""
        g = Graph(1000)
        assert g._num_vertices == 1000
        assert len(g._adj_matrix) == 1000
        assert len(g._adj_lists) == 1000

    def test_perf_init_2000(self):
        """Создание графа с 2000 вершинами"""
        g = Graph(2000)
        assert g._num_vertices == 2000
        assert len(g._adj_matrix) == 2000
        assert len(g._adj_lists) == 2000

    def test_perf_init_5000(self):
        """Создание графа с 5000 вершинами"""
        g = Graph(5000)
        assert g._num_vertices == 5000
        assert len(g._adj_matrix) == 5000
        assert len(g._adj_lists) == 5000

    def test_perf_set_adj_matrix_100(self):
        """Установка матрицы 100x100"""
        n = 100
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_matrix()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_matrix_200(self):
        """Установка матрицы 200x200"""
        n = 200
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_matrix()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_matrix_500(self):
        """Установка матрицы 500x500"""
        n = 500
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_matrix()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_matrix_1000(self):
        """Установка матрицы 1000x1000"""
        n = 1000
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_matrix()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_matrix_2000(self):
        """Установка матрицы 2000x2000"""
        n = 2000
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_matrix()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_matrix_5000(self):
        """Установка матрицы 5000x5000"""
        n = 5000
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_matrix()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_list_100(self):
        """Установка списков для 100 вершин (полный граф)"""
        n = 100
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_list()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_list_200(self):
        """Установка списков для 200 вершин (полный граф)"""
        n = 200
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_list()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_list_500(self):
        """Установка списков для 500 вершин (полный граф)"""
        n = 500
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_list()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_list_1000(self):
        """Установка списков для 1000 вершин (полный граф)"""
        n = 1000
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_list()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_list_2000(self):
        """Установка списков для 2000 вершин (полный граф)"""
        n = 2000
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_list()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges

    def test_perf_set_adj_list_5000(self):
        """Установка списков для 5000 вершин (полный граф)"""
        n = 5000
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(n)
            g.set_adj_list()
            expected_edges = n * (n + 1) // 2
            assert g._num_edges == expected_edges