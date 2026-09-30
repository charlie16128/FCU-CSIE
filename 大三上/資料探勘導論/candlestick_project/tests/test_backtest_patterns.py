import numpy as np
import pandas as pd

from src.backtest_patterns import backtest_patterns


def test_backtest_computes_directional_metrics(patterns, validation_rows):
    metrics, signals = backtest_patterns(
        patterns,
        validation_rows,
        np.ones(10),
        threshold=0.1,
        chunk_size=1,
    )

    bullish = metrics.set_index("pattern_id").loc["bullish_0001"]
    bearish = metrics.set_index("pattern_id").loc["bearish_0001"]
    assert bullish["occurrence_count"] == 2
    assert bullish["success_count"] == 1
    assert bullish["accuracy"] == 0.5
    assert bearish["occurrence_count"] == 1
    assert bearish["success_count"] == 1
    assert bearish["accuracy"] == 1.0
    bearish_signal = signals.query("direction == 'bearish'").iloc[0]
    assert bearish_signal["directional_profit"] == 0.07


def test_strict_five_percent_boundary_is_not_success(patterns, validation_rows):
    _, signals = backtest_patterns(
        patterns.iloc[[0]],
        validation_rows,
        np.ones(10),
        threshold=0.1,
    )

    boundary = signals.loc[signals["return_3d"].eq(0.05)].iloc[0]
    assert not bool(boundary["success"])


def test_patterns_with_no_matches_remain_in_metrics(patterns, validation_rows):
    far_pattern = patterns.iloc[[0]].copy()
    far_pattern["pattern_id"] = "bullish_far"
    far_pattern["centroid_z"] = [np.full(10, 100.0).tolist()]
    combined = pd.concat([patterns, far_pattern], ignore_index=True)

    metrics, _ = backtest_patterns(
        combined,
        validation_rows,
        np.ones(10),
        threshold=0.1,
    )

    far = metrics.set_index("pattern_id").loc["bullish_far"]
    assert far["occurrence_count"] == 0
    assert far["success_count"] == 0
    assert far["accuracy"] == 0.0
