from collections import Counter

import pandas as pd

from src.download_data import download_universe


def test_download_continues_after_one_ticker_fails(tmp_path, sample_ohlcv):
    attempts = Counter()

    def downloader(ticker: str, start: str, end: str) -> pd.DataFrame:
        attempts[ticker] += 1
        if ticker == "BAD.TW":
            raise RuntimeError("synthetic download failure")
        return sample_ohlcv.copy()

    summary = download_universe(
        ["GOOD.TW", "BAD.TW"],
        tmp_path,
        downloader=downloader,
        retries=2,
        retry_backoff_seconds=0,
    )

    assert summary["successful"] == ["GOOD.TW"]
    assert summary["failed"] == ["BAD.TW"]
    assert attempts == Counter({"BAD.TW": 2, "GOOD.TW": 1})
    saved = pd.read_csv(tmp_path / "GOOD.TW.csv")
    assert {
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Adj Close",
        "Dividends",
        "Stock Splits",
    } <= set(saved.columns)


def test_empty_download_is_retried_and_reported(tmp_path):
    attempts = 0

    def downloader(ticker: str, start: str, end: str) -> pd.DataFrame:
        nonlocal attempts
        attempts += 1
        return pd.DataFrame()

    summary = download_universe(
        ["EMPTY.TW"],
        tmp_path,
        downloader=downloader,
        retries=3,
        retry_backoff_seconds=0,
    )

    assert attempts == 3
    assert summary["failed"] == ["EMPTY.TW"]
    assert not (tmp_path / "EMPTY.TW.csv").exists()
