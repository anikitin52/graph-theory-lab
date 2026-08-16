def input_adj_matrix(num_vertices):
    """
    Задание графа с помощью матрицы смежности
    :param num_vertices: количество вершин в графе
    :return: Матрица смежности (список списков)
    """

    print("Введите матрицу смежности")
    adj_matrix = []  # Инициализация матрицы

    # Заполнение матрицы
    for i in range(num_vertices):
        try:
            row = list(map(int, input().split()))
        except ValueError:
            raise ValueError(
                f'Ошибка ввода в строке {i + 1}: все значения должны быть целыми числами. '
            )
        if len(row) != num_vertices:
            raise ValueError(
                f'Ошибка ввода матрицы смежности: '
                f'ожидалось {num_vertices} элементов, получено {len(row)}'
            )
        adj_matrix.append(row)

    return adj_matrix


def input_adj_lists(num_vertices):
    """
    Задание графа с помощью списков смежности
    :param num_vertices: количество вершин в графе
    :return: списки смежности
    """

    print("Введите списки смежности")
    adj_list = {}  # Инициализация словаря {номер вершины: список вершин}

    for i in range(num_vertices):
        try:
            neighbours = list(
                map(int, input(f'Вершина {i + 1}: ').split()))  # Показываем пользователю вершины с 1, но храним с 0
        except ValueError:
            raise ValueError(
                f'Ошибка ввода в строке {i + 1}: все значения должны быть целыми числами. '
            )
        for x in neighbours:
            if not 1 <= x <= num_vertices:
                raise ValueError(
                    f'Ошибка ввода в строке {i+1}: вершины {x} не существует'
                )

        neighbours = [x - 1 for x in neighbours]  # Преобразуем в 0-based индексы
        adj_list[i] = neighbours

    return adj_list