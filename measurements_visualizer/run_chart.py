"""Chart of one run's current over time."""

import tkinter as tk

from src.models import MeasurementSample

CHART_WIDTH = 460
CHART_HEIGHT = 300
CHART_MARGIN = 60


class RunChart(tk.Canvas):
    """
    A line chart of current over time, with a dashed line at the mean.
    """

    def __init__(self, parent: tk.Misc):
        """
        Initialize the RunChart.

        Args:
            parent (tk.Misc): The window or frame to put the chart in.
        """
        super().__init__(parent, width=CHART_WIDTH, height=CHART_HEIGHT, background="white")

    def draw(self, samples: list[MeasurementSample], mean: float):
        """
        Draw the samples, replacing the previous chart.

        Args:
            samples (list[MeasurementSample]): The samples to draw.
            mean (float): The mean current, drawn as a dashed line.
        """
        self.delete("all")

        left, top = CHART_MARGIN, CHART_MARGIN
        right, bottom = CHART_WIDTH - CHART_MARGIN, CHART_HEIGHT - CHART_MARGIN

        last_time = max(sample.timestamp for sample in samples) or 1.0  # "or 1.0" avoids dividing by 0
        low = min(sample.current for sample in samples)
        high = max(sample.current for sample in samples)
        current_range = (high - low) or 1.0

        def to_x(time_s: float) -> float:
            return left + time_s / last_time * (right - left)

        def to_y(current: float) -> float:
            return bottom - (current - low) / current_range * (bottom - top)

        # Axes and their labels
        self.create_line(left, top, left, bottom)
        self.create_line(left, bottom, right, bottom)
        self.create_text(CHART_WIDTH / 2, 20, text="Current over time")
        self.create_text(left - 5, top, text=f"{high:.3f}", anchor="e")
        self.create_text(left - 5, bottom, text=f"{low:.3f}", anchor="e")
        self.create_text(left, bottom + 12, text="0 s")
        self.create_text(right, bottom + 12, text=f"{last_time:.1f} s")

        # Mean line
        self.create_line(left, to_y(mean), right, to_y(mean), fill="red", dash=(4, 2))
        self.create_text(right, to_y(mean) - 8, text=f"mean {mean:.3f}", fill="red", anchor="e")

        # Samples: a line through them and a dot on each one
        points = [(to_x(sample.timestamp), to_y(sample.current)) for sample in samples]
        if len(points) > 1:
            self.create_line(points, fill="blue", width=2)
        for x, y in points:
            self.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue", outline="")
