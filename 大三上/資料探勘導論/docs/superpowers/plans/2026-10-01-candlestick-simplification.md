# Candlestick Project Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current many-module candlestick project with five understandable Python files while preserving the assignment's required download, feature, pattern, validation, 2026-test, chart, and GUI behavior.

**Architecture:** `main.py` orchestrates four public operations implemented by `data_loader.py`, `kline_analysis.py`, and `gui.py`; `config.py` is the single source of fixed data ranges and parameters. Analysis artifacts are plain CSV/JSON so the GUI and report can consume them without importing training internals.

**Tech Stack:** Python 3.11+, yfinance, pandas, NumPy, scikit-learn, matplotlib, Tkinter, pytest.

---

### Task 1: Establish the simplified configuration and data boundary

**Files:**
- Create: `candlestick_project/config.py`
- Create: `candlestick_project/data_loader.py`
- Replace: `candlestick_project/tests/test_core.py`
- Reference: `candlestick_project/config/tickers.txt`
- Reference: `candlestick_project/config/test_tickers.txt`

- [ ] **Step 1: Write failing tests for fixed universes, cleaning, and resilient downloads**

```python
def test_fixed_universes_have_assignment_sizes():
    assert len(STOCK_TICKERS) >= 50
    assert len(TEST_TICKERS) >= 10
    assert set(TEST_TICKERS) <= set(STOCK_TICKERS)


def test_clean_ohlcv_excludes_corporate_action_neighborhood(sample_ohlcv):
    cleaned, summary = clean_ohlcv(sample_ohlcv)
    action_position = cleaned.index.get_loc(pd.Timestamp("2025-01-08"))
    excluded = cleaned.iloc[action_position - 1 : action_position + 4]
    assert not excluded["pattern_eligible"].any()
    assert summary["corporate_action_excluded"] == 5


def test_download_continues_after_one_failure(tmp_path, sample_ohlcv):
    def fake_download(ticker, start, end):
        if ticker == "BAD.TW":
            raise RuntimeError("network failure")
        return sample_ohlcv

    summary = download_market_data(
        tmp_path, ("GOOD.TW", "BAD.TW"), downloader=fake_download, retries=1
    )
    assert summary == {"successful": ["GOOD.TW"], "failed": ["BAD.TW"]}
```

- [ ] **Step 2: Run tests and confirm missing-module failures**

Run: `python -m pytest tests/test_core.py -q`

Expected: collection fails because `config.py` and `data_loader.py` do not exist.

- [ ] **Step 3: Implement `config.py` with explicit constants**

```python
DOWNLOAD_START = "2018-01-01"
DOWNLOAD_END = "2027-01-01"
DISCOVERY_START, DISCOVERY_END = "2018-01-01", "2023-12-31"
VALIDATION_START, VALIDATION_END = "2024-01-01", "2025-12-31"
TEST_START, TEST_END = "2026-01-01", "2026-12-31"

WEIGHT_PRESETS = {
    "equal": (1.0,) * 10,
    "shape_first": (1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.25, 1.25, 0.75, 0.75),
    "position_trend": (1.0, 1.0, 1.0, 0.75, 0.75, 0.75, 1.5, 1.5, 1.0, 1.5),
}
SIMILARITY_THRESHOLDS = (0.6, 0.8, 1.0)
CLUSTER_DISTANCE_THRESHOLD = 1.0
MIN_OCCURRENCES = 10
MIN_ACCURACY = 0.55
```

Copy the existing 50-stock and 10-stock fixed lists into `STOCK_TICKERS` and `TEST_TICKERS` tuples. Do not fetch a changing constituent list at runtime.

- [ ] **Step 4: Implement `data_loader.py`**

Provide these public functions:

```python
def yfinance_downloader(ticker: str, start: str, end: str) -> pd.DataFrame: ...
def download_market_data(output_dir: Path, tickers=STOCK_TICKERS, *, downloader=yfinance_downloader, retries=3) -> dict[str, list[str]]: ...
def clean_ohlcv(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]: ...
def load_clean_stocks(raw_dir: Path) -> dict[str, pd.DataFrame]: ...
```

Use `yf.Ticker(ticker).history(auto_adjust=False, actions=True)`, write one UTF-8 CSV per ticker, normalize timezone-aware indexes, and isolate failures. `clean_ohlcv` must sort, de-duplicate, reject invalid OHLCV, default missing corporate-action columns to zero, and mark the previous/current/next three trading rows ineligible.

- [ ] **Step 5: Run the focused tests**

Run: `python -m pytest tests/test_core.py -q`

Expected: configuration, cleaning, and download tests pass.

- [ ] **Step 6: Commit the data boundary**

```powershell
git add candlestick_project/config.py candlestick_project/data_loader.py candlestick_project/tests/test_core.py
git commit -m "refactor: simplify candlestick data boundary"
```

### Task 2: Consolidate feature, similarity, and pattern discovery logic

**Files:**
- Create: `candlestick_project/kline_analysis.py`
- Modify: `candlestick_project/tests/test_core.py`

- [ ] **Step 1: Add failing tests for the assignment formulas and similarity**

```python
def test_feature_formulas_match_assignment(sample_ohlcv):
    result = build_features(clean_ohlcv(sample_ohlcv)[0])
    row = result.loc["2025-01-08"]
    assert row["upper"] == pytest.approx(
        (row["High"] - max(row["Open"], row["Close"])) / row["Close"] * 100
    )
    assert row["body"] == pytest.approx(
        (row["Close"] - row["Open"]) / row["Close"] * 100
    )


def test_weighted_distance_and_threshold_rules():
    assert weighted_distance([1, 2], [1, 2], [1, 1]) == 0
    assert weighted_distance([1, 0], [0, 0], [2, 1]) > weighted_distance(
        [1, 0], [0, 0], [1, 1]
    )
    assert is_match(0.8, 0.8)
```

- [ ] **Step 2: Run the focused tests and confirm missing imports**

Run: `python -m pytest tests/test_core.py -q`

Expected: fails because `kline_analysis.py` does not exist.

- [ ] **Step 3: Implement feature and distance primitives**

Expose:

```python
FEATURE_COLUMNS = (
    "upper", "lower", "body", "prev_upper", "prev_lower", "prev_body",
    "open_style", "close_style", "volume_feature", "trend",
)

def build_features(frame: pd.DataFrame) -> pd.DataFrame: ...
def weighted_distance(vector_a, vector_b, weights) -> float: ...
def pairwise_weighted_distances(patterns, rows, weights) -> np.ndarray: ...
def is_match(distance: float, threshold: float) -> bool: ...
```

Use the exact formulas in the assignment. `return_3d` is a label only. Validate that weights are finite, non-negative, and match the vector width.

- [ ] **Step 4: Implement discovery and compact validation**

Expose:

```python
def discover_patterns(feature_rows: pd.DataFrame) -> tuple[StandardScaler, pd.DataFrame]: ...
def backtest_patterns(patterns, rows, weights, threshold) -> tuple[pd.DataFrame, pd.DataFrame]: ...
def choose_parameters(patterns, validation_rows) -> dict[str, object]: ...
def select_top_patterns(metrics, patterns, weights) -> pd.DataFrame: ...
```

`discover_patterns` must fit the scaler only on valid 2018–2023 features, create strict `return_3d > .05` / `< -.05` candidates, cluster each direction with fixed-threshold `AgglomerativeClustering`, and store raw plus standardized centroids. `choose_parameters` must evaluate only the three named presets and three similarity thresholds. Parameter ranking is mean Top-10 directional profit, then accuracy, occurrence, then the stricter threshold. `select_top_patterns` first applies occurrence/accuracy thresholds; if fewer than 10 qualify, it fills by the same score and emits a warning.

- [ ] **Step 5: Run core math tests**

Run: `python -m pytest tests/test_core.py -q`

Expected: all feature, distance, discovery-boundary, and selection tests pass.

- [ ] **Step 6: Commit consolidated analysis primitives**

```powershell
git add candlestick_project/kline_analysis.py candlestick_project/tests/test_core.py
git commit -m "refactor: consolidate candlestick analysis"
```

### Task 3: Add end-to-end analysis, 2026 testing, and figures

**Files:**
- Modify: `candlestick_project/kline_analysis.py`
- Modify: `candlestick_project/tests/test_core.py`

- [ ] **Step 1: Add a failing synthetic pipeline test**

```python
def test_synthetic_project_writes_locked_model_and_results(tmp_path, synthetic_stocks):
    write_raw_stocks(tmp_path / "data" / "raw", synthetic_stocks)
    summary = analyze_project(tmp_path)
    assert summary["pattern_count"] >= 20
    assert (tmp_path / "data/results/final_patterns.json").exists()
    assert (tmp_path / "data/results/top10_bullish.csv").exists()
    assert (tmp_path / "data/results/top10_bearish.csv").exists()
```

- [ ] **Step 2: Implement project-level operations**

Expose:

```python
def analyze_project(project_root: Path) -> dict[str, object]: ...
def test_project(project_root: Path) -> dict[str, float | int]: ...
def generate_figures(project_root: Path) -> list[Path]: ...
```

`analyze_project` loads local raw CSV files, creates per-ticker features, performs discovery and validation, and writes Top-10 CSV plus a single JSON model containing scaler mean/scale, weights, threshold, and patterns. `test_project` must reject rows outside 2026, require at least 10 configured tickers with valid rows, preserve individual pattern hits, exclude same-day bullish/bearish conflicts from simulated trades, and write signal/pattern/stock/overall results. Figure creation writes the four filenames in the design and never mutates input frames.

- [ ] **Step 3: Run the synthetic pipeline test**

Run: `python -m pytest tests/test_core.py -q`

Expected: the synthetic pipeline and all earlier tests pass without network access.

- [ ] **Step 4: Commit project-level analysis**

```powershell
git add candlestick_project/kline_analysis.py candlestick_project/tests/test_core.py
git commit -m "feat: add simplified analysis pipeline"
```

### Task 4: Replace the CLI and GUI with simple public interfaces

**Files:**
- Replace: `candlestick_project/main.py`
- Create: `candlestick_project/gui.py`
- Modify: `candlestick_project/tests/test_core.py`

- [ ] **Step 1: Add failing CLI and GUI-helper tests**

```python
def test_cli_all_runs_download_analyze_and_test(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(main, "download_project", lambda root: calls.append("download"))
    monkeypatch.setattr(main, "analyze_project", lambda root: calls.append("analyze"))
    monkeypatch.setattr(main, "test_project", lambda root: calls.append("test"))
    assert main.run(["--all"], project_root=tmp_path) == 0
    assert calls == ["download", "analyze", "test"]


def test_relative_candles_produces_two_valid_ohlc_rows():
    candles = relative_candles([1, 1, 2, 1, 1, -1, 0.5, 1, 0.2, 0.1])
    assert len(candles) == 2
    assert all(high >= max(open_, close) and low <= min(open_, close)
               for open_, high, low, close in candles)
```

- [ ] **Step 2: Implement the CLI**

`main.py` imports only `config`, `data_loader`, `kline_analysis`, and `gui`. It exposes `parser()` and `run(argv=None, project_root=None)`. `--all` runs download, analyze, and test in order; `--gui` never triggers those stages.

- [ ] **Step 3: Implement the read-only Tkinter GUI**

`gui.py` exposes:

```python
def load_gui_records(project_root: Path) -> pd.DataFrame: ...
def relative_candles(features: list[float]) -> list[tuple[float, float, float, float]]: ...
def launch_gui(project_root: Path) -> None: ...
```

The GUI displays bullish and bearish tabs, validation occurrence/accuracy/profit, 2026 matches/accuracy, and the reconstructed previous/current candle. Missing 2026 results are displayed as blank values; missing Top-10 files raise `FileNotFoundError("Run --analyze before --gui")`.

- [ ] **Step 4: Run CLI and GUI-helper tests**

Run: `python -m pytest tests/test_core.py -q`

Expected: all tests pass without opening a GUI window.

- [ ] **Step 5: Commit CLI and GUI**

```powershell
git add candlestick_project/main.py candlestick_project/gui.py candlestick_project/tests/test_core.py
git commit -m "refactor: simplify candlestick CLI and GUI"
```

### Task 5: Remove the replaced structure and rewrite usage documentation

**Files:**
- Replace: `candlestick_project/README.md`
- Modify: `candlestick_project/requirements.txt`
- Delete: `candlestick_project/src/`
- Delete: old files under `candlestick_project/tests/` except `test_core.py`
- Delete: `candlestick_project/config/settings.yaml`
- Delete: `candlestick_project/config/tickers.txt`
- Delete: `candlestick_project/config/test_tickers.txt`

- [ ] **Step 1: Rewrite README around the five-file structure**

Document installation and exactly these commands:

```powershell
python main.py --download
python main.py --analyze
python main.py --test
python main.py --gui
python main.py --all
python -m pytest -q
```

Explain the three time periods, the three weight presets, output paths, and investment limitations in plain Traditional Chinese. Remove claims about the 11,264-combination grid search.

- [ ] **Step 2: Keep only required dependencies**

`requirements.txt` must contain `yfinance`, `pandas`, `numpy`, `scikit-learn`, `matplotlib`, and `pytest`. Remove `joblib` and `PyYAML` because the simplified implementation does not import them.

- [ ] **Step 3: Delete only confirmed replaced code**

Before deletion, run:

```powershell
rg -n "from src|import src|settings.yaml|config/tickers|config/test_tickers" candlestick_project
```

Expected: only obsolete files refer to those paths. Delete `src/`, all former test modules, and three obsolete config files while preserving `data/`, `outputs/`, `logs/`, and any user-generated results.

- [ ] **Step 4: Run all tests and static import checks**

Run:

```powershell
python -m pytest -q
python -m compileall -q main.py config.py data_loader.py kline_analysis.py gui.py
python main.py --help
```

Expected: tests pass, compileall is silent, and help lists five modes.

- [ ] **Step 5: Commit the cleanup**

```powershell
git add -A candlestick_project
git commit -m "refactor: finish simplified candlestick project"
```

### Task 6: Final verification and scope audit

**Files:**
- Verify: `candlestick_project/`

- [ ] **Step 1: Confirm exactly five main Python files**

Run: `Get-ChildItem -Path . -Filter *.py | Select-Object -ExpandProperty Name`

Expected: `config.py`, `data_loader.py`, `gui.py`, `kline_analysis.py`, and `main.py`.

- [ ] **Step 2: Confirm no obsolete imports or parameter-search claims remain**

Run:

```powershell
rg -n "from src|import src|settings.yaml|11264|11,264|optimize_similarity" .
```

Expected: no matches outside historical design/plan documents.

- [ ] **Step 3: Run the complete offline verification suite again**

Run:

```powershell
python -m pytest -q
python -m compileall -q main.py config.py data_loader.py kline_analysis.py gui.py
python main.py --help
git status --short
```

Expected: tests pass, imports compile, help succeeds, and Git status contains only the intended candlestick simplification changes plus the user's pre-existing unrelated HW3 changes and `作業一.md`.
