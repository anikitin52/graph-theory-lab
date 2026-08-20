import io
import pytest
from unittest.mock import patch
from graph.graph import Graph


class TestGraphInit:
    """Тесты для конструктора Graph"""

    def test_init_valid_int(self):
        """Создание графа с корректным целым числом"""
        g = Graph(5)
        assert g._num_vertices == 5
        assert g._num_edges == 0
        assert g._directed is False
        assert g._is_tournament is False
        assert len(g._adj_matrix) == 5
        assert all(len(row) == 5 for row in g._adj_matrix)
        assert len(g._adj_lists) == 5
        assert all(g._adj_lists[i] == [] for i in range(5))

    def test_init_zero_vertices(self):
        """Создание графа с 0 вершинами"""
        g = Graph(0)
        assert g._num_vertices == 0
        assert g._num_edges == 0
        assert g._adj_matrix == []
        assert g._adj_lists == {}

    def test_init_negative_vertices(self):
        """Отрицательное количество вершин"""
        with pytest.raises(ValueError) as exc_info:
            Graph(-1)
        assert "Количество вершин не может быть отрицательным" in str(exc_info.value)

    def test_init_float(self):
        """Вещественное число вместо целого"""
        with pytest.raises(TypeError) as exc_info:
            Graph(5.5)
        assert "Количество вершин должно быть целым числом" in str(exc_info.value)

    def test_init_string(self):
        """Строка вместо числа"""
        with pytest.raises(TypeError) as exc_info:
            Graph("5")
        assert "Количество вершин должно быть целым числом" in str(exc_info.value)

    def test_init_bool(self):
        """Булево значение вместо числа"""
        with pytest.raises(TypeError) as exc_info:
            Graph(True)
        assert "Количество вершин должно быть целым числом" in str(exc_info.value)

    def test_init_none(self):
        """None вместо числа"""
        with pytest.raises(TypeError) as exc_info:
            Graph(None)
        assert "Количество вершин должно быть целым числом" in str(exc_info.value)


class TestGraphSetAdjMatrix:
    """Тесты для метода set_adj_matrix"""

    def test_set_adj_matrix_directed(self):
        """Установка ориентированного графа матрицей"""
        input_data = "0 1 0\n0 0 1\n1 0 0"
        expected_matrix = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(3)
            g.set_adj_matrix()
            assert g._adj_matrix == expected_matrix
            assert g._directed is True
            assert g._num_edges == 3

    def test_set_adj_matrix_tournament(self):
        """Установка турнира матрицей"""
        input_data = "0 1 0\n0 0 1\n1 0 0"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(3)
            g.set_adj_matrix()
            assert g._is_tournament is True

    def test_set_adj_matrix_with_loops(self):
        """Установка графа с петлями"""
        input_data = "1 1 0\n1 0 1\n0 1 0"
        expected_matrix = [[1, 1, 0], [1, 0, 1], [0, 1, 0]]

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(3)
            g.set_adj_matrix()
            assert g._adj_matrix == expected_matrix

    def test_set_adj_matrix_one_vertex(self):
        """Граф с одной вершиной"""
        input_data = "0"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(1)
            g.set_adj_matrix()
            assert g._adj_matrix == [[0]]
            assert g._adj_lists == {0: []}
            assert g._num_edges == 0
            assert g._directed is False

    def test_set_adj_matrix_one_vertex_with_loop(self):
        """Граф с одной вершиной и петлей"""
        input_data = "1"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(1)
            g.set_adj_matrix()
            assert g._adj_matrix == [[1]]
            assert g._adj_lists == {0: [0]}
            assert g._num_edges == 1

    def test_set_adj_matrix_invalid_input(self):
        """Некорректный ввод матрицы"""
        input_data = "1 2\n3 4 5"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(2)
            with pytest.raises(ValueError):
                g.set_adj_matrix()

    def test_set_adj_matrix_empty_graph(self):
        """Пустой граф"""
        input_data = "0 0\n0 0"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(2)
            g.set_adj_matrix()
            assert g._adj_matrix == [[0, 0], [0, 0]]
            assert g._adj_lists == {0: [], 1: []}
            assert g._num_edges == 0
            assert g._directed is False


class TestGraphSetAdjList:
    """Тесты для метода set_adj_list"""

    def test_set_adj_list_undirected(self):
        """Установка неориентированного графа списками"""
        input_data = "2 3\n1 3\n1 2"
        expected_lists = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        expected_matrix = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(3)
            g.set_adj_list()
            assert g._adj_lists == expected_lists
            assert g._adj_matrix == expected_matrix
            assert g._directed is False
            assert g._num_edges == 3

    def test_set_adj_list_directed(self):
        """Установка ориентированного графа списками"""
        input_data = "2\n3\n1"
        expected_lists = {0: [1], 1: [2], 2: [0]}
        expected_matrix = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(3)
            g.set_adj_list()
            assert g._adj_lists == expected_lists
            assert g._adj_matrix == expected_matrix
            assert g._directed is True
            assert g._num_edges == 3

    def test_set_adj_list_with_loops(self):
        """Установка графа с петлями"""
        input_data = "1 2\n1 3\n2"
        expected_lists = {0: [0, 1], 1: [0, 2], 2: [1]}

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(3)
            g.set_adj_list()
            assert g._adj_lists == expected_lists
            assert g._adj_matrix[0][0] == 1

    def test_set_adj_list_one_vertex(self):
        """Граф с одной вершиной"""
        input_data = "\n"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(1)
            g.set_adj_list()
            assert g._adj_lists == {0: []}
            assert g._adj_matrix == [[0]]
            assert g._num_edges == 0

    def test_set_adj_list_one_vertex_with_loop(self):
        """Граф с одной вершиной и петлей"""
        input_data = "1"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(1)
            g.set_adj_list()
            assert g._adj_lists == {0: [0]}
            assert g._adj_matrix == [[1]]
            assert g._num_edges == 1

    def test_set_adj_list_invalid_vertex(self):
        """Несуществующая вершина в списке"""
        input_data = "2 4\n1 3\n1 2"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(3)
            with pytest.raises(ValueError):
                g.set_adj_list()

    def test_set_adj_list_empty_graph(self):
        """Пустой граф"""
        input_data = "\n\n\n"

        with patch('sys.stdin', io.StringIO(input_data)):
            g = Graph(3)
            g.set_adj_list()
            assert g._adj_lists == {0: [], 1: [], 2: []}
            assert g._adj_matrix == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            assert g._num_edges == 0


class TestGraphProperties:
    """Тесты для свойств графа после инициализации"""

    def test_num_vertices_property(self):
        """Проверка доступа к количеству вершин"""
        g = Graph(5)
        assert g._num_vertices == 5

    def test_num_edges_after_init(self):
        """Количество ребер после инициализации"""
        g = Graph(5)
        assert g._num_edges == 0

    def test_directed_property_after_init(self):
        """Направленность после инициализации"""
        g = Graph(5)
        assert g._directed is False

    def test_tournament_property_after_init(self):
        """Турнирность после инициализации"""
        g = Graph(5)
        assert g._is_tournament is False

    def test_adj_matrix_is_correct_type(self):
        """Проверка типа матрицы смежности"""
        g = Graph(3)
        assert isinstance(g._adj_matrix, list)
        assert all(isinstance(row, list) for row in g._adj_matrix)

    def test_adj_lists_is_correct_type(self):
        """Проверка типа списков смежности"""
        g = Graph(3)
        assert isinstance(g._adj_lists, dict)
        assert all(isinstance(key, int) for key in g._adj_lists.keys())
        assert all(isinstance(val, list) for val in g._adj_lists.values())