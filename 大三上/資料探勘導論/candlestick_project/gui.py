"""Read-only Tkinter viewer for saved candlestick results."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from kline_analysis import relative_candles


def _read_patterns(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if "centroid_raw" in frame.columns:
        frame["centroid_raw"] = frame["centroid_raw"].map(
            lambda value: json.loads(value) if isinstance(value, str) else value
        )
    return frame


def load_gui_records(project_root: Path) -> pd.DataFrame:
    """Merge validation Top-10 rows with optional 2026 metrics."""
    result_dir = Path(project_root) / "data" / "results"
    bullish_path = result_dir / "top10_bullish.csv"
    bearish_path = result_dir / "top10_bearish.csv"
    if not bullish_path.exists() or not bearish_path.exists():
        raise FileNotFoundError("Run --analyze before --gui")
    patterns = pd.concat(
        [_read_patterns(bullish_path), _read_patterns(bearish_path)],
        ignore_index=True,
    )
    patterns = patterns.rename(columns={"accuracy": "validation_accuracy"})

    test_path = result_dir / "test_2026_pattern_metrics.csv"
    if test_path.exists():
        test = pd.read_csv(test_path)
    else:
        test = pd.DataFrame(
            columns=[
                "pattern_id",
                "number_of_matches",
                "test_accuracy",
                "test_average_directional_profit",
            ]
        )
    keep = [
        column
        for column in (
            "pattern_id",
            "number_of_matches",
            "test_accuracy",
            "test_average_directional_profit",
        )
        if column in test.columns
    ]
    if "pattern_id" not in keep:
        test["pattern_id"] = pd.Series(dtype=str)
        keep.insert(0, "pattern_id")
    return patterns.merge(test[keep], on="pattern_id", how="left", validate="one_to_one")


def launch_gui(project_root: Path) -> None:
    """Open saved results without retraining or downloading data."""
    import tkinter as tk
    from tkinter import ttk

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    records = load_gui_records(project_root)
    root = tk.Tk()
    root.title("Candlestick Pattern Top 10")
    root.geometry("1180x700")

    notebook = ttk.Notebook(root)
    notebook.pack(side="left", fill="both", expand=True)
    detail = ttk.Frame(root)
    detail.pack(side="right", fill="both", expand=True)
    figure = Figure(figsize=(5.2, 4.2), dpi=100)
    axis = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, master=detail)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    description = tk.Text(detail, width=52, height=14)
    description.pack(fill="x")

    def show_record(record: pd.Series) -> None:
        axis.clear()
        for x, (open_price, high, low, close) in enumerate(
            relative_candles(record["centroid_raw"])
        ):
            color = "#d62728" if close >= open_price else "#2ca02c"
            axis.vlines(x, low, high, color=color, linewidth=1.5)
            height = close - open_price
            axis.bar(
                x,
                height if not np.isclose(height, 0.0) else 0.04,
                bottom=open_price,
                width=0.5,
                color=color,
            )
        axis.set_xticks([0, 1], ["Previous", "Current"])
        axis.set_title(f"{record['pattern_id']} representative shape")
        canvas.draw_idle()
        description.delete("1.0", tk.END)
        description.insert(
            "1.0",
            "Relative reconstruction; not actual stock prices.\n\n"
            + record.to_string(),
        )

    columns = (
        "pattern_id",
        "occurrence_count",
        "validation_accuracy",
        "average_directional_profit",
        "number_of_matches",
        "test_accuracy",
    )
    for direction, title in (
        ("bullish", "Bullish Top 10"),
        ("bearish", "Bearish Top 10"),
    ):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=125, anchor="center")
        subset = records.loc[records["direction"].eq(direction)].reset_index(drop=True)
        for index, row in subset.iterrows():
            tree.insert(
                "",
                "end",
                iid=str(index),
                values=[row.get(column, "") for column in columns],
            )

        def on_select(event, values=subset) -> None:
            selected = event.widget.selection()
            if selected:
                show_record(values.iloc[int(selected[0])])

        tree.bind("<<TreeviewSelect>>", on_select)
        tree.pack(fill="both", expand=True)

    root.mainloop()
