import sys
import os
from plot_generator import PlotGenerator

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def pytest_sessionfinish(session, exitstatus):
    generator = PlotGenerator()
    generator.generate_all_plots()
    generator.generate_combined_plot()
    generator.generate_longest_cycle_plot()