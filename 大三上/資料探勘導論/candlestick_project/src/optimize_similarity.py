from __future__ import annotations

from itertools import product

import numpy as np
import pandas as pd

from .similarity import expand_group_weights, pairwise_weighted_distances


VALIDATION_START = pd.Timestamp("2024-01-01")
VALIDATION_END = pd.Timestamp("2025-12-31")
WEIGHT_COLUMNS = (
    "today_weight",
    "previous_weight",
    "position_weight",
    "volume_weight",
    "trend_weight",
)


def _minmax(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="raise").astype(float)
    minimum = numeric.min()
    maximum = numeric.max()
    if np.isclose(minimum, maximum):
        return pd.Series(1.0, index=values.index, dtype=float)
    return (numeric - minimum) / (maximum - minimum)


def add_pattern_scores(metrics: pd.DataFrame) -> pd.DataFrame:
    required = {
        "average_directional_profit",
        "accuracy",
        "occurrence_count",
    }
    missing = sorted(required - set(metrics.columns))
    if missing:
        raise ValueError(f"Pattern metrics are missing columns: {', '.join(missing)}")
    if metrics.empty:
        raise ValueError("At least one eligible pattern is required")

    scored = metrics.copy()
    scored["normalized_average_directional_profit"] = _minmax(
        scored["average_directional_profit"]
    )
    scored["normalized_accuracy"] = _minmax(scored["accuracy"])
    scored["normalized_log_occurrence"] = _minmax(
        np.log1p(scored["occurrence_count"])
    )
    scored["pattern_score"] = (
        0.50 * scored["normalized_average_directional_profit"]
        + 0.30 * scored["normalized_accuracy"]
        + 0.20 * scored["normalized_log_occurrence"]
    )
    return scored


def choose_best_parameter_set(results: pd.DataFrame) -> dict[str, object]:
    if results.empty:
        raise ValueError("No valid parameter set is available")
    required = {
        "parameter_set_score",
        "mean_directional_profit",
        "mean_accuracy",
        "total_occurrence",
        "similarity_threshold",
    }
    missing = sorted(required - set(results.columns))
    if missing:
        raise ValueError(f"Parameter results are missing columns: {', '.join(missing)}")

    ordered = results.sort_values(
        [
            "parameter_set_score",
            "mean_directional_profit",
            "mean_accuracy",
            "total_occurrence",
            "similarity_threshold",
        ],
        ascending=[False, False, False, False, True],
        kind="stable",
    )
    return ordered.iloc[0].to_dict()


def _validate_inputs(
    patterns: pd.DataFrame,
    validation_rows: pd.DataFrame,
    weight_values: tuple[float, ...],
    thresholds: tuple[float, ...],
    chunk_size: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if patterns.empty:
        raise ValueError("At least one pattern is required")
    if validation_rows.empty:
        raise ValueError("At least one validation row is required")
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")

    pattern_required = {"pattern_id", "direction", "centroid_z"}
    row_required = {"date", "features_z", "return_3d"}
    missing_patterns = sorted(pattern_required - set(patterns.columns))
    missing_rows = sorted(row_required - set(validation_rows.columns))
    if missing_patterns:
        raise ValueError(
            f"Patterns are missing columns: {', '.join(missing_patterns)}"
        )
    if missing_rows:
        raise ValueError(
            f"Validation rows are missing columns: {', '.join(missing_rows)}"
        )
    if patterns["pattern_id"].duplicated().any():
        raise ValueError("pattern_id values must be unique")
    if not set(patterns["direction"]).issubset({"bullish", "bearish"}):
        raise ValueError("Pattern direction must be bullish or bearish")

    dates = pd.to_datetime(validation_rows["date"], errors="raise")
    if dates.min() < VALIDATION_START or dates.max() > VALIDATION_END:
        raise ValueError("Validation rows must be limited to 2024-2025")

    weight_array = np.asarray(weight_values, dtype=float)
    if weight_array.ndim != 1 or len(weight_array) == 0:
        raise ValueError("weight_values must not be empty")
    if not np.isfinite(weight_array).all() or (weight_array < 0).any():
        raise ValueError("weight_values must be finite and non-negative")

    threshold_array = np.asarray(thresholds, dtype=float)
    if threshold_array.ndim != 1 or len(threshold_array) == 0:
        raise ValueError("thresholds must not be empty")
    if (
        not np.isfinite(threshold_array).all()
        or (threshold_array <= 0).any()
        or np.any(np.diff(threshold_array) <= 0)
    ):
        raise ValueError("thresholds must be finite, positive, and strictly increasing")

    centroids = np.vstack(patterns["centroid_z"].map(np.asarray)).astype(float)
    vectors = np.vstack(validation_rows["features_z"].map(np.asarray)).astype(float)
    if centroids.shape[1] != vectors.shape[1]:
        raise ValueError("Patterns and validation rows must have equal feature widths")
    return weight_array, threshold_array, vectors


def _threshold_statistics(
    patterns: pd.DataFrame,
    centroids: np.ndarray,
    vectors: np.ndarray,
    returns: np.ndarray,
    feature_weights: np.ndarray,
    thresholds: np.ndarray,
    chunk_size: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pattern_count = len(patterns)
    threshold_count = len(thresholds)
    shape = (pattern_count, threshold_count)
    occurrence_bins = np.zeros(shape, dtype=np.int64)
    success_bins = np.zeros(shape, dtype=np.int64)
    profit_bins = np.zeros(shape, dtype=float)
    bullish_patterns = patterns["direction"].eq("bullish").to_numpy()

    for start in range(0, len(vectors), chunk_size):
        stop = min(start + chunk_size, len(vectors))
        distances = pairwise_weighted_distances(
            centroids,
            vectors[start:stop],
            feature_weights,
        )
        pattern_positions, local_positions = np.nonzero(
            distances <= thresholds[-1]
        )
        if len(pattern_positions) == 0:
            continue

        matched_distances = distances[pattern_positions, local_positions]
        threshold_bins = np.searchsorted(
            thresholds,
            matched_distances,
            side="left",
        )
        flat_positions = pattern_positions * threshold_count + threshold_bins
        matched_returns = returns[start + local_positions]
        bullish = bullish_patterns[pattern_positions]
        successes = np.where(
            bullish,
            matched_returns > 0.05,
            matched_returns < -0.05,
        )
        directional_profit = np.where(
            bullish,
            matched_returns,
            -matched_returns,
        )

        flat_size = pattern_count * threshold_count
        occurrence_bins += np.bincount(
            flat_positions,
            minlength=flat_size,
        ).reshape(shape)
        success_bins += np.bincount(
            flat_positions,
            weights=successes.astype(np.int64),
            minlength=flat_size,
        ).astype(np.int64).reshape(shape)
        profit_bins += np.bincount(
            flat_positions,
            weights=directional_profit,
            minlength=flat_size,
        ).reshape(shape)

    return (
        np.cumsum(occurrence_bins, axis=1),
        np.cumsum(success_bins, axis=1),
        np.cumsum(profit_bins, axis=1),
    )


def _score_parameter_set(
    patterns: pd.DataFrame,
    occurrence: np.ndarray,
    successes: np.ndarray,
    profit_sum: np.ndarray,
    minimum_occurrence: int,
    minimum_accuracy: float,
) -> dict[str, float | int] | None:
    accuracy = np.divide(
        successes,
        occurrence,
        out=np.zeros_like(profit_sum, dtype=float),
        where=occurrence > 0,
    )
    average_profit = np.divide(
        profit_sum,
        occurrence,
        out=np.full_like(profit_sum, np.nan, dtype=float),
        where=occurrence > 0,
    )
    metrics = patterns[["pattern_id", "direction"]].copy()
    metrics["occurrence_count"] = occurrence
    metrics["success_count"] = successes
    metrics["accuracy"] = accuracy
    metrics["average_directional_profit"] = average_profit
    eligible = metrics.loc[
        metrics["occurrence_count"].ge(minimum_occurrence)
        & metrics["accuracy"].ge(minimum_accuracy)
    ]

    top_by_direction: list[pd.DataFrame] = []
    eligible_counts: dict[str, int] = {}
    for direction in ("bullish", "bearish"):
        direction_metrics = eligible.loc[eligible["direction"].eq(direction)]
        eligible_counts[direction] = len(direction_metrics)
        if direction_metrics.empty:
            return None
        scored = add_pattern_scores(direction_metrics)
        top_by_direction.append(scored.nlargest(10, "pattern_score"))

    bullish_top, bearish_top = top_by_direction
    selected = pd.concat(top_by_direction, ignore_index=True)
    return {
        "parameter_set_score": float(
            0.5 * bullish_top["pattern_score"].mean()
            + 0.5 * bearish_top["pattern_score"].mean()
        ),
        "mean_directional_profit": float(
            selected["average_directional_profit"].mean()
        ),
        "mean_accuracy": float(selected["accuracy"].mean()),
        "total_occurrence": int(selected["occurrence_count"].sum()),
        "eligible_bullish_patterns": eligible_counts["bullish"],
        "eligible_bearish_patterns": eligible_counts["bearish"],
    }


def optimize_similarity(
    patterns: pd.DataFrame,
    validation_rows: pd.DataFrame,
    *,
    weight_values: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0),
    thresholds: tuple[float, ...] = (0.5, 0.6, 0.7, 0.8),
    minimum_occurrence: int = 30,
    minimum_accuracy: float = 0.60,
    chunk_size: int = 25_000,
) -> tuple[dict[str, object], pd.DataFrame]:
    if minimum_occurrence < 1:
        raise ValueError("minimum_occurrence must be positive")
    if not 0 <= minimum_accuracy <= 1:
        raise ValueError("minimum_accuracy must be between 0 and 1")

    weight_array, threshold_array, vectors = _validate_inputs(
        patterns,
        validation_rows,
        weight_values,
        thresholds,
        chunk_size,
    )
    centroids = np.vstack(patterns["centroid_z"].map(np.asarray)).astype(float)
    returns = pd.to_numeric(
        validation_rows["return_3d"],
        errors="raise",
    ).to_numpy(dtype=float)
    if not np.isfinite(centroids).all() or not np.isfinite(vectors).all():
        raise ValueError("Pattern and validation features must be finite")
    if not np.isfinite(returns).all():
        raise ValueError("Validation returns must be finite")

    search_rows: list[dict[str, object]] = []
    for group_weights in product(weight_array.tolist(), repeat=5):
        feature_weights = expand_group_weights(group_weights)
        occurrence, successes, profit_sum = _threshold_statistics(
            patterns,
            centroids,
            vectors,
            returns,
            feature_weights,
            threshold_array,
            chunk_size,
        )
        for threshold_index, threshold in enumerate(threshold_array):
            score = _score_parameter_set(
                patterns,
                occurrence[:, threshold_index],
                successes[:, threshold_index],
                profit_sum[:, threshold_index],
                minimum_occurrence,
                minimum_accuracy,
            )
            if score is None:
                continue
            row: dict[str, object] = dict(zip(WEIGHT_COLUMNS, group_weights))
            row["similarity_threshold"] = float(threshold)
            row.update(score)
            search_rows.append(row)

    search = pd.DataFrame(search_rows)
    if search.empty:
        raise ValueError(
            "No parameter set produced eligible bullish and bearish patterns"
        )
    best = choose_best_parameter_set(search)
    return best, search
