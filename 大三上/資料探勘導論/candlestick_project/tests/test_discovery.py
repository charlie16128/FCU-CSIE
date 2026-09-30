import numpy as np
import pandas as pd

from src.build_features import FEATURE_COLUMNS
from src.cluster_patterns import cluster_candidates, fit_discovery_scaler
from src.find_candidates import find_candidates


def test_candidates_use_discovery_period_and_strict_five_percent_boundaries(
    feature_frame,
):
    boundary = feature_frame.iloc[[0, 1]].copy()
    boundary["date"] = [pd.Timestamp("2023-12-29"), pd.Timestamp("2024-01-02")]
    boundary["return_3d"] = [0.05, 0.08]
    data = pd.concat([feature_frame, boundary], ignore_index=True)

    result = find_candidates(
        data,
        pd.Timestamp("2018-01-01"),
        pd.Timestamp("2023-12-31"),
    )

    assert result["date"].max() <= pd.Timestamp("2023-12-31")
    assert result.query("direction == 'bullish'")["return_3d"].gt(0.05).all()
    assert result.query("direction == 'bearish'")["return_3d"].lt(-0.05).all()
    assert not result["return_3d"].eq(0.05).any()
    assert {"ticker", "date", "direction", "return_3d", *FEATURE_COLUMNS} <= set(
        result.columns
    )


def test_discovery_excludes_label_realized_after_2023(feature_frame):
    crossing = feature_frame.iloc[[0]].copy()
    crossing["date"] = pd.Timestamp("2023-12-29")
    crossing["return_3d_date"] = pd.Timestamp("2024-01-04")
    crossing["return_3d"] = 0.08

    result = find_candidates(
        crossing,
        pd.Timestamp("2018-01-01"),
        pd.Timestamp("2023-12-31"),
    )

    assert result.empty


def test_cluster_centroids_preserve_standardized_and_raw_scales(candidate_frame):
    scaler = fit_discovery_scaler(candidate_frame)

    patterns = cluster_candidates(
        candidate_frame,
        scaler=scaler,
        distance_threshold=1.0,
    )

    assert set(patterns["direction"]) == {"bullish", "bearish"}
    assert {"centroid_z", "centroid_raw", "source_candidates"} <= set(
        patterns.columns
    )
    assert patterns["centroid_z"].map(len).eq(10).all()
    assert patterns["centroid_raw"].map(len).eq(10).all()
    assert patterns["cluster_size"].sum() == len(candidate_frame)
    assert patterns["source_candidates"].map(len).sum() == len(candidate_frame)


def test_single_candidate_direction_forms_one_cluster(candidate_frame):
    one_each = pd.concat(
        [
            candidate_frame.query("direction == 'bullish'").head(1),
            candidate_frame.query("direction == 'bearish'").head(1),
        ],
        ignore_index=True,
    )
    scaler = fit_discovery_scaler(candidate_frame)

    patterns = cluster_candidates(one_each, scaler, distance_threshold=1.0)

    assert len(patterns) == 2
    assert patterns["cluster_size"].eq(1).all()
