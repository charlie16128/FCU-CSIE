import numpy as np
import pandas as pd
import pytest

from src.optimize_similarity import (
    add_pattern_scores,
    choose_best_parameter_set,
    optimize_similarity,
)


def test_pattern_score_uses_required_coefficients(metric_frame):
    scored = add_pattern_scores(metric_frame)
    expected = (
        0.50 * scored["normalized_average_directional_profit"]
        + 0.30 * scored["normalized_accuracy"]
        + 0.20 * scored["normalized_log_occurrence"]
    )

    assert np.allclose(scored["pattern_score"], expected)


def test_tie_break_prefers_profit_accuracy_occurrence_then_lower_threshold(
    parameter_results,
):
    best = choose_best_parameter_set(parameter_results)

    assert best["similarity_threshold"] == 0.5


def test_small_grid_search_evaluates_each_parameter_set_and_prefers_stricter_tie(
    optimizer_data,
):
    patterns, validation = optimizer_data

    best, search = optimize_similarity(
        patterns,
        validation,
        weight_values=(1.0,),
        thresholds=(0.1, 0.2),
        minimum_occurrence=30,
        minimum_accuracy=0.60,
        chunk_size=11,
    )

    assert len(search) == 2
    assert best["similarity_threshold"] == 0.1
    assert best["parameter_set_score"] == 1.0
    assert search["eligible_bullish_patterns"].eq(10).all()
    assert search["eligible_bearish_patterns"].eq(10).all()
    assert {"today_shape_weight", "previous_shape_weight"} <= set(search.columns)
    assert "today_weight" not in search.columns
    assert "previous_weight" not in search.columns


def test_optimizer_rejects_2026_rows(optimizer_data):
    patterns, validation = optimizer_data
    validation.loc[0, "date"] = pd.Timestamp("2026-01-02")

    with pytest.raises(ValueError, match="2024-2025"):
        optimize_similarity(
            patterns,
            validation,
            weight_values=(1.0,),
            thresholds=(0.1,),
        )
