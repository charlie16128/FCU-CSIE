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


@pytest.fixture
def patterns() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "pattern_id": "bullish_0001",
                "direction": "bullish",
                "centroid_z": np.zeros(10).tolist(),
            },
            {
                "pattern_id": "bearish_0001",
                "direction": "bearish",
                "centroid_z": np.ones(10).tolist(),
            },
        ]
    )


@pytest.fixture
def validation_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "ticker": "2330.TW",
                "date": pd.Timestamp("2024-01-02"),
                "features_z": np.zeros(10).tolist(),
                "return_3d": 0.06,
            },
            {
                "ticker": "2454.TW",
                "date": pd.Timestamp("2024-01-03"),
                "features_z": np.ones(10).tolist(),
                "return_3d": -0.07,
            },
            {
                "ticker": "2308.TW",
                "date": pd.Timestamp("2024-01-04"),
                "features_z": np.full(10, 0.02).tolist(),
                "return_3d": 0.05,
            },
        ]
    )


@pytest.fixture
def metric_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "pattern_id": ["a", "b", "c"],
            "direction": ["bullish", "bullish", "bullish"],
            "occurrence_count": [30, 60, 90],
            "success_count": [18, 42, 72],
            "accuracy": [0.60, 0.70, 0.80],
            "average_directional_profit": [0.05, 0.06, 0.07],
        }
    )


@pytest.fixture
def parameter_results() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "parameter_set_score": 0.8,
                "mean_directional_profit": 0.07,
                "mean_accuracy": 0.7,
                "total_occurrence": 400,
                "similarity_threshold": 0.6,
            },
            {
                "parameter_set_score": 0.8,
                "mean_directional_profit": 0.07,
                "mean_accuracy": 0.7,
                "total_occurrence": 400,
                "similarity_threshold": 0.5,
            },
        ]
    )


@pytest.fixture
def optimizer_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    pattern_rows = []
    for direction, centroid in (("bullish", 0.0), ("bearish", 1.0)):
        for index in range(10):
            pattern_rows.append(
                {
                    "pattern_id": f"{direction}_{index:02d}",
                    "direction": direction,
                    "centroid_z": np.full(10, centroid).tolist(),
                }
            )
    validation = []
    for index in range(30):
        validation.append(
            {
                "ticker": "2330.TW",
                "date": pd.Timestamp("2024-01-02") + pd.offsets.BDay(index),
                "features_z": np.zeros(10).tolist(),
                "return_3d": 0.06,
            }
        )
        validation.append(
            {
                "ticker": "2454.TW",
                "date": pd.Timestamp("2024-01-02") + pd.offsets.BDay(index),
                "features_z": np.ones(10).tolist(),
                "return_3d": -0.07,
            }
        )
    return pd.DataFrame(pattern_rows), pd.DataFrame(validation)
