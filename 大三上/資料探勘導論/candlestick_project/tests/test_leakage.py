import numpy as np
import pandas as pd
import pytest

from src.build_features import FEATURE_COLUMNS
from src.cluster_patterns import fit_discovery_scaler


def test_scaler_rejects_non_discovery_rows(feature_frame):
    feature_frame.loc[0, "date"] = pd.Timestamp("2026-01-02")

    with pytest.raises(ValueError, match="2018-2023"):
        fit_discovery_scaler(feature_frame)


def test_scaler_is_fit_only_on_valid_discovery_features(feature_frame):
    feature_frame.loc[0, FEATURE_COLUMNS[0]] = np.nan

    scaler = fit_discovery_scaler(feature_frame)
    valid = feature_frame[list(FEATURE_COLUMNS)].dropna()
    transformed = scaler.transform(valid)

    assert np.allclose(transformed.mean(axis=0), 0.0, atol=1e-12)
