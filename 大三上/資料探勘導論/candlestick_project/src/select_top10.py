from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

from .similarity import weighted_distance


REQUIRED_COLUMNS = {
    "pattern_id",
    "direction",
    "centroid_z",
    "occurrence_count",
    "accuracy",
    "average_directional_profit",
}


def _has_ten_each(frame: pd.DataFrame) -> bool:
    counts = frame["direction"].value_counts()
    return all(int(counts.get(direction, 0)) >= 10 for direction in ("bullish", "bearish"))


def _eligible(
    metrics: pd.DataFrame,
    occurrences: Sequence[int],
    accuracies: Sequence[float],
) -> tuple[pd.DataFrame, int, float]:
    primary_accuracy = float(accuracies[0])
    for occurrence in occurrences:
        subset = metrics.loc[
            metrics["occurrence_count"].ge(occurrence)
            & metrics["accuracy"].ge(primary_accuracy)
        ]
        if _has_ten_each(subset):
            return subset.copy(), int(occurrence), primary_accuracy

    for accuracy in accuracies[1:]:
        for occurrence in occurrences:
            subset = metrics.loc[
                metrics["occurrence_count"].ge(occurrence)
                & metrics["accuracy"].ge(accuracy)
            ]
            if _has_ten_each(subset):
                return subset.copy(), int(occurrence), float(accuracy)

    raise ValueError(
        "Fewer than ten eligible patterns remain in one or both directions"
    )


def _validate_sequence(
    values: Sequence[float],
    name: str,
    *,
    lower: float,
    upper: float | None = None,
) -> tuple[float, ...]:
    converted = tuple(float(value) for value in values)
    if not converted:
        raise ValueError(f"{name} must not be empty")
    array = np.asarray(converted)
    if not np.isfinite(array).all() or (array < lower).any():
        raise ValueError(f"{name} contains an invalid value")
    if upper is not None and (array > upper).any():
        raise ValueError(f"{name} contains an invalid value")
    return converted


def select_top_patterns(
    metrics: pd.DataFrame,
    weights: np.ndarray,
    occurrences: Sequence[int] = (30, 25, 20),
    accuracies: Sequence[float] = (0.60, 0.58, 0.55),
    dedup_thresholds: Sequence[float] = (0.30, 0.25, 0.20),
) -> tuple[pd.DataFrame, dict[str, float | int]]:
    missing = sorted(REQUIRED_COLUMNS - set(metrics.columns))
    if missing:
        raise ValueError(f"Pattern metrics are missing columns: {', '.join(missing)}")
    if metrics.empty:
        raise ValueError("Pattern metrics must not be empty")
    if metrics["pattern_id"].duplicated().any():
        raise ValueError("pattern_id values must be unique")
    if not set(metrics["direction"]).issubset({"bullish", "bearish"}):
        raise ValueError("Pattern direction must be bullish or bearish")

    occurrence_values = _validate_sequence(
        occurrences,
        "occurrences",
        lower=1,
    )
    if any(not value.is_integer() for value in occurrence_values):
        raise ValueError("occurrences must contain integers")
    accuracy_values = _validate_sequence(
        accuracies,
        "accuracies",
        lower=0,
        upper=1,
    )
    dedup_values = _validate_sequence(
        dedup_thresholds,
        "dedup_thresholds",
        lower=np.nextafter(0.0, 1.0),
    )

    eligible, occurrence, accuracy = _eligible(
        metrics,
        tuple(int(value) for value in occurrence_values),
        accuracy_values,
    )

    for dedup_threshold in dedup_values:
        selected: list[dict[str, object]] = []
        complete = True
        for direction in ("bullish", "bearish"):
            chosen: list[dict[str, object]] = []
            ranked = eligible.loc[eligible["direction"].eq(direction)].sort_values(
                "average_directional_profit",
                ascending=False,
                kind="stable",
            )
            for _, row in ranked.iterrows():
                candidate = row.to_dict()
                if all(
                    weighted_distance(
                        candidate["centroid_z"],
                        previous["centroid_z"],
                        weights,
                    )
                    >= dedup_threshold
                    for previous in chosen
                ):
                    chosen.append(candidate)
                if len(chosen) == 10:
                    break
            if len(chosen) < 10:
                complete = False
                break
            selected.extend(chosen)

        if complete:
            result = pd.DataFrame(selected).reset_index(drop=True)
            return result, {
                "minimum_occurrence": occurrence,
                "minimum_accuracy": accuracy,
                "dedup_threshold": dedup_threshold,
            }

    raise ValueError(
        "Pattern deduplication left fewer than ten patterns in one or both directions"
    )
