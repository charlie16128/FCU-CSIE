from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = ("Open", "High", "Low", "Close", "Volume")
ACTION_COLUMNS = ("Dividends", "Stock Splits")


def clean_ohlcv(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required OHLCV columns: {', '.join(missing)}")

    data = frame.copy()
    index = pd.DatetimeIndex(pd.to_datetime(data.index))
    if index.tz is not None:
        index = index.tz_localize(None)
    data.index = index
    data.index.name = "Date"
    input_rows = len(data)

    data = data.loc[~data.index.duplicated(keep="last")].sort_index()
    for column in ACTION_COLUMNS:
        if column not in data.columns:
            data[column] = 0.0
        data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0.0)

    numeric_columns = list(REQUIRED_COLUMNS)
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    complete = data[numeric_columns].notna().all(axis=1)
    positive_prices = data[["Open", "High", "Low", "Close"]].gt(0).all(axis=1)
    nonnegative_volume = data["Volume"].ge(0)
    data = data.loc[complete & positive_prices & nonnegative_volume].copy()

    action = data["Dividends"].ne(0) | data["Stock Splits"].ne(0)
    excluded = action.copy()
    for offset in (-1, 1, 2, 3):
        excluded |= action.shift(offset, fill_value=False)
    data["pattern_eligible"] = ~excluded

    summary = {
        "input_rows": input_rows,
        "valid_rows": len(data),
        "removed_invalid_rows": input_rows - len(data),
        "corporate_action_excluded": int(excluded.sum()),
    }
    return data, summary
