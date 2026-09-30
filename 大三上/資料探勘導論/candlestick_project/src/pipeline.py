from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from .build_features import FEATURE_COLUMNS, build_features
from .clean_data import clean_ohlcv
from .utils import configure_logging, ensure_project_directories, write_csv


def prepare_data(
    project_root: Path,
    *,
    logger: logging.Logger | None = None,
) -> dict[str, object]:
    project_root = project_root.resolve()
    ensure_project_directories(project_root)
    logger = logger or configure_logging(project_root / "logs")
    raw_paths = sorted((project_root / "data/raw").glob("*.csv"))
    if not raw_paths:
        raise FileNotFoundError("No raw CSV files found. Run --download first.")

    successful = 0
    failed_tickers: list[str] = []
    total_valid_rows = 0
    total_corporate_action_excluded = 0
    total_feature_rows = 0

    for path in raw_paths:
        ticker = path.stem
        try:
            raw = pd.read_csv(path, index_col="Date", parse_dates=True)
            cleaned, cleaning_summary = clean_ohlcv(raw)
            featured = build_features(cleaned)
            output = featured.reset_index()
            write_csv(output, project_root / "data/processed" / path.name)
            successful += 1
            total_valid_rows += int(cleaning_summary["valid_rows"])
            total_corporate_action_excluded += int(
                cleaning_summary["corporate_action_excluded"]
            )
            total_feature_rows += int(
                (
                    featured["pattern_eligible"].fillna(False)
                    & featured[list(FEATURE_COLUMNS)].notna().all(axis=1)
                ).sum()
            )
            logger.info(
                "Prepared %s: %d valid rows, %d eligible feature rows",
                ticker,
                cleaning_summary["valid_rows"],
                total_feature_rows,
            )
        except Exception as error:  # isolate one stock from the universe
            failed_tickers.append(ticker)
            logger.exception("Prepare failed for %s: %s", ticker, error)

    summary: dict[str, object] = {
        "successful": successful,
        "failed": len(failed_tickers),
        "failed_tickers": failed_tickers,
        "valid_rows": total_valid_rows,
        "corporate_action_excluded": total_corporate_action_excluded,
        "feature_rows": total_feature_rows,
    }
    logger.info("Prepare summary: %s", summary)
    return summary
