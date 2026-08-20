import io
import pytest
from unittest.mock import patch
from graph.graph_input import input_adj_matrix, input_adj_lists


class TestePerformanceInput:
    """Тестирование производительности ввода данных"""

    def test_perf_matrix_1000(self):
        """perf: num_vertices = 1000"""
        n = 1000
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(n)
            assert len(result) == n
            assert all(len(row) == n for row in result)

    def test_perf_matrix_2000(self):
        """perf: num_vertices = 2000"""
        n = 2000
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(n)
            assert len(result) == n
            assert all(len(row) == n for row in result)

    def test_perf_matrix_5000(self):
        """perf: num_vertices = 5000"""
        n = 5000
        rows = [" ".join("1" for _ in range(n)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(n)
            assert len(result) == n
            assert all(len(row) == n for row in result)

    def test_perf_lists_1000(self):
        """perf: num_vertices = 1000"""
        n = 1000
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(n)
            assert len(result) == n

    def test_perf_lists_2000(self):
        """perf: num_vertices = 2000"""
        n = 2000
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(n)
            assert len(result) == n

    def test_perf_lists_5000(self):
        """perf: num_vertices = 5000"""
        n = 5000
        rows = [" ".join(str(i) for i in range(1, n + 1)) for _ in range(n)]
        input_data = "\n".join(rows)

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(n)
            assert len(result) == n
