from graph_input import input_adj_matrix
from graph_input import input_adj_lists


class Graph:
    def __init__(self, num_vertices):
        self._num_vertices = num_vertices

        self._num_edges = 0
        self._directed = False
        self._adj_matrix = [[0] * self._num_vertices for _ in range(self._num_vertices)]
        self._adj_lists = {i: [] for i in range(self._num_vertices)}

    # ВВОД ДАННЫХ
    def set_adj_matrix(self):
        """
        Задание графа матрицей смежности
        :return:
        """
        self._adj_matrix = input_adj_matrix(self._num_vertices)  # Матрица смежности
        self._directed = self._is_directed_by_matrix()  # Ориентированность графа
        self._num_edges = self._count_edges_from_matrix()  # Количество ребер
        self._adj_matrix_to_adj_lists()  # Перевод в списки смежности

    def set_adj_list(self):
        """
        Задание графа списками смежности
        :return:
        """
        self._adj_lists = input_adj_lists(self._num_vertices)  # Списки смежности
        self._directed = self._is_directed_by_lists()  # Ориентированность графа
        self._num_edges = self._count_edges_from_lists()  # Количество ребер
        self._adj_lists_to_adj_matrix()  # Перевод в матрицу смежности

    # КЛАССИФИКАЦИЯ ГРАФА
    def _is_directed_by_matrix(self):
        """
        Определяет, является ли граф ориентированным по его матрице смежности
        :return: статус ориентированности графа
        """
        matrix = self._adj_matrix
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] != matrix[j][i]:
                    return True
        return False

    def _is_directed_by_lists(self):
        """
        Определяет, является ли граф ориентированным по его спискам смежности
        :return: статус ориентированности графа
        """
        lists = self._adj_lists
        all_edges = set()  # Создание множества всех ребер
        for vertex, neighbors in lists.items():
            for neighbor in neighbors:
                all_edges.add((vertex, neighbor))

        # Проверка наличия обратных ребер
        for u, v in all_edges:
            if (v, u) not in all_edges:
                return True
        return False

    def _count_edges_from_matrix(self):
        """
        Подсчет ребер по матрице смежности
        :return: количество ребер в графе
        """
        n = len(self._adj_matrix)
        matrix = self._adj_matrix
        edges = 0

        if self._directed:
            # Граф ориентированный. Считаем все ненулевые элементы
            for i in range(n):
                for j in range(n):
                    if matrix[i][j] != 0:
                        edges += 1
            return edges
        else:
            # Граф неориентированный. Считаем только верхний треугольник
            for i in range(n):
                for j in range(i, n):
                    if matrix[i][j] != 0:
                        edges += 1
            return edges

    def _count_edges_from_lists(self):
        """
        Подсчет ребер по спискам смежности
        :return: количество ребер в графе
        """
        if self._directed:
            return sum(len(neighbors) for neighbors in self._adj_lists.values())
        else:
            edges = set()

            for vertex, neighbors in self._adj_lists.items():
                for neighbor in neighbors:
                    edge = (min(vertex, neighbor), max(vertex, neighbor))
                    edges.add(edge)
            return len(edges)

    # ПРЕОБРАЗОВАНИЯ
    def _adj_matrix_to_adj_lists(self):
        """
        Преобразование из матрицы смежности в списки смежности
        :return: None
        """
        self._adj_lists = {i: [] for i in range(self._num_vertices)}
        for i in range(self._num_vertices):
            for j in range(self._num_vertices):
                if self._adj_matrix[i][j] != 0:
                    self._adj_lists[i].append(j)

    def _adj_lists_to_adj_matrix(self):
        """
        Преобразование из списков смежности в матрицу смежности
        :return: None
        """
        self._adj_matrix = [[0] * self._num_vertices for _ in range(self._num_vertices)]
        for vertex, neighbours in self._adj_lists.items():
            for neighbour in neighbours:
                self._adj_matrix[vertex][neighbour] = 1
                if not self._directed:
                    self._adj_matrix[neighbour][vertex] = 1

    def __str__(self):
        """
        Преобразование графа в строку
        :return: Строковое описание графа
        """
        result = f''' Граф
            Вершин: {self._num_vertices} 
            Ребер: {self._num_edges}
            {'ориентированный' if self._directed else 'неориeнтированный'} 
            '''
        result += "\nМатрица смежности \n"
        for row in self._adj_matrix:
            result += ' '.join(map(str, row)) + '\n'

        result += "Списки смежности: \n"
        for vertex in sorted(self._adj_lists.keys()):
            # Преобразуем обратно к 1-based для отображения
            neighbors_1based = [x + 1 for x in self._adj_lists[vertex]]
            result += f'{vertex + 1}: {neighbors_1based}\n'

        return result

    # ДРУГОЕ


'''
    def _is_eulerian(self):
        if self.directed:
            out_degree = [len(self.adj_lists[i]) for i in range(self.num_vertices)]
            in_degree = [0] * self.num_vertices
            for i in range(self.num_vertices):
                for neighbor in self.adj_lists[i]:
                    in_degree[neighbor] += 1
            return all(out_degree[i] == in_degree[i] for i in range(self.num_vertices))
        else:
            # Для неориентированного графа: каждая петля добавляет 2 к степени
            degrees = [0] * self.num_vertices
            for i in range(self.num_vertices):
                for neighbor in self.adj_lists[i]:
                    if neighbor == i:  # Петля
                        degrees[i] += 2
                    else:
                        degrees[i] += 1
            return all(degree % 2 == 0 for degree in degrees)

    def find_eulerian_cycle(self):
        if not self._is_eulerian():
            print('No Eulerian cycle')
            return None

        # Создаем копию структуры графа
        adj_list_copy = {}
        for v in range(self.num_vertices):
            adj_list_copy[v] = self.adj_lists[v][:]  # Всегда используем списки

        stack = []
        cycle = []

        # Выбор стартовой вершины
        start_vertex = 0
        for i in range(self.num_vertices):
            if adj_list_copy[i]:
                start_vertex = i
                break

        current_vertex = start_vertex

        while True:
            # Если есть ребра из текущей вершины
            if adj_list_copy[current_vertex]:
                stack.append(current_vertex)
                next_vertex = adj_list_copy[current_vertex].pop()

                # Удаляем обратное ребро для неориентированного графа
                if not self.directed and current_vertex != next_vertex:
                    # Находим и удаляем обратное ребро
                    if current_vertex in adj_list_copy[next_vertex]:
                        idx = adj_list_copy[next_vertex].index(current_vertex)
                        del adj_list_copy[next_vertex][idx]

                current_vertex = next_vertex
            else:
                # Нет исходящих ребер
                cycle.append(current_vertex)
                if not stack:
                    break
                current_vertex = stack.pop()

        cycle.reverse()

        # Проверяем что цикл корректен
        if len(cycle) == self.num_edges + 1:
            return cycle
        else:
            print(f"Найден некорректный цикл длиной {len(cycle)} (ожидалось {self.num_edges + 1})")
            return None

    def find_hamiltonian_cycle(self):
        """
        Возвращает гамильтонов цикл как список вершин (длиной num_vertices+1,
        где последняя совпадает с первой), или None, если цикла нет.
        """
        if self.num_vertices < 3:
            print('No Hamiltonian cycle')
            return None

        # Начинаем с вершины 0, можно выбрать любую
        start = 0
        path = [start]
        visited = [False] * self.num_vertices
        visited[start] = True

        # Рекурсивный backtracking
        def backtrack(v):
            if len(path) == self.num_vertices:
                # Проверяем, есть ли ребро из последней вершины в стартовую
                if start in self.adj_lists[path[-1]]:
                    return True
                return False

            for neighbour in self.adj_lists[v]:
                if not visited[neighbour]:
                    visited[neighbour] = True
                    path.append(neighbour)
                    if backtrack(neighbour):
                        return True
                    # Откат
                    visited[neighbour] = False
                    path.pop()
            return False

        if backtrack(start):
            # Формируем цикл с возвратом в начальную вершину
            cycle = path + [start]
            return cycle
        else:
            print('No Hamiltonian cycle')
            return None

    def find_hamiltonian_path(self):
        """
        Поиск гамильтонова пути в обыкновенном графе.
        Возвращает список вершин пути (длиной num_vertices) или None,
        если путь не существует.
        """
        if self.num_vertices == 0:
            return None

        # Пробуем каждую вершину в качестве начальной
        for start in range(self.num_vertices):
            path = [start]
            visited = [False] * self.num_vertices
            visited[start] = True

            def backtrack(v):
                if len(path) == self.num_vertices:
                    return True
                for neighbour in self.adj_lists[v]:
                    if not visited[neighbour]:
                        visited[neighbour] = True
                        path.append(neighbour)
                        if backtrack(neighbour):
                            return True
                        visited[neighbour] = False
                        path.pop()
                return False

            if backtrack(start):
                return path

        return None

    def is_tournament(self):
        """Проверяет, является ли ориентированный граф турниром."""
        if not self.directed:
            return False
        n = self.num_vertices
        for i in range(n):
            for j in range(i + 1, n):
                ij = self.adj_matrix[i][j] == 1
                ji = self.adj_matrix[j][i] == 1
                if ij == ji:  # либо оба 0, либо оба 1 – не турнир
                    return False
        return True

    def find_hamiltonian_cycle_tournament(self):
        """
        Поиск гамильтонова цикла в турнире.
        Возвращает список вершин цикла (длина num_vertices + 1, конец совпадает с началом)
        или None, если цикла нет (граф не сильно связный).
        """
        if not self.is_tournament():
            return None
        n = self.num_vertices
        if n == 0:
            return None

        # 1. Строим гамильтонов путь методом вставки
        path = [0]
        for v in range(1, n):
            # вставка v в путь
            if self.adj_matrix[v][path[0]] == 1:
                path.insert(0, v)
            elif self.adj_matrix[path[-1]][v] == 1:
                path.append(v)
            else:
                for i in range(len(path) - 1):
                    if self.adj_matrix[path[i]][v] == 1 and self.adj_matrix[v][path[i + 1]] == 1:
                        path.insert(i + 1, v)
                        break

        # 2. Пытаемся замкнуть путь в цикл
        if self.adj_matrix[path[-1]][path[0]] == 1:
            return path + [path[0]]

        # Ищем k (2 ≤ k ≤ n-1 в 1-индексации) такое, что
        # есть рёбра path[k-1] → path[0] и path[k-2] → path[-1]
        for k in range(2, n):  # k = 2..n-1 (позиции с 1), индекс в path = k-1
            if self.adj_matrix[path[k - 1]][path[0]] == 1 and self.adj_matrix[path[k - 2]][path[-1]] == 1:
                cycle = [path[0]] + path[k - 1:] + path[1:k - 1] + [path[0]]
                return cycle

        return None  # турнир не сильно связен, гамильтонова цикла нет
'''
