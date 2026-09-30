from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

from .build_features import FEATURE_COLUMNS


DISCOVERY_START = pd.Timestamp(date(2018, 1, 1))
DISCOVERY_END = pd.Timestamp(date(2023, 12, 31))


def fit_discovery_scaler(frame: pd.DataFrame) -> StandardScaler:
    if "date" not in frame.columns:
        raise ValueError("Scaler fit data must contain a date column")
    dates = pd.to_datetime(frame["date"], errors="raise")
    if dates.empty or dates.min() < DISCOVERY_START or dates.max() > DISCOVERY_END:
        raise ValueError("Scaler fit data must be limited to 2018-2023")

    values = frame.loc[
        frame[list(FEATURE_COLUMNS)].notna().all(axis=1),
        list(FEATURE_COLUMNS),
    ]
    if values.empty:
        raise ValueError("No valid discovery features are available for scaler fit")
    return StandardScaler().fit(values)


def cluster_candidates(
    candidates: pd.DataFrame,
    scaler: StandardScaler,
    distance_threshold: float,
) -> pd.DataFrame:
    if distance_threshold <= 0:
        raise ValueError("distance_threshold must be positive")
    required = {"ticker", "date", "direction", *FEATURE_COLUMNS}
    missing = sorted(required - set(candidates.columns))
    if missing:
        raise ValueError(f"Candidate data is missing columns: {', '.join(missing)}")
    if candidates.empty:
        raise ValueError("No candidates are available for clustering")

    rows: list[dict[str, object]] = []
    for direction in ("bullish", "bearish"):
        subset = candidates.loc[candidates["direction"].eq(direction)].reset_index(
            drop=True
        )
        if subset.empty:
            raise ValueError(f"No {direction} candidates are available for clustering")
        standardized = scaler.transform(subset[list(FEATURE_COLUMNS)])
        if len(subset) == 1:
            labels = np.zeros(1, dtype=int)
        else:
            labels = AgglomerativeClustering(
                n_clusters=None,
                distance_threshold=distance_threshold,
                linkage="ward",
            ).fit_predict(standardized)

        unique_labels = sorted(np.unique(labels))
        for sequence, label in enumerate(unique_labels, start=1):
            positions = np.flatnonzero(labels == label)
            members = subset.iloc[positions]
            centroid_z = standardized[positions].mean(axis=0)
            source_candidates = [
                {
                    "ticker": str(member["ticker"]),
                    "date": pd.Timestamp(member["date"]).strftime("%Y-%m-%d"),
                }
                for _, member in members.iterrows()
            ]
            rows.append(
                {
                    "pattern_id": f"{direction}_{sequence:04d}",
                    "direction": direction,
                    "cluster_size": int(len(members)),
                    "centroid_z": centroid_z.tolist(),
                    "centroid_raw": scaler.inverse_transform(
                        centroid_z.reshape(1, -1)
                    )[0].tolist(),
                    "source_candidates": source_candidates,
                }
            )

    return pd.DataFrame(rows)
