# Candlestick Match Coverage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Select candlestick patterns with real validation coverage while preserving the 2026 holdout boundary.

**Architecture:** Expand configuration grids, pass clustering distance explicitly through discovery, reuse each weighted distance matrix across all similarity thresholds, and rank parameter combinations by qualified coverage before profit. Final selection admits only patterns meeting `occurrence >= 5` and `accuracy >= 0.55`.

**Tech Stack:** Python 3.11+, pandas, NumPy, scikit-learn, pytest

---

### Task 1: Lock the new configuration contract

**Files:**
- Modify: `candlestick_project/config.py`
- Test: `candlestick_project/tests/test_core.py`

- [ ] **Step 1: Write the failing configuration test**

```python
def test_match_coverage_search_configuration():
    from config import (
        CLUSTER_DISTANCE_THRESHOLDS,
        MIN_ACCURACY,
        MIN_OCCURRENCES,
        SIMILARITY_THRESHOLDS,
    )

    assert SIMILARITY_THRESHOLDS == tuple(round(0.4 + index * 0.1, 1) for index in range(11))
    assert CLUSTER_DISTANCE_THRESHOLDS == (1.0, 1.25, 1.5, 2.0)
    assert MIN_OCCURRENCES == 5
    assert MIN_ACCURACY == pytest.approx(0.55)
```

- [ ] **Step 2: Run the test and confirm it fails**

Run: `python -m pytest tests/test_core.py::test_match_coverage_search_configuration -q`
Expected: FAIL because `CLUSTER_DISTANCE_THRESHOLDS` is absent and the existing threshold grid is incomplete.

- [ ] **Step 3: Implement the constants**

```python
SIMILARITY_THRESHOLDS = (0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4)
CLUSTER_DISTANCE_THRESHOLDS = (1.0, 1.25, 1.5, 2.0)
CLUSTER_DISTANCE_THRESHOLD = CLUSTER_DISTANCE_THRESHOLDS[0]
MIN_OCCURRENCES = 5
MIN_ACCURACY = 0.55
```

- [ ] **Step 4: Run the focused test**

Run: `python -m pytest tests/test_core.py::test_match_coverage_search_configuration -q`
Expected: PASS.

### Task 2: Make validation summaries coverage-first

**Files:**
- Modify: `candlestick_project/kline_analysis.py`
- Test: `candlestick_project/tests/test_core.py`

- [ ] **Step 1: Replace the fill-based summary tests with coverage tests**

Add tests that assert `_parameter_summary()` reports bullish/bearish qualified counts, `min_qualified_patterns`, `has_ten_each`, and aggregates only qualified Top-10 rows. Add a ranking test where a lower-profit configuration with ten qualified patterns per direction defeats a high-profit configuration with only one qualified pattern per direction.

- [ ] **Step 2: Run the focused tests and confirm failure**

Run: `python -m pytest tests/test_core.py -k "parameter_summary or parameter_search" -q`
Expected: FAIL because the new fields and coverage-first ranking do not exist.

- [ ] **Step 3: Implement `_parameter_summary()` and `_rank_parameter_search()`**

`_parameter_summary()` must filter with `MIN_OCCURRENCES` and `MIN_ACCURACY`, take at most ten qualified patterns from each direction, and return:

```python
{
    "parameter_set_score": mean_directional_profit,
    "mean_accuracy": mean_accuracy,
    "total_occurrence": selected_occurrence,
    "qualified_patterns": bullish_count + bearish_count,
    "qualified_bullish_patterns": bullish_count,
    "qualified_bearish_patterns": bearish_count,
    "min_qualified_patterns": min(bullish_count, bearish_count),
    "has_ten_each": int(bullish_count >= 10 and bearish_count >= 10),
}
```

`_rank_parameter_search()` sorts by the design's coverage-first ordering and returns a reset-index DataFrame.

- [ ] **Step 4: Run the focused tests**

Run: `python -m pytest tests/test_core.py -k "parameter_summary or parameter_search" -q`
Expected: PASS.

### Task 3: Reuse distance matrices across similarity thresholds

**Files:**
- Modify: `candlestick_project/kline_analysis.py`
- Test: `candlestick_project/tests/test_core.py`

- [ ] **Step 1: Add a behavior test for `_pattern_metrics_from_distances()`**

Use two patterns, two rows, and a fixed distance matrix. Assert that changing the threshold changes occurrence and success counts without recomputing features.

- [ ] **Step 2: Run the focused test and confirm failure**

Run: `python -m pytest tests/test_core.py::test_pattern_metrics_from_precomputed_distances -q`
Expected: FAIL because the helper does not exist.

- [ ] **Step 3: Extract metric calculation and update `choose_parameters()`**

Create `_pattern_metrics_from_distances(patterns, rows, distances, threshold)` with the same metric schema as `backtest_patterns()`. In `choose_parameters()`, compute `pairwise_weighted_distances()` once per weight preset, reuse it for all similarity thresholds, and rank with `_rank_parameter_search()`.

- [ ] **Step 4: Keep final backtesting behavior compatible**

Update `backtest_patterns()` to use the extracted metric helper while retaining signal rows and the existing CSV schema.

- [ ] **Step 5: Run distance and backtest tests**

Run: `python -m pytest tests/test_core.py -k "distance or backtest or parameter" -q`
Expected: PASS.

### Task 4: Search clustering thresholds without 2026 leakage

**Files:**
- Modify: `candlestick_project/kline_analysis.py`
- Test: `candlestick_project/tests/test_core.py`

- [ ] **Step 1: Add clustering-threshold propagation tests**

Assert that `discover_patterns(feature_rows, cluster_distance_threshold=1.5)` passes `1.5` to both bullish and bearish `_cluster_direction()` calls. Update the analyze-project contract test to return coverage fields and assert `cluster_distance_threshold` is saved in the final JSON and summary.

- [ ] **Step 2: Run the tests and confirm failure**

Run: `python -m pytest tests/test_core.py -k "cluster_distance or analyze_project" -q`
Expected: FAIL because discovery has a fixed threshold and the model does not record it.

- [ ] **Step 3: Pass clustering distance through discovery**

Add a `cluster_distance_threshold` argument to `_cluster_direction()` and `discover_patterns()`, defaulting to `CLUSTER_DISTANCE_THRESHOLD` for compatibility.

- [ ] **Step 4: Search all clustering thresholds in `analyze_project()`**

For each value in `CLUSTER_DISTANCE_THRESHOLDS`, discover patterns and run validation parameter search. Combine all search rows with a `cluster_distance_threshold` column, rank globally with `_rank_parameter_search()`, then rediscover/use the winning candidate set for final metrics and selection. Do not read 2026 data.

- [ ] **Step 5: Persist the selected clustering threshold**

Write it to `validation_results.csv`, `final_patterns.json`, and the returned analysis summary.

- [ ] **Step 6: Run focused tests**

Run: `python -m pytest tests/test_core.py -k "cluster_distance or analyze_project" -q`
Expected: PASS.

### Task 5: Forbid unqualified Top-10 fillers

**Files:**
- Modify: `candlestick_project/kline_analysis.py`
- Test: `candlestick_project/tests/test_core.py`

- [ ] **Step 1: Add a failing selection test**

Build metrics with nine qualified and one unqualified pattern per direction. Assert `select_top_patterns()` raises `ValueError` containing both direction and qualified count.

- [ ] **Step 2: Run the test and confirm failure**

Run: `python -m pytest tests/test_core.py::test_select_top_patterns_rejects_unqualified_fillers -q`
Expected: FAIL because the current implementation fills by rank.

- [ ] **Step 3: Restrict selection candidates**

Filter candidates before ranking. Raise when fewer than ten qualify. Retain duplicate avoidance and allow only other qualified patterns to fill slots after duplicate filtering.

- [ ] **Step 4: Run the focused test**

Run: `python -m pytest tests/test_core.py::test_select_top_patterns_rejects_unqualified_fillers -q`
Expected: PASS.

### Task 6: Verify the implementation and regenerate results

**Files:**
- Potentially update generated files under `candlestick_project/data/results/` and `candlestick_project/outputs/figures/`

- [ ] **Step 1: Run the complete test suite**

Run: `python -m pytest -q`
Expected: all tests pass.

- [ ] **Step 2: Run syntax compilation and CLI smoke test**

Run: `python -m compileall -q main.py config.py data_loader.py kline_analysis.py gui.py`
Expected: exit code 0.

Run: `python main.py --help`
Expected: exit code 0 with all supported modes.

- [ ] **Step 3: Run analysis from existing local data**

Run: `python main.py --analyze`
Expected: either a locked model with ten qualified patterns per direction or a precise qualification error without replacing valid outputs.

- [ ] **Step 4: Run the locked 2026 test when analysis succeeds**

Run: `python main.py --test`
Expected: exit code 0 and refreshed `test_2026_*` outputs.

- [ ] **Step 5: Inspect output coverage**

Read `validation_results.csv`, `top10_bullish.csv`, `top10_bearish.csv`, and `test_2026_pattern_metrics.csv`. Confirm selected patterns meet the qualification rules and report the number of 2026 matches without using that number to change parameters.

