import json
import os
import random
import time
import pytest

from graph.graph import Graph

SIZES = [2000, 4000, 6000, 8000, 10000]


# ==================== Генераторы графов ====================


def _build_graph(n, edges):
    """Graph на n вершинах (0-based); петли и дубликаты рёбер отбрасываются."""
    neighbours = [set() for _ in range(n)]
    for a, b in edges:
        if a != b:
            neighbours[a].add(b)
            neighbours[b].add(a)
    graph = Graph(n)
    graph._directed = False
    graph._adj_lists = {v: sorted(neighbours[v]) for v in range(n)}
    graph._num_edges = sum(len(x) for x in neighbours) // 2
    return graph


def _random_edges(n, m, rng, allowed=None):
    """m различных случайных рёбер; allowed(a, b) - необязательный фильтр пар вершин."""
    edges = set()
    while len(edges) < m:
        a, b = rng.randrange(n), rng.randrange(n)
        if a == b or (allowed and not allowed(a, b)):
            continue
        edges.add((min(a, b), max(a, b)))
    return edges


def gen_random_sparse(n, seed=1):
    """Случайный граф общего вида, средняя степень 10"""
    return _build_graph(n, _random_edges(n, 5 * n, random.Random(seed)))


def gen_random_dense(n, seed=1):
    """Случайный граф общего вида, средняя степень 50"""
    return _build_graph(n, _random_edges(n, 25 * n, random.Random(seed)))


def gen_bipartite(n, seed=1):
    """Случайный двудольный граф: чётные вершины - одна доля, нечётные - другая"""
    rng = random.Random(seed)
    return _build_graph(n, _random_edges(n, 5 * n, rng, allowed=lambda a, b: (a + b) % 2 == 1))


def gen_split(n, seed=1):
    """Случайный расщепляемый граф: клика из n//50 вершин + независимое множество,
    каждая независимая вершина соединена с 5 вершинами клики"""
    rng = random.Random(seed)
    k = max(6, n // 50)
    edges = [(i, j) for i in range(k) for j in range(i + 1, k)]
    for v in range(k, n):
        edges.extend((u, v) for u in rng.sample(range(k), 5))
    return _build_graph(n, edges)


def gen_chordal(n, seed=1):
    """Случайный триангулированный (хордальный) граф - 3-дерево: каждая новая вершина
    соединяется со всеми вершинами одной из ранее созданных клик"""
    rng = random.Random(seed)
    k = 3
    edges = [(i, j) for i in range(k + 1) for j in range(i + 1, k + 1)]
    cliques = [list(range(k + 1))]
    for v in range(k + 1, n):
        sub = rng.sample(rng.choice(cliques), k)
        edges.extend((u, v) for u in sub)
        cliques.append(sub + [v])
    return _build_graph(n, edges)


GENERATORS = {
    "random_sparse": gen_random_sparse,
    "random_dense": gen_random_dense,
    "bipartite": gen_bipartite,
    "split": gen_split,
    "chordal": gen_chordal,
}

class TestLongestCyclePerformance:
    """Тесты производительности поиска наибольшего простого цикла"""
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

    @staticmethod
    def _assert_valid_cycle(graph, cycle):
        """Цикл (1-based) простой и состоит из рёбер графа"""
        assert len(cycle) >= 3
        assert len(set(cycle)) == len(cycle)
        for i, v in enumerate(cycle):
            assert cycle[(i + 1) % len(cycle)] - 1 in graph._adj_lists[v - 1]

    def _run_performance_test(self, graph_type, n):
        """Генерирует граф, замеряет только find_longest_cycle, проверяет результат"""
        graph = GENERATORS[graph_type](n)

        start_time = time.perf_counter()
        cycle = graph.find_longest_cycle()
        end_time = time.perf_counter()

        self._assert_valid_cycle(graph, cycle)
        if graph_type == "bipartite":
            assert len(cycle) % 2 == 0
        return (end_time - start_time) * 1000

    @pytest.mark.parametrize("n", SIZES)
    def test_longest_cycle_perf_random_sparse(self, n):
        elapsed = self._run_performance_test("random_sparse", n)
        self._save_results("longest_cycle", "random_sparse", [{"vertices": n, "time_ms": elapsed}])

    @pytest.mark.parametrize("n", SIZES)
    def test_longest_cycle_perf_random_dense(self, n):
        elapsed = self._run_performance_test("random_dense", n)
        self._save_results("longest_cycle", "random_dense", [{"vertices": n, "time_ms": elapsed}])

    @pytest.mark.parametrize("n", SIZES)
    def test_longest_cycle_perf_bipartite(self, n):
        elapsed = self._run_performance_test("bipartite", n)
        self._save_results("longest_cycle", "bipartite", [{"vertices": n, "time_ms": elapsed}])

    @pytest.mark.parametrize("n", SIZES)
    def test_longest_cycle_perf_split(self, n):
        elapsed = self._run_performance_test("split", n)
        self._save_results("longest_cycle", "split", [{"vertices": n, "time_ms": elapsed}])

    @pytest.mark.parametrize("n", SIZES)
    def test_longest_cycle_perf_chordal(self, n):
        elapsed = self._run_performance_test("chordal", n)
        self._save_results("longest_cycle", "chordal", [{"vertices": n, "time_ms": elapsed}])