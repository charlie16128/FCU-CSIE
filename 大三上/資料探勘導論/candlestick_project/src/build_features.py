from __future__ import annotations

import numpy as np
import pandas as pd


FEATURE_COLUMNS = (
    "upper",
    "lower",
    "body",
    "prev_upper",
    "prev_lower",
    "prev_body",
    "open_style",
    "close_style",
    "volume_feature",
    "trend",
)


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    if "pattern_eligible" not in data.columns:
        data["pattern_eligible"] = True

    open_price = data["Open"].astype(float)
    high = data["High"].astype(float)
    low = data["Low"].astype(float)
    close = data["Close"].astype(float)
    volume = data["Volume"].astype(float)

    upper = (high - pd.concat([open_price, close], axis=1).max(axis=1)) / close * 100
    lower = (pd.concat([open_price, close], axis=1).min(axis=1) - low) / close * 100
    body = (close - open_price) / close * 100
    previous_close = close.shift(1)
    five_day_mean_volume = volume.rolling(window=5, min_periods=5).mean()

    data["upper"] = upper
    data["lower"] = lower
    data["body"] = body
    data["prev_upper"] = upper.shift(1)
    data["prev_lower"] = lower.shift(1)
    data["prev_body"] = body.shift(1)
    data["open_style"] = (open_price - previous_close) / close * 100
    data["close_style"] = (close - previous_close) / close * 100
    with np.errstate(divide="ignore", invalid="ignore"):
        data["volume_feature"] = np.where(
            volume.ne(0),
            (volume - five_day_mean_volume) / volume,
            np.nan,
        )
    data["trend"] = (close.shift(2) - close.shift(7)) / close.shift(7)
    data["return_3d"] = (close.shift(-3) - close) / close
    data.loc[volume.eq(0), "pattern_eligible"] = False
    return data
