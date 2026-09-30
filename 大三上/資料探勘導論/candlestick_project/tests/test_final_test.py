from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

from src.test_2026 import evaluate_final_test


@pytest.fixture
def locked_model() -> dict[str, object]:
    return {
        "patterns": [
            {
                "pattern_id": "bullish_01",
                "direction": "bullish",
                "centroid_z": np.zeros(10).tolist(),
            },
            {
                "pattern_id": "bearish_01",
                "direction": "bearish",
                "centroid_z": np.ones(10).tolist(),
            },
        ],
        "feature_weights": np.ones(10).tolist(),
        "similarity_threshold": 0.10,
    }


@pytest.fixture
def final_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "ticker": "2330.TW",
                "date": pd.Timestamp("2026-01-05"),
                "features_z": np.zeros(10).tolist(),
                "return_3d": 0.06,
            },
            {
                "ticker": "2454.TW",
                "date": pd.Timestamp("2026-01-06"),
                "features_z": np.ones(10).tolist(),
                "return_3d": -0.07,
            },
        ]
    )


def test_final_test_rejects_pre_2026_rows(locked_model, final_rows):
    final_rows.loc[0, "date"] = pd.Timestamp("2025-12-31")

    with pytest.raises(ValueError, match="2026"):
        evaluate_final_test(locked_model, final_rows)


def test_conflicting_trade_signal_is_excluded_but_pattern_hits_remain(locked_model):
    locked_model["patterns"][1]["centroid_z"] = np.zeros(10).tolist()
    conflict_rows = pd.DataFrame(
        [
            {
                "ticker": "2330.TW",
                "date": pd.Timestamp("2026-02-02"),
                "features_z": np.zeros(10).tolist(),
                "return_3d": 0.06,
            }
        ]
    )

    result = evaluate_final_test(locked_model, conflict_rows)

    assert result.signals["conflict_signal"].all()
    assert result.overall_metrics["total_signals"] == 0
    assert len(result.pattern_metrics) == 2
    assert result.pattern_metrics["number_of_matches"].eq(1).all()


def test_final_metrics_cover_overall_direction_and_stock(locked_model, final_rows):
    result = evaluate_final_test(locked_model, final_rows)

    assert result.overall_metrics["total_signals"] == 2
    assert result.overall_metrics["successful_signals"] == 2
    assert result.overall_metrics["overall_accuracy"] == 1.0
    assert result.overall_metrics["bullish_signal_count"] == 1
    assert result.overall_metrics["bearish_signal_count"] == 1
    assert set(result.stock_metrics["ticker"]) == {"2330.TW", "2454.TW"}


def test_final_test_does_not_modify_locked_model(locked_model, final_rows):
    before = deepcopy(locked_model)

    evaluate_final_test(locked_model, final_rows)

    assert locked_model == before
