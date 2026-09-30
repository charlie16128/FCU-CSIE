import json

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.build_features import FEATURE_COLUMNS


def _patterns() -> pd.DataFrame:
    rows = []
    for direction, offset in (("bullish", 0.0), ("bearish", 20.0)):
        for index in range(10):
            centroid = np.zeros(10)
            centroid[0] = offset + index
            rows.append(
                {
                    "pattern_id": f"{direction}_{index:02d}",
                    "direction": direction,
                    "cluster_size": 1,
                    "centroid_z": centroid.tolist(),
                    "centroid_raw": centroid.tolist(),
                    "source_candidates": [],
                }
            )
    return pd.DataFrame(rows)


def _identity_scaler() -> StandardScaler:
    values = pd.DataFrame(
        np.vstack([-np.ones(10), np.ones(10)]),
        columns=FEATURE_COLUMNS,
    )
    return StandardScaler().fit(values)


def _processed_rows() -> pd.DataFrame:
    rows = []
    for date, return_3d in (
        (pd.Timestamp("2023-01-03"), 0.06),
        (pd.Timestamp("2023-01-04"), -0.06),
    ):
        row = {
            "Date": date,
            "pattern_eligible": True,
            "return_3d": return_3d,
        }
        row.update(dict.fromkeys(FEATURE_COLUMNS, 0.0))
        rows.append(row)

    dates = pd.bdate_range("2024-01-02", periods=30)
    for direction, offset, return_3d in (
        ("bullish", 0.0, 0.06),
        ("bearish", 20.0, -0.06),
    ):
        for index in range(10):
            centroid = np.zeros(10)
            centroid[0] = offset + index
            for date in dates:
                row = {
                    "Date": date,
                    "pattern_eligible": True,
                    "return_3d": return_3d,
                }
                row.update(dict(zip(FEATURE_COLUMNS, centroid)))
                rows.append(row)

    for date, first_feature, return_3d in (
        (pd.Timestamp("2026-01-05"), 0.0, 0.06),
        (pd.Timestamp("2026-01-06"), 20.0, -0.06),
    ):
        centroid = np.zeros(10)
        centroid[0] = first_feature
        row = {
            "Date": date,
            "pattern_eligible": True,
            "return_3d": return_3d,
        }
        row.update(dict(zip(FEATURE_COLUMNS, centroid)))
        rows.append(row)
    return pd.DataFrame(rows)


def _write_config(root) -> None:
    (root / "config").mkdir(parents=True)
    (root / "config" / "settings.yaml").write_text(
        """
dates:
  discovery_start: "2018-01-01"
  discovery_end: "2023-12-31"
  validation_start: "2024-01-01"
  validation_end: "2025-12-31"
  test_start: "2026-01-01"
  test_end: "2026-12-31"
clustering:
  distance_threshold: 1.0
validation:
  weight_values: [1.0]
  similarity_thresholds: [0.1]
selection:
  minimum_occurrences: [30, 25, 20]
  minimum_accuracies: [0.60, 0.58, 0.55]
  dedup_thresholds: [0.30, 0.25, 0.20]
runtime:
  distance_chunk_size: 17
""".strip(),
        encoding="utf-8",
    )
    (root / "config" / "test_tickers.txt").write_text(
        "2330.TW\n",
        encoding="utf-8",
    )


def test_synthetic_train_validate_and_test_write_all_artifacts(tmp_path, monkeypatch):
    from src import pipeline

    _write_config(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)
    _processed_rows().to_csv(processed_dir / "2330.TW.csv", index=False)
    patterns = _patterns()
    scaler = _identity_scaler()

    monkeypatch.setattr(pipeline, "fit_discovery_scaler", lambda data: scaler)
    monkeypatch.setattr(
        pipeline,
        "cluster_candidates",
        lambda candidates, fitted_scaler, threshold: patterns.copy(),
    )

    def fake_optimize(pattern_frame, rows, **kwargs):
        best = {
            "today_weight": 1.0,
            "previous_weight": 1.0,
            "position_weight": 1.0,
            "volume_weight": 1.0,
            "trend_weight": 1.0,
            "similarity_threshold": 0.1,
            "parameter_set_score": 1.0,
            "mean_directional_profit": 0.06,
            "mean_accuracy": 1.0,
            "total_occurrence": 600,
            "eligible_bullish_patterns": 10,
            "eligible_bearish_patterns": 10,
        }
        return best, pd.DataFrame([best])

    monkeypatch.setattr(pipeline, "optimize_similarity", fake_optimize)

    train_summary = pipeline.train_patterns(tmp_path)
    best = pipeline.validate_patterns(tmp_path)
    overall = pipeline.test_patterns(tmp_path)

    assert train_summary["patterns"] == 20
    assert best["similarity_threshold"] == 0.1
    assert overall["total_signals"] == 2

    expected = {
        "data/results/bullish_candidates.csv",
        "data/results/bearish_candidates.csv",
        "data/results/all_bullish_patterns.csv",
        "data/results/all_bearish_patterns.csv",
        "data/results/validation_results.csv",
        "data/results/top10_bullish.csv",
        "data/results/top10_bearish.csv",
        "data/results/test_2026_signals.csv",
        "data/results/test_2026_pattern_metrics.csv",
        "data/results/test_2026_stock_metrics.csv",
        "data/results/test_2026_overall_metrics.json",
        "models/scaler.pkl",
        "models/best_params.json",
        "models/final_patterns.json",
        "outputs/figures/top10_bullish.png",
        "outputs/figures/top10_bearish.png",
        "outputs/figures/validation_parameter_search.png",
        "outputs/figures/2026_pattern_performance.png",
        "outputs/figures/2026_stock_performance.png",
    }
    assert all((tmp_path / relative).exists() for relative in expected)
    locked = json.loads(
        (tmp_path / "models" / "final_patterns.json").read_text(encoding="utf-8")
    )
    assert len(locked["patterns"]) == 20
    assert locked["feature_weights"] == [1.0] * 10
    assert joblib.load(tmp_path / "models" / "scaler.pkl").n_features_in_ == 10
