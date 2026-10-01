from __future__ import annotations

from pathlib import Path
import json

import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

import kline_analysis as analysis
from config import STOCK_TICKERS, TEST_TICKERS
from data_loader import clean_ohlcv, download_market_data, load_clean_stocks
from kline_analysis import (
    FEATURE_COLUMNS,
    build_features,
    discover_patterns,
    is_match,
    weighted_distance,
)


def sample_ohlcv() -> pd.DataFrame:
    dates = pd.date_range("2025-01-01", periods=12, freq="D")
    frame = pd.DataFrame(
        {
            "Open": [100 + index for index in range(12)],
            "High": [103 + index for index in range(12)],
            "Low": [98 + index for index in range(12)],
            "Close": [101 + index for index in range(12)],
            "Volume": [1000 + index * 10 for index in range(12)],
            "Dividends": [0.0] * 7 + [1.0] + [0.0] * 4,
            "Stock Splits": [0.0] * 12,
        },
        index=dates,
    )
    frame.index.name = "Date"
    return frame


def test_fixed_universes_have_assignment_sizes():
    assert len(STOCK_TICKERS) >= 50
    assert len(TEST_TICKERS) >= 10
    assert set(TEST_TICKERS) <= set(STOCK_TICKERS)


def test_match_coverage_search_configuration():
    from config import (
        CLUSTER_DISTANCE_THRESHOLDS,
        MIN_ACCURACY,
        MIN_OCCURRENCES,
        SIMILARITY_THRESHOLDS,
    )

    expected_thresholds = tuple(round(0.4 + index * 0.1, 1) for index in range(17))
    assert SIMILARITY_THRESHOLDS == expected_thresholds
    assert CLUSTER_DISTANCE_THRESHOLDS == (1.0, 1.25, 1.5, 2.0)
    assert MIN_OCCURRENCES == 3
    assert MIN_ACCURACY == pytest.approx(0.55)


def test_clean_ohlcv_excludes_corporate_action_neighborhood():
    cleaned, summary = clean_ohlcv(sample_ohlcv())
    action_position = cleaned.index.get_loc(pd.Timestamp("2025-01-08"))
    excluded = cleaned.iloc[action_position - 1 : action_position + 4]

    assert not excluded["pattern_eligible"].any()
    assert summary["corporate_action_excluded"] == 5


def test_download_continues_after_one_failure(tmp_path: Path):
    def fake_download(ticker: str, start: str, end: str) -> pd.DataFrame:
        if ticker == "BAD.TW":
            raise RuntimeError("network failure")
        return sample_ohlcv()

    summary = download_market_data(
        tmp_path,
        ("GOOD.TW", "BAD.TW"),
        downloader=fake_download,
        retries=1,
    )

    assert summary == {"successful": ["GOOD.TW"], "failed": ["BAD.TW"]}
    assert (tmp_path / "GOOD.TW.csv").exists()
    assert not (tmp_path / "BAD.TW.csv").exists()


def test_loading_fixed_universe_ignores_stale_csv(tmp_path: Path):
    sample_ohlcv().to_csv(tmp_path / "GOOD.TW.csv")
    sample_ohlcv().to_csv(tmp_path / "STALE.TW.csv")

    stocks = load_clean_stocks(tmp_path, tickers=("GOOD.TW",))

    assert set(stocks) == {"GOOD.TW"}


def test_feature_formulas_match_assignment():
    result = build_features(clean_ohlcv(sample_ohlcv())[0])
    row = result.loc["2025-01-08"]
    previous = result.loc["2025-01-07"]

    assert row["upper"] == pytest.approx(
        (row["High"] - max(row["Open"], row["Close"])) / row["Close"] * 100
    )
    assert row["lower"] == pytest.approx(
        (min(row["Open"], row["Close"]) - row["Low"]) / row["Close"] * 100
    )
    assert row["body"] == pytest.approx(
        (row["Close"] - row["Open"]) / row["Close"] * 100
    )
    assert row["prev_upper"] == pytest.approx(previous["upper"])
    assert row["prev_lower"] == pytest.approx(previous["lower"])
    assert row["prev_body"] == pytest.approx(previous["body"])
    assert row["open_style"] == pytest.approx(
        (row["Open"] - previous["Close"]) / row["Close"] * 100
    )
    assert row["close_style"] == pytest.approx(
        (row["Close"] - previous["Close"]) / row["Close"] * 100
    )
    expected_mean_volume = result.loc["2025-01-04":"2025-01-08", "Volume"].mean()
    assert row["volume_feature"] == pytest.approx(
        (row["Volume"] - expected_mean_volume) / row["Volume"]
    )
    assert row["trend"] == pytest.approx(
        (result.iloc[5]["Close"] - result.iloc[0]["Close"])
        / result.iloc[0]["Close"]
    )
    label_row = result.loc["2025-01-05"]
    future_close = result.loc["2025-01-08", "Close"]
    assert label_row["return_3d"] == pytest.approx(
        (future_close - label_row["Close"]) / label_row["Close"]
    )


def test_weighted_distance_and_threshold_rules():
    assert weighted_distance([1, 2], [1, 2], [1, 1]) == 0
    assert weighted_distance([1, 0], [0, 0], [2, 1]) > weighted_distance(
        [1, 0], [0, 0], [1, 1]
    )
    assert is_match(0.8, 0.8)


def test_parameter_summary_only_uses_qualified_patterns():
    metrics = pd.DataFrame(
        [
            {
                "pattern_id": "BULL-001",
                "direction": "bullish",
                "occurrence_count": 20,
                "accuracy": 0.8,
                "average_directional_profit": 0.20,
            },
            {
                "pattern_id": "BEAR-001",
                "direction": "bearish",
                "occurrence_count": 2,
                "accuracy": 0.4,
                "average_directional_profit": -0.10,
            },
        ]
    )

    summary = analysis._parameter_summary(metrics)

    assert summary["qualified_patterns"] == 1
    assert summary["qualified_bullish_patterns"] == 1
    assert summary["qualified_bearish_patterns"] == 0
    assert summary["min_qualified_patterns"] == 0
    assert summary["has_ten_each"] == 0
    assert summary["total_occurrence"] == 20


def test_parameter_search_ranking_prefers_qualified_coverage():
    search = pd.DataFrame(
        [
            {
                "weight_preset": "high-profit-low-coverage",
                "similarity_threshold": 0.6,
                "cluster_distance_threshold": 1.0,
                "has_ten_each": 0,
                "min_qualified_patterns": 1,
                "qualified_patterns": 2,
                "total_occurrence": 10,
                "parameter_set_score": 0.50,
                "mean_accuracy": 1.0,
            },
            {
                "weight_preset": "adequate-coverage",
                "similarity_threshold": 1.2,
                "cluster_distance_threshold": 1.5,
                "has_ten_each": 1,
                "min_qualified_patterns": 10,
                "qualified_patterns": 20,
                "total_occurrence": 150,
                "parameter_set_score": 0.08,
                "mean_accuracy": 0.65,
            },
        ]
    )

    ranked = analysis._rank_parameter_search(search)

    assert ranked.iloc[0]["weight_preset"] == "adequate-coverage"


def test_pattern_metrics_from_precomputed_distances():
    patterns = pd.DataFrame(
        {
            "pattern_id": ["BULL-001", "BEAR-001"],
            "direction": ["bullish", "bearish"],
        }
    )
    rows = pd.DataFrame({"return_3d": [0.08, -0.07]})
    distances = np.asarray([[0.5, 1.2], [1.1, 0.6]])

    strict = analysis._pattern_metrics_from_distances(
        patterns, rows, distances, threshold=0.8
    )
    loose = analysis._pattern_metrics_from_distances(
        patterns, rows, distances, threshold=1.2
    )

    assert strict["occurrence_count"].tolist() == [1, 1]
    assert strict["success_count"].tolist() == [1, 1]
    assert loose["occurrence_count"].tolist() == [2, 2]


def test_select_top_patterns_rejects_unqualified_fillers():
    records = []
    metrics = []
    for direction in ("bullish", "bearish"):
        prefix = "BULL" if direction == "bullish" else "BEAR"
        for index in range(10):
            pattern_id = f"{prefix}-{index:03d}"
            records.append(
                {
                    "pattern_id": pattern_id,
                    "direction": direction,
                    "centroid_z": [float(index)] * 10,
                }
            )
            metrics.append(
                {
                    "pattern_id": pattern_id,
                    "direction": direction,
                    "occurrence_count": 3 if index < 9 else 2,
                    "accuracy": 0.60,
                    "average_directional_profit": 0.05,
                }
            )

    with pytest.raises(ValueError, match="9 qualified bullish"):
        analysis.select_top_patterns(
            pd.DataFrame(metrics), pd.DataFrame(records), [1.0] * 10
        )


def test_discovery_passes_cluster_distance_to_both_directions(monkeypatch):
    calls: list[tuple[str, float]] = []

    def fake_cluster(candidates, direction, scaler, cluster_distance_threshold):
        calls.append((direction, cluster_distance_threshold))
        return []

    monkeypatch.setattr(analysis, "_cluster_direction", fake_cluster)
    feature_rows = pd.DataFrame(
        {
            "ticker": ["UP.TW", "DOWN.TW"],
            "date": [pd.Timestamp("2023-01-03"), pd.Timestamp("2023-01-04")],
            "return_3d_date": [
                pd.Timestamp("2023-01-06"),
                pd.Timestamp("2023-01-09"),
            ],
            "return_3d": [0.08, -0.08],
            "pattern_eligible": [True, True],
            **{
                name: [float(index), float(index + 1)]
                for index, name in enumerate(FEATURE_COLUMNS)
            },
        }
    )

    with pytest.raises(ValueError, match="Discovery found no"):
        discover_patterns(feature_rows, cluster_distance_threshold=1.5)

    assert calls == [("bullish", 1.5), ("bearish", 1.5)]




def test_conflicts_are_marked_but_excluded_from_trade_metrics():
    signals = pd.DataFrame(
        [
            {
                "pattern_id": "BULL-001",
                "direction": "bullish",
                "ticker": "2330.TW",
                "date": pd.Timestamp("2026-01-05"),
                "return_3d": 0.01,
                "distance": 0.2,
                "success": False,
                "directional_profit": 0.01,
            },
            {
                "pattern_id": "BEAR-001",
                "direction": "bearish",
                "ticker": "2330.TW",
                "date": pd.Timestamp("2026-01-05"),
                "return_3d": 0.01,
                "distance": 0.3,
                "success": False,
                "directional_profit": -0.01,
            },
            {
                "pattern_id": "BULL-002",
                "direction": "bullish",
                "ticker": "2454.TW",
                "date": pd.Timestamp("2026-01-06"),
                "return_3d": 0.08,
                "distance": 0.2,
                "success": True,
                "directional_profit": 0.08,
            },
        ]
    )

    annotated = analysis._mark_conflicts(signals)
    trades = analysis._trade_level_signals(annotated)

    assert annotated.loc[annotated["ticker"].eq("2330.TW"), "conflict_signal"].all()
    assert len(trades) == 1
    assert trades.iloc[0]["ticker"] == "2454.TW"


def test_empty_backtest_signals_keep_csv_schema():
    patterns = pd.DataFrame(
        [
            {
                "pattern_id": "BULL-001",
                "direction": "bullish",
                "centroid_z": [0.0] * 10,
            }
        ]
    )
    rows = pd.DataFrame(
        [
            {
                "ticker": "2330.TW",
                "date": pd.Timestamp("2026-01-05"),
                "return_3d": 0.01,
                "features_z": [10.0] * 10,
            }
        ]
    )

    _, signals = analysis.backtest_patterns(patterns, rows, [1.0] * 10, 0.1)

    assert signals.empty
    assert list(signals.columns) == list(analysis.SIGNAL_COLUMNS)


def test_valid_2026_rows_must_cover_all_fixed_tickers():
    rows = pd.DataFrame({"ticker": list(TEST_TICKERS[:-1])})

    with pytest.raises(ValueError, match="valid 2026 rows"):
        analysis._validate_test_rows(rows)


def test_locked_model_requires_ten_unique_patterns_per_direction():
    patterns = pd.DataFrame(
        {
            "pattern_id": [f"BULL-{index:03d}" for index in range(20)],
            "direction": ["bullish"] * 20,
            "centroid_z": [[0.0] * 10 for _ in range(20)],
        }
    )

    with pytest.raises(ValueError, match="10 unique bullish and 10 unique bearish"):
        analysis._validate_locked_patterns(patterns)


def test_discovery_scaler_ignores_2026_rows():
    rows = []
    for index, date in enumerate(pd.date_range("2023-01-01", periods=4)):
        row = {name: float(index) for name in FEATURE_COLUMNS}
        row.update(
            {
                "ticker": "TEST.TW",
                "date": date,
                "return_3d_date": date + pd.Timedelta(days=3),
                "return_3d": 0.08 if index < 2 else -0.08,
                "pattern_eligible": True,
            }
        )
        rows.append(row)
    future = rows[0].copy()
    future.update(
        {
            "date": pd.Timestamp("2026-01-05"),
            "return_3d_date": pd.Timestamp("2026-01-08"),
            **{name: 999.0 for name in FEATURE_COLUMNS},
        }
    )
    scaler, patterns = discover_patterns(pd.DataFrame([*rows, future]))

    assert scaler.mean_[0] == pytest.approx(1.5)
    assert set(patterns["direction"]) == {"bullish", "bearish"}


def test_analyze_project_writes_locked_model(monkeypatch, tmp_path: Path):
    from config import CLUSTER_DISTANCE_THRESHOLDS

    feature_rows = pd.DataFrame(
        {
            "ticker": ["TEST.TW"],
            "date": [pd.Timestamp("2024-01-08")],
            "return_3d_date": [pd.Timestamp("2024-01-11")],
            "return_3d": [0.08],
            "pattern_eligible": [True],
            **{name: [0.0] for name in FEATURE_COLUMNS},
        }
    )
    patterns = pd.DataFrame(
        [
            {
                "pattern_id": f"{'BULL' if index < 10 else 'BEAR'}-{index + 1:03d}",
                "direction": "bullish" if index < 10 else "bearish",
                "cluster_size": 1,
                "centroid_z": [float(index)] * 10,
                "centroid_raw": [float(index)] * 10,
                "source_candidates": [f"TEST.TW:2023-01-{index + 1:02d}"],
            }
            for index in range(20)
        ]
    )
    metrics = patterns[["pattern_id", "direction"]].copy()
    metrics["occurrence_count"] = 20
    metrics["success_count"] = 15
    metrics["accuracy"] = 0.75
    metrics["average_return_3d"] = 0.06
    metrics["average_directional_profit"] = 0.06
    scaler = StandardScaler().fit(np.asarray([[0.0] * 10, [2.0] * 10]))
    stale_result = tmp_path / "data/results/test_2026_pattern_metrics.csv"
    stale_result.parent.mkdir(parents=True)
    stale_result.write_text("pattern_id,test_accuracy\nOLD,1.0\n", encoding="utf-8")
    searched_cluster_thresholds: list[float] = []

    monkeypatch.setattr(
        analysis,
        "load_clean_stocks",
        lambda path, tickers=None, logger=None: {"TEST.TW": sample_ohlcv()},
    )
    monkeypatch.setattr(analysis, "combine_feature_stocks", lambda stocks: feature_rows)
    def fake_discover(rows, cluster_distance_threshold):
        searched_cluster_thresholds.append(cluster_distance_threshold)
        return scaler, patterns

    monkeypatch.setattr(analysis, "discover_patterns", fake_discover)
    monkeypatch.setattr(
        analysis,
        "evaluation_rows",
        lambda rows, fitted_scaler, start, end: feature_rows.assign(
            features_z=[[0.0] * 10]
        ),
    )
    def fake_choose_parameters(
        pattern_rows, validation, cluster_distance_threshold
    ):
        result = {
            "weight_preset": "equal",
            "weights": [1.0] * 10,
            "similarity_threshold": 0.8,
            "cluster_distance_threshold": cluster_distance_threshold,
            "has_ten_each": 1,
            "min_qualified_patterns": 10,
            "qualified_patterns": 20,
            "qualified_bullish_patterns": 10,
            "qualified_bearish_patterns": 10,
            "total_occurrence": 400,
            "parameter_set_score": 0.06,
            "mean_accuracy": 0.75,
        }
        result["search_results"] = [result.copy()]
        return result

    monkeypatch.setattr(analysis, "choose_parameters", fake_choose_parameters)
    monkeypatch.setattr(
        analysis,
        "backtest_patterns",
        lambda pattern_rows, validation, weights, threshold: (metrics, pd.DataFrame()),
    )
    monkeypatch.setattr(
        analysis,
        "select_top_patterns",
        lambda metric_rows, pattern_rows, weights: pattern_rows.merge(
            metric_rows, on=["pattern_id", "direction"]
        ),
    )
    monkeypatch.setattr(analysis, "generate_figures", lambda root: [])

    summary = analysis.analyze_project(tmp_path)

    assert summary["selected_patterns"] == 20
    assert summary["cluster_distance_threshold"] == 1.0
    assert searched_cluster_thresholds == list(CLUSTER_DISTANCE_THRESHOLDS)
    assert (tmp_path / "data/results/final_patterns.json").exists()
    assert (tmp_path / "data/results/top10_bullish.csv").exists()
    assert (tmp_path / "data/results/top10_bearish.csv").exists()
    assert not stale_result.exists()
    model = json.loads(
        (tmp_path / "data/results/final_patterns.json").read_text(encoding="utf-8")
    )
    assert model["cluster_distance_threshold"] == 1.0


def test_final_test_requires_all_fixed_tickers(monkeypatch, tmp_path: Path):
    result_dir = tmp_path / "data" / "results"
    result_dir.mkdir(parents=True)
    (result_dir / "final_patterns.json").write_text(
        json.dumps(
            {
                "scaler": {
                    "mean": [0.0] * 10,
                    "scale": [1.0] * 10,
                    "sample_count": 10,
                },
                "weights": [1.0] * 10,
                "similarity_threshold": 0.8,
                "patterns": [],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        analysis,
        "load_clean_stocks",
        lambda path, tickers=None, logger=None: {TEST_TICKERS[0]: sample_ohlcv()},
    )

    with pytest.raises(ValueError, match="requires all 10 fixed tickers"):
        analysis.test_project(tmp_path)


def test_final_test_writes_conflicts_and_all_stock_rows(monkeypatch, tmp_path: Path):
    result_dir = tmp_path / "data" / "results"
    result_dir.mkdir(parents=True)
    patterns = [
        {
            "pattern_id": f"BULL-{index:03d}",
            "direction": "bullish",
            "centroid_z": [0.0] * 10,
        }
        for index in range(10)
    ] + [
        {
            "pattern_id": f"BEAR-{index:03d}",
            "direction": "bearish",
            "centroid_z": [0.0] * 10,
        }
        for index in range(10)
    ]
    (result_dir / "final_patterns.json").write_text(
        json.dumps(
            {
                "scaler": {
                    "mean": [0.0] * 10,
                    "scale": [1.0] * 10,
                    "sample_count": 10,
                },
                "weights": [1.0] * 10,
                "similarity_threshold": 0.8,
                "patterns": patterns,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        analysis,
        "load_clean_stocks",
        lambda path, tickers=None, logger=None: {
            ticker: sample_ohlcv() for ticker in TEST_TICKERS
        },
    )
    monkeypatch.setattr(analysis, "combine_feature_stocks", lambda stocks: pd.DataFrame())
    monkeypatch.setattr(
        analysis,
        "evaluation_rows",
        lambda feature_rows, scaler, start, end: pd.DataFrame(
            {"ticker": list(TEST_TICKERS)}
        ),
    )
    metrics = pd.DataFrame(
        {
            "pattern_id": [pattern["pattern_id"] for pattern in patterns],
            "direction": [pattern["direction"] for pattern in patterns],
            "occurrence_count": [1] * 20,
            "success_count": [0] * 20,
            "accuracy": [0.0] * 20,
            "average_return_3d": [0.0] * 20,
            "average_directional_profit": [0.0] * 20,
        }
    )
    signals = pd.DataFrame(
        [
            {
                "pattern_id": "BULL-000",
                "direction": "bullish",
                "ticker": TEST_TICKERS[0],
                "date": "2026-01-05",
                "return_3d": 0.01,
                "distance": 0.2,
                "success": False,
                "directional_profit": 0.01,
            },
            {
                "pattern_id": "BEAR-000",
                "direction": "bearish",
                "ticker": TEST_TICKERS[0],
                "date": "2026-01-05",
                "return_3d": 0.01,
                "distance": 0.2,
                "success": False,
                "directional_profit": -0.01,
            },
        ]
    )
    monkeypatch.setattr(
        analysis,
        "backtest_patterns",
        lambda locked_patterns, rows, weights, threshold: (metrics, signals),
    )
    monkeypatch.setattr(analysis, "generate_figures", lambda root: [])

    overall = analysis.test_project(tmp_path)

    written_signals = pd.read_csv(result_dir / "test_2026_signals.csv")
    written_stocks = pd.read_csv(result_dir / "test_2026_stock_metrics.csv")
    assert written_signals["conflict_signal"].all()
    assert len(written_stocks) == 10
    assert overall["total_signals"] == 0


def test_relative_candles_produce_valid_ohlc():
    candles = analysis.relative_candles(
        [1.0, 1.0, 2.0, 1.0, 1.0, -1.0, 0.5, 1.0, 0.2, 0.1]
    )

    assert len(candles) == 2
    assert all(
        high >= max(open_price, close) and low <= min(open_price, close)
        for open_price, high, low, close in candles
    )


def test_generate_figures_writes_required_files(tmp_path: Path):
    result_dir = tmp_path / "data" / "results"
    result_dir.mkdir(parents=True)
    for direction in ("bullish", "bearish"):
        frame = pd.DataFrame(
            {
                "pattern_id": [f"{direction}-{index}" for index in range(10)],
                "centroid_raw": [json.dumps([0.1] * 10)] * 10,
                "average_directional_profit": [0.05] * 10,
            }
        )
        frame.to_csv(result_dir / f"top10_{direction}.csv", index=False)

    paths = analysis.generate_figures(tmp_path)

    assert len(paths) == 4
    assert all(path.exists() and path.stat().st_size > 0 for path in paths)


def test_cli_all_runs_three_data_stages(monkeypatch, tmp_path: Path):
    import main

    calls: list[str] = []
    monkeypatch.setattr(
        main, "download_project", lambda root: calls.append("download")
    )
    monkeypatch.setattr(main, "analyze_project", lambda root: calls.append("analyze"))
    monkeypatch.setattr(main, "test_project", lambda root: calls.append("test"))
    monkeypatch.setattr(
        main,
        "launch_gui",
        lambda root: (_ for _ in ()).throw(AssertionError("GUI must not open")),
    )

    assert main.run(["--all"], project_root=tmp_path) == 0
    assert calls == ["download", "analyze", "test"]


def test_gui_loader_merges_optional_2026_metrics(tmp_path: Path):
    from gui import load_gui_records

    result_dir = tmp_path / "data" / "results"
    result_dir.mkdir(parents=True)
    for direction in ("bullish", "bearish"):
        pd.DataFrame(
            {
                "pattern_id": [f"{direction}-1"],
                "direction": [direction],
                "occurrence_count": [20],
                "accuracy": [0.7],
                "average_directional_profit": [0.06],
                "centroid_raw": [json.dumps([0.1] * 10)],
            }
        ).to_csv(result_dir / f"top10_{direction}.csv", index=False)
    pd.DataFrame(
        {
            "pattern_id": ["bullish-1"],
            "number_of_matches": [4],
            "test_accuracy": [0.5],
        }
    ).to_csv(result_dir / "test_2026_pattern_metrics.csv", index=False)

    records = load_gui_records(tmp_path)

    bullish = records.loc[records["pattern_id"].eq("bullish-1")].iloc[0]
    bearish = records.loc[records["pattern_id"].eq("bearish-1")].iloc[0]
    assert bullish["number_of_matches"] == 4
    assert pd.isna(bearish["number_of_matches"])
