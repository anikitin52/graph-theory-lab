import pytest
from graph.graph import Graph


class TestHamiltonianCycle:
    """Функциональные тесты для гамильтонова цикла"""

    def test_hamiltonian_cycle_exists(self):
        """Граф C4 (цикл из 4 вершин) — гамильтонов цикл существует"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1, 3],
            1: [0, 2],
            2: [1, 3],
            3: [0, 2]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == 5
        assert cycle[0] == cycle[-1]
        # Метод возвращает 1-based, поэтому ожидаем [1,2,3,4]
        assert sorted(cycle[:-1]) == [1, 2, 3, 4]

    def test_hamiltonian_cycle_path_no_cycle(self):
        """Путь P4 (0-1-2-3) — гамильтонов путь есть, цикла нет"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is None

    def test_hamiltonian_cycle_no_path_no_cycle(self):
        """Две компоненты (0-1 и 2-3) — ни пути, ни цикла"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is None

    def test_hamiltonian_cycle_bipartite(self):
        """Двудольный граф K_{2,3} — цикла нет (доли разного размера)"""
        graph = Graph(5)
        graph._directed = False
        graph._adj_lists = {
            0: [2, 3, 4],
            1: [2, 3, 4],
            2: [0, 1],
            3: [0, 1],
            4: [0, 1]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is None

    def test_hamiltonian_cycle_split_graph(self):
        """Расщепляемый граф без гамильтонова цикла"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1, 2, 3],
            1: [0, 2],
            2: [0, 1],
            3: [0]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is None

    def test_hamiltonian_cycle_co_bipartite(self):
        """Дополнение двудольного графа — две несвязные клики, цикла нет"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is None

    def test_hamiltonian_cycle_chordal(self):
        """Хордальный граф (P4) — нет цикла"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is None

    def test_hamiltonian_cycle_directed(self):
        """Ориентированный цикл 0->1->2->0 — гамильтонов цикл существует"""
        graph = Graph(3)
        graph._directed = True
        graph._adj_lists = {
            0: [1],
            1: [2],
            2: [0]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == 4
        assert cycle[0] == cycle[-1]
        assert sorted(cycle[:-1]) == [1, 2, 3]

    def test_hamiltonian_cycle_multiple_edges(self):
        """Граф с кратными рёбрами (K3 с дубликатами) — цикл должен найтись"""
        graph = Graph(3)
        graph._directed = False
        graph._adj_lists = {
            0: [1, 1, 2],
            1: [0, 0, 2],
            2: [0, 1]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == 4
        assert cycle[0] == cycle[-1]
        assert sorted(cycle[:-1]) == [1, 2, 3]

    def test_hamiltonian_cycle_with_loop(self):
        """Граф с петлёй (K3 с петлёй у вершины 0) — цикл сохраняется"""
        graph = Graph(3)
        graph._directed = False
        graph._adj_lists = {
            0: [0, 1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == 4
        assert cycle[0] == cycle[-1]
        assert sorted(cycle[:-1]) == [1, 2, 3]


class TestHamiltonianPath:
    """Функциональные тесты для гамильтонова пути"""

    def test_hamiltonian_path_graph_with_cycle(self):
        """Граф C4 (цикл) — гамильтонов путь существует"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1, 3],
            1: [0, 2],
            2: [1, 3],
            3: [0, 2]
        }
        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == 4
        assert sorted(path) == [1, 2, 3, 4]

    def test_hamiltonian_path_path_no_cycle(self):
        """Путь P4 (0-1-2-3) — гамильтонов путь есть"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == 4
        assert set(path) == {1, 2, 3, 4}

    def test_hamiltonian_path_no_path_no_cycle(self):
        """Две компоненты (0-1 и 2-3) — ни пути, ни цикла"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        path = graph.find_hamiltonian_path()
        assert path is None

    def test_hamiltonian_path_split_graph(self):
        """Расщепляемый граф (клика {0,1}, независимое {2,3}, рёбра 0-2,0-3,1-2) — путь есть"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1, 2, 3],
            1: [0, 2],
            2: [0, 1],
            3: [0]
        }
        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == 4
        assert set(path) == {1, 2, 3, 4}

    def test_hamiltonian_path_co_bipartite(self):
        """Дополнение двудольного графа — две несвязные клики, пути нет"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        path = graph.find_hamiltonian_path()
        assert path is None

    def test_hamiltonian_path_chordal(self):
        """Хордальный граф P4 — путь есть"""
        graph = Graph(4)
        graph._directed = False
        graph._adj_lists = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == 4
        assert set(path) == {1, 2, 3, 4}

    def test_hamiltonian_path_directed(self):
        """Ориентированный путь 0->1->2 — гамильтонов путь существует"""
        graph = Graph(3)
        graph._directed = True
        graph._adj_lists = {
            0: [1],
            1: [2],
            2: []
        }
        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == 3
        assert set(path) == {1, 2, 3}

    def test_hamiltonian_path_multiple_edges(self):
        """Граф с кратными рёбрами (K3 с дубликатами) — путь есть"""
        graph = Graph(3)
        graph._directed = False
        graph._adj_lists = {
            0: [1, 1, 2],
            1: [0, 0, 2],
            2: [0, 1]
        }
        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == 3
        assert set(path) == {1, 2, 3}

    def test_hamiltonian_path_with_loop(self):
        """Граф с петлёй (K3 с петлёй у вершины 0) — путь существует"""
        graph = Graph(3)
        graph._directed = False
        graph._adj_lists = {
            0: [0, 1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == 3
        assert set(path) == {1, 2, 3}


class TestHamiltonianCycleTournament:
    """Функциональные тесты для гамильтонова цикла в турнире"""

    def test_hamiltonian_cycle_tournament_small_3(self):
        """Турнир на 3 вершинах (цикл 0->1->2->0) — цикл существует"""
        graph = Graph(3)
        graph._directed = True
        graph._adj_lists = {
            0: [1],
            1: [2],
            2: [0]
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        assert cycle is not None
        assert len(cycle) == 4
        assert cycle[0] == cycle[-1]
        assert sorted(cycle[:-1]) == [1, 2, 3]

    def test_hamiltonian_cycle_tournament_strongly_connected_4(self):
        """Сильно связный турнир на 4 вершинах (содержит цикл)"""
        graph = Graph(4)
        graph._directed = True
        graph._adj_lists = {
            0: [1, 2],
            1: [2, 3],
            2: [3],
            3: [0]
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        assert cycle is not None
        assert len(cycle) == 5
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == {1, 2, 3, 4}

    def test_hamiltonian_cycle_tournament_not_strongly_connected_4(self):
        """Турнир с источником (0) — не сильно связный, цикла нет"""
        graph = Graph(4)
        graph._directed = True
        graph._adj_lists = {
            0: [1, 2, 3],
            1: [2, 3],
            2: [3],
            3: []
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        assert cycle is None

    def test_hamiltonian_cycle_tournament_strongly_connected_5(self):
        """Сильно связный турнир на 5 вершинах (содержит цикл)"""
        graph = Graph(5)
        graph._directed = True
        graph._adj_lists = {
            0: [1, 2],
            1: [2, 3, 4],
            2: [3, 4],
            3: [4, 0],
            4: [0]
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        assert cycle is not None
        assert len(cycle) == 6
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == {1, 2, 3, 4, 5}

    def test_hamiltonian_cycle_tournament_single_vertex(self):
        """Турнир из одной вершины — гамильтонова цикла нет"""
        graph = Graph(1)
        graph._directed = True
        graph._adj_lists = {0: []}
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        assert cycle is None

    def test_hamiltonian_cycle_tournament_two_vertices(self):
        """Турнир на 2 вершинах (0->1) — цикла нет"""
        graph = Graph(2)
        graph._directed = True
        graph._adj_lists = {
            0: [1],
            1: []
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        assert cycle is None

    def test_hamiltonian_cycle_tournament_transitive_5(self):
        """Транзитивный турнир на 5 вершинах — не сильно связный, цикла нет"""
        graph = Graph(5)
        graph._directed = True
        graph._adj_lists = {
            0: [1, 2, 3, 4],
            1: [2, 3, 4],
            2: [3, 4],
            3: [4],
            4: []
        }
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        assert cycle is None

    def test_hamiltonian_cycle_tournament_zero_vertices(self):
        """Пустой турнир (0 вершин) — цикла нет"""
        graph = Graph(0)
        graph._directed = True
        graph._adj_lists = {}
        graph._adj_lists_to_adj_matrix()
        cycle = graph.find_hamiltonian_cycle_tournament()
        assert cycle is None