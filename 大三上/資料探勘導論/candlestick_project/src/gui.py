from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


def load_gui_records(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    required = {"bullish", "bearish", "pattern_test"}
    missing = sorted(required - set(data))
    if missing:
        raise ValueError(f"GUI inputs are missing datasets: {', '.join(missing)}")

    patterns = pd.concat(
        [data["bullish"].copy(), data["bearish"].copy()],
        ignore_index=True,
    )
    pattern_required = {
        "pattern_id",
        "direction",
        "accuracy",
        "centroid_raw",
    }
    missing_patterns = sorted(pattern_required - set(patterns.columns))
    if missing_patterns:
        raise ValueError(
            f"GUI pattern data is missing columns: {', '.join(missing_patterns)}"
        )
    patterns = patterns.rename(columns={"accuracy": "validation_accuracy"})

    test = data["pattern_test"].copy()
    if test.empty:
        test = pd.DataFrame(
            columns=[
                "pattern_id",
                "number_of_matches",
                "test_accuracy",
                "test_average_directional_profit",
            ]
        )
    else:
        test_required = {"pattern_id", "number_of_matches", "accuracy"}
        missing_test = sorted(test_required - set(test.columns))
        if missing_test:
            raise ValueError(
                f"GUI test data is missing columns: {', '.join(missing_test)}"
            )
        test = test.rename(
            columns={
                "accuracy": "test_accuracy",
                "average_directional_profit": "test_average_directional_profit",
            }
        )

    test_columns = ["pattern_id", "number_of_matches", "test_accuracy"]
    if "test_average_directional_profit" in test.columns:
        test_columns.append("test_average_directional_profit")
    return patterns.merge(
        test[test_columns],
        on="pattern_id",
        how="left",
        validate="one_to_one",
    )


def relative_candles(features: list[float]) -> list[tuple[float, float, float, float]]:
    values = np.asarray(features, dtype=float)
    if values.shape != (10,) or not np.isfinite(values).all():
        raise ValueError("centroid_raw must contain ten finite feature values")
    (
        upper,
        lower,
        _body,
        prev_upper,
        prev_lower,
        prev_body,
        open_style,
        close_style,
        _volume,
        _trend,
    ) = values

    previous_close = 100.0
    previous_open = previous_close * (1.0 - prev_body / 100.0)
    previous_high = max(previous_open, previous_close) + prev_upper
    previous_low = min(previous_open, previous_close) - prev_lower

    denominator = 1.0 - close_style / 100.0
    current_close = (
        previous_close / denominator
        if denominator > np.finfo(float).eps
        else previous_close
    )
    current_open = previous_close + open_style * current_close / 100.0
    current_high = max(current_open, current_close) + upper * current_close / 100.0
    current_low = min(current_open, current_close) - lower * current_close / 100.0
    return [
        (previous_open, previous_high, previous_low, previous_close),
        (current_open, current_high, current_low, current_close),
    ]


def _decode_centroid(value: object) -> list[float]:
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, (list, tuple, np.ndarray)):
        raise ValueError("centroid_raw must be an array or a JSON array")
    return list(value)


def launch_gui(project_root: Path) -> None:
    import tkinter as tk
    from tkinter import ttk

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    result_dir = Path(project_root) / "data" / "results"
    paths = {
        "bullish": result_dir / "top10_bullish.csv",
        "bearish": result_dir / "top10_bearish.csv",
        "pattern_test": result_dir / "test_2026_pattern_metrics.csv",
    }
    if not paths["bullish"].exists() or not paths["bearish"].exists():
        raise FileNotFoundError("Run --validate before --gui")

    data = {
        "bullish": pd.read_csv(paths["bullish"]),
        "bearish": pd.read_csv(paths["bearish"]),
        "pattern_test": (
            pd.read_csv(paths["pattern_test"])
            if paths["pattern_test"].exists()
            else pd.DataFrame(
                columns=["pattern_id", "number_of_matches", "accuracy"]
            )
        ),
    }
    records = load_gui_records(data)

    root = tk.Tk()
    root.title("Candlestick Pattern Explorer")
    root.geometry("1250x720")

    notebook = ttk.Notebook(root)
    notebook.pack(side="left", fill="both", expand=True)
    detail = ttk.Frame(root)
    detail.pack(side="right", fill="both", expand=True)
    figure = Figure(figsize=(5.5, 4.5), dpi=100)
    axis = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, master=detail)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    feature_text = tk.Text(detail, width=58, height=16)
    feature_text.pack(fill="x")

    def show_record(record: pd.Series) -> None:
        raw = _decode_centroid(record["centroid_raw"])
        axis.clear()
        for x, (open_, high, low, close) in enumerate(relative_candles(raw)):
            color = "#d62728" if close >= open_ else "#2ca02c"
            axis.vlines(x, low, high, color=color, linewidth=1.5)
            height = close - open_
            axis.bar(
                x,
                height if not np.isclose(height, 0.0) else 0.05,
                bottom=open_,
                width=0.5,
                color=color,
            )
        axis.set_xticks([0, 1], ["Previous", "Current"])
        axis.set_title(f"{record['pattern_id']} representative reconstruction")
        canvas.draw_idle()
        feature_text.delete("1.0", tk.END)
        feature_text.insert(
            "1.0",
            "Representative centroid reconstruction; not actual prices.\n\n"
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
            tree.column(column, width=135, anchor="center")
        subset = records.loc[records["direction"].eq(direction)].reset_index(
            drop=True
        )
        for index, row in subset.iterrows():
            tree.insert(
                "",
                "end",
                iid=str(index),
                values=[row.get(column, "") for column in columns],
            )

        def on_select(event, values=subset) -> None:
            selection = event.widget.selection()
            if selection:
                show_record(values.iloc[int(selection[0])])

        tree.bind("<<TreeviewSelect>>", on_select)
        tree.pack(fill="both", expand=True)

    root.mainloop()
