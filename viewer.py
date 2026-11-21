"""Opens the results viewer window.

Run from the project folder:  python viewer.py
"""

import tkinter as tk

from measurements_visualizer.results_viewer import ResultsViewer
from src.config import load_config
from src.mesurements.results_manager import ResultsManager


def main():
    config = load_config("config/config.yaml")
    root = tk.Tk()
    ResultsViewer(root, ResultsManager(config.results_dir))
    root.mainloop()


if __name__ == "__main__":
    main()
