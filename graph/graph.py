from .graph_input import input_adj_matrix
from .graph_input import input_adj_lists


class Graph:
    def __init__(self, num_vertices):
        if type(num_vertices) is not int:
            raise TypeError(
                'Количество вершин должно быть целым числом.'
            )
        if num_vertices < 0:
            raise ValueError(
                'Количество вершин не может быть отрицательным.'
            )
        self._num_vertices = num_vertices
        self._num_edges = 0
        self._directed = False
        self._is_tournament = False
        self._adj_matrix = [[0] * self._num_vertices for _ in range(self._num_vertices)]
        self._adj_lists = {i: [] for i in range(self._num_vertices)}

    # ВВОД ДАННЫХ
    def set_adj_matrix(self):
        """
        Задание графа матрицей смежности
        :return: None
        """
        self._adj_matrix = input_adj_matrix(self._num_vertices)
        self._directed = self._is_directed_by_matrix()
        self._num_edges = self._count_edges_from_matrix()
        self._is_tournament = self.is_tournament()
        self._adj_matrix_to_adj_lists()

    def set_adj_list(self):
        """
        Задание графа списками смежности
        :return: None
        """
        self._adj_lists = input_adj_lists(self._num_vertices)
        self._directed = self._is_directed_by_lists()
        self._num_edges = self._count_edges_from_lists()
        self._is_tournament = self.is_tournament()
        self._adj_lists_to_adj_matrix()

    # КЛАССИФИКАЦИЯ ГРАФА
    def _is_directed_by_matrix(self):
        """
        Определяет, является ли граф ориентированным
        по его матрице смежности
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
        Определяет, является ли граф ориентированным
        по его спискам смежности
        :return: статус ориентированности графа
        """
        lists = self._adj_lists
        all_edges = set()

        for vertex, neighbors in lists.items():
            for neighbor in neighbors:
                all_edges.add((vertex, neighbor))

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
            # Граф ориентированный. Считаем все ненулевые элементы.
            for i in range(n):
                for j in range(n):
                    if matrix[i][j] != 0:
                        edges += 1
            return edges
        else:
            # Граф неориентированный.
            for i in range(n):
                for j in range(i, n):
                    if matrix[i][j] != 0:
                        edges += 1
                    elif i != j and matrix[j][i] != 0:
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
            edges = 0
            for vertex, neighbors in self._adj_lists.items():
                for neighbor in neighbors:
                    if vertex <= neighbor:
                        edges += 1
            return edges

    def is_tournament(self):
        """
        Проверка, является ли граф турниром
        :return: True, если граф - турнир, иначе False
        """
        if not self._directed:
            return False
        n = self._num_vertices
        for i in range(n):
            for j in range(i + 1, n):
                ij = self._adj_matrix[i][j] == 1
                ji = self._adj_matrix[j][i] == 1
                if ij == ji:  # либо оба 0, либо оба 1 – не турнир
                    return False
        return True

    # ПРЕОБРАЗОВАНИЯ
    def _adj_matrix_to_adj_lists(self):
        """
        Преобразование из матрицы смежности в списки смежности
        :return: None
        """
        self._adj_lists = {
            i: [] for i in range(self._num_vertices)
        }

        for i in range(self._num_vertices):
            for j in range(self._num_vertices):
                if self._adj_matrix[i][j] != 0:
                    self._adj_lists[i].append(j)

    def _adj_lists_to_adj_matrix(self):
        """
        Преобразование из списков смежности в матрицу смежности
        :return: None
        """
        self._adj_matrix = [
            [0] * self._num_vertices
            for _ in range(self._num_vertices)
        ]

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
            {'ориентированный' if self._directed else 'неориентированный'}
            '''

        result += "\nМатрица смежности \n"
        for row in self._adj_matrix:
            result += ' '.join(map(str, row)) + '\n'

        result += "Списки смежности: \n"
        for vertex in sorted(self._adj_lists.keys()):
            neighbors_1based = [
                x + 1 for x in self._adj_lists[vertex]
            ]
            result += f'{vertex + 1}: {neighbors_1based}\n'

        return result

    # ЭЙЛЕРОВ ЦИКЛ
    def _is_eulerian(self):
        """
        Проверка наличия эйлерова цикла в графе
        :return: True, если эйлеров цикл существует, иначе False
        """

        if self._num_vertices == 0:
            return False

        # Проверка степеней
        if self._directed:
            out_degree = [
                len(self._adj_lists[i])
                for i in range(self._num_vertices)
            ]
            in_degree = [0] * self._num_vertices
            for i in range(self._num_vertices):
                for neighbor in self._adj_lists[i]:
                    in_degree[neighbor] += 1
            if not all(
                    out_degree[i] == in_degree[i]
                    for i in range(self._num_vertices)
            ):
                return False
        else:
            # Проверка чётности степеней
            for i in range(self._num_vertices):
                degree = 0
                for neighbor in self._adj_lists[i]:
                    if neighbor == i:
                        degree += 2
                    else:
                        degree += 1

                if degree % 2 != 0:
                    return False

        # Поиск первой вершины, имеющей хотя бы одно ребро
        start = None
        for i in range(self._num_vertices):
            if len(self._adj_lists[i]) > 0:
                start = i
                break

        if start is None:
            return True

        # Проверка связности (слабой связности для ориентированного графа)
        visited = set()
        stack = [start]

        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)

            for neighbor in self._adj_lists[vertex]:
                if neighbor not in visited:
                    stack.append(neighbor)

            if self._directed:
                for vertex2 in range(self._num_vertices):
                    if vertex in self._adj_lists[vertex2] and vertex2 not in visited:
                        stack.append(vertex2)

        for i in range(self._num_vertices):
            has_edges = len(self._adj_lists[i]) > 0
            if not has_edges:
                if self._directed:
                    has_edges = any(i in self._adj_lists[j] for j in range(self._num_vertices))
            if has_edges and i not in visited:
                return False

        return True

    def find_eulerian_cycle(self):
        """
        Поиск эйлерова цикла алгоритмом на двух стеках.
        :return: список вершин эйлерова цикла в 1-based или None
        """

        if not self._is_eulerian():
            print('No Eulerian cycle')
            return None

        adj_list_copy = {}
        for v in range(self._num_vertices):
            adj_list_copy[v] = self._adj_lists[v][:]

        stack = []
        cycle_stack = []
        start_vertex = 0

        for i in range(self._num_vertices):
            if adj_list_copy[i]:
                start_vertex = i
                break
        stack.append(start_vertex)

        while stack:
            current_vertex = stack[-1]

            if adj_list_copy[current_vertex]:
                next_vertex = adj_list_copy[current_vertex].pop()

                if (
                        not self._directed
                        and current_vertex != next_vertex
                ):
                    if current_vertex in adj_list_copy[next_vertex]:
                        index = adj_list_copy[next_vertex].index(
                            current_vertex
                        )
                        del adj_list_copy[next_vertex][index]

                stack.append(next_vertex)
            else:
                cycle_stack.append(stack.pop())

        cycle = []
        while cycle_stack:
            cycle.append(cycle_stack.pop())

        if len(cycle) == self._num_edges + 1:
            return [x + 1 for x in cycle]

        print(
            f'Найден некорректный цикл длиной {len(cycle)} '
            f'(ожидалось {self._num_edges + 1})'
        )

        return None

    # ГАМИЛЬТОНОВ ЦИКЛ И ПУТЬ
    def find_hamiltonian_cycle(self):
        """
        Поиск гамильтонова цикла в графе
        :return: список вершин гамильтонова цикла в 1-based или None, если цикла нет
        """
        if self._num_vertices < 3:
            print('No Hamiltonian cycle')
            return None

        if self._is_tournament:
            return self.find_hamiltonian_cycle_tournament()

        start = 0
        path = [start]
        visited = [False] * self._num_vertices
        visited[start] = True

        def backtrack(v):
            if len(path) == self._num_vertices:
                if start in self._adj_lists[path[-1]]:
                    return True
                return False

            for neighbour in self._adj_lists[v]:
                if not visited[neighbour]:
                    visited[neighbour] = True
                    path.append(neighbour)
                    if backtrack(neighbour):
                        return True
                    visited[neighbour] = False
                    path.pop()
            return False

        if backtrack(start):
            cycle = path + [start]
            return [x + 1 for x in cycle]
        else:
            print('No Hamiltonian cycle')
            return None

    def find_hamiltonian_path(self):
        """
        Поиск гамильтонова пути в графе
        :return: список вершин гамильтонова пути в 1-based или None, если пути нет
        """
        if self._num_vertices == 0:
            return None

        for start in range(self._num_vertices):
            path = [start]
            visited = [False] * self._num_vertices
            visited[start] = True

            def backtrack(v):
                if len(path) == self._num_vertices:
                    return True
                for neighbour in self._adj_lists[v]:
                    if not visited[neighbour]:
                        visited[neighbour] = True
                        path.append(neighbour)
                        if backtrack(neighbour):
                            return True
                        visited[neighbour] = False
                        path.pop()
                return False

            if backtrack(start):
                return [x + 1 for x in path]

        return None

    def find_hamiltonian_cycle_tournament(self):
        """
        Поиск гамильтонова цикла в турнире
        :return: список вершин гамильтонова цикла в 1-based, если он есть, иначе None
        """
        if not self.is_tournament():
            return None
        n = self._num_vertices
        if n == 0:
            return None

        path = [0]
        for v in range(1, n):
            if self._adj_matrix[v][path[0]] == 1:
                path.insert(0, v)
            elif self._adj_matrix[path[-1]][v] == 1:
                path.append(v)
            else:
                for i in range(len(path) - 1):
                    if self._adj_matrix[path[i]][v] == 1 and self._adj_matrix[v][path[i + 1]] == 1:
                        path.insert(i + 1, v)
                        break

        if self._adj_matrix[path[-1]][path[0]] == 1:
            cycle = path + [path[0]]
            return [x + 1 for x in cycle]

        for i in range(1, n):
            if self._adj_matrix[path[i]][path[0]] == 1 and self._adj_matrix[path[i - 1]][path[-1]] == 1:
                cycle = [path[0]] + path[i:] + path[1:i] + [path[0]]
                return [x + 1 for x in cycle]

        return None