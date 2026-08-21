import io
import pytest
import time
import json
import os
from unittest.mock import patch
from graph.graph import Graph


class TestEulerianPerformance:
    """Тесты производительности для Эйлерова цикла"""

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
            # Объединяем результаты
            existing_results = {r["vertices"]: r["time_ms"] for r in existing_data.get("results", [])}
            for r in results:
                existing_results[r["vertices"]] = r["time_ms"]
            data["results"] = [{"vertices": k, "time_ms": v} for k, v in sorted(existing_results.items())]

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _run_performance_test(self, n, graph_type, expected_cycle=True):
        """Запуск теста производительности и возврат времени выполнения"""
        graph = Graph(n)
        graph._directed = False

        if graph_type == "cycle":
            # Циклический граф - есть эйлеров цикл
            for i in range(n):
                graph._adj_lists[i] = [(i - 1) % n, (i + 1) % n]
            graph._num_edges = n
        else:  # path
            # Путь - нет эйлерова цикла
            for i in range(n):
                neighbors = []
                if i > 0:
                    neighbors.append(i - 1)
                if i < n - 1:
                    neighbors.append(i + 1)
                graph._adj_lists[i] = neighbors
            graph._num_edges = n - 1

        start_time = time.perf_counter()
        cycle = graph.find_eulerian_cycle()
        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000

        if expected_cycle:
            assert cycle is not None
            assert len(cycle) == n + 1
            assert cycle[0] == cycle[-1]
        else:
            assert cycle is None

        return elapsed_ms

    # ==================== Графы с Эйлеровым циклом ====================

    def test_eulerian_cycle_perf_100(self):
        n = 100
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_200(self):
        n = 200
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_500(self):
        n = 500
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_1000(self):
        n = 1000
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_2000(self):
        n = 2000
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_5000(self):
        n = 5000
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_10000(self):
        n = 10000
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_15000(self):
        n = 15000
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_20000(self):
        n = 20000
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_eulerian_cycle_perf_25000(self):
        n = 25000
        elapsed = self._run_performance_test(n, "cycle", True)
        self._save_results("eulerian", "with_cycle", [{"vertices": n, "time_ms": elapsed}])

    # ==================== Графы без Эйлерова цикла ====================

    def test_non_eulerian_perf_100(self):
        n = 100
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_200(self):
        n = 200
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_500(self):
        n = 500
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_1000(self):
        n = 1000
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_2000(self):
        n = 2000
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_5000(self):
        n = 5000
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_10000(self):
        n = 10000
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_15000(self):
        n = 15000
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_20000(self):
        n = 20000
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])

    def test_non_eulerian_perf_25000(self):
        n = 25000
        elapsed = self._run_performance_test(n, "path", False)
        self._save_results("eulerian", "without_cycle", [{"vertices": n, "time_ms": elapsed}])