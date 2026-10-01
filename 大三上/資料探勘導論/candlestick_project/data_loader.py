"""Download and clean daily stock data."""

from __future__ import annotations

from collections.abc import Callable, Iterable
import logging
from pathlib import Path
import time

import pandas as pd

from config import DOWNLOAD_END, DOWNLOAD_START, STOCK_TICKERS


Downloader = Callable[[str, str, str], pd.DataFrame]
REQUIRED_COLUMNS = ("Open", "High", "Low", "Close", "Volume")
ACTION_COLUMNS = ("Dividends", "Stock Splits")


def yfinance_downloader(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Return unadjusted OHLCV and corporate actions for one ticker."""
    import yfinance as yf

    return yf.Ticker(ticker).history(
        start=start,
        end=end,
        auto_adjust=False,
        actions=True,
    )


def _normalise_download(frame: pd.DataFrame) -> pd.DataFrame:
    if frame is None or frame.empty:
        raise ValueError("download returned no rows")
    data = frame.copy()
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    index = pd.DatetimeIndex(pd.to_datetime(data.index, errors="raise"))
    if index.tz is not None:
        index = index.tz_localize(None)
    data.index = index
    data.index.name = "Date"
    return data


def download_market_data(
    output_dir: Path,
    tickers: Iterable[str] = STOCK_TICKERS,
    *,
    downloader: Downloader = yfinance_downloader,
    retries: int = 3,
    retry_delay: float = 0.5,
    start: str = DOWNLOAD_START,
    end: str = DOWNLOAD_END,
    logger: logging.Logger | None = None,
) -> dict[str, list[str]]:
    """Download each ticker independently and keep going after a failure."""
    if retries < 1:
        raise ValueError("retries must be at least 1")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    successful: list[str] = []
    failed: list[str] = []

    for ticker in tickers:
        last_error: Exception | None = None
        for attempt in range(retries):
            try:
                data = _normalise_download(downloader(ticker, start, end))
                data.to_csv(
                    output_dir / f"{ticker}.csv",
                    encoding="utf-8",
                    date_format="%Y-%m-%d",
                )
                successful.append(ticker)
                if logger:
                    logger.info("Downloaded %s (%d rows)", ticker, len(data))
                break
            except Exception as error:  # one ticker must not stop the universe
                last_error = error
                if attempt + 1 < retries and retry_delay > 0:
                    time.sleep(retry_delay * (2**attempt))
        else:
            failed.append(ticker)
            if logger:
                logger.error("Download failed for %s: %s", ticker, last_error)

    return {"successful": successful, "failed": failed}


def clean_ohlcv(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Validate OHLCV and mark rows near corporate actions as ineligible."""
    data = frame.copy()
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
        data = data.set_index("Date")
    data.index = pd.DatetimeIndex(pd.to_datetime(data.index, errors="coerce"))
    data = data.loc[~data.index.isna()]
    input_rows = len(data)
    data = data.loc[~data.index.duplicated(keep="last")].sort_index()

    missing = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing:
        raise ValueError(f"missing required OHLCV columns: {', '.join(missing)}")
    for column in (*REQUIRED_COLUMNS, *ACTION_COLUMNS):
        if column not in data.columns:
            data[column] = 0.0
        data[column] = pd.to_numeric(data[column], errors="coerce")

    prices = data[["Open", "High", "Low", "Close"]]
    valid = prices.notna().all(axis=1) & prices.gt(0).all(axis=1)
    valid &= data["Volume"].notna() & data["Volume"].ge(0)
    valid &= data["High"].ge(prices[["Open", "Close", "Low"]].max(axis=1))
    valid &= data["Low"].le(prices[["Open", "Close", "High"]].min(axis=1))
    data = data.loc[valid].copy()
    data["pattern_eligible"] = True

    actions = data["Dividends"].fillna(0).ne(0) | data["Stock Splits"].fillna(0).ne(0)
    excluded = pd.Series(False, index=data.index)
    for position in range(len(data)):
        if bool(actions.iloc[position]):
            start = max(0, position - 1)
            stop = min(len(data), position + 4)
            excluded.iloc[start:stop] = True
    data.loc[excluded, "pattern_eligible"] = False

    summary = {
        "input_rows": input_rows,
        "valid_rows": len(data),
        "invalid_rows_removed": input_rows - len(data),
        "corporate_action_excluded": int(excluded.sum()),
    }
    return data, summary


def load_clean_stocks(
    raw_dir: Path,
    *,
    tickers: Iterable[str] | None = None,
    logger: logging.Logger | None = None,
) -> dict[str, pd.DataFrame]:
    """Load and clean every local ticker CSV."""
    raw_dir = Path(raw_dir)
    if tickers is None:
        paths = sorted(raw_dir.glob("*.csv"))
    else:
        requested = tuple(dict.fromkeys(tickers))
        paths = [raw_dir / f"{ticker}.csv" for ticker in requested]
        missing = [path.stem for path in paths if not path.exists()]
        if missing and logger:
            logger.warning("Missing configured raw CSV files: %s", ", ".join(missing))
        paths = [path for path in paths if path.exists()]
    if not paths:
        raise FileNotFoundError("No raw CSV files found. Run --download first.")

    stocks: dict[str, pd.DataFrame] = {}
    for path in paths:
        try:
            raw = pd.read_csv(path, index_col="Date", parse_dates=True)
            stocks[path.stem] = clean_ohlcv(raw)[0]
        except Exception as error:
            if logger:
                logger.error("Skipped %s: %s", path.stem, error)
    if not stocks:
        raise ValueError("No valid stock CSV files could be loaded")
    return stocks


def download_project(project_root: Path) -> dict[str, list[str]]:
    """Download the configured universe into a project."""
    root = Path(project_root).resolve()
    log_dir = root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f"candlestick-download:{root}")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_dir / "latest.log", encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        )
        logger.addHandler(handler)
    summary = download_market_data(root / "data" / "raw", logger=logger)
    if len(summary["successful"]) < len(STOCK_TICKERS):
        logger.warning(
            "Only %d of %d configured stocks downloaded successfully",
            len(summary["successful"]),
            len(STOCK_TICKERS),
        )
    return summary
