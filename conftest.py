import sys
import os
from plot_generator import PlotGenerator

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Генерация графиков
generator = PlotGenerator()
generator.generate_all_plots()
generator.generate_combined_plot()