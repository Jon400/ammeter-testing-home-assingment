"""Table of saved test runs, one row per run."""

import tkinter as tk
from tkinter import ttk
from typing import Callable

from src.models import MeasurementResult

# Column name -> title shown in the header
COLUMNS = {
    "started_at": "Started at",
    "meter": "Meter",
    "count": "Samples",
    "mean": "Mean (A)",
    "std": "Std dev (A)",
    "failed": "Failed",
}


class HistoryTable(ttk.Frame):
    """
    A table of test runs, newest first. Clicking a row selects that run.
    """

    def __init__(self, parent: tk.Misc, on_select: Callable[[str], None]):
        """
        Initialize the HistoryTable.

        Args:
            parent (tk.Misc): The window or frame to put the table in.
            on_select (Callable[[str], None]): Called with the run id of the selected row.
        """
        super().__init__(parent, padding=(8, 0))
        self.on_select = on_select

        ttk.Label(self, text="Results history (newest first)").pack(anchor="w")

        self.table = ttk.Treeview(self, columns=list(COLUMNS), show="headings", height=8)
        for column, title in COLUMNS.items():
            self.table.heading(column, text=title)
            self.table.column(column, width=140, anchor="center")
        self.table.pack(fill="x")
        self.table.bind("<<TreeviewSelect>>", self.on_row_selected)

    def show_results(self, results: list[MeasurementResult]):
        """
        Show the results in the table, newest first, and select the newest one.

        Args:
            results (list[MeasurementResult]): The results to show, oldest first, as ResultsManager returns them.
        """
        self.table.delete(*self.table.get_children())

        for result in reversed(results):
            stats = result.measurement_data.stats
            self.table.insert(
                "",
                "end",
                iid=str(result.run_id),  # the row id is the run id, so a click knows which run it is
                values=(
                    result.started_at.astimezone().strftime("%Y-%m-%d %H:%M:%S"),  # local time
                    result.ammeter_type.value,
                    stats.count,
                    f"{stats.mean_current:.4f}",
                    f"{stats.std_dev_current:.4f}",
                    result.failed_samples,
                ),
            )

        rows = self.table.get_children()
        if rows:
            self.table.selection_set(rows[0])  # this also calls on_row_selected

    def on_row_selected(self, event):
        """
        Pass the run id of the selected row to on_select.
        """
        selected = self.table.selection()
        if selected:
            self.on_select(selected[0])
