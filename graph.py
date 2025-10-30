from graph_io import *


class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices

        self.num_edges = 0
        self.directed = False
        self.adj_matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]
        self.adj_lists = {i: [] for i in range(self.num_vertices)}

    def set_adj_matrix(self):
        res = input_adj_matrix(self.num_vertices)
        self.adj_matrix = res[0]
        self.directed = res[1]
        self.num_edges = res[2]
        self._adj_matrix_to_adj_lists()

    def set_adj_list(self):
        res = input_adj_lists(self.num_vertices)
        self.adj_lists = res[0]
        self.directed = res[1]
        self.num_edges = res[2]
        self._adj_lists_to_adj_matrix()

    def _adj_matrix_to_adj_lists(self):
        self.adj_lists = {i: [] for i in range(self.num_vertices)}
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.adj_matrix[i][j] != 0:
                    self.adj_lists[i].append(j)

    def _adj_lists_to_adj_matrix(self):
        self.adj_matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]
        for vertex, neighbors in self.adj_lists.items():
            for neighbor in neighbors:
                self.adj_matrix[vertex][neighbor] = 1
                if not self.directed:
                    self.adj_matrix[neighbor][vertex] = 1

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

    def __str__(self):
        result = f''' Граф
Вершин: {self.num_vertices} 
Ребер: {self.num_edges}
{'ориентированный' if self.directed else 'неориeнтированный'} 
        '''
        result += "\nМатрица смежности \n"
        for row in self.adj_matrix:
            result += ' '.join(map(str, row)) + '\n'

        result += "Списки смежности: \n"
        for vertex in sorted(self.adj_lists.keys()):
            # Преобразуем обратно к 1-based для отображения
            neighbors_1based = [x + 1 for x in self.adj_lists[vertex]]
            result += f'{vertex + 1}: {neighbors_1based}\n'

        return result
