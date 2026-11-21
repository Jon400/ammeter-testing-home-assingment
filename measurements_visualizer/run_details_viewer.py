"""Shows one test run: its settings and stats, every sample, and a chart."""

import tkinter as tk
from tkinter import ttk

from measurements_visualizer.run_chart import RunChart
from src.models import MeasurementResult


class RunDetailsViewer(ttk.Frame):
    """
    The details of one run: stats and samples on the left, a chart on the right.
    """

    def __init__(self, parent: tk.Misc):
        """
        Initialize the RunDetailsViewer.

        Args:
            parent (tk.Misc): The window or frame to put the details in.
        """
        super().__init__(parent, padding=8)

        left = ttk.Frame(self)
        left.pack(side="left", fill="y")

        self.stats_label = ttk.Label(left, text="Select a run to see it", font=("Consolas", 10), justify="left")
        self.stats_label.pack(anchor="w")

        self.samples_table = ttk.Treeview(left, columns=("number", "time", "current"), show="headings", height=10)
        for column, title, width in (("number", "#", 40), ("time", "Time (s)", 90), ("current", "Current (A)", 130)):
            self.samples_table.heading(column, text=title)
            self.samples_table.column(column, width=width, anchor="center")
        self.samples_table.pack(anchor="w", pady=(8, 0))

        self.chart = RunChart(self)
        self.chart.pack(side="left", anchor="n", padx=(16, 0))

    def show_run(self, result: MeasurementResult):
        """
        Show one run.

        Args:
            result (MeasurementResult): The run to show.
        """
        stats = result.measurement_data.stats
        settings = result.sample_config

        self.stats_label.config(text=(
            f"Run id:    {result.run_id}\n"
            f"Meter:     {result.ammeter_type.value}\n"
            f"Started:   {result.started_at.astimezone():%Y-%m-%d %H:%M:%S}\n"
            f"Settings:  {settings.number_of_samples} samples at {settings.sample_rate} Hz, "
            f"at most {settings.total_duration} s\n"
            f"\n"
            f"Count:     {stats.count}   (failed: {result.failed_samples})\n"
            f"Mean:      {stats.mean_current:.4f} {stats.unit}\n"
            f"Median:    {stats.median_current:.4f} {stats.unit}\n"
            f"Std dev:   {stats.std_dev_current:.4f} {stats.unit}\n"
            f"Min:       {stats.min_current:.4f} {stats.unit}\n"
            f"Max:       {stats.max_current:.4f} {stats.unit}"
        ))

        self.samples_table.delete(*self.samples_table.get_children())
        for number, sample in enumerate(result.measurement_data.samples, start=1):
            self.samples_table.insert("", "end", values=(number, f"{sample.timestamp:.3f}", f"{sample.current:.4f}"))

        self.chart.draw(result.measurement_data.samples, stats.mean_current)

    def clear(self, message: str):
        """
        Empty the details, for when there is no run to show.

        Args:
            message (str): The text to show instead of the stats.
        """
        self.stats_label.config(text=message)
        self.samples_table.delete(*self.samples_table.get_children())
        self.chart.delete("all")
