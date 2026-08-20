import io
import pytest
from unittest.mock import patch
from graph.graph_input import input_adj_matrix, input_adj_lists


class TestInputAdjMatrix:
    """ Тесты для ввода матрицы смежности """

    def test_correct_matrix(self):
        """Корректная матрица 3*3. Ввод num_vertices = 3 и матрицы 3*3 """
        input_data = "1 0 1 \n0 1 0 \n1 0 1"
        output_data = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(3)
            assert result == output_data

    def test_row_shorter_than_num_vertices(self):
        """Строка короче num_vertices. Ввод num_vertices = 3 и матрицы 2*3"""
        input_data = "1 0\n0 1 0\n1 0 1"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_matrix(3)
            assert "ожидалось 3 элементов, получено 2" in str(exc_info.value)

    def test_row_longer_than_num_vertices(self):
        """Строка длиннее num_vertices. Ввод num_vertices = 3 и матрицы 4*3"""
        input_data = "1 0 1 0\n0 1 0 0\n1 0 1 0"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_matrix(3)
            assert "ожидалось 3 элементов, получено 4" in str(exc_info.value)

    def test_incorrect_length_one_row(self):
        """Неправильная длина одной строки. Ввод num_vertices = 3 и рядов длиной 3, 2, 3"""
        input_data = "1 0 1\n0 1\n1 0 1"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_matrix(3)
            assert "ожидалось 3 элементов, получено 2" in str(exc_info.value)

    def test_zero_matrix(self):
        """Нулевая матрица. Ввод num_vertices = 0"""
        input_data = ""
        output_data = []

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(0)
            assert result == output_data

    def test_non_numeric_values(self):
        """Нечисловые значения. Ввод num_vertices = 3 и в ряде символ abc"""
        input_data = "1 0 1\n0 abc 0\n1 0 1"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_matrix(3)
            assert "все значения должны быть целыми числами" in str(exc_info.value)

    def test_empty_line(self):
        """Пустая строка. Ввод num_vertices = 3 и строк длиной 3, 0, 3"""
        input_data = "1 0 1\n\n1 0 1"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_matrix(3)
            assert "ожидалось 3 элементов, получено 0" in str(exc_info.value)

    def test_extra_spaces(self):
        """Лишние пробелы. Ввод num_vertices = 3 и одной из строк '1   2   3'"""
        input_data = "1   2   3\n4 5 6\n7 8 9"
        output_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(3)
            assert result == output_data

    def test_negative_values(self):
        """Отрицательные значения"""
        input_data = "-1 0 1\n0 -2 0\n1 0 -3"
        output_data = [[-1, 0, 1], [0, -2, 0], [1, 0, -3]]

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(3)
            assert result == output_data

    def test_float_values(self):
        """Дробные значения"""
        input_data = "1.5 0 1\n0 2.5 0\n1 0 3.5"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_matrix(3)
            assert "все значения должны быть целыми числами" in str(exc_info.value)

    def test_num_vertices_one(self):
        """num_vertices = 1"""
        input_data = "5"
        output_data = [[5]]

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_matrix(1)
            assert result == output_data


class TestInputAdjLists:
    """ Тесты для ввода списков смежности """

    def test_correct_adj_list(self):
        """Корректный список смежности. num_vertices = 3, списки длиной 3"""
        input_data = "2 3\n1 3\n1 2"
        output_data = {0: [1, 2], 1: [0, 2], 2: [0, 1]}

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(3)
            assert result == output_data

    def test_row_shorter_than_num_vertices(self):
        """Строка короче num_vertices. num_vertices = 3, строки длиной 2"""
        input_data = "2 3\n1\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(3)
            expected = {0: [1, 2], 1: [0], 2: [0, 1]}
            assert result == expected

    def test_row_longer_than_num_vertices(self):
        """Строка длиннее num_vertices. num_vertices = 3, строка длиной 4"""
        input_data = "2 3 4 5\n1 3\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_lists(3)
            assert "вершины 4 не существует" in str(exc_info.value) or "вершины 5 не существует" in str(exc_info.value)

    def test_different_row_lengths(self):
        """Разная длина строк. num_vertices = 3, строки длиной 3, 2, 1"""
        input_data = "2 3\n1 3\n1"
        output_data = {0: [1, 2], 1: [0, 2], 2: [0]}

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(3)
            assert result == output_data

    def test_zero_length_row(self):
        """Нулевая длина строки. num_vertices = 3, строки длиной 0"""
        input_data = "2 3\n\n1 2"
        output_data = {0: [1, 2], 1: [], 2: [0, 1]}

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(3)
            assert result == output_data

    def test_num_vertices_zero(self):
        """num_vertices = 0"""
        input_data = ""
        output_data = {}

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(0)
            assert result == output_data

    def test_num_vertices_one(self):
        """num_vertices = 1"""
        input_data = "\n"  # Одна пустая строка
        output_data = {0: []}

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(1)
            assert result == output_data

    def test_non_numeric_values(self):
        """Нечисловые значения"""
        input_data = "2 abc\n1 3\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_lists(3)
            assert "все значения должны быть целыми числами" in str(exc_info.value)

    def test_extra_spaces(self):
        """Лишние пробелы"""
        input_data = "2   3\n1   3\n1   2"
        output_data = {0: [1, 2], 1: [0, 2], 2: [0, 1]}

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(3)
            assert result == output_data

    def test_negative_values(self):
        """Отрицательные значения"""
        input_data = "-1 3\n1 -2\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_lists(3)
            assert "вершины -1 не существует" in str(exc_info.value)

    def test_float_values(self):
        """Дробные значения"""
        input_data = "2 3.5\n1 3\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_lists(3)
            assert "все значения должны быть целыми числами" in str(exc_info.value)

    def test_nonexistent_vertex(self):
        """Несуществующая вершина. num_vertices = 3, ввод вершины 4"""
        input_data = "2 4\n1 3\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_lists(3)
            assert "вершины 4 не существует" in str(exc_info.value)

    def test_zero_vertex(self):
        """Нулевая вершина. num_vertices = 3, ввод вершины 0"""
        input_data = "2 0\n1 3\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            with pytest.raises(ValueError) as exc_info:
                input_adj_lists(3)
            assert "вершины 0 не существует" in str(exc_info.value)

    def test_duplicate_vertices(self):
        """Повторяющиеся вершины. num_vertices = 3, ввод строки [2, 2, 3]"""
        input_data = "2 2 3\n1 3\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(3)
            expected = {0: [1, 1, 2], 1: [0, 2], 2: [0, 1]}
            assert result == expected

    def test_self_loop(self):
        """Петля. Ввод для вершины 1 в список вершины 1"""
        input_data = "1 2\n1 3\n1 2"
        output_data = {0: [0, 1], 1: [0, 2], 2: [0, 1]}

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(3)
            assert result == output_data

    def test_empty_graph(self):
        """Полностью пустой граф"""
        input_data = "\n\n\n"  # Три пустые строки
        output_data = {0: [], 1: [], 2: []}

        with patch('sys.stdin', io.StringIO(input_data)):
            result = input_adj_lists(3)
            assert result == output_data