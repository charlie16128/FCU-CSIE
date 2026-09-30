from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .gui import relative_candles


FIGURE_SPECS = (
    (
        "validation",
        "label",
        "parameter_set_score",
        "Validation Parameter Search",
        "validation_parameter_search.png",
    ),
    (
        "pattern_test",
        "pattern_id",
        "average_directional_profit",
        "2026 Pattern Performance",
        "2026_pattern_performance.png",
    ),
    (
        "stock_test",
        "ticker",
        "average_directional_profit",
        "2026 Stock Performance",
        "2026_stock_performance.png",
    ),
)


def _centroid_values(value: object) -> list[float]:
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, (list, tuple)):
        raise ValueError("centroid_raw must be a list or JSON array")
    return list(value)


def _draw_candle(axis, x: int, candle: tuple[float, float, float, float]) -> None:
    open_, high, low, close = candle
    color = "#d62728" if close >= open_ else "#2ca02c"
    axis.vlines(x, low, high, color=color, linewidth=1.3)
    height = close - open_
    axis.bar(
        x,
        height if not math.isclose(height, 0.0) else 0.04,
        bottom=open_,
        width=0.5,
        color=color,
    )


def _save_pattern_grid(frame: pd.DataFrame, title: str, path: Path) -> Path:
    missing = sorted({"pattern_id", "centroid_raw"} - set(frame.columns))
    if missing:
        raise ValueError(f"Pattern figure data is missing columns: {', '.join(missing)}")
    display = frame.head(10).reset_index(drop=True)
    columns = 5
    row_count = max(1, math.ceil(len(display) / columns))
    figure, axes = plt.subplots(
        row_count,
        columns,
        figsize=(15, 3.2 * row_count),
        squeeze=False,
    )
    flat_axes = axes.ravel()
    for position, axis in enumerate(flat_axes):
        if position >= len(display):
            axis.axis("off")
            continue
        record = display.iloc[position]
        for x, candle in enumerate(
            relative_candles(_centroid_values(record["centroid_raw"]))
        ):
            _draw_candle(axis, x, candle)
        axis.set_xticks([0, 1], ["Prev", "Today"])
        axis.set_title(str(record["pattern_id"]), fontsize=9)
        axis.grid(axis="y", alpha=0.2)
    figure.suptitle(f"{title} — representative reconstruction", fontsize=14)
    figure.tight_layout(rect=(0, 0, 1, 0.94))
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def _save_bar(
    frame: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    path: Path,
) -> Path:
    missing = sorted({x, y} - set(frame.columns))
    if missing:
        raise ValueError(f"Figure data is missing columns: {', '.join(missing)}")

    figure, axis = plt.subplots(figsize=(10, 5))
    if not frame.empty:
        axis.bar(frame[x].astype(str), frame[y].astype(float), color="#4472C4")
        axis.tick_params(axis="x", rotation=70)
    axis.set_title(title)
    axis.set_xlabel(x.replace("_", " ").title())
    axis.set_ylabel(y.replace("_", " ").title())
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def generate_required_figures(
    data: dict[str, pd.DataFrame],
    output_dir: Path,
) -> list[Path]:
    required_keys = {"bullish", "bearish", *(spec[0] for spec in FIGURE_SPECS)}
    missing = sorted(required_keys - set(data))
    if missing:
        raise ValueError(f"Figure inputs are missing datasets: {', '.join(missing)}")

    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    generated = [
        _save_pattern_grid(
            data["bullish"],
            "Top 10 Bullish Patterns",
            target / "top10_bullish.png",
        ),
        _save_pattern_grid(
            data["bearish"],
            "Top 10 Bearish Patterns",
            target / "top10_bearish.png",
        ),
    ]
    for key, x, y, title, filename in FIGURE_SPECS:
        generated.append(_save_bar(data[key], x, y, title, target / filename))
    return generated
