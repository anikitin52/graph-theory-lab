def input_adj_matrix(num_vertices):
    print("Введите матрицу смежности")
    adj_matrix = []

    for i in range(num_vertices):
        row = list(map(int, input().split()))
        adj_matrix.append(row)

    is_directed = is_directed_by_matrix(adj_matrix)
    edges = count_edges_from_matrix(adj_matrix, is_directed)

    return adj_matrix, is_directed, edges


def input_adj_lists(num_vertices):
    print("Введите списки смежности")

    adj_list = {}
    for i in range(num_vertices):
        # Показываем пользователю вершины с 1, но храним с 0
        neighbours = list(map(int, input(f'Вершина {i + 1}: ').split()))
        # Преобразуем в 0-based индексы
        neighbours = [x - 1 for x in neighbours]
        adj_list[i] = neighbours

    is_directed = is_directed_by_lists(adj_list)
    edges = count_edges_from_lists(adj_list, is_directed)

    return adj_list, is_directed, edges


def is_directed_by_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                return True
    return False


def is_directed_by_lists(lists):
    # Создание множества всех ребер
    all_edges = set()
    for vertex, neighbors in lists.items():
        for neighbor in neighbors:
            all_edges.add((vertex, neighbor))

    # Проверка наличия обратных ребер
    for u, v in all_edges:
        if (v, u) not in all_edges:
            return True
    return False


def count_edges_from_matrix(matrix, is_directed):
    n = len(matrix)
    edges = 0

    if is_directed:
        # Для ориентированного графа: считаем ВСЕ ненулевые элементы
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    edges += 1
        return edges
    else:
        # Для неориентированного графа: считаем только верхний треугольник
        for i in range(n):
            for j in range(i, n):
                if matrix[i][j] != 0:
                    edges += 1
        return edges

def count_edges_from_lists(lists, is_directed):
    if is_directed:
        return sum(len(neighbors) for neighbors in lists.values())
    else:
        edges = set()

        for vertex, neighbors in lists.items():
            for neighbor in neighbors:
                edge = (min(vertex, neighbor), max(vertex, neighbor))
                edges.add(edge)
        return len(edges)
