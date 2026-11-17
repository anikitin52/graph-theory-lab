import random
import pytest
from graph.graph import Graph


# ==================== Вспомогательные функции ====================

def build_graph(n, edges):
    """Граф на n вершинах (0-based) из списка рёбер; петли и дубликаты отбрасываются."""
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

def cycle_graph(n):
    return build_graph(n, [(i, (i + 1) % n) for i in range(n)])

def complete_graph(n):
    return build_graph(n, [(i, j) for i in range(n) for j in range(i + 1, n)])

def complete_bipartite(a, b):
    return build_graph(a + b, [(i, a + j) for i in range(a) for j in range(b)])

def assert_valid_cycle(graph, cycle):
    """Проверяет, что cycle (1-based) - простой цикл в графе: длина >= 3, вершины
    различны, соседние (и последняя с первой) вершины смежны."""
    assert len(cycle) >= 3
    assert len(set(cycle)) == len(cycle), "вершины цикла повторяются"
    assert all(1 <= v <= graph._num_vertices for v in cycle), "вершина вне диапазона 1..n"
    for i, v in enumerate(cycle):
        nxt = cycle[(i + 1) % len(cycle)]
        assert nxt - 1 in graph._adj_lists[v - 1], f"нет ребра {v}-{nxt}"

def has_cycle(n, edges):
    """Есть ли в графе цикл: |E| > |V| - (число компонент связности)."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    components = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            components -= 1
    return len(set(edges)) > n - components

def brute_force_longest_cycle(graph):
    """Длина наибольшего простого цикла полным перебором (для n <= 9)."""
    n = graph._num_vertices
    adj = graph._adj_lists
    best = 0

    def dfs(start, v, visited, length):
        nonlocal best
        for w in adj[v]:
            if w == start and length >= 3:
                best = max(best, length)
            elif w > start and w not in visited:
                visited.add(w)
                dfs(start, w, visited, length + 1)
                visited.remove(w)

    for s in range(n):
        dfs(s, s, {s}, 1)
    return best

def random_edges(n, p, rng):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]

class TestLongestCycle:
    """Тесты для поиска наибольшего простого цикла (ветвь DFS-дерева + обратное ребро). """

    # ---------- Обычные графы ----------

    def test_square_with_diagonals(self):
        """Квадрат с диагоналями (K4) - наибольший цикл содержит все 4 вершины"""
        graph = build_graph(4, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)])
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert sorted(cycle) == [1, 2, 3, 4]

    @pytest.mark.parametrize("n", [3, 5, 8])
    def test_complete_graph(self, n):
        graph = complete_graph(n)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert len(cycle) == n

    def test_two_triangles_sharing_edge(self):
        """Ромб (K4 без ребра): наибольший цикл 4, алгоритм даёт корректный цикл длины 3..4"""
        graph = build_graph(4, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert 3 <= len(cycle) <= 4

    # ---------- Единственный цикл ----------

    @pytest.mark.parametrize("n", [3, 4, 7])
    def test_single_cycle_graph(self, n):
        """Граф-цикл C_n - единственный цикл содержит все вершины"""
        graph = cycle_graph(n)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert sorted(cycle) == list(range(1, n + 1))

    def test_single_cycle_with_tail(self):
        """Треугольник с «хвостом» 2-3-4: в цикл хвост не входит"""
        graph = build_graph(5, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)])
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert set(cycle) == {1, 2, 3}

    def test_single_cycle_with_isolated_vertices(self):
        """C4 и две изолированные вершины"""
        graph = build_graph(6, [(0, 1), (1, 2), (2, 3), (3, 0)])
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert set(cycle) == {1, 2, 3, 4}

    # ---------- Графы без циклов ----------

    def test_empty_graph_zero_vertices(self):
        """Граф без вершин - циклов нет"""
        assert Graph(0).find_longest_cycle() == []

    def test_single_vertex(self):
        """Одна вершина - циклов нет"""
        assert Graph(1).find_longest_cycle() == []

    def test_no_edges(self):
        """Граф без рёбер - циклов нет"""
        assert Graph(5).find_longest_cycle() == []

    def test_single_edge(self):
        """Одно ребро - цикла нет"""
        assert build_graph(2, [(0, 1)]).find_longest_cycle() == []

    def test_path_graph(self):
        """Путь P6 - цикла нет"""
        graph = build_graph(6, [(i, i + 1) for i in range(5)])
        assert graph.find_longest_cycle() == []

    def test_star_graph(self):
        """Звезда - дерево, цикла нет"""
        graph = build_graph(6, [(0, i) for i in range(1, 6)])
        assert graph.find_longest_cycle() == []

    def test_forest(self):
        """Лес из двух деревьев - цикла нет"""
        graph = build_graph(7, [(0, 1), (1, 2), (1, 3), (4, 5), (5, 6)])
        assert graph.find_longest_cycle() == []

    # ---------- Другие стандартные случаи ----------

    def test_disconnected_picks_largest_cycle(self):
        """Две компоненты: треугольник и C5 - выбирается цикл длины 5"""
        edges = [(0, 1), (1, 2), (2, 0)] + [(3 + i, 3 + (i + 1) % 5) for i in range(5)]
        graph = build_graph(8, edges)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert set(cycle) == {4, 5, 6, 7, 8}

    def test_wheel_graph(self):
        """Колесо W6 (центр + C5) - корректный цикл, не длиннее 6"""
        edges = [(i, i % 5 + 1) for i in range(1, 6)] + [(0, i) for i in range(1, 6)]
        graph = build_graph(6, edges)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert len(cycle) <= 6

    def test_cube_graph(self):
        """Куб Q3 (гамильтонов, цикл длины 8) - корректный цикл длины 4..8"""
        edges = [(v, v ^ (1 << b)) for v in range(8) for b in range(3) if v < v ^ (1 << b)]
        graph = build_graph(8, edges)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert 4 <= len(cycle) <= 8

    def test_directed_graph_raises(self):
        """Ориентированный граф не поддерживается - ValueError"""
        graph = Graph(3)
        graph._directed = True
        graph._adj_lists = {0: [1], 1: [2], 2: [0]}
        with pytest.raises(ValueError):
            graph.find_longest_cycle()

    def test_self_loops_and_multiple_edges_ignored(self):
        """Петли и кратные рёбра сами цикла не образуют"""
        graph = Graph(2)
        graph._directed = False
        graph._adj_lists = {0: [0, 1, 1], 1: [0, 0, 1]}
        assert graph.find_longest_cycle() == []

    def test_graph_not_modified(self):
        """Поиск цикла не изменяет граф"""
        graph = complete_graph(5)
        before = {v: list(x) for v, x in graph._adj_lists.items()}
        graph.find_longest_cycle()
        assert graph._adj_lists == before

        # ---------- Случайные графы ----------

        @pytest.mark.parametrize("n", [5, 7, 9])
        def test_random_graphs(self, n):
            """Случайные графы G(n, p): цикл корректен, найден тогда и только тогда, когда
            граф не является лесом, и не длиннее настоящего наибольшего цикла (перебор)"""
            rng = random.Random(n)
            for p in (0.15, 0.3, 0.5, 0.8):
                for _ in range(10):
                    edges = random_edges(n, p, rng)
                    graph = build_graph(n, edges)
                    cycle = graph.find_longest_cycle()
                    if not has_cycle(n, edges):
                        assert cycle == []
                    else:
                        assert_valid_cycle(graph, cycle)
                        assert len(cycle) <= brute_force_longest_cycle(graph)

    # ---------- Двудольные графы ----------

    def test_complete_bipartite_k33(self):
        """K_{3,3} - гамильтонов цикл длины 6"""
        graph = complete_bipartite(3, 3)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert len(cycle) == 6

    def test_complete_bipartite_k23(self):
        """K_{2,3} - доли разного размера, наибольший цикл длины 4"""
        graph = complete_bipartite(2, 3)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert len(cycle) == 4

    def test_random_bipartite_even_cycle(self):
        """В двудольном графе все циклы чётной длины"""
        rng = random.Random(42)
        for _ in range(10):
            n = 12
            edges = [(i, j) for i in range(0, n, 2) for j in range(1, n, 2) if rng.random() < 0.4]
            graph = build_graph(n, edges)
            cycle = graph.find_longest_cycle()
            if cycle:
                assert_valid_cycle(graph, cycle)
                assert len(cycle) % 2 == 0
                assert all((v - 1) % 2 == (cycle[0] - 1 + i) % 2 for i, v in enumerate(cycle))

    def test_bipartite_tree_no_cycle(self):
        """Дерево двудольно, но цикла в нём нет"""
        graph = build_graph(7, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
        assert graph.find_longest_cycle() == []

    # ---------- Расщепляемые графы ----------

    def test_split_graph_pendant_independent(self):
        """Клика K4 + 3 висячие независимые вершины - цикл только по клике (длина 4)"""
        edges = [(i, j) for i in range(4) for j in range(i + 1, 4)] + [(0, 4), (1, 5), (2, 6)]
        graph = build_graph(7, edges)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert sorted(cycle) == [1, 2, 3, 4]

    def test_split_graph_independent_degree_two(self):
        """Расщепляемый граф: независимые вершины не могут стоять в цикле рядом"""
        k = 4
        edges = [(i, j) for i in range(k) for j in range(i + 1, k)]
        edges += [(k, 0), (k, 1), (k + 1, 1), (k + 1, 2), (k + 2, 2), (k + 2, 3)]
        graph = build_graph(k + 3, edges)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        independent_in_cycle = [v for v in cycle if v - 1 >= k]
        assert len(independent_in_cycle) <= len(cycle) // 2

    # ---------- Триангулированные (хордальные) графы ----------

    @pytest.mark.parametrize("n", [4, 6, 10])
    def test_triangulated_polygon_fan(self, n):
        """Триангуляция n-угольника «веером» из вершины 0 - гамильтонов цикл длины n"""
        edges = [(i, i + 1) for i in range(n - 1)] + [(0, n - 1)] + [(0, i) for i in range(2, n - 1)]
        graph = build_graph(n, edges)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert len(cycle) == n

    def test_random_chordal_graph(self):
        """Случайное 2-дерево (хордальный граф): цикл корректен, длина не больше n"""
        rng = random.Random(7)
        n = 12
        edges = [(0, 1), (0, 2), (1, 2)]
        triangles = [(0, 1, 2)]
        for v in range(3, n):
            a, b, c = rng.choice(triangles)
            x, y = rng.sample([a, b, c], 2)
            edges += [(x, v), (y, v)]
            triangles.append((x, y, v))
        graph = build_graph(n, edges)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert len(cycle) <= n

    def test_chordal_block_graph_triangles_chain(self):
        """Цепочка треугольников, соединённых вершинами - наибольший цикл 3"""
        graph = build_graph(7, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2), (4, 5), (5, 6), (6, 4)])
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert len(cycle) == 3

    # ---------- Прочие типы графов ----------

    def test_grid_graph(self):
        """Решётка 3x4 - корректный цикл длины 4..12"""
        rows, cols = 3, 4
        edges = []
        for r in range(rows):
            for c in range(cols):
                v = r * cols + c
                if c + 1 < cols:
                    edges.append((v, v + 1))
                if r + 1 < rows:
                    edges.append((v, v + cols))
        graph = build_graph(rows * cols, edges)
        cycle = graph.find_longest_cycle()
        assert_valid_cycle(graph, cycle)
        assert 4 <= len(cycle) <= rows * cols

    def test_cycle_returned_one_based(self):
        """Вершины цикла возвращаются в 1-based"""
        graph = cycle_graph(4)
        cycle = graph.find_longest_cycle()
        assert min(cycle) >= 1 and max(cycle) <= 4
        assert 0 not in cycle
