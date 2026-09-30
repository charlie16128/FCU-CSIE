from pathlib import Path

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def sample_ohlcv() -> pd.DataFrame:
    dates = pd.bdate_range("2023-01-02", periods=14)
    close = np.arange(100.0, 114.0)
    return pd.DataFrame(
        {
            "Open": close - 1.0,
            "High": close + 2.0,
            "Low": close - 3.0,
            "Close": close,
            "Volume": np.arange(1_000.0, 2_400.0, 100.0),
            "Adj Close": close,
            "Dividends": 0.0,
            "Stock Splits": 0.0,
            "pattern_eligible": True,
        },
        index=dates,
    ).rename_axis("Date")


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    for relative in (
        "config",
        "data/raw",
        "data/processed",
        "data/results",
        "models",
        "logs",
        "outputs/figures",
        "outputs/patterns",
    ):
        (tmp_path / relative).mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture
def feature_frame() -> pd.DataFrame:
    count = 40
    frame = pd.DataFrame(
        {
            "ticker": ["2330.TW"] * count,
            "date": pd.bdate_range("2020-01-02", periods=count),
            "pattern_eligible": True,
            "return_3d": np.zeros(count),
        }
    )
    for feature_index, column in enumerate(
        (
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
    ):
        frame[column] = np.linspace(0.0, 1.0 + feature_index / 10, count)
    frame.loc[5:14, "return_3d"] = 0.06
    frame.loc[20:29, "return_3d"] = -0.06
    return frame


@pytest.fixture
def candidate_frame(feature_frame: pd.DataFrame) -> pd.DataFrame:
    frame = feature_frame.loc[feature_frame["return_3d"].abs() > 0.05].copy()
    frame["direction"] = np.where(
        frame["return_3d"] > 0,
        "bullish",
        "bearish",
    )
    return frame.reset_index(drop=True)
