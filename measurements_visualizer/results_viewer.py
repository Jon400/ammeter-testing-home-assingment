"""Window for browsing saved results: choose a meter, see its test history, and look into one run."""

import tkinter as tk

from measurements_visualizer.history_table import HistoryTable
from measurements_visualizer.meter_type_selector import MeterTypeSelector
from measurements_visualizer.run_details_viewer import RunDetailsViewer
from src.mesurements.results_manager import ResultsManager


class ResultsViewer:
    """
    A class to visualize measurement results.
    """

    def __init__(self, parent: tk.Tk, results_manager: ResultsManager):
        """
        Initialize the ResultsViewer.

        Args:
            parent (tk.Tk): The parent window.
            results_manager (ResultsManager): The results manager to load results from.
        """
        self.results_manager = results_manager
        self.widget = parent
        self.widget.title("Ammeter results")

        self.create_meter_type_selector()
        self.create_history_table()
        self.create_run_details_viewer()

        self.load_results()

    #################################
    # Components
    #################################

    def create_meter_type_selector(self):
        """
        Create a dropdown selector for ammeter types.
        """
        self.meter_type_selector = MeterTypeSelector(self.widget, on_change=self.load_results)
        self.meter_type_selector.pack(fill="x")

    def create_history_table(self):
        """
        Create the table of test runs.
        """
        self.history_table = HistoryTable(self.widget, on_select=self.show_run)
        self.history_table.pack(fill="x")

    def create_run_details_viewer(self):
        """
        Create the area that shows one run.
        """
        self.run_details_viewer = RunDetailsViewer(self.widget)
        self.run_details_viewer.pack(fill="both", expand=True)

    #################################
    # Actions
    #################################

    def load_results(self):
        """
        Load the chosen meter's results into the history table.
        """
        ammeter_type = self.meter_type_selector.get_ammeter_type()
        results = self.results_manager.load_all_results(ammeter_type)

        self.history_table.show_results(results)  # selects the newest run, which calls show_run
        if not results:
            self.run_details_viewer.clear("No results for this meter")

    def show_run(self, run_id: str):
        """
        Show one run in the details area.

        Args:
            run_id (str): The run id of the run to show.
        """
        self.run_details_viewer.show_run(self.results_manager.load_result(run_id))
