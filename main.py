from graph.graph import Graph

print("=== НАУЧНАЯ РАБОТА ПО ТЕОРИИ ГРАФОВ === \n")

vertices = None
graph = None

while True:
    if vertices is None:
        while True:
            try:
                print("Граф не задан, введите количество вершин")
                vertices = int(input())
                if vertices < 0:
                    print("Ошибка: количество вершин не может быть отрицательным!")
                    continue
                graph = Graph(vertices)
                print(f"Граф с {vertices} вершинами создан!")
                break
            except ValueError:
                print("Ошибка: введите целое число!")
            except Exception as e:
                print(f"Ошибка: {e}")

        continue

    print(''' Главное меню:
    1. Ввести матрицу смежности графа
    2. Ввести списки смежности
    3. Показать информацию о графе 
    4. Найти эйлеров цикл 
    5. Найти гамильтонов цикл
    6. Найти гамильтонов путь
    7. Выход
    ''')

    choice = input("Выберите действие: ").strip()

    if choice == '1':
        try:
            graph.set_adj_matrix()
            print("Матрица смежности успешно введена!")
        except ValueError as e:
            print(f"Ошибка ввода матрицы смежности: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

    elif choice == '2':
        try:
            graph.set_adj_list()
            print("Списки смежности успешно введены!")
        except ValueError as e:
            print(f"Ошибка ввода списков смежности: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

    elif choice == '3':
        try:
            print(graph)
        except Exception as e:
            print(f"Ошибка при выводе информации о графе: {e}")

    elif choice == '4':
        try:
            result = graph.find_eulerian_cycle()
            if result:
                print(f"Эйлеров цикл: {result}")
            else:
                print("Эйлеров цикл не найден")
        except Exception as e:
            print(f"Ошибка при поиске эйлерова цикла: {e}")

    elif choice == '5':
        try:
            result = graph.find_hamiltonian_cycle()
            if result:
                print(f"Гамильтонов цикл: {result}")
            else:
                print("Гамильтонов цикл не найден")
        except Exception as e:
            print(f"Ошибка при поиске гамильтонова цикла: {e}")

    elif choice == '6':
        try:
            result = graph.find_hamiltonian_path()
            if result:
                print(f"Гамильтонов путь: {result}")
            else:
                print("Гамильтонов путь не найден")
        except Exception as e:
            print(f"Ошибка при поиске гамильтонова пути: {e}")

    elif choice == '7':
        print("Выход из программы ...")
        break

    else:
        print("Ошибка ввода! Выберите действие от 1 до 7.")

print("Программа завершена.")