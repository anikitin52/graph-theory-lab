from graph import Graph

print("=== ЛАБОРАТОРНАЯ РАБОТА 1: ТЕОРИЯ ГРАФОВ === \n")

vertices = None
graph = None

while True:
    if vertices is None:
        print("Граф не задан, введите количество вершин")
        vertices = int(input())
        graph = Graph(vertices)
        continue

    print(''' Главное меню:
    1. Ввести матрицу смежности графа
    2. Ввести списки смежности
    3. Показать информацию о графе 
    4. Найти эйлеров цикл 
    5. Выход
    ''')

    choice = input("Выберите действие: ").strip()

    if choice == '1':
        graph.set_adj_matrix()
    elif choice == '2':
        graph.set_adj_list()
    elif choice == '3':
        print(graph)
    elif choice == '4':
        print(graph.find_eulerian_cycle())
    elif choice == '5':
        print("Выход из программы ...")
        break
    else:
        print("Ошибка ввода!")
