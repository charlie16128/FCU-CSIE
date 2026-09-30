import numpy as np
import pandas as pd

from src.clean_data import REQUIRED_COLUMNS, clean_ohlcv


def test_corporate_action_excludes_previous_current_and_next_three_days(
    sample_ohlcv,
):
    sample_ohlcv.loc[sample_ohlcv.index[5], "Dividends"] = 1.0

    cleaned, summary = clean_ohlcv(sample_ohlcv)

    assert cleaned.loc[cleaned.index[4:9], "pattern_eligible"].eq(False).all()
    assert cleaned.loc[cleaned.index[:4], "pattern_eligible"].all()
    assert cleaned.loc[cleaned.index[9:], "pattern_eligible"].all()
    assert summary["corporate_action_excluded"] == 5


def test_cleaning_sorts_deduplicates_and_removes_invalid_rows(sample_ohlcv):
    duplicated = pd.concat([sample_ohlcv.iloc[::-1], sample_ohlcv.iloc[[3]]])
    duplicated.iloc[0, duplicated.columns.get_loc("Close")] = -1
    duplicated.iloc[1, duplicated.columns.get_loc("Volume")] = -1
    duplicated.iloc[2, duplicated.columns.get_loc("Open")] = np.nan

    cleaned, summary = clean_ohlcv(duplicated)

    assert cleaned.index.is_monotonic_increasing
    assert cleaned.index.is_unique
    assert (cleaned[list(REQUIRED_COLUMNS[:4])] > 0).all().all()
    assert (cleaned["Volume"] >= 0).all()
    assert summary["removed_invalid_rows"] >= 3


def test_missing_corporate_action_columns_default_to_zero(sample_ohlcv):
    without_actions = sample_ohlcv.drop(columns=["Dividends", "Stock Splits"])

    cleaned, summary = clean_ohlcv(without_actions)

    assert {"Dividends", "Stock Splits"} <= set(cleaned.columns)
    assert cleaned["pattern_eligible"].all()
    assert summary["corporate_action_excluded"] == 0
