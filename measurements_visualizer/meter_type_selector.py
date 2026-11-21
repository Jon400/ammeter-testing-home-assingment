"""Dropdown for choosing which ammeter's results to show."""

import tkinter as tk
from tkinter import ttk
from typing import Callable

from src.enums import AmmeterType

ALL_METERS = "all"


class MeterTypeSelector(ttk.Frame):
    """
    A dropdown for choosing an ammeter type, with a button to reload the results.
    """

    def __init__(self, parent: tk.Misc, on_change: Callable[[], None]):
        """
        Initialize the MeterTypeSelector.

        Args:
            parent (tk.Misc): The window or frame to put the selector in.
            on_change (Callable[[], None]): Called when a meter is chosen or Refresh is clicked.
        """
        super().__init__(parent, padding=8)

        ttk.Label(self, text="Meter:").pack(side="left")

        self.meter_box = ttk.Combobox(
            self,
            values=[ALL_METERS] + [meter.value for meter in AmmeterType],
            state="readonly",
            width=12,
        )
        self.meter_box.set(ALL_METERS)
        self.meter_box.pack(side="left", padx=6)
        self.meter_box.bind("<<ComboboxSelected>>", lambda event: on_change())

        ttk.Button(self, text="Refresh", command=on_change).pack(side="left")

    def get_ammeter_type(self) -> AmmeterType | None:
        """
        Get the chosen ammeter type.

        Returns:
            AmmeterType | None: The chosen type, or None when "all" is chosen.
        """
        meter = self.meter_box.get()
        return None if meter == ALL_METERS else AmmeterType(meter)
