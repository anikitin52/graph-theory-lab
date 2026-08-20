import pytest
import time
import json
import os
from graph.graph import Graph


class TestHamiltonianPerformance:
    """Тесты производительности для гамильтонова цикла и пути"""

    # Папка для сохранения результатов
    RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'performance')

    @classmethod
    def setup_class(cls):
        """Создание папки для результатов перед запуском тестов"""
        os.makedirs(cls.RESULTS_DIR, exist_ok=True)

    def _save_results(self, algorithm, graph_type, results):
        """Сохранение результатов в JSON файл"""
        data = {
            "algorithm": algorithm,
            "type": graph_type,
            "results": results  # список [{"vertices": n, "time_ms": time}]
        }
        filename = f"{algorithm}_{graph_type}.json"
        filepath = os.path.join(self.RESULTS_DIR, filename)

        # Если файл существует, загружаем и обновляем
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            existing_results = {r["vertices"]: r["time_ms"] for r in existing_data.get("results", [])}
            for r in results:
                existing_results[r["vertices"]] = r["time_ms"]
            data["results"] = [{"vertices": k, "time_ms": v} for k, v in sorted(existing_results.items())]

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _run_cycle_test(self, n):
        """Запуск теста гамильтонова цикла на полном графе"""
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]
        graph._num_edges = n * (n - 1) // 2

        start_time = time.perf_counter()
        cycle = graph.find_hamiltonian_cycle()
        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000

        assert cycle is not None
        assert len(cycle) == n + 1
        assert cycle[0] == cycle[-1]
        assert set(cycle[:-1]) == set(range(1, n + 1))

        return elapsed_ms

    def _run_path_test(self, n):
        """Запуск теста гамильтонова пути на полном графе"""
        graph = Graph(n)
        graph._directed = False
        for i in range(n):
            graph._adj_lists[i] = [j for j in range(n) if j != i]

        start_time = time.perf_counter()
        path = graph.find_hamiltonian_path()
        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000

        assert path is not None
        assert len(path) == n
        assert set(path) == set(range(1, n + 1))

        return elapsed_ms

    # ==================== Гамильтонов цикл: полные графы ====================

    def test_hamiltonian_cycle_complete_5(self):
        n = 5
        elapsed = self._run_cycle_test(n)
        self._save_results("hamiltonian_cycle", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_cycle_complete_6(self):
        n = 6
        elapsed = self._run_cycle_test(n)
        self._save_results("hamiltonian_cycle", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_cycle_complete_7(self):
        n = 7
        elapsed = self._run_cycle_test(n)
        self._save_results("hamiltonian_cycle", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_cycle_complete_8(self):
        n = 8
        elapsed = self._run_cycle_test(n)
        self._save_results("hamiltonian_cycle", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_cycle_complete_9(self):
        n = 9
        elapsed = self._run_cycle_test(n)
        self._save_results("hamiltonian_cycle", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_cycle_complete_10(self):
        n = 10
        elapsed = self._run_cycle_test(n)
        self._save_results("hamiltonian_cycle", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_cycle_complete_12(self):
        n = 12
        elapsed = self._run_cycle_test(n)
        self._save_results("hamiltonian_cycle", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_cycle_complete_15(self):
        n = 15
        elapsed = self._run_cycle_test(n)
        self._save_results("hamiltonian_cycle", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    # ==================== Гамильтонов путь: полные графы ====================

    def test_hamiltonian_path_complete_5(self):
        n = 5
        elapsed = self._run_path_test(n)
        self._save_results("hamiltonian_path", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_path_complete_10(self):
        n = 10
        elapsed = self._run_path_test(n)
        self._save_results("hamiltonian_path", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_path_complete_15(self):
        n = 15
        elapsed = self._run_path_test(n)
        self._save_results("hamiltonian_path", "complete_graph", [{"vertices": n, "time_ms": elapsed}])

    def test_hamiltonian_path_complete_20(self):
        n = 20
        elapsed = self._run_path_test(n)
        self._save_results("hamiltonian_path", "complete_graph", [{"vertices": n, "time_ms": elapsed}])