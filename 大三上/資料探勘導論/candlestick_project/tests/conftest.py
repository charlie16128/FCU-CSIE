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
