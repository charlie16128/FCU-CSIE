from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


FIGURE_SPECS = (
    (
        "bullish",
        "pattern_id",
        "average_directional_profit",
        "Top 10 Bullish Patterns",
        "top10_bullish.png",
    ),
    (
        "bearish",
        "pattern_id",
        "average_directional_profit",
        "Top 10 Bearish Patterns",
        "top10_bearish.png",
    ),
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
    missing = sorted({spec[0] for spec in FIGURE_SPECS} - set(data))
    if missing:
        raise ValueError(f"Figure inputs are missing datasets: {', '.join(missing)}")

    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    generated = []
    for key, x, y, title, filename in FIGURE_SPECS:
        generated.append(_save_bar(data[key], x, y, title, target / filename))
    return generated
