from __future__ import annotations

import pandas as pd

from .build_features import FEATURE_COLUMNS


def find_candidates(
    frame: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> pd.DataFrame:
    required = {"ticker", "date", "pattern_eligible", "return_3d", *FEATURE_COLUMNS}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Candidate data is missing columns: {', '.join(missing)}")

    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
    if start.year < 2018 or end.year > 2023:
        raise ValueError("Pattern discovery must be limited to 2018-2023")

    data = frame.copy()
    data["date"] = pd.to_datetime(data["date"])
    if "return_3d_date" in data.columns:
        data["return_3d_date"] = pd.to_datetime(
            data["return_3d_date"],
            errors="coerce",
        )
    else:
        ordered = data.sort_values(["ticker", "date"], kind="stable")
        ordered["return_3d_date"] = ordered.groupby(
            "ticker",
            observed=True,
        )["date"].shift(-3)
        data["return_3d_date"] = ordered["return_3d_date"]
    valid = (
        data["date"].between(start, end)
        & data["return_3d_date"].between(start, end)
        & data["pattern_eligible"].fillna(False)
        & data[list(FEATURE_COLUMNS)].notna().all(axis=1)
        & data["return_3d"].notna()
    )
    data = data.loc[valid].copy()
    bullish = data["return_3d"].gt(0.05)
    bearish = data["return_3d"].lt(-0.05)
    data = data.loc[bullish | bearish].copy()
    data["direction"] = "bullish"
    data.loc[data["return_3d"].lt(-0.05), "direction"] = "bearish"
    return data.reset_index(drop=True)
