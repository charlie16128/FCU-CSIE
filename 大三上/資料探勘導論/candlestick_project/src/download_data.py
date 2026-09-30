from __future__ import annotations

from collections.abc import Callable, Iterable
import logging
from pathlib import Path
import time

import pandas as pd


Downloader = Callable[[str, str, str], pd.DataFrame]


def yfinance_downloader(ticker: str, start: str, end: str) -> pd.DataFrame:
    import yfinance as yf

    return yf.Ticker(ticker).history(
        start=start,
        end=end,
        auto_adjust=False,
        actions=True,
    )


def download_universe(
    tickers: Iterable[str],
    output_dir: Path,
    downloader: Downloader = yfinance_downloader,
    *,
    retries: int = 3,
    retry_backoff_seconds: float = 1.0,
    start: str = "2018-01-01",
    end: str = "2027-01-01",
    logger: logging.Logger | None = None,
) -> dict[str, list[str]]:
    if retries < 1:
        raise ValueError("retries must be at least 1")
    output_dir.mkdir(parents=True, exist_ok=True)
    successful: list[str] = []
    failed: list[str] = []

    for ticker in tickers:
        last_error: Exception | None = None
        for attempt in range(1, retries + 1):
            try:
                frame = downloader(ticker, start, end)
                if frame is None or frame.empty:
                    raise ValueError("download returned no rows")
                data = frame.copy()
                index = pd.DatetimeIndex(pd.to_datetime(data.index))
                if index.tz is not None:
                    index = index.tz_localize(None)
                data.index = index
                data.index.name = "Date"
                data.to_csv(
                    output_dir / f"{ticker}.csv",
                    encoding="utf-8",
                    date_format="%Y-%m-%d",
                )
                successful.append(ticker)
                if logger:
                    logger.info("Downloaded %s: %d rows", ticker, len(data))
                break
            except Exception as error:  # isolate one ticker from the universe
                last_error = error
                if attempt < retries and retry_backoff_seconds > 0:
                    time.sleep(retry_backoff_seconds * (2 ** (attempt - 1)))
        else:
            failed.append(ticker)
            if logger:
                logger.error(
                    "Download failed for %s after %d attempts: %s",
                    ticker,
                    retries,
                    last_error,
                )

    return {"successful": successful, "failed": failed}
