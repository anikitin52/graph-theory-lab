import json
import os
import matplotlib.pyplot as plt
from pathlib import Path


class PlotGenerator:
    """Универсальный генератор графиков из JSON файлов с результатами тестов"""

    # Папки для работы
    RESULTS_DIR = Path(__file__).parent / "test" / "results" / "performance"
    PLOTS_DIR = Path(__file__).parent / "plots"

    # Настройки стилей для разных алгоритмов
    STYLES = {
        "eulerian": {
            "color": "blue",
            "marker": "o",
            "label": "Эйлеров цикл"
        },
        "hamiltonian_cycle": {
            "color": "green",
            "marker": "s",
            "label": "Гамильтонов цикл"
        },
        "hamiltonian_path": {
            "color": "red",
            "marker": "^",
            "label": "Гамильтонов путь"
        }
    }

    # Настройки для разных типов графов
    TYPE_LABELS = {
        "with_cycle": "с эйлеровым циклом",
        "without_cycle": "без эйлерова цикла",
        "complete_graph": "полный граф"
    }

    def __init__(self):
        """Инициализация генератора графиков"""
        # Создаем папку для графиков, если её нет
        self.PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    def load_json(self, json_path):
        """Загрузка данных из JSON файла"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"❌ Файл не найден: {json_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка парсинга JSON: {e}")
            return None

    def create_plot(self, data, json_filename):
        """Создание графика по данным из JSON"""
        if not data:
            return

        algorithm = data.get("algorithm", "unknown")
        graph_type = data.get("type", "unknown")
        results = data.get("results", [])

        if not results:
            print(f"⚠️ Нет данных для построения графика: {json_filename}")
            return

        # Извлекаем данные
        vertices = [r["vertices"] for r in results]
        times = [r["time_ms"] for r in results]

        # Создаем фигуру
        fig, ax = plt.subplots(figsize=(10, 6))

        # Получаем стиль для алгоритма
        style = self.STYLES.get(algorithm, {})
        color = style.get("color", "black")
        marker = style.get("marker", "o")
        label_prefix = style.get("label", algorithm)

        # Получаем подпись для типа графа
        type_label = self.TYPE_LABELS.get(graph_type, graph_type)

        # Строим график
        ax.plot(vertices, times,
                color=color,
                marker=marker,
                linestyle='-',
                linewidth=2,
                markersize=8,
                label=f"{label_prefix} ({type_label})")

        # Настройка графика
        ax.set_xlabel("Количество вершин", fontsize=12)
        ax.set_ylabel("Время выполнения (мс)", fontsize=12)

        # Формируем заголовок
        title = f"{label_prefix}\n{type_label}"
        ax.set_title(title, fontsize=14, fontweight='bold')

        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10)

        # Добавляем значения на точки
        for i, (v, t) in enumerate(zip(vertices, times)):
            ax.annotate(f'{t:.2f}',
                        (v, t),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center',
                        fontsize=8)

        # Сохраняем график
        plot_filename = json_filename.replace('.json', '.png')
        plot_path = self.PLOTS_DIR / plot_filename

        plt.tight_layout()
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✅ График сохранен: {plot_path}")

    def generate_all_plots(self):
        """Генерация всех графиков из JSON файлов"""
        # Проверяем наличие папки с результатами
        if not self.RESULTS_DIR.exists():
            print(f"❌ Папка с результатами не найдена: {self.RESULTS_DIR}")
            return

        # Ищем все JSON файлы
        json_files = list(self.RESULTS_DIR.glob("*.json"))

        if not json_files:
            print(f"⚠️ JSON файлы не найдены в: {self.RESULTS_DIR}")
            return

        print(f"📊 Найдено {len(json_files)} JSON файлов")

        for json_file in json_files:
            print(f"\n📄 Обработка: {json_file.name}")
            data = self.load_json(json_file)
            if data:
                self.create_plot(data, json_file.name)

        print(f"\n✅ Все графики сохранены в: {self.PLOTS_DIR}")

    def generate_combined_plot(self):
        """Генерация сводного графика со всеми данными"""
        if not self.RESULTS_DIR.exists():
            print(f"❌ Папка с результатами не найдена: {self.RESULTS_DIR}")
            return

        json_files = list(self.RESULTS_DIR.glob("*.json"))

        if not json_files:
            print(f"⚠️ JSON файлы не найдены в: {self.RESULTS_DIR}")
            return

        fig, ax = plt.subplots(figsize=(12, 8))

        colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']
        color_idx = 0

        for json_file in json_files:
            data = self.load_json(json_file)
            if not data:
                continue

            algorithm = data.get("algorithm", "unknown")
            graph_type = data.get("type", "unknown")
            results = data.get("results", [])

            if not results:
                continue

            vertices = [r["vertices"] for r in results]
            times = [r["time_ms"] for r in results]

            style = self.STYLES.get(algorithm, {})
            label_prefix = style.get("label", algorithm)
            type_label = self.TYPE_LABELS.get(graph_type, graph_type)

            ax.plot(vertices, times,
                    color=colors[color_idx % len(colors)],
                    marker='o',
                    linestyle='-',
                    linewidth=2,
                    markersize=6,
                    label=f"{label_prefix} ({type_label})")

            color_idx += 1

        ax.set_xlabel("Количество вершин", fontsize=12)
        ax.set_ylabel("Время выполнения (мс)", fontsize=12)
        ax.set_title("Сравнение производительности алгоритмов", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10)

        # Сохраняем сводный график
        plot_path = self.PLOTS_DIR / "combined_performance.png"
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✅ Сводный график сохранен: {plot_path}")


