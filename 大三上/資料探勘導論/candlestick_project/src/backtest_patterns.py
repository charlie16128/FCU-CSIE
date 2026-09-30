from __future__ import annotations

import numpy as np
import pandas as pd

from .similarity import pairwise_weighted_distances


METRIC_COLUMNS = (
    "occurrence_count",
    "success_count",
    "accuracy",
    "average_return_3d",
    "median_return_3d",
    "std_return_3d",
    "average_directional_profit",
    "median_directional_profit",
)


def _empty_metrics(patterns: pd.DataFrame) -> pd.DataFrame:
    metrics = patterns[["pattern_id", "direction"]].copy()
    metrics["occurrence_count"] = 0
    metrics["success_count"] = 0
    metrics["accuracy"] = 0.0
    for column in METRIC_COLUMNS[3:]:
        metrics[column] = np.nan
    return metrics


def backtest_patterns(
    patterns: pd.DataFrame,
    rows: pd.DataFrame,
    weights: np.ndarray,
    threshold: float,
    *,
    chunk_size: int = 25_000,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")
    if patterns.empty:
        raise ValueError("At least one pattern is required")
    if patterns["pattern_id"].duplicated().any():
        raise ValueError("pattern_id values must be unique")
    if rows.empty:
        return _empty_metrics(patterns), pd.DataFrame()

    centroids = np.vstack(patterns["centroid_z"].map(np.asarray))
    vectors = np.vstack(rows["features_z"].map(np.asarray))
    signal_frames: list[pd.DataFrame] = []

    for start in range(0, len(rows), chunk_size):
        stop = min(start + chunk_size, len(rows))
        distances = pairwise_weighted_distances(
            centroids,
            vectors[start:stop],
            weights,
        )
        pattern_positions, local_row_positions = np.nonzero(
            distances <= threshold
        )
        if len(pattern_positions) == 0:
            continue
        absolute_row_positions = start + local_row_positions
        signals = rows.iloc[absolute_row_positions].reset_index(drop=True).copy()
        pattern_rows = patterns.iloc[pattern_positions].reset_index(drop=True)
        signals["pattern_id"] = pattern_rows["pattern_id"]
        signals["direction"] = pattern_rows["direction"]
        signals["distance"] = distances[
            pattern_positions,
            local_row_positions,
        ]
        signal_frames.append(signals)

    if not signal_frames:
        return _empty_metrics(patterns), pd.DataFrame()

    signals = pd.concat(signal_frames, ignore_index=True)
    bullish = signals["direction"].eq("bullish")
    signals["success"] = np.where(
        bullish,
        signals["return_3d"].gt(0.05),
        signals["return_3d"].lt(-0.05),
    )
    signals["directional_profit"] = np.where(
        bullish,
        signals["return_3d"],
        -signals["return_3d"],
    )

    aggregated = (
        signals.groupby(["pattern_id", "direction"], observed=True)
        .agg(
            occurrence_count=("success", "size"),
            success_count=("success", "sum"),
            accuracy=("success", "mean"),
            average_return_3d=("return_3d", "mean"),
            median_return_3d=("return_3d", "median"),
            std_return_3d=("return_3d", "std"),
            average_directional_profit=("directional_profit", "mean"),
            median_directional_profit=("directional_profit", "median"),
        )
        .reset_index()
    )
    metrics = patterns[["pattern_id", "direction"]].merge(
        aggregated,
        on=["pattern_id", "direction"],
        how="left",
        validate="one_to_one",
    )
    metrics["occurrence_count"] = (
        metrics["occurrence_count"].fillna(0).astype(int)
    )
    metrics["success_count"] = metrics["success_count"].fillna(0).astype(int)
    metrics["accuracy"] = metrics["accuracy"].fillna(0.0)
    return metrics, signals
