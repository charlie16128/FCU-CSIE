import numpy as np
import pandas as pd
import pytest

from src.select_top10 import select_top_patterns


def _pattern_row(
    pattern_id: str,
    direction: str,
    centroid: float,
    *,
    occurrence: int = 30,
    accuracy: float = 0.70,
    profit: float = 0.05,
) -> dict[str, object]:
    return {
        "pattern_id": pattern_id,
        "direction": direction,
        "centroid_z": np.full(10, centroid).tolist(),
        "occurrence_count": occurrence,
        "accuracy": accuracy,
        "average_directional_profit": profit,
    }


def test_selection_relaxes_occurrence_before_accuracy():
    rows = []
    for direction in ("bullish", "bearish"):
        for index in range(10):
            rows.append(
                _pattern_row(
                    f"{direction}_{index}",
                    direction,
                    float(index),
                    occurrence=20,
                    accuracy=0.61,
                    profit=0.05 + index / 1000,
                )
            )

    selected, policy = select_top_patterns(
        pd.DataFrame(rows),
        np.ones(10),
        occurrences=(30, 25, 20),
        accuracies=(0.60, 0.58, 0.55),
    )

    assert len(selected) == 20
    assert policy["minimum_occurrence"] == 20
    assert policy["minimum_accuracy"] == 0.60


def test_selection_lowers_accuracy_only_after_occurrence_attempts_fail():
    rows = []
    for direction in ("bullish", "bearish"):
        for index in range(10):
            rows.append(
                _pattern_row(
                    f"{direction}_{index}",
                    direction,
                    float(index),
                    occurrence=30,
                    accuracy=0.58,
                )
            )

    _, policy = select_top_patterns(pd.DataFrame(rows), np.ones(10))

    assert policy["minimum_occurrence"] == 30
    assert policy["minimum_accuracy"] == 0.58


def test_near_duplicate_centroids_are_not_selected_twice():
    rows = [
        _pattern_row("bullish_best", "bullish", 0.0, profit=0.10),
        _pattern_row("bullish_duplicate", "bullish", 0.01, profit=0.09),
    ]
    rows.extend(
        _pattern_row(
            f"bullish_{index}",
            "bullish",
            float(index),
            profit=0.08 - index / 1000,
        )
        for index in range(1, 10)
    )
    rows.extend(
        _pattern_row(
            f"bearish_{index}",
            "bearish",
            float(index),
            profit=0.08 - index / 1000,
        )
        for index in range(10)
    )

    selected, policy = select_top_patterns(pd.DataFrame(rows), np.ones(10))

    assert len(selected) == 20
    assert selected["pattern_id"].nunique() == len(selected)
    assert "bullish_best" in set(selected["pattern_id"])
    assert "bullish_duplicate" not in set(selected["pattern_id"])
    assert policy["dedup_threshold"] == 0.30


def test_selection_fails_when_either_direction_has_fewer_than_ten_patterns():
    rows = [
        _pattern_row(f"bullish_{index}", "bullish", float(index))
        for index in range(10)
    ]
    rows.extend(
        _pattern_row(f"bearish_{index}", "bearish", float(index))
        for index in range(9)
    )

    with pytest.raises(ValueError, match="Fewer than ten eligible patterns"):
        select_top_patterns(pd.DataFrame(rows), np.ones(10))
