import math

import numpy as np

from src.build_features import FEATURE_COLUMNS, build_features


def test_feature_formulas_use_exact_specification(sample_ohlcv):
    result = build_features(sample_ohlcv)
    position = 7
    row = result.iloc[position]
    current = sample_ohlcv.iloc[position]
    previous = sample_ohlcv.iloc[position - 1]
    close = current["Close"]
    volume_mean = sample_ohlcv["Volume"].iloc[position - 4 : position + 1].mean()

    assert math.isclose(
        row["upper"],
        (current["High"] - max(current["Open"], close)) / close * 100,
    )
    assert math.isclose(
        row["lower"],
        (min(current["Open"], close) - current["Low"]) / close * 100,
    )
    assert math.isclose(row["body"], (close - current["Open"]) / close * 100)
    assert math.isclose(row["prev_upper"], result.iloc[position - 1]["upper"])
    assert math.isclose(row["prev_lower"], result.iloc[position - 1]["lower"])
    assert math.isclose(row["prev_body"], result.iloc[position - 1]["body"])
    assert math.isclose(
        row["open_style"], (current["Open"] - previous["Close"]) / close * 100
    )
    assert math.isclose(
        row["close_style"], (close - previous["Close"]) / close * 100
    )
    assert math.isclose(
        row["volume_feature"], (current["Volume"] - volume_mean) / current["Volume"]
    )
    assert math.isclose(
        row["trend"],
        (
            sample_ohlcv.iloc[position - 2]["Close"]
            - sample_ohlcv.iloc[position - 7]["Close"]
        )
        / sample_ohlcv.iloc[position - 7]["Close"],
    )
    assert math.isclose(
        row["return_3d"],
        (sample_ohlcv.iloc[position + 3]["Close"] - close) / close,
    )
    assert list(FEATURE_COLUMNS) == [
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
    ]


def test_zero_volume_is_never_pattern_eligible(sample_ohlcv):
    sample_ohlcv.loc[sample_ohlcv.index[8], "Volume"] = 0

    result = build_features(sample_ohlcv)

    assert np.isnan(result.loc[sample_ohlcv.index[8], "volume_feature"])
    assert not bool(result.loc[sample_ohlcv.index[8], "pattern_eligible"])


def test_rolling_and_future_boundaries_remain_nan(sample_ohlcv):
    result = build_features(sample_ohlcv)

    assert result["trend"].iloc[:7].isna().all()
    assert result["volume_feature"].iloc[:4].isna().all()
    assert result["return_3d"].iloc[-3:].isna().all()
