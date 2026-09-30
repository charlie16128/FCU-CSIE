# Candlestick Patterns Discovering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete, testable Python project specified by `作業一.md`, without downloading the formal 50-stock dataset or producing the final report in this implementation pass.

**Architecture:** A staged CLI pipeline writes immutable artifacts between download, preparation, discovery, validation, selection, and final-test stages. Pure NumPy/Pandas functions implement formulas and metrics, scikit-learn handles scaling and agglomerative clustering, and the Tkinter GUI only reads locked artifacts.

**Tech Stack:** Python 3.11+, pandas, NumPy, scikit-learn, yfinance, Matplotlib, joblib, PyYAML, Tkinter, pytest

---

## File map

- `candlestick_project/main.py`: command-line entry point and stage ordering.
- `candlestick_project/config/settings.yaml`: all experiment dates, thresholds, paths, weights, and retry limits.
- `candlestick_project/config/tickers.txt`: fixed 50-stock Taiwan 50 universe.
- `candlestick_project/config/test_tickers.txt`: fixed representative 2026 test universe.
- `candlestick_project/src/settings.py`: typed settings loader and project paths.
- `candlestick_project/src/utils.py`: logging, UTF-8 CSV/JSON I/O, ticker loading, and validation helpers.
- `candlestick_project/src/pipeline.py`: artifact validation and stage orchestration.
- `candlestick_project/src/download_data.py`: yfinance download with retries and per-ticker failure isolation.
- `candlestick_project/src/clean_data.py`: OHLCV validation and corporate-action exclusion mask.
- `candlestick_project/src/build_features.py`: the exact ten features and three-trading-day return.
- `candlestick_project/src/find_candidates.py`: discovery-period filtering and candidate CSV creation.
- `candlestick_project/src/cluster_patterns.py`: discovery-only scaler fit and direction-specific clustering.
- `candlestick_project/src/similarity.py`: grouped weights, weighted distances, and matching.
- `candlestick_project/src/backtest_patterns.py`: vectorized pattern matches and per-pattern metrics.
- `candlestick_project/src/optimize_similarity.py`: weight/threshold grid search and parameter-set scoring.
- `candlestick_project/src/select_top10.py`: eligibility relaxation, profit ranking, and centroid deduplication.
- `candlestick_project/src/test_2026.py`: locked-model final evaluation and conflict-aware trade metrics.
- `candlestick_project/src/visualization.py`: pattern and performance PNG generation.
- `candlestick_project/src/gui.py`: read-only Tkinter result browser.
- `candlestick_project/tests/conftest.py`: deterministic OHLCV and project fixtures shared by tests.
- `candlestick_project/tests/`: unit and synthetic integration tests.

### Task 1: Project skeleton, settings, and safe I/O

**Files:**
- Create: `candlestick_project/requirements.txt`
- Create: `candlestick_project/config/settings.yaml`
- Create: `candlestick_project/config/tickers.txt`
- Create: `candlestick_project/config/test_tickers.txt`
- Create: `candlestick_project/src/__init__.py`
- Create: `candlestick_project/src/settings.py`
- Create: `candlestick_project/src/utils.py`
- Create: `candlestick_project/tests/conftest.py`
- Test: `candlestick_project/tests/test_settings.py`

- [ ] **Step 1: Write the failing settings tests**

```python
from pathlib import Path

from src.settings import DateRanges, Settings, load_settings
from src.utils import load_tickers


def test_periods_are_non_overlapping():
    ranges = DateRanges()
    assert ranges.discovery_end < ranges.validation_start
    assert ranges.validation_end < ranges.test_start


def test_fixed_universes_have_required_sizes(project_root: Path):
    assert len(load_tickers(project_root / "config/tickers.txt")) >= 50
    assert len(load_tickers(project_root / "config/test_tickers.txt")) >= 10


def test_load_settings_resolves_paths(project_root: Path):
    settings = load_settings(project_root / "config/settings.yaml")
    assert isinstance(settings, Settings)
    assert settings.project_root == project_root
```

Create the shared test fixtures before running the first test:

```python
# tests/conftest.py
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
    for relative in ("data/raw", "data/processed", "data/results", "models", "logs", "outputs/figures"):
        (tmp_path / relative).mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture
def fake_downloader(sample_ohlcv):
    def download(ticker: str, start: str, end: str) -> pd.DataFrame:
        if ticker == "BAD.TW":
            raise RuntimeError("synthetic download failure")
        return sample_ohlcv.copy()
    return download


@pytest.fixture
def feature_frame() -> pd.DataFrame:
    count = 40
    frame = pd.DataFrame({
        "ticker": ["2330.TW"] * count,
        "date": pd.bdate_range("2020-01-02", periods=count),
        "pattern_eligible": True,
        "return_3d": np.zeros(count),
    })
    for column in (
        "upper", "lower", "body", "prev_upper", "prev_lower", "prev_body",
        "open_style", "close_style", "volume_feature", "trend",
    ):
        frame[column] = np.linspace(0.0, 1.0, count)
    frame.loc[5:14, "return_3d"] = 0.06
    frame.loc[20:29, "return_3d"] = -0.06
    return frame


@pytest.fixture
def candidate_frame(feature_frame) -> pd.DataFrame:
    frame = feature_frame.loc[feature_frame["return_3d"].abs() > 0.05].copy()
    frame["direction"] = np.where(frame["return_3d"] > 0, "bullish", "bearish")
    return frame.reset_index(drop=True)


@pytest.fixture
def patterns() -> pd.DataFrame:
    return pd.DataFrame([
        {"pattern_id": "bullish_0001", "direction": "bullish", "centroid_z": np.zeros(10).tolist()},
        {"pattern_id": "bearish_0001", "direction": "bearish", "centroid_z": np.ones(10).tolist()},
    ])


@pytest.fixture
def validation_rows() -> pd.DataFrame:
    return pd.DataFrame([
        {"ticker": "2330.TW", "date": pd.Timestamp("2024-01-02"), "features_z": np.zeros(10).tolist(), "return_3d": 0.06},
        {"ticker": "2454.TW", "date": pd.Timestamp("2024-01-03"), "features_z": np.ones(10).tolist(), "return_3d": -0.07},
    ])


@pytest.fixture
def metric_frame() -> pd.DataFrame:
    return pd.DataFrame({
        "pattern_id": ["a", "b", "c"],
        "direction": ["bullish", "bullish", "bullish"],
        "occurrence_count": [30, 60, 90],
        "accuracy": [0.60, 0.70, 0.80],
        "average_directional_profit": [0.05, 0.06, 0.07],
    })


@pytest.fixture
def parameter_results() -> pd.DataFrame:
    return pd.DataFrame([
        {"parameter_set_score": 0.8, "mean_directional_profit": 0.07, "mean_accuracy": 0.7, "total_occurrence": 400, "similarity_threshold": 0.6},
        {"parameter_set_score": 0.8, "mean_directional_profit": 0.07, "mean_accuracy": 0.7, "total_occurrence": 400, "similarity_threshold": 0.5},
    ])


def _selection_rows() -> list[dict]:
    rows = []
    for direction_index, direction in enumerate(("bullish", "bearish")):
        for index in range(10):
            centroid = np.zeros(10)
            centroid[0] = direction_index * 20 + index
            rows.append({
                "pattern_id": f"{direction}_{index:02d}",
                "direction": direction,
                "occurrence_count": 20,
                "accuracy": 0.61,
                "average_directional_profit": 0.20 - index * 0.005,
                "centroid_z": centroid.tolist(),
            })
    return rows


@pytest.fixture
def pattern_metrics() -> pd.DataFrame:
    return pd.DataFrame(_selection_rows())


@pytest.fixture
def duplicate_pattern_metrics() -> pd.DataFrame:
    rows = _selection_rows()
    duplicate = rows[0].copy()
    duplicate["pattern_id"] = "bullish_duplicate"
    duplicate["average_directional_profit"] = 0.19
    rows.append(duplicate)
    return pd.DataFrame(rows)


@pytest.fixture
def locked_model() -> dict:
    return {
        "feature_weights": np.ones(10).tolist(),
        "similarity_threshold": 0.5,
        "patterns": [
            {"pattern_id": "bullish_0001", "direction": "bullish", "centroid_z": np.zeros(10).tolist()},
            {"pattern_id": "bearish_0001", "direction": "bearish", "centroid_z": np.zeros(10).tolist()},
        ],
    }


@pytest.fixture
def final_rows() -> pd.DataFrame:
    return pd.DataFrame([{
        "ticker": "2330.TW",
        "date": pd.Timestamp("2026-01-02"),
        "features_z": np.zeros(10).tolist(),
        "return_3d": 0.06,
    }])


@pytest.fixture
def conflict_rows(final_rows) -> pd.DataFrame:
    return final_rows.copy()


@pytest.fixture
def display_fixture() -> dict[str, pd.DataFrame]:
    pattern = pd.DataFrame([{
        "pattern_id": "bullish_0001",
        "direction": "bullish",
        "occurrence_count": 30,
        "accuracy": 0.65,
        "average_directional_profit": 0.07,
        "centroid_raw": np.zeros(10).tolist(),
    }])
    return {
        "bullish": pattern,
        "bearish": pattern.assign(pattern_id="bearish_0001", direction="bearish"),
        "validation": pd.DataFrame([{"label": "set-1", "parameter_set_score": 0.8}]),
        "pattern_test": pd.DataFrame([
            {"pattern_id": "bullish_0001", "number_of_matches": 3, "accuracy": 0.67, "average_directional_profit": 0.06},
            {"pattern_id": "bearish_0001", "number_of_matches": 2, "accuracy": 0.50, "average_directional_profit": 0.04},
        ]),
        "stock_test": pd.DataFrame([{"ticker": "2330.TW", "average_directional_profit": 0.05}]),
    }
```

- [ ] **Step 2: Run the tests and confirm the import failure**

Run: `python -m pytest tests/test_settings.py -v`

Expected: FAIL because `src.settings` does not exist.

- [ ] **Step 3: Implement typed settings and utilities**

```python
# src/settings.py
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import yaml


@dataclass(frozen=True)
class DateRanges:
    download_start: date = date(2018, 1, 1)
    discovery_start: date = date(2018, 1, 1)
    discovery_end: date = date(2023, 12, 31)
    validation_start: date = date(2024, 1, 1)
    validation_end: date = date(2025, 12, 31)
    test_start: date = date(2026, 1, 1)


@dataclass(frozen=True)
class Settings:
    project_root: Path
    dates: DateRanges = field(default_factory=DateRanges)
    cluster_distance_threshold: float = 1.0
    weight_values: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0)
    similarity_thresholds: tuple[float, ...] = tuple(round(x / 10, 1) for x in range(4, 15))
    minimum_occurrences: tuple[int, ...] = (30, 25, 20)
    minimum_accuracies: tuple[float, ...] = (0.60, 0.58, 0.55)
    dedup_thresholds: tuple[float, ...] = (0.30, 0.25, 0.20)
    random_seed: int = 42
    download_retries: int = 3


def load_settings(path: Path) -> Settings:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    root = path.resolve().parent.parent
    return Settings(
        project_root=root,
        cluster_distance_threshold=float(raw["clustering"]["distance_threshold"]),
        weight_values=tuple(map(float, raw["validation"]["weight_values"])),
        similarity_thresholds=tuple(map(float, raw["validation"]["similarity_thresholds"])),
        minimum_occurrences=tuple(map(int, raw["selection"]["minimum_occurrences"])),
        minimum_accuracies=tuple(map(float, raw["selection"]["minimum_accuracies"])),
        dedup_thresholds=tuple(map(float, raw["selection"]["dedup_thresholds"])),
        random_seed=int(raw["runtime"]["random_seed"]),
        download_retries=int(raw["download"]["retries"]),
    )
```

```python
# src/utils.py
from pathlib import Path
from datetime import datetime
import json
import logging
import numpy as np
import pandas as pd


def load_tickers(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, encoding="utf-8")


def write_json(value: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    def convert(item):
        if isinstance(item, np.integer):
            return int(item)
        if isinstance(item, np.floating):
            return float(item)
        if isinstance(item, np.ndarray):
            return item.tolist()
        if isinstance(item, (pd.Timestamp, datetime)):
            return item.isoformat()
        raise TypeError(f"Cannot serialize {type(item).__name__}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=convert), encoding="utf-8")


def configure_logging(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("candlestick_project")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        file_handler = logging.FileHandler(log_dir / f"run_{stamp}.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
```

Use these dependencies in `requirements.txt`:

```text
yfinance>=0.2.54
pandas>=2.2
numpy>=1.26
scikit-learn>=1.4
matplotlib>=3.8
joblib>=1.3
PyYAML>=6.0
pytest>=8.0
```

Use this exact settings file:

```yaml
# config/settings.yaml
dates:
  download_start: "2018-01-01"
  download_end: "2027-01-01"
  discovery_start: "2018-01-01"
  discovery_end: "2023-12-31"
  validation_start: "2024-01-01"
  validation_end: "2025-12-31"
  test_start: "2026-01-01"
  test_end: "2026-12-31"
clustering:
  distance_threshold: 1.0
validation:
  weight_values: [0.5, 1.0, 1.5, 2.0]
  similarity_thresholds: [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
selection:
  minimum_occurrences: [30, 25, 20]
  minimum_accuracies: [0.60, 0.58, 0.55]
  dedup_thresholds: [0.30, 0.25, 0.20]
download:
  retries: 3
runtime:
  random_seed: 42
```

Use the fixed 2026-09-30 Yuanta 0050 holdings snapshot for `tickers.txt`:

```text
1216.TW
1303.TW
2059.TW
2301.TW
2303.TW
2308.TW
2317.TW
2327.TW
2330.TW
2344.TW
2345.TW
2357.TW
2360.TW
2368.TW
2382.TW
2383.TW
2395.TW
2408.TW
2412.TW
2449.TW
2454.TW
2603.TW
2880.TW
2881.TW
2882.TW
2883.TW
2884.TW
2885.TW
2886.TW
2887.TW
2890.TW
2891.TW
2892.TW
3008.TW
3017.TW
3037.TW
3045.TW
3231.TW
3443.TW
3653.TW
3665.TW
3711.TW
4904.TW
4958.TW
5880.TW
6446.TW
6505.TW
6669.TW
7769.TW
8046.TW
```

Use these fixed representative large-cap stocks for `test_tickers.txt`:

```text
2330.TW
2454.TW
2308.TW
2317.TW
3711.TW
2303.TW
3037.TW
2383.TW
2881.TW
2891.TW
```

- [ ] **Step 4: Run the tests**

Run: `python -m pytest tests/test_settings.py -v`

Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/config candlestick_project/src candlestick_project/tests/test_settings.py candlestick_project/requirements.txt
git commit -m "build: scaffold candlestick project settings"
```

### Task 2: Data cleaning and exact feature formulas

**Files:**
- Create: `candlestick_project/src/clean_data.py`
- Create: `candlestick_project/src/build_features.py`
- Test: `candlestick_project/tests/test_clean_data.py`
- Test: `candlestick_project/tests/test_build_features.py`

- [ ] **Step 1: Write failing feature and corporate-action tests**

```python
import numpy as np
import pandas as pd

from src.build_features import FEATURE_COLUMNS, build_features
from src.clean_data import clean_ohlcv


def test_feature_formulas_use_exact_specification(sample_ohlcv):
    result = build_features(sample_ohlcv)
    row = result.iloc[7]
    close = sample_ohlcv.iloc[7]["Close"]
    assert row["upper"] == (sample_ohlcv.iloc[7]["High"] - max(sample_ohlcv.iloc[7]["Open"], close)) / close * 100
    assert row["lower"] == (min(sample_ohlcv.iloc[7]["Open"], close) - sample_ohlcv.iloc[7]["Low"]) / close * 100
    assert row["body"] == (close - sample_ohlcv.iloc[7]["Open"]) / close * 100
    assert row["trend"] == (sample_ohlcv.iloc[5]["Close"] - sample_ohlcv.iloc[0]["Close"]) / sample_ohlcv.iloc[0]["Close"]
    assert row["return_3d"] == (sample_ohlcv.iloc[10]["Close"] - close) / close
    assert list(FEATURE_COLUMNS) == [
        "upper", "lower", "body", "prev_upper", "prev_lower", "prev_body",
        "open_style", "close_style", "volume_feature", "trend",
    ]


def test_corporate_action_excludes_previous_current_and_next_three_days(sample_ohlcv):
    sample_ohlcv.loc[sample_ohlcv.index[5], "Dividends"] = 1.0
    cleaned, summary = clean_ohlcv(sample_ohlcv)
    assert cleaned.loc[cleaned.index[4:9], "pattern_eligible"].eq(False).all()
    assert summary["corporate_action_excluded"] == 5
```

- [ ] **Step 2: Run tests and confirm missing-module failures**

Run: `python -m pytest tests/test_clean_data.py tests/test_build_features.py -v`

Expected: FAIL because the two modules do not exist.

- [ ] **Step 3: Implement cleaning and formulas**

```python
# src/clean_data.py
import pandas as pd

REQUIRED_COLUMNS = ("Open", "High", "Low", "Close", "Volume")


def clean_ohlcv(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    data = frame.copy()
    data.index = pd.to_datetime(data.index).tz_localize(None)
    data = data[~data.index.duplicated(keep="last")].sort_index()
    for column in ("Dividends", "Stock Splits"):
        if column not in data:
            data[column] = 0.0
    before = len(data)
    data = data.dropna(subset=list(REQUIRED_COLUMNS))
    valid = (data[["Open", "High", "Low", "Close"]] > 0).all(axis=1) & (data["Volume"] >= 0)
    data = data.loc[valid].copy()
    action = data["Dividends"].ne(0) | data["Stock Splits"].ne(0)
    excluded = action.copy()
    for offset in (-1, 1, 2, 3):
        excluded |= action.shift(offset, fill_value=False)
    data["pattern_eligible"] = ~excluded
    return data, {
        "input_rows": before,
        "valid_rows": len(data),
        "corporate_action_excluded": int(excluded.sum()),
    }
```

```python
# src/build_features.py
import numpy as np
import pandas as pd

FEATURE_COLUMNS = (
    "upper", "lower", "body", "prev_upper", "prev_lower", "prev_body",
    "open_style", "close_style", "volume_feature", "trend",
)


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    close = data["Close"]
    upper = (data["High"] - data[["Open", "Close"]].max(axis=1)) / close * 100
    lower = (data[["Open", "Close"]].min(axis=1) - data["Low"]) / close * 100
    body = (close - data["Open"]) / close * 100
    previous_close = close.shift(1)
    volume_mean = data["Volume"].rolling(5, min_periods=5).mean()
    data["upper"] = upper
    data["lower"] = lower
    data["body"] = body
    data["prev_upper"] = upper.shift(1)
    data["prev_lower"] = lower.shift(1)
    data["prev_body"] = body.shift(1)
    data["open_style"] = (data["Open"] - previous_close) / close * 100
    data["close_style"] = (close - previous_close) / close * 100
    data["volume_feature"] = np.where(data["Volume"] > 0, (data["Volume"] - volume_mean) / data["Volume"], np.nan)
    data["trend"] = (close.shift(2) - close.shift(7)) / close.shift(7)
    data["return_3d"] = (close.shift(-3) - close) / close
    data.loc[data["Volume"].eq(0), "pattern_eligible"] = False
    return data
```

- [ ] **Step 4: Run focused tests**

Run: `python -m pytest tests/test_clean_data.py tests/test_build_features.py -v`

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/src/clean_data.py candlestick_project/src/build_features.py candlestick_project/tests
git commit -m "feat: clean market data and build exact features"
```

### Task 3: Download and preparation stages

**Files:**
- Create: `candlestick_project/src/download_data.py`
- Test: `candlestick_project/tests/test_download_data.py`
- Test: `candlestick_project/tests/test_prepare_pipeline.py`

- [ ] **Step 1: Write failing isolated-download and preparation tests**

```python
from src.download_data import download_universe
from src.pipeline import prepare_data


def test_download_continues_after_one_ticker_fails(tmp_path, fake_downloader):
    summary = download_universe(["GOOD.TW", "BAD.TW"], tmp_path, fake_downloader, retries=2)
    assert summary["successful"] == ["GOOD.TW"]
    assert summary["failed"] == ["BAD.TW"]
    assert (tmp_path / "GOOD.TW.csv").exists()


def test_prepare_writes_one_processed_file(tmp_project, sample_ohlcv):
    sample_ohlcv.to_csv(tmp_project / "data/raw/2330.TW.csv")
    summary = prepare_data(tmp_project)
    assert summary["successful"] == 1
    assert (tmp_project / "data/processed/2330.TW.csv").exists()
```

- [ ] **Step 2: Run tests and confirm missing API failures**

Run: `python -m pytest tests/test_download_data.py tests/test_prepare_pipeline.py -v`

Expected: FAIL because `download_universe` and `prepare_data` are unavailable.

- [ ] **Step 3: Implement retries, raw preservation, and per-file preparation**

```python
# src/download_data.py
from collections.abc import Callable, Iterable
from pathlib import Path
import time
import pandas as pd


def yfinance_downloader(ticker: str, start: str, end: str) -> pd.DataFrame:
    import yfinance as yf
    return yf.Ticker(ticker).history(start=start, end=end, auto_adjust=False, actions=True)


def download_universe(
    tickers: Iterable[str],
    output_dir: Path,
    downloader: Callable[[str, str, str], pd.DataFrame] = yfinance_downloader,
    retries: int = 3,
    start: str = "2018-01-01",
    end: str = "2027-01-01",
) -> dict[str, list[str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    successful, failed = [], []
    for ticker in tickers:
        for attempt in range(retries):
            try:
                frame = downloader(ticker, start, end)
                if frame.empty:
                    raise ValueError("empty download")
                frame.to_csv(output_dir / f"{ticker}.csv", encoding="utf-8")
                successful.append(ticker)
                break
            except Exception:
                if attempt + 1 == retries:
                    failed.append(ticker)
                else:
                    time.sleep(2 ** attempt)
    return {"successful": successful, "failed": failed}
```

```python
# src/pipeline.py
from pathlib import Path
import pandas as pd
from .build_features import build_features
from .clean_data import clean_ohlcv
from .utils import write_csv


def prepare_data(project_root: Path) -> dict[str, int]:
    successful = failed = 0
    for path in sorted((project_root / "data/raw").glob("*.csv")):
        try:
            raw = pd.read_csv(path, index_col="Date", parse_dates=True)
            clean, _ = clean_ohlcv(raw)
            featured = build_features(clean)
            write_csv(featured.reset_index(), project_root / "data/processed" / path.name)
            successful += 1
        except Exception:
            failed += 1
    return {"successful": successful, "failed": failed}
```

- [ ] **Step 4: Run stage tests**

Run: `python -m pytest tests/test_download_data.py tests/test_prepare_pipeline.py -v`

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/src/download_data.py candlestick_project/src/pipeline.py candlestick_project/tests
git commit -m "feat: add resilient download and preparation stages"
```

### Task 4: Candidate discovery, scaler fit, and clustering

**Files:**
- Create: `candlestick_project/src/find_candidates.py`
- Create: `candlestick_project/src/cluster_patterns.py`
- Test: `candlestick_project/tests/test_discovery.py`
- Test: `candlestick_project/tests/test_leakage.py`

- [ ] **Step 1: Write failing discovery and leakage tests**

```python
import pandas as pd
import pytest

from src.find_candidates import find_candidates
from src.cluster_patterns import fit_discovery_scaler, cluster_candidates


def test_candidates_use_discovery_period_and_strict_five_percent_boundaries(feature_frame):
    result = find_candidates(feature_frame, pd.Timestamp("2018-01-01"), pd.Timestamp("2023-12-31"))
    assert result["date"].max() <= pd.Timestamp("2023-12-31")
    assert result.query("direction == 'bullish'")["return_3d"].gt(0.05).all()
    assert result.query("direction == 'bearish'")["return_3d"].lt(-0.05).all()


def test_scaler_rejects_non_discovery_rows(feature_frame):
    feature_frame.loc[0, "date"] = pd.Timestamp("2026-01-02")
    with pytest.raises(ValueError, match="2018-2023"):
        fit_discovery_scaler(feature_frame)


def test_cluster_centroids_preserve_both_scales(candidate_frame):
    scaler = fit_discovery_scaler(candidate_frame)
    patterns = cluster_candidates(candidate_frame, scaler=scaler, distance_threshold=1.0)
    assert {"centroid_z", "centroid_raw", "source_candidates"} <= set(patterns.columns)
```

- [ ] **Step 2: Run tests and confirm missing-module failures**

Run: `python -m pytest tests/test_discovery.py tests/test_leakage.py -v`

Expected: FAIL because discovery modules do not exist.

- [ ] **Step 3: Implement strict discovery filtering and deterministic agglomerative clusters**

```python
# src/find_candidates.py
import pandas as pd
from .build_features import FEATURE_COLUMNS


def find_candidates(frame: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    valid = frame.loc[
        frame["date"].between(start, end)
        & frame["pattern_eligible"].fillna(False)
        & frame[list(FEATURE_COLUMNS)].notna().all(axis=1)
        & frame["return_3d"].notna()
    ].copy()
    valid["direction"] = pd.NA
    valid.loc[valid["return_3d"] > 0.05, "direction"] = "bullish"
    valid.loc[valid["return_3d"] < -0.05, "direction"] = "bearish"
    return valid.dropna(subset=["direction"])
```

```python
# src/cluster_patterns.py
import json
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from .build_features import FEATURE_COLUMNS


def fit_discovery_scaler(frame: pd.DataFrame) -> StandardScaler:
    dates = pd.to_datetime(frame["date"])
    if dates.max().year > 2023 or dates.min().year < 2018:
        raise ValueError("Scaler fit data must be limited to 2018-2023")
    return StandardScaler().fit(frame[list(FEATURE_COLUMNS)])


def cluster_candidates(candidates: pd.DataFrame, scaler: StandardScaler, distance_threshold: float) -> pd.DataFrame:
    rows = []
    for direction, subset in candidates.groupby("direction", sort=True):
        z = scaler.transform(subset[list(FEATURE_COLUMNS)])
        labels = AgglomerativeClustering(
            n_clusters=None, distance_threshold=distance_threshold, linkage="ward"
        ).fit_predict(z)
        for label in sorted(set(labels)):
            members = subset.iloc[np.flatnonzero(labels == label)]
            centroid_z = z[labels == label].mean(axis=0)
            rows.append({
                "pattern_id": f"{direction}_{label + 1:04d}",
                "direction": direction,
                "cluster_size": len(members),
                "centroid_z": centroid_z.tolist(),
                "centroid_raw": scaler.inverse_transform([centroid_z])[0].tolist(),
                "source_candidates": json.dumps(
                    members[["ticker", "date"]].astype(str).to_dict("records"),
                    ensure_ascii=False,
                ),
            })
    return pd.DataFrame(rows)
```

- [ ] **Step 4: Run discovery tests**

Run: `python -m pytest tests/test_discovery.py tests/test_leakage.py -v`

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/src/find_candidates.py candlestick_project/src/cluster_patterns.py candlestick_project/tests
git commit -m "feat: discover and cluster candlestick candidates"
```

### Task 5: Similarity and vectorized pattern backtest

**Files:**
- Create: `candlestick_project/src/similarity.py`
- Create: `candlestick_project/src/backtest_patterns.py`
- Test: `candlestick_project/tests/test_similarity.py`
- Test: `candlestick_project/tests/test_backtest_patterns.py`

- [ ] **Step 1: Write failing distance and metric tests**

```python
import numpy as np

from src.similarity import expand_group_weights, is_match, weighted_distance
from src.backtest_patterns import backtest_patterns


def test_weighted_distance_rules():
    a = np.zeros(10)
    b = np.ones(10)
    assert weighted_distance(a, a, np.ones(10)) == 0
    assert weighted_distance(a, b, np.full(10, 2.0)) > weighted_distance(a, b, np.ones(10))
    assert is_match(0.5, 0.5)
    assert not is_match(0.500001, 0.5)


def test_group_weight_expansion():
    assert expand_group_weights((1.5, 0.5, 1.0, 1.5, 2.0)).tolist() == [
        1.5, 1.5, 1.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.5, 2.0
    ]


def test_bearish_profit_is_negated(patterns, validation_rows):
    metrics, signals = backtest_patterns(patterns, validation_rows, np.ones(10), 0.5)
    bearish = signals.query("direction == 'bearish'")
    assert np.allclose(bearish["directional_profit"], -bearish["return_3d"])
```

- [ ] **Step 2: Run tests and confirm missing-module failures**

Run: `python -m pytest tests/test_similarity.py tests/test_backtest_patterns.py -v`

Expected: FAIL because similarity and backtest modules do not exist.

- [ ] **Step 3: Implement weighted distance and chunked backtest**

```python
# src/similarity.py
import numpy as np


def expand_group_weights(groups: tuple[float, float, float, float, float]) -> np.ndarray:
    today, previous, position, volume, trend = groups
    return np.asarray([today] * 3 + [previous] * 3 + [position] * 2 + [volume, trend], dtype=float)


def weighted_distance(a, b, weights) -> float:
    delta = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    return float(np.sqrt(np.sum(np.asarray(weights, dtype=float) * delta * delta)))


def is_match(distance: float, threshold: float) -> bool:
    return distance <= threshold
```

```python
# src/backtest_patterns.py
import numpy as np
import pandas as pd


def backtest_patterns(patterns: pd.DataFrame, rows: pd.DataFrame, weights: np.ndarray, threshold: float):
    centroids = np.vstack(patterns["centroid_z"].map(np.asarray))
    vectors = np.vstack(rows["features_z"].map(np.asarray))
    distances = np.sqrt(((centroids[:, None, :] - vectors[None, :, :]) ** 2 * weights).sum(axis=2))
    pattern_index, row_index = np.nonzero(distances <= threshold)
    signals = rows.iloc[row_index].reset_index(drop=True).copy()
    signals["pattern_id"] = patterns.iloc[pattern_index]["pattern_id"].to_numpy()
    signals["direction"] = patterns.iloc[pattern_index]["direction"].to_numpy()
    signals["distance"] = distances[pattern_index, row_index]
    signals["success"] = np.where(
        signals["direction"].eq("bullish"),
        signals["return_3d"] > 0.05,
        signals["return_3d"] < -0.05,
    )
    signals["directional_profit"] = np.where(
        signals["direction"].eq("bullish"), signals["return_3d"], -signals["return_3d"]
    )
    grouped = signals.groupby(["pattern_id", "direction"], observed=True)
    metrics = grouped.agg(
        occurrence_count=("success", "size"),
        success_count=("success", "sum"),
        accuracy=("success", "mean"),
        average_return_3d=("return_3d", "mean"),
        median_return_3d=("return_3d", "median"),
        std_return_3d=("return_3d", "std"),
        average_directional_profit=("directional_profit", "mean"),
        median_directional_profit=("directional_profit", "median"),
    ).reset_index()
    return metrics, signals
```

- [ ] **Step 4: Run similarity and backtest tests**

Run: `python -m pytest tests/test_similarity.py tests/test_backtest_patterns.py -v`

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/src/similarity.py candlestick_project/src/backtest_patterns.py candlestick_project/tests
git commit -m "feat: add weighted similarity and pattern backtests"
```

### Task 6: Validation score and parameter optimization

**Files:**
- Create: `candlestick_project/src/optimize_similarity.py`
- Test: `candlestick_project/tests/test_optimize_similarity.py`

- [ ] **Step 1: Write failing normalization and tie-break tests**

```python
from src.optimize_similarity import add_pattern_scores, choose_best_parameter_set


def test_pattern_score_uses_required_coefficients(metric_frame):
    scored = add_pattern_scores(metric_frame)
    expected = (
        0.50 * scored["normalized_average_directional_profit"]
        + 0.30 * scored["normalized_accuracy"]
        + 0.20 * scored["normalized_log_occurrence"]
    )
    assert scored["pattern_score"].equals(expected)


def test_tie_break_prefers_profit_accuracy_occurrence_then_lower_threshold(parameter_results):
    best = choose_best_parameter_set(parameter_results)
    assert best["similarity_threshold"] == 0.5
```

- [ ] **Step 2: Run tests and confirm missing-module failure**

Run: `python -m pytest tests/test_optimize_similarity.py -v`

Expected: FAIL because `src.optimize_similarity` does not exist.

- [ ] **Step 3: Implement min-max scoring, the full product grid, and deterministic tie-break**

```python
# src/optimize_similarity.py
from itertools import product
import numpy as np
import pandas as pd
from .backtest_patterns import backtest_patterns
from .similarity import expand_group_weights


def _minmax(series: pd.Series) -> pd.Series:
    low, high = series.min(), series.max()
    if high == low:
        return pd.Series(np.ones(len(series)), index=series.index, dtype=float)
    return (series - low) / (high - low)


def add_pattern_scores(metrics: pd.DataFrame) -> pd.DataFrame:
    scored = metrics.copy()
    scored["normalized_average_directional_profit"] = _minmax(scored["average_directional_profit"])
    scored["normalized_accuracy"] = _minmax(scored["accuracy"])
    scored["normalized_log_occurrence"] = _minmax(np.log1p(scored["occurrence_count"]))
    scored["pattern_score"] = (
        0.50 * scored["normalized_average_directional_profit"]
        + 0.30 * scored["normalized_accuracy"]
        + 0.20 * scored["normalized_log_occurrence"]
    )
    return scored


def choose_best_parameter_set(results: pd.DataFrame) -> dict:
    ordered = results.sort_values(
        ["parameter_set_score", "mean_directional_profit", "mean_accuracy", "total_occurrence", "similarity_threshold"],
        ascending=[False, False, False, False, True],
        kind="mergesort",
    )
    return ordered.iloc[0].to_dict()


def optimize(patterns, validation_rows, weight_values, thresholds, minimum_occurrence=30, minimum_accuracy=0.60):
    rows = []
    for groups in product(weight_values, repeat=5):
        weights = expand_group_weights(groups)
        for threshold in thresholds:
            metrics, _ = backtest_patterns(patterns, validation_rows, weights, threshold)
            eligible = metrics.query(
                "occurrence_count >= @minimum_occurrence and accuracy >= @minimum_accuracy"
            )
            scored_parts = []
            for direction in ("bullish", "bearish"):
                part = eligible.query("direction == @direction")
                if not part.empty:
                    scored_parts.append(add_pattern_scores(part).nlargest(10, "pattern_score"))
            if len(scored_parts) != 2:
                continue
            top = pd.concat(scored_parts, ignore_index=True)
            direction_means = top.groupby("direction")["pattern_score"].mean()
            rows.append({
                "today_shape_weight": groups[0],
                "previous_shape_weight": groups[1],
                "position_weight": groups[2],
                "volume_weight": groups[3],
                "trend_weight": groups[4],
                "similarity_threshold": threshold,
                "parameter_set_score": 0.5 * direction_means["bullish"] + 0.5 * direction_means["bearish"],
                "mean_directional_profit": top["average_directional_profit"].mean(),
                "mean_accuracy": top["accuracy"].mean(),
                "total_occurrence": int(top["occurrence_count"].sum()),
            })
    if not rows:
        raise ValueError("No parameter set produced eligible bullish and bearish patterns")
    result = pd.DataFrame(rows)
    return choose_best_parameter_set(result), result
```

- [ ] **Step 4: Run optimizer tests**

Run: `python -m pytest tests/test_optimize_similarity.py -v`

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/src/optimize_similarity.py candlestick_project/tests/test_optimize_similarity.py
git commit -m "feat: optimize validation similarity parameters"
```

### Task 7: Eligibility relaxation, ranking, deduplication, and model locking

**Files:**
- Create: `candlestick_project/src/select_top10.py`
- Test: `candlestick_project/tests/test_select_top10.py`

- [ ] **Step 1: Write failing relaxation and deduplication tests**

```python
import numpy as np
from src.select_top10 import select_top_patterns


def test_selection_relaxes_occurrence_before_accuracy(pattern_metrics):
    selected, policy = select_top_patterns(
        pattern_metrics, np.ones(10), occurrences=(30, 25, 20), accuracies=(0.60, 0.58, 0.55)
    )
    assert policy["minimum_occurrence"] == 20
    assert policy["minimum_accuracy"] == 0.60


def test_near_duplicate_centroids_are_not_selected_twice(duplicate_pattern_metrics):
    selected, _ = select_top_patterns(duplicate_pattern_metrics, np.ones(10))
    assert selected["pattern_id"].nunique() == len(selected)
    assert "bullish_duplicate" not in set(selected["pattern_id"])
```

- [ ] **Step 2: Run tests and confirm missing-module failure**

Run: `python -m pytest tests/test_select_top10.py -v`

Expected: FAIL because `src.select_top10` does not exist.

- [ ] **Step 3: Implement ordered relaxation and profit-first deduplication**

```python
# src/select_top10.py
import numpy as np
import pandas as pd
from .similarity import weighted_distance


def _eligible(metrics, occurrences, accuracies):
    for occurrence in occurrences:
        subset = metrics.query("occurrence_count >= @occurrence and accuracy >= @accuracies[0]")
        if all(len(subset.query("direction == @d")) >= 10 for d in ("bullish", "bearish")):
            return subset, occurrence, accuracies[0]
    for accuracy in accuracies[1:]:
        for occurrence in occurrences:
            subset = metrics.query("occurrence_count >= @occurrence and accuracy >= @accuracy")
            if all(len(subset.query("direction == @d")) >= 10 for d in ("bullish", "bearish")):
                return subset, occurrence, accuracy
    raise ValueError("Fewer than ten eligible patterns remain in one or both directions")


def select_top_patterns(
    metrics: pd.DataFrame,
    weights: np.ndarray,
    occurrences=(30, 25, 20),
    accuracies=(0.60, 0.58, 0.55),
    dedup_thresholds=(0.30, 0.25, 0.20),
):
    eligible, occurrence, accuracy = _eligible(metrics, occurrences, accuracies)
    for dedup_threshold in dedup_thresholds:
        selected = []
        for direction in ("bullish", "bearish"):
            chosen = []
            ranked = eligible.query("direction == @direction").sort_values(
                "average_directional_profit", ascending=False, kind="mergesort"
            )
            for _, row in ranked.iterrows():
                if all(weighted_distance(row["centroid_z"], old["centroid_z"], weights) >= dedup_threshold for old in chosen):
                    chosen.append(row.to_dict())
                if len(chosen) == 10:
                    break
            selected.extend(chosen)
        if sum(item["direction"] == "bullish" for item in selected) == 10 and sum(item["direction"] == "bearish" for item in selected) == 10:
            return pd.DataFrame(selected), {
                "minimum_occurrence": occurrence,
                "minimum_accuracy": accuracy,
                "dedup_threshold": dedup_threshold,
            }
    raise ValueError("Pattern deduplication left fewer than ten patterns in one or both directions")
```

- [ ] **Step 4: Run selection tests**

Run: `python -m pytest tests/test_select_top10.py -v`

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/src/select_top10.py candlestick_project/tests/test_select_top10.py
git commit -m "feat: select and lock top candlestick patterns"
```

### Task 8: Locked 2026 final test and conflict-aware evaluation

**Files:**
- Create: `candlestick_project/src/test_2026.py`
- Test: `candlestick_project/tests/test_final_test.py`

- [ ] **Step 1: Write failing time-boundary and conflict tests**

```python
import pandas as pd
import pytest
from src.test_2026 import evaluate_final_test


def test_final_test_rejects_pre_2026_rows(locked_model, final_rows):
    final_rows.loc[0, "date"] = pd.Timestamp("2025-12-31")
    with pytest.raises(ValueError, match="2026"):
        evaluate_final_test(locked_model, final_rows)


def test_conflicting_trade_signal_is_excluded_but_pattern_hits_remain(locked_model, conflict_rows):
    result = evaluate_final_test(locked_model, conflict_rows)
    assert result.signals["conflict_signal"].all()
    assert result.overall_metrics["total_signals"] == 0
    assert len(result.pattern_metrics) == 2
```

- [ ] **Step 2: Run tests and confirm missing-module failure**

Run: `python -m pytest tests/test_final_test.py -v`

Expected: FAIL because `src.test_2026` does not exist.

- [ ] **Step 3: Implement immutable-model evaluation and aggregate outputs**

```python
# src/test_2026.py
from dataclasses import dataclass
import numpy as np
import pandas as pd
from .backtest_patterns import backtest_patterns


@dataclass(frozen=True)
class FinalTestResult:
    signals: pd.DataFrame
    pattern_metrics: pd.DataFrame
    stock_metrics: pd.DataFrame
    overall_metrics: dict[str, float | int]


def evaluate_final_test(model: dict, rows: pd.DataFrame) -> FinalTestResult:
    dates = pd.to_datetime(rows["date"])
    if dates.min().year != 2026 or dates.max().year != 2026:
        raise ValueError("Final test rows must all be from 2026")
    patterns = pd.DataFrame(model["patterns"])
    weights = np.asarray(model["feature_weights"], dtype=float)
    pattern_metrics, hits = backtest_patterns(patterns, rows, weights, float(model["similarity_threshold"]))
    pattern_metrics = pattern_metrics.rename(columns={"occurrence_count": "number_of_matches"})
    direction_count = hits.groupby(["ticker", "date"])["direction"].nunique()
    conflicts = direction_count[direction_count > 1].index
    hits["conflict_signal"] = pd.MultiIndex.from_frame(hits[["ticker", "date"]]).isin(conflicts)
    trades = hits.loc[~hits["conflict_signal"]].drop_duplicates(["ticker", "date", "direction"])
    stock_metrics = trades.groupby("ticker").agg(
        number_of_signals=("success", "size"),
        accuracy=("success", "mean"),
        average_directional_profit=("directional_profit", "mean"),
    ).reset_index()
    bullish = trades.loc[trades["direction"].eq("bullish")]
    bearish = trades.loc[trades["direction"].eq("bearish")]
    overall = {
        "total_signals": int(len(trades)),
        "successful_signals": int(trades["success"].sum()),
        "overall_accuracy": float(trades["success"].mean()) if len(trades) else 0.0,
        "average_directional_profit": float(trades["directional_profit"].mean()) if len(trades) else 0.0,
        "median_directional_profit": float(trades["directional_profit"].median()) if len(trades) else 0.0,
        "bullish_signal_count": int(len(bullish)),
        "bullish_accuracy": float(bullish["success"].mean()) if len(bullish) else 0.0,
        "bullish_average_return": float(bullish["return_3d"].mean()) if len(bullish) else 0.0,
        "bearish_signal_count": int(len(bearish)),
        "bearish_accuracy": float(bearish["success"].mean()) if len(bearish) else 0.0,
        "bearish_average_directional_profit": float(bearish["directional_profit"].mean()) if len(bearish) else 0.0,
    }
    return FinalTestResult(hits, pattern_metrics, stock_metrics, overall)
```

- [ ] **Step 4: Run final-test tests**

Run: `python -m pytest tests/test_final_test.py -v`

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/src/test_2026.py candlestick_project/tests/test_final_test.py
git commit -m "feat: evaluate locked patterns on 2026 data"
```

### Task 9: Required figures and read-only GUI

**Files:**
- Create: `candlestick_project/src/visualization.py`
- Create: `candlestick_project/src/gui.py`
- Test: `candlestick_project/tests/test_visualization.py`
- Test: `candlestick_project/tests/test_gui_data.py`

- [ ] **Step 1: Write failing artifact and GUI-loading tests**

```python
from src.visualization import generate_required_figures
from src.gui import load_gui_records


def test_required_figure_names_are_written(tmp_path, display_fixture):
    generate_required_figures(display_fixture, tmp_path)
    expected = {
        "top10_bullish.png", "top10_bearish.png", "validation_parameter_search.png",
        "2026_pattern_performance.png", "2026_stock_performance.png",
    }
    assert expected <= {path.name for path in tmp_path.glob("*.png")}


def test_gui_loader_merges_validation_and_2026_metrics(tmp_path, display_fixture):
    records = load_gui_records(display_fixture)
    assert {"pattern_id", "validation_accuracy", "test_accuracy", "centroid_raw"} <= set(records.columns)
```

- [ ] **Step 2: Run tests and confirm missing-module failures**

Run: `python -m pytest tests/test_visualization.py tests/test_gui_data.py -v`

Expected: FAIL because visualization and GUI modules do not exist.

- [ ] **Step 3: Implement deterministic PNG output and GUI data loading**

```python
# src/visualization.py
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _save_bar(frame, x, y, title, path):
    figure, axis = plt.subplots(figsize=(10, 5))
    if not frame.empty:
        axis.bar(frame[x].astype(str), frame[y])
        axis.tick_params(axis="x", rotation=70)
    axis.set_title(title)
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def generate_required_figures(data: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _save_bar(data["bullish"], "pattern_id", "average_directional_profit", "Top 10 Bullish", output_dir / "top10_bullish.png")
    _save_bar(data["bearish"], "pattern_id", "average_directional_profit", "Top 10 Bearish", output_dir / "top10_bearish.png")
    _save_bar(data["validation"], "label", "parameter_set_score", "Validation Parameter Search", output_dir / "validation_parameter_search.png")
    _save_bar(data["pattern_test"], "pattern_id", "average_directional_profit", "2026 Pattern Performance", output_dir / "2026_pattern_performance.png")
    _save_bar(data["stock_test"], "ticker", "average_directional_profit", "2026 Stock Performance", output_dir / "2026_stock_performance.png")
```

```python
# src/gui.py
from pathlib import Path
import json
import numpy as np
import pandas as pd


def load_gui_records(data: dict) -> pd.DataFrame:
    patterns = pd.concat([data["bullish"], data["bearish"]], ignore_index=True)
    test = data["pattern_test"].rename(columns={"accuracy": "test_accuracy"})
    patterns = patterns.rename(columns={"accuracy": "validation_accuracy"})
    return patterns.merge(test[["pattern_id", "number_of_matches", "test_accuracy"]], on="pattern_id", how="left")


def _relative_candles(features: list[float]) -> list[tuple[float, float, float, float]]:
    upper, lower, body, prev_upper, prev_lower, prev_body, open_style, close_style, _, _ = features
    previous_close = 100.0
    previous_open = previous_close * (1 - prev_body / 100)
    previous_high = max(previous_open, previous_close) + prev_upper * previous_close / 100
    previous_low = min(previous_open, previous_close) - prev_lower * previous_close / 100
    denominator = 1 - close_style / 100
    current_close = previous_close / denominator if abs(denominator) > 1e-9 else previous_close
    current_open = previous_close + open_style * current_close / 100
    current_high = max(current_open, current_close) + upper * current_close / 100
    current_low = min(current_open, current_close) - lower * current_close / 100
    return [
        (previous_open, previous_high, previous_low, previous_close),
        (current_open, current_high, current_low, current_close),
    ]


def launch_gui(project_root: Path) -> None:
    import tkinter as tk
    from tkinter import ttk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    result_dir = project_root / "data/results"
    paths = {
        "bullish": result_dir / "top10_bullish.csv",
        "bearish": result_dir / "top10_bearish.csv",
        "pattern_test": result_dir / "test_2026_pattern_metrics.csv",
    }
    if not paths["bullish"].exists() or not paths["bearish"].exists():
        raise FileNotFoundError("Run --validate before --gui")
    data = {
        "bullish": pd.read_csv(paths["bullish"]),
        "bearish": pd.read_csv(paths["bearish"]),
        "pattern_test": pd.read_csv(paths["pattern_test"]) if paths["pattern_test"].exists() else pd.DataFrame(
            columns=["pattern_id", "number_of_matches", "accuracy"]
        ),
    }
    records = load_gui_records(data)

    root = tk.Tk()
    root.title("Candlestick Pattern Explorer")
    root.geometry("1250x720")
    notebook = ttk.Notebook(root)
    notebook.pack(side="left", fill="both", expand=True)
    detail = ttk.Frame(root)
    detail.pack(side="right", fill="both", expand=True)
    figure = Figure(figsize=(5.5, 4.5), dpi=100)
    axis = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, master=detail)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    feature_text = tk.Text(detail, width=58, height=16)
    feature_text.pack(fill="x")

    def show_record(record: pd.Series) -> None:
        raw = record["centroid_raw"]
        if isinstance(raw, str):
            raw = json.loads(raw)
        axis.clear()
        for x, (open_, high, low, close) in enumerate(_relative_candles(raw)):
            color = "#d62728" if close >= open_ else "#2ca02c"
            axis.vlines(x, low, high, color=color, linewidth=1.5)
            axis.bar(x, close - open_, bottom=open_, width=0.5, color=color)
        axis.set_xticks([0, 1], ["Previous", "Current"])
        axis.set_title(f"{record['pattern_id']} reconstructed centroid")
        canvas.draw_idle()
        feature_text.delete("1.0", tk.END)
        feature_text.insert("1.0", record.to_string())

    columns = (
        "pattern_id", "occurrence_count", "validation_accuracy",
        "average_directional_profit", "number_of_matches", "test_accuracy",
    )
    for direction, title in (("bullish", "Bullish Top 10"), ("bearish", "Bearish Top 10")):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=135, anchor="center")
        subset = records.query("direction == @direction").reset_index(drop=True)
        for index, row in subset.iterrows():
            tree.insert("", "end", iid=str(index), values=[row.get(column, "") for column in columns])
        tree.bind("<<TreeviewSelect>>", lambda event, values=subset: show_record(values.iloc[int(event.widget.selection()[0])]))
        tree.pack(fill="both", expand=True)
    root.mainloop()
```

- [ ] **Step 4: Run headless GUI-data and figure tests**

Run: `python -m pytest tests/test_visualization.py tests/test_gui_data.py -v`

Expected: all tests pass and no interactive window opens during tests.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/src/visualization.py candlestick_project/src/gui.py candlestick_project/tests
git commit -m "feat: add result figures and Tkinter explorer"
```

### Task 10: Stage orchestration and CLI contract

**Files:**
- Modify: `candlestick_project/src/pipeline.py`
- Create: `candlestick_project/main.py`
- Test: `candlestick_project/tests/test_cli.py`
- Test: `candlestick_project/tests/test_synthetic_pipeline.py`

- [ ] **Step 1: Write failing CLI and synthetic pipeline tests**

```python
import subprocess
import sys


def test_help_lists_all_modes(project_root):
    result = subprocess.run(
        [sys.executable, "main.py", "--help"],
        cwd=project_root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    for mode in ("--download", "--prepare", "--train", "--validate", "--test", "--gui", "--all"):
        assert mode in result.stdout


def test_gui_does_not_call_training(monkeypatch, project_root):
    from main import run
    monkeypatch.setattr("src.gui.launch_gui", lambda root: None)
    monkeypatch.setattr("src.pipeline.train_patterns", lambda root: (_ for _ in ()).throw(AssertionError()))
    assert run(["--gui"], project_root=project_root) == 0
```

- [ ] **Step 2: Run tests and confirm missing-entry-point failure**

Run: `python -m pytest tests/test_cli.py tests/test_synthetic_pipeline.py -v`

Expected: FAIL because `main.py` and complete stage orchestration are unavailable.

- [ ] **Step 3: Implement mutually composable CLI stages**

```python
# main.py
import argparse
from pathlib import Path
from src import pipeline
from src.gui import launch_gui


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Candlestick pattern discovery pipeline")
    for flag in ("download", "prepare", "train", "validate", "test", "gui", "all"):
        value.add_argument(f"--{flag}", action="store_true")
    return value


def run(argv=None, project_root: Path | None = None) -> int:
    args = parser().parse_args(argv)
    root = (project_root or Path(__file__).resolve().parent).resolve()
    if args.all or args.download:
        pipeline.download_data(root)
    if args.all or args.prepare:
        pipeline.prepare_data(root)
    if args.all or args.train:
        pipeline.train_patterns(root)
    if args.all or args.validate:
        pipeline.validate_patterns(root)
    if args.all or args.test:
        pipeline.test_patterns(root)
    if args.gui:
        launch_gui(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
```

Add these orchestration functions to `src/pipeline.py`:

```python
import json
import joblib
import numpy as np
from .backtest_patterns import backtest_patterns
from .build_features import FEATURE_COLUMNS
from .cluster_patterns import cluster_candidates, fit_discovery_scaler
from .download_data import download_universe
from .find_candidates import find_candidates
from .optimize_similarity import optimize
from .select_top10 import select_top_patterns
from .settings import load_settings
from .similarity import expand_group_weights
from .test_2026 import evaluate_final_test
from .utils import configure_logging, load_tickers, write_csv, write_json
from .visualization import generate_required_figures


def _require(path: Path, instruction: str) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. {instruction}")
    return path


def _load_processed(project_root: Path) -> pd.DataFrame:
    paths = sorted((project_root / "data/processed").glob("*.csv"))
    if not paths:
        raise FileNotFoundError("No processed data. Run --prepare first")
    frames = []
    for path in paths:
        frame = pd.read_csv(path, parse_dates=["Date"]).rename(columns={"Date": "date"})
        frame["ticker"] = path.stem
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def _decode_vectors(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    for column in ("centroid_z", "centroid_raw"):
        if column in result:
            result[column] = result[column].map(lambda value: json.loads(value) if isinstance(value, str) else value)
    return result


def download_data(project_root: Path) -> dict:
    settings = load_settings(project_root / "config/settings.yaml")
    tickers = load_tickers(project_root / "config/tickers.txt")
    summary = download_universe(
        tickers,
        project_root / "data/raw",
        retries=settings.download_retries,
        start=settings.dates.download_start.isoformat(),
        end="2027-01-01",
    )
    if len(summary["successful"]) < 50:
        configure_logging(project_root / "logs").warning("Only %d tickers downloaded", len(summary["successful"]))
    return summary


def train_patterns(project_root: Path) -> dict[str, int]:
    settings = load_settings(project_root / "config/settings.yaml")
    data = _load_processed(project_root)
    discovery = data.loc[
        data["date"].between(
            pd.Timestamp(settings.dates.discovery_start),
            pd.Timestamp(settings.dates.discovery_end),
        )
        & data["pattern_eligible"].fillna(False)
        & data[list(FEATURE_COLUMNS)].notna().all(axis=1)
    ].copy()
    scaler = fit_discovery_scaler(discovery)
    model_dir = project_root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, model_dir / "scaler.pkl")
    candidates = find_candidates(
        data,
        pd.Timestamp(settings.dates.discovery_start),
        pd.Timestamp(settings.dates.discovery_end),
    )
    bullish = candidates.query("direction == 'bullish'")
    bearish = candidates.query("direction == 'bearish'")
    write_csv(bullish, project_root / "data/results/bullish_candidates.csv")
    write_csv(bearish, project_root / "data/results/bearish_candidates.csv")
    patterns = cluster_candidates(candidates, scaler, settings.cluster_distance_threshold)
    write_csv(patterns.query("direction == 'bullish'"), project_root / "data/results/all_bullish_patterns.csv")
    write_csv(patterns.query("direction == 'bearish'"), project_root / "data/results/all_bearish_patterns.csv")
    logger = configure_logging(project_root / "logs")
    for direction in ("bullish", "bearish"):
        count = int(patterns["direction"].eq(direction).sum())
        if count < 20 or count > 300:
            logger.warning("%s cluster count %d is outside 20..300", direction, count)
    return {
        "bullish_candidates": len(bullish),
        "bearish_candidates": len(bearish),
        "patterns": len(patterns),
    }


def _validation_rows(data: pd.DataFrame, scaler, start, end) -> pd.DataFrame:
    rows = data.loc[
        data["date"].between(pd.Timestamp(start), pd.Timestamp(end))
        & data["pattern_eligible"].fillna(False)
        & data[list(FEATURE_COLUMNS)].notna().all(axis=1)
        & data["return_3d"].notna()
    ].copy()
    rows["features_z"] = scaler.transform(rows[list(FEATURE_COLUMNS)]).tolist()
    return rows


def validate_patterns(project_root: Path) -> dict:
    settings = load_settings(project_root / "config/settings.yaml")
    scaler = joblib.load(_require(project_root / "models/scaler.pkl", "Run --train first"))
    bullish = _decode_vectors(pd.read_csv(_require(
        project_root / "data/results/all_bullish_patterns.csv", "Run --train first"
    )))
    bearish = _decode_vectors(pd.read_csv(_require(
        project_root / "data/results/all_bearish_patterns.csv", "Run --train first"
    )))
    patterns = pd.concat([bullish, bearish], ignore_index=True)
    rows = _validation_rows(
        _load_processed(project_root),
        scaler,
        settings.dates.validation_start,
        settings.dates.validation_end,
    )
    best, search = optimize(
        patterns,
        rows,
        settings.weight_values,
        settings.similarity_thresholds,
    )
    groups = (
        best["today_shape_weight"],
        best["previous_shape_weight"],
        best["position_weight"],
        best["volume_weight"],
        best["trend_weight"],
    )
    weights = expand_group_weights(groups)
    metrics, _ = backtest_patterns(patterns, rows, weights, best["similarity_threshold"])
    metrics = metrics.merge(patterns, on=["pattern_id", "direction"], how="left")
    selected, policy = select_top_patterns(
        metrics,
        weights,
        settings.minimum_occurrences,
        settings.minimum_accuracies,
        settings.dedup_thresholds,
    )
    best_params = {
        **{key: best[key] for key in (
            "today_shape_weight", "previous_shape_weight", "position_weight",
            "volume_weight", "trend_weight", "similarity_threshold",
        )},
        **policy,
        "feature_weights": weights.tolist(),
    }
    final_model = {
        "scaler_path": "models/scaler.pkl",
        "feature_weights": weights.tolist(),
        "similarity_threshold": best["similarity_threshold"],
        "minimum_occurrence": policy["minimum_occurrence"],
        "minimum_accuracy": policy["minimum_accuracy"],
        "patterns": selected.to_dict("records"),
    }
    write_csv(search, project_root / "data/results/validation_results.csv")
    write_csv(selected.query("direction == 'bullish'"), project_root / "data/results/top10_bullish.csv")
    write_csv(selected.query("direction == 'bearish'"), project_root / "data/results/top10_bearish.csv")
    write_json(best_params, project_root / "models/best_params.json")
    write_json(final_model, project_root / "models/final_patterns.json")
    configure_logging(project_root / "logs").info("Selection policy: %s", policy)
    return best_params


def test_patterns(project_root: Path) -> dict:
    model_path = _require(project_root / "models/final_patterns.json", "Run --validate first")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    scaler = joblib.load(_require(project_root / "models/scaler.pkl", "Run --train first"))
    test_tickers = set(load_tickers(project_root / "config/test_tickers.txt"))
    data = _load_processed(project_root)
    rows = data.loc[
        data["ticker"].isin(test_tickers)
        & pd.to_datetime(data["date"]).dt.year.eq(2026)
        & data["pattern_eligible"].fillna(False)
        & data[list(FEATURE_COLUMNS)].notna().all(axis=1)
        & data["return_3d"].notna()
    ].copy()
    rows["features_z"] = scaler.transform(rows[list(FEATURE_COLUMNS)]).tolist()
    result = evaluate_final_test(model, rows)
    result_dir = project_root / "data/results"
    write_csv(result.signals, result_dir / "test_2026_signals.csv")
    write_csv(result.pattern_metrics, result_dir / "test_2026_pattern_metrics.csv")
    write_csv(result.stock_metrics, result_dir / "test_2026_stock_metrics.csv")
    write_json(result.overall_metrics, result_dir / "test_2026_overall_metrics.json")
    validation = pd.read_csv(_require(result_dir / "validation_results.csv", "Run --validate first"))
    validation["label"] = np.arange(len(validation)).astype(str)
    generate_required_figures(
        {
            "bullish": pd.read_csv(result_dir / "top10_bullish.csv"),
            "bearish": pd.read_csv(result_dir / "top10_bearish.csv"),
            "validation": validation.nlargest(30, "parameter_set_score"),
            "pattern_test": result.pattern_metrics,
            "stock_test": result.stock_metrics,
        },
        project_root / "outputs/figures",
    )
    return result.overall_metrics
```

- [ ] **Step 4: Run CLI and synthetic end-to-end tests**

Run: `python -m pytest tests/test_cli.py tests/test_synthetic_pipeline.py -v`

Expected: all tests pass; synthetic artifacts include candidates, patterns, best parameters, final patterns, final-test signals, and the five figures.

- [ ] **Step 5: Commit**

```bash
git add candlestick_project/main.py candlestick_project/src/pipeline.py candlestick_project/tests
git commit -m "feat: orchestrate complete candlestick CLI pipeline"
```

### Task 11: Documentation, quality checks, and final verification

**Files:**
- Create: `candlestick_project/README.md`
- Create: `candlestick_project/.gitignore`
- Modify: `candlestick_project/requirements.txt`

- [ ] **Step 1: Write the README execution contract**

````markdown
# Candlestick Patterns Discovering

This project implements the method in `作業一.md` for a fixed 50-stock Taiwan 50 universe.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Tkinter is supplied by the standard Windows Python installer and is not a pip dependency.

## Time split and leakage rules

- 2018-01-01 through 2023-12-31: discovery, scaler fit, candidates, and clustering.
- 2024-01-01 through 2025-12-31: grouped-weight/threshold search and Top 10 selection.
- 2026-01-01 through 2026-12-31: final out-of-sample test only.

The 2026 rows never fit the scaler, form clusters, choose weights or thresholds, relax eligibility, or select the Top 10.

## Commands

```powershell
python main.py --download
python main.py --prepare
python main.py --train
python main.py --validate
python main.py --test
python main.py --gui
python main.py --all
```

`--gui` reads existing Top 10 and test artifacts and never starts training. `--all` runs the data pipeline but does not launch the GUI. The full 1024-by-11 validation grid over 50 stocks can take substantial time.

## Data handling

Raw, unadjusted OHLCV and Yahoo Finance corporate actions are saved in `data/raw`. The corporate-action day, the previous trading day, and the next three trading days are excluded from pattern analysis. Prices are never forward-filled.

Generated data goes to `data/processed` and `data/results`; locked models go to `models`; logs go to `logs`; report figures go to `outputs`.

## Tests

```powershell
python -m pytest -q
```

The tests use synthetic data and do not require network access.

## Investment-result limitations

Historical results do not guarantee future performance. Patterns can overfit and market regimes can change. Simulated results omit fees and slippage. Bearish directional profit is a theoretical short return and does not model Taiwan short-sale availability or restrictions.
````

- [ ] **Step 2: Add repository hygiene**

```gitignore
__pycache__/
.pytest_cache/
.venv/
*.py[cod]
data/raw/*.csv
data/processed/*.csv
data/results/*.csv
models/*.pkl
models/*.joblib
models/*.json
logs/*.log
outputs/**/*.png
```

- [ ] **Step 3: Install and run the complete test suite**

Run: `python -m pip install -r requirements.txt`

Expected: dependency installation succeeds.

Run: `python -m pytest -q`

Expected: all tests pass.

- [ ] **Step 4: Run static import and CLI smoke checks**

Run: `python -m compileall -q src main.py`

Expected: exit code 0.

Run: `python main.py --help`

Expected: exit code 0 and all seven flags are shown.

- [ ] **Step 5: Verify specification coverage**

Run: `rg -n "2018|2023|2024|2025|2026|0\\.05|0\\.60|0\\.30|1\\.4" src config tests README.md`

Expected: the required splits and boundary constants appear in configuration, validation, and tests; no model-selection code reads 2026 rows.

- [ ] **Step 6: Commit**

```bash
git add candlestick_project/README.md candlestick_project/.gitignore candlestick_project/requirements.txt
git commit -m "docs: add candlestick project usage guide"
```

## Final acceptance

- `python -m pytest -q` passes without network access.
- `python -m compileall -q src main.py` exits successfully.
- `python main.py --help` exposes the specified modes.
- Synthetic integration tests produce all specified artifact names.
- No test, scaler fit, cluster fit, parameter search, eligibility relaxation, or Top 10 selection reads 2026 data.
- The formal 50-stock download and long-running grid search remain user-triggered operations for the next phase.
