from __future__ import annotations

from datetime import date, datetime
import json
import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def load_tickers(path: Path) -> list[str]:
    tickers = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if len(tickers) != len(set(tickers)):
        raise ValueError(f"Duplicate ticker found in {path}")
    return tickers


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    output = frame.copy()
    for column in output.columns:
        if output[column].map(
            lambda value: isinstance(value, (list, tuple, dict, np.ndarray))
        ).any():
            output[column] = output[column].map(
                lambda value: json.dumps(
                    value,
                    ensure_ascii=False,
                    default=_json_default,
                )
                if isinstance(value, (list, tuple, dict, np.ndarray))
                else value
            )
    output.to_csv(path, index=False, encoding="utf-8", date_format="%Y-%m-%d")


def _json_default(value: Any) -> Any:
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()
    if pd.isna(value):
        return None
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def write_json(value: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, default=_json_default),
        encoding="utf-8",
    )


def configure_logging(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f"candlestick_project.{log_dir.resolve()}")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if logger.handlers:
        return logger
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler(
        log_dir / f"run_{stamp}.log", encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def ensure_project_directories(project_root: Path) -> None:
    for relative in (
        "data/raw",
        "data/processed",
        "data/results",
        "models",
        "logs",
        "outputs/figures",
        "outputs/patterns",
    ):
        (project_root / relative).mkdir(parents=True, exist_ok=True)
