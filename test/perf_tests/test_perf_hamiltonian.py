import pytest
from graph.graph import Graph


class TestHamiltonianPerformance:
    """Тесты производительности для гамильтонова цикла и пути"""

    # ==================== Гамильтонов цикл: полные графы ====================

    def test_hamiltonian_cycle_complete_5(self):
        """Полный граф K5 — гамильтонов цикл существует"""
        n = 5
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

    def test_hamiltonian_cycle_complete_6(self):
        """Полный граф K6 — гамильтонов цикл существует"""
        n = 6
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

    def test_hamiltonian_cycle_complete_7(self):
        """Полный граф K7 — гамильтонов цикл существует"""
        n = 7
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

    def test_hamiltonian_cycle_complete_8(self):
        """Полный граф K8 — гамильтонов цикл существует"""
        n = 8
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

    def test_hamiltonian_cycle_complete_9(self):
        """Полный граф K9 — гамильтонов цикл существует"""
        n = 9
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

    def test_hamiltonian_cycle_complete_10(self):
        """Полный граф K10 — гамильтонов цикл существует"""
        n = 10
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

    def test_hamiltonian_cycle_complete_12(self):
        """Полный граф K12 — гамильтонов цикл существует"""
        n = 12
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

    def test_hamiltonian_cycle_complete_15(self):
        """Полный граф K15 — гамильтонов цикл существует"""
        n = 15
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        cycle = graph.find_hamiltonian_cycle()
        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

    # ==================== Гамильтонов путь: полные графы ====================

    def test_hamiltonian_path_complete_5(self):
        """Полный граф K5 — гамильтонов путь существует"""
        n = 5
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]

        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == n
        assert set(path) == set(range(1, n + 1))

    def test_hamiltonian_path_complete_10(self):
        """Полный граф K10 — гамильтонов путь существует"""
        n = 10
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]

        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == n
        assert set(path) == set(range(1, n + 1))

    def test_hamiltonian_path_complete_15(self):
        """Полный граф K15 — гамильтонов путь существует"""
        n = 15
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]

        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == n
        assert set(path) == set(range(1, n + 1))

    def test_hamiltonian_path_complete_20(self):
        """Полный граф K20 — гамильтонов путь существует"""
        n = 20
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]

        path = graph.find_hamiltonian_path()
        assert path is not None
        assert len(path) == n
        assert set(path) == set(range(1, n + 1))