import io
import pytest
from unittest.mock import patch
from graph.graph_input import input_adj_matrix


class TestInputAdjMatrix:
    """ Тесты для ввода матрицы смежности """

    def test_correct_matrix(self):
        """Корректная матрица 3*3 """
        input_data = "1 0 1 \n0 1 0 \n1 0 1"
        output_data = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(3)
            assert result == output_data