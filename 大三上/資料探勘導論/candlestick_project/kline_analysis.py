"""Feature engineering, pattern discovery, backtesting, and reporting."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any
import warnings

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

from config import (
    CLUSTER_DISTANCE_THRESHOLD,
    DISCOVERY_END,
    DISCOVERY_START,
    MIN_ACCURACY,
    MIN_OCCURRENCES,
    SIMILARITY_THRESHOLDS,
    STOCK_TICKERS,
    TEST_END,
    TEST_START,
    TEST_TICKERS,
    VALIDATION_END,
    VALIDATION_START,
    WEIGHT_PRESETS,
)
from data_loader import load_clean_stocks


FEATURE_COLUMNS = (
    "upper",
    "lower",
    "body",
    "prev_upper",
    "prev_lower",
    "prev_body",
    "open_style",
    "close_style",
    "volume_feature",
    "trend",
)

SIGNAL_COLUMNS = (
    "pattern_id",
    "direction",
    "ticker",
    "date",
    "return_3d",
    "distance",
    "success",
    "directional_profit",
)

TEST_RESULT_FILENAMES = (
    "test_2026_signals.csv",
    "test_2026_pattern_metrics.csv",
    "test_2026_stock_metrics.csv",
    "test_2026_overall_metrics.json",
)


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Calculate the assignment's ten features and the three-day label."""
    data = frame.copy()
    if "pattern_eligible" not in data.columns:
        data["pattern_eligible"] = True

    open_price = data["Open"].astype(float)
    high = data["High"].astype(float)
    low = data["Low"].astype(float)
    close = data["Close"].astype(float)
    volume = data["Volume"].astype(float)
    upper = (high - pd.concat([open_price, close], axis=1).max(axis=1)) / close * 100
    lower = (pd.concat([open_price, close], axis=1).min(axis=1) - low) / close * 100
    body = (close - open_price) / close * 100
    previous_close = close.shift(1)
    five_day_volume = volume.rolling(window=5, min_periods=5).mean()

    data["upper"] = upper
    data["lower"] = lower
    data["body"] = body
    data["prev_upper"] = upper.shift(1)
    data["prev_lower"] = lower.shift(1)
    data["prev_body"] = body.shift(1)
    data["open_style"] = (open_price - previous_close) / close * 100
    data["close_style"] = (close - previous_close) / close * 100
    with np.errstate(divide="ignore", invalid="ignore"):
        data["volume_feature"] = np.where(
            volume.ne(0),
            (volume - five_day_volume) / volume,
            np.nan,
        )
    data["trend"] = (close.shift(2) - close.shift(7)) / close.shift(7)
    data["return_3d"] = (close.shift(-3) - close) / close
    data["return_3d_date"] = pd.Series(data.index, index=data.index).shift(-3)
    data.loc[volume.eq(0), "pattern_eligible"] = False
    return data


def _validated_weights(weights: Any, width: int) -> np.ndarray:
    values = np.asarray(weights, dtype=float)
    if values.shape != (width,):
        raise ValueError(f"weights must contain {width} values")
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("weights must be finite and non-negative")
    return values


def weighted_distance(vector_a: Any, vector_b: Any, weights: Any) -> float:
    first = np.asarray(vector_a, dtype=float)
    second = np.asarray(vector_b, dtype=float)
    if first.ndim != 1 or first.shape != second.shape:
        raise ValueError("vectors must be one-dimensional and have the same width")
    values = _validated_weights(weights, first.size)
    return float(np.sqrt(np.sum(values * np.square(first - second))))


def pairwise_weighted_distances(patterns: Any, rows: Any, weights: Any) -> np.ndarray:
    pattern_values = np.asarray(patterns, dtype=float)
    row_values = np.asarray(rows, dtype=float)
    if pattern_values.ndim != 2 or row_values.ndim != 2:
        raise ValueError("patterns and rows must be two-dimensional")
    if pattern_values.shape[1] != row_values.shape[1]:
        raise ValueError("patterns and rows must have the same feature width")
    values = _validated_weights(weights, pattern_values.shape[1])
    pattern_norms = np.sum(np.square(pattern_values) * values, axis=1)[:, None]
    row_norms = np.sum(np.square(row_values) * values, axis=1)[None, :]
    cross = (pattern_values * values) @ row_values.T
    squared = np.maximum(pattern_norms + row_norms - 2.0 * cross, 0.0)
    return np.sqrt(squared)


def is_match(distance: float, threshold: float) -> bool:
    return bool(distance <= threshold)


def _period_rows(
    frame: pd.DataFrame,
    start: str,
    end: str,
    *,
    require_label: bool = True,
) -> pd.DataFrame:
    data = frame.copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    data["return_3d_date"] = pd.to_datetime(data["return_3d_date"], errors="coerce")
    mask = data["date"].between(pd.Timestamp(start), pd.Timestamp(end))
    mask &= data["pattern_eligible"].fillna(False)
    mask &= data[list(FEATURE_COLUMNS)].notna().all(axis=1)
    if require_label:
        mask &= data["return_3d"].notna()
        mask &= data["return_3d_date"].between(pd.Timestamp(start), pd.Timestamp(end))
    return data.loc[mask].copy()


def combine_feature_stocks(stocks: dict[str, pd.DataFrame]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for ticker, frame in stocks.items():
        featured = build_features(frame).reset_index()
        featured = featured.rename(columns={featured.columns[0]: "date"})
        featured["ticker"] = ticker
        frames.append(featured)
    if not frames:
        raise ValueError("No stock data is available")
    return pd.concat(frames, ignore_index=True)


def _cluster_direction(
    candidates: pd.DataFrame,
    direction: str,
    scaler: StandardScaler,
) -> list[dict[str, object]]:
    if candidates.empty:
        return []
    features_raw = candidates[list(FEATURE_COLUMNS)].to_numpy(dtype=float)
    features_z = scaler.transform(features_raw)
    if len(candidates) == 1:
        labels = np.array([0])
    else:
        model = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=CLUSTER_DISTANCE_THRESHOLD,
            linkage="ward",
        )
        labels = model.fit_predict(features_z)

    records: list[dict[str, object]] = []
    prefix = "BULL" if direction == "bullish" else "BEAR"
    for number, label in enumerate(sorted(np.unique(labels)), start=1):
        members = candidates.loc[labels == label]
        member_z = features_z[labels == label]
        centroid_z = member_z.mean(axis=0)
        centroid_raw = scaler.inverse_transform(centroid_z.reshape(1, -1))[0]
        records.append(
            {
                "pattern_id": f"{prefix}-{number:03d}",
                "direction": direction,
                "cluster_size": len(members),
                "centroid_z": centroid_z.tolist(),
                "centroid_raw": centroid_raw.tolist(),
                "source_candidates": [
                    f"{row.ticker}:{pd.Timestamp(row.date).date()}"
                    for row in members.itertuples()
                ],
            }
        )
    return records


def discover_patterns(
    feature_rows: pd.DataFrame,
) -> tuple[StandardScaler, pd.DataFrame]:
    """Fit discovery-only scaling and cluster strict ±5% candidates."""
    discovery = _period_rows(feature_rows, DISCOVERY_START, DISCOVERY_END)
    if discovery.empty:
        raise ValueError("No valid 2018-2023 discovery rows")
    scaler = StandardScaler().fit(
        discovery[list(FEATURE_COLUMNS)].to_numpy(dtype=float)
    )
    bullish = discovery.loc[discovery["return_3d"] > 0.05].copy()
    bearish = discovery.loc[discovery["return_3d"] < -0.05].copy()
    records = [
        *_cluster_direction(bullish, "bullish", scaler),
        *_cluster_direction(bearish, "bearish", scaler),
    ]
    if not records:
        raise ValueError("Discovery found no bullish or bearish candidates")
    return scaler, pd.DataFrame(records)


def evaluation_rows(
    feature_rows: pd.DataFrame,
    scaler: StandardScaler,
    start: str,
    end: str,
) -> pd.DataFrame:
    rows = _period_rows(feature_rows, start, end)
    if rows.empty:
        raise ValueError(f"No valid rows from {start} through {end}")
    rows["features_z"] = scaler.transform(
        rows[list(FEATURE_COLUMNS)].to_numpy(dtype=float)
    ).tolist()
    return rows


def _decode_vector(value: object) -> list[float]:
    if isinstance(value, str):
        value = json.loads(value)
    result = np.asarray(value, dtype=float)
    if result.shape != (len(FEATURE_COLUMNS),):
        raise ValueError("pattern centroid must contain ten values")
    return result.tolist()


def backtest_patterns(
    patterns: pd.DataFrame,
    rows: pd.DataFrame,
    weights: Any,
    threshold: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Match every pattern against rows and return metrics plus signals."""
    pattern_vectors = np.vstack(patterns["centroid_z"].map(_decode_vector))
    row_vectors = np.vstack(rows["features_z"].map(_decode_vector))
    distances = pairwise_weighted_distances(pattern_vectors, row_vectors, weights)
    signal_records: list[dict[str, object]] = []
    metric_records: list[dict[str, object]] = []

    for pattern_position, pattern in patterns.reset_index(drop=True).iterrows():
        matched_positions = np.flatnonzero(distances[pattern_position] <= threshold)
        matched = rows.iloc[matched_positions]
        direction = str(pattern["direction"])
        if direction == "bullish":
            successes = matched["return_3d"] > 0.05
            directional = matched["return_3d"]
        elif direction == "bearish":
            successes = matched["return_3d"] < -0.05
            directional = -matched["return_3d"]
        else:
            raise ValueError(f"Unknown pattern direction: {direction}")

        for local_position, (row_index, row) in enumerate(matched.iterrows()):
            signal_records.append(
                {
                    "pattern_id": pattern["pattern_id"],
                    "direction": direction,
                    "ticker": row["ticker"],
                    "date": row["date"],
                    "return_3d": float(row["return_3d"]),
                    "distance": float(distances[pattern_position, matched_positions[local_position]]),
                    "success": bool(successes.loc[row_index]),
                    "directional_profit": float(directional.loc[row_index]),
                }
            )

        count = len(matched)
        metric_records.append(
            {
                "pattern_id": pattern["pattern_id"],
                "direction": direction,
                "occurrence_count": count,
                "success_count": int(successes.sum()),
                "accuracy": float(successes.mean()) if count else 0.0,
                "average_return_3d": float(matched["return_3d"].mean()) if count else 0.0,
                "average_directional_profit": float(directional.mean()) if count else 0.0,
            }
        )
    return pd.DataFrame(metric_records), pd.DataFrame(
        signal_records,
        columns=SIGNAL_COLUMNS,
    )


def _parameter_summary(metrics: pd.DataFrame) -> dict[str, float | int]:
    selected_parts: list[pd.DataFrame] = []
    qualified_count = 0
    direction_profits: list[float] = []
    direction_accuracies: list[float] = []
    for direction in ("bullish", "bearish"):
        part = metrics.loc[metrics["direction"].eq(direction)]
        if part.empty:
            return {
                "parameter_set_score": float("-inf"),
                "mean_accuracy": 0.0,
                "total_occurrence": 0,
                "qualified_patterns": qualified_count,
            }
        qualified = part.loc[
            part["occurrence_count"].ge(MIN_OCCURRENCES)
            & part["accuracy"].ge(MIN_ACCURACY)
        ]
        qualified_count += len(qualified)
        ranked = part.sort_values(
            ["average_directional_profit", "accuracy", "occurrence_count"],
            ascending=False,
            kind="stable",
        )
        top = pd.concat(
            [
                qualified.sort_values(
                    ["average_directional_profit", "accuracy", "occurrence_count"],
                    ascending=False,
                    kind="stable",
                ),
                ranked.loc[~ranked["pattern_id"].isin(qualified["pattern_id"])],
            ],
            ignore_index=True,
        ).head(10)
        selected_parts.append(top)
        direction_profits.append(float(top["average_directional_profit"].mean()))
        direction_accuracies.append(float(top["accuracy"].mean()))
    selected = pd.concat(selected_parts, ignore_index=True)
    return {
        "parameter_set_score": float(np.mean(direction_profits)),
        "mean_accuracy": float(np.mean(direction_accuracies)),
        "total_occurrence": int(selected["occurrence_count"].sum()),
        "qualified_patterns": int(qualified_count),
    }


def choose_parameters(
    patterns: pd.DataFrame,
    validation_rows: pd.DataFrame,
) -> dict[str, object]:
    """Choose among three understandable weight presets and three thresholds."""
    results: list[dict[str, object]] = []
    for name, weights in WEIGHT_PRESETS.items():
        for threshold in SIMILARITY_THRESHOLDS:
            metrics, _ = backtest_patterns(patterns, validation_rows, weights, threshold)
            results.append(
                {
                    "weight_preset": name,
                    "weights": list(weights),
                    "similarity_threshold": float(threshold),
                    **_parameter_summary(metrics),
                }
            )
    search = pd.DataFrame(results).sort_values(
        [
            "parameter_set_score",
            "mean_accuracy",
            "total_occurrence",
            "similarity_threshold",
        ],
        ascending=[False, False, False, True],
        kind="stable",
    )
    best = search.iloc[0].to_dict()
    best["search_results"] = search.to_dict("records")
    return best


def select_top_patterns(
    metrics: pd.DataFrame,
    patterns: pd.DataFrame,
    weights: Any,
) -> pd.DataFrame:
    """Select ten profitable, reliable, and non-duplicate patterns per side."""
    combined = metrics.merge(
        patterns,
        on=["pattern_id", "direction"],
        validate="one_to_one",
    )
    selected_rows: list[pd.Series] = []
    for direction in ("bullish", "bearish"):
        ranked = combined.loc[combined["direction"].eq(direction)].sort_values(
            ["average_directional_profit", "accuracy", "occurrence_count"],
            ascending=False,
            kind="stable",
        )
        qualified = ranked.loc[
            ranked["occurrence_count"].ge(MIN_OCCURRENCES)
            & ranked["accuracy"].ge(MIN_ACCURACY)
        ]
        if len(qualified) < 10:
            warnings.warn(
                f"Only {len(qualified)} qualified {direction} patterns; filling by rank",
                RuntimeWarning,
                stacklevel=2,
            )
        candidates = pd.concat(
            [qualified, ranked.loc[~ranked["pattern_id"].isin(qualified["pattern_id"])]],
            ignore_index=True,
        )
        direction_selected: list[pd.Series] = []
        for _, candidate in candidates.iterrows():
            vector = _decode_vector(candidate["centroid_z"])
            if all(
                weighted_distance(vector, _decode_vector(item["centroid_z"]), weights)
                >= 0.30
                for item in direction_selected
            ):
                direction_selected.append(candidate)
            if len(direction_selected) == 10:
                break
        if len(direction_selected) < 10:
            used = {str(row["pattern_id"]) for row in direction_selected}
            for _, candidate in candidates.iterrows():
                if str(candidate["pattern_id"]) not in used:
                    direction_selected.append(candidate)
                    used.add(str(candidate["pattern_id"]))
                if len(direction_selected) == 10:
                    break
        if len(direction_selected) < 10:
            raise ValueError(f"Fewer than 10 {direction} patterns are available")
        selected_rows.extend(direction_selected)
    return pd.DataFrame(selected_rows).reset_index(drop=True)


def _json_default(value: object) -> object:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.ndarray,)):
        return value.tolist()
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    raise TypeError(f"Cannot encode {type(value).__name__}")


def _write_json(value: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, default=_json_default),
        encoding="utf-8",
    )


def _write_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    value = frame.copy()
    for column in ("centroid_z", "centroid_raw", "source_candidates", "weights"):
        if column in value.columns:
            value[column] = value[column].map(
                lambda item: json.dumps(item, ensure_ascii=False, default=_json_default)
            )
    value.to_csv(path, index=False, encoding="utf-8", date_format="%Y-%m-%d")


def _project_logger(project_root: Path) -> logging.Logger:
    logger = logging.getLogger(f"candlestick:{Path(project_root).resolve()}")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    log_dir = Path(project_root) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_dir / "latest.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    return logger


def _scaler_from_model(model: dict[str, object]) -> StandardScaler:
    scaler_data = model.get("scaler")
    if not isinstance(scaler_data, dict):
        raise ValueError("final_patterns.json has no scaler")
    mean = np.asarray(scaler_data.get("mean"), dtype=float)
    scale = np.asarray(scaler_data.get("scale"), dtype=float)
    if mean.shape != (len(FEATURE_COLUMNS),) or scale.shape != mean.shape:
        raise ValueError("final_patterns.json contains an invalid scaler")
    if not np.isfinite(mean).all() or not np.isfinite(scale).all() or (scale <= 0).any():
        raise ValueError("final_patterns.json contains an invalid scaler")
    scaler = StandardScaler()
    scaler.mean_ = mean
    scaler.scale_ = scale
    scaler.var_ = np.square(scale)
    scaler.n_features_in_ = len(FEATURE_COLUMNS)
    scaler.n_samples_seen_ = int(scaler_data.get("sample_count", 1))
    return scaler


def _read_json(path: Path) -> object:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run --analyze first.")
    return json.loads(path.read_text(encoding="utf-8"))


def _invalidate_test_outputs(result_dir: Path) -> None:
    """Remove 2026 metrics that belong to a previously locked model."""
    for filename in TEST_RESULT_FILENAMES:
        (result_dir / filename).unlink(missing_ok=True)


def analyze_project(project_root: Path) -> dict[str, object]:
    """Run discovery and validation from local CSV files."""
    root = Path(project_root).resolve()
    logger = _project_logger(root)
    stocks = load_clean_stocks(
        root / "data" / "raw",
        tickers=STOCK_TICKERS,
        logger=logger,
    )
    if len(stocks) < 50:
        logger.warning(
            "Only %d valid stocks are available; the formal assignment requires 50",
            len(stocks),
        )
    feature_rows = combine_feature_stocks(stocks)
    scaler, patterns = discover_patterns(feature_rows)
    validation = evaluation_rows(
        feature_rows,
        scaler,
        VALIDATION_START,
        VALIDATION_END,
    )
    best = choose_parameters(patterns, validation)
    weights = np.asarray(best["weights"], dtype=float)
    threshold = float(best["similarity_threshold"])
    metrics, _ = backtest_patterns(patterns, validation, weights, threshold)
    selected = select_top_patterns(metrics, patterns, weights)

    result_dir = root / "data" / "results"
    _invalidate_test_outputs(result_dir)
    search_results = pd.DataFrame(best.get("search_results", []))
    _write_csv(patterns, result_dir / "all_patterns.csv")
    _write_csv(search_results, result_dir / "validation_results.csv")
    _write_csv(
        selected.loc[selected["direction"].eq("bullish")],
        result_dir / "top10_bullish.csv",
    )
    _write_csv(
        selected.loc[selected["direction"].eq("bearish")],
        result_dir / "top10_bearish.csv",
    )

    final_model = {
        "feature_columns": list(FEATURE_COLUMNS),
        "periods": {
            "discovery": [DISCOVERY_START, DISCOVERY_END],
            "validation": [VALIDATION_START, VALIDATION_END],
            "test": [TEST_START, TEST_END],
        },
        "scaler": {
            "mean": scaler.mean_.tolist(),
            "scale": scaler.scale_.tolist(),
            "sample_count": int(np.asarray(scaler.n_samples_seen_).max()),
        },
        "weight_preset": best["weight_preset"],
        "weights": weights.tolist(),
        "similarity_threshold": threshold,
        "patterns": selected.to_dict("records"),
    }
    _write_json(final_model, result_dir / "final_patterns.json")
    generate_figures(root)
    summary = {
        "valid_stocks": len(stocks),
        "discovery_patterns": len(patterns),
        "selected_patterns": len(selected),
        "weight_preset": str(best["weight_preset"]),
        "similarity_threshold": threshold,
    }
    logger.info("Analysis complete: %s", summary)
    return summary


def _empty_overall_metrics() -> dict[str, float | int]:
    return {
        "total_signals": 0,
        "successful_signals": 0,
        "overall_accuracy": 0.0,
        "average_directional_profit": 0.0,
        "median_directional_profit": 0.0,
        "bullish_signal_count": 0,
        "bullish_accuracy": 0.0,
        "bullish_average_return": 0.0,
        "bearish_signal_count": 0,
        "bearish_accuracy": 0.0,
        "bearish_average_directional_profit": 0.0,
    }


def _mark_conflicts(signals: pd.DataFrame) -> pd.DataFrame:
    """Mark individual pattern hits that share a bullish/bearish date conflict."""
    result = signals.copy()
    if result.empty:
        result["conflict_signal"] = pd.Series(dtype=bool)
        return result
    direction_counts = result.groupby(["ticker", "date"], observed=True)[
        "direction"
    ].transform("nunique")
    result["conflict_signal"] = direction_counts.gt(1)
    return result


def _trade_level_signals(signals: pd.DataFrame) -> pd.DataFrame:
    if signals.empty:
        return pd.DataFrame(
            columns=[
                "ticker",
                "date",
                "direction",
                "return_3d",
                "success",
                "directional_profit",
                "conflict_signal",
            ]
        )
    unique = signals.drop_duplicates(["ticker", "date", "direction"]).copy()
    if "conflict_signal" not in unique.columns:
        unique = _mark_conflicts(unique)
    return unique.loc[~unique["conflict_signal"]].reset_index(drop=True)


def _validate_test_rows(rows: pd.DataFrame) -> None:
    available = set(rows["ticker"].astype(str)) if "ticker" in rows.columns else set()
    missing = sorted(set(TEST_TICKERS) - available)
    if missing:
        raise ValueError(
            "2026 test requires valid 2026 rows for all 10 fixed tickers; missing: "
            + ", ".join(missing)
        )


def _validate_locked_patterns(patterns: pd.DataFrame) -> None:
    required = {"pattern_id", "direction", "centroid_z"}
    missing_columns = sorted(required - set(patterns.columns))
    if missing_columns:
        raise ValueError(
            "Locked model is missing pattern fields: " + ", ".join(missing_columns)
        )
    unique = patterns.drop_duplicates("pattern_id")
    counts = unique["direction"].value_counts().to_dict()
    if len(unique) != len(patterns) or counts != {"bullish": 10, "bearish": 10}:
        raise ValueError(
            "Locked model must contain 10 unique bullish and 10 unique bearish patterns"
        )


def _overall_metrics(trades: pd.DataFrame) -> dict[str, float | int]:
    if trades.empty:
        return _empty_overall_metrics()
    bullish = trades.loc[trades["direction"].eq("bullish")]
    bearish = trades.loc[trades["direction"].eq("bearish")]
    return {
        "total_signals": len(trades),
        "successful_signals": int(trades["success"].sum()),
        "overall_accuracy": float(trades["success"].mean()),
        "average_directional_profit": float(trades["directional_profit"].mean()),
        "median_directional_profit": float(trades["directional_profit"].median()),
        "bullish_signal_count": len(bullish),
        "bullish_accuracy": float(bullish["success"].mean()) if len(bullish) else 0.0,
        "bullish_average_return": float(bullish["return_3d"].mean()) if len(bullish) else 0.0,
        "bearish_signal_count": len(bearish),
        "bearish_accuracy": float(bearish["success"].mean()) if len(bearish) else 0.0,
        "bearish_average_directional_profit": (
            float(bearish["directional_profit"].mean()) if len(bearish) else 0.0
        ),
    }


def test_project(project_root: Path) -> dict[str, float | int]:
    """Evaluate the locked Top-10 model on fixed 2026 tickers."""
    root = Path(project_root).resolve()
    logger = _project_logger(root)
    model_value = _read_json(root / "data" / "results" / "final_patterns.json")
    if not isinstance(model_value, dict):
        raise ValueError("final_patterns.json must contain an object")
    model = model_value
    stocks = load_clean_stocks(
        root / "data" / "raw",
        tickers=TEST_TICKERS,
        logger=logger,
    )
    missing = sorted(set(TEST_TICKERS) - set(stocks))
    if missing:
        raise ValueError(
            "2026 test requires all 10 fixed tickers; missing: " + ", ".join(missing)
        )
    selected_stocks = {ticker: stocks[ticker] for ticker in TEST_TICKERS}
    feature_rows = combine_feature_stocks(selected_stocks)
    scaler = _scaler_from_model(model)
    rows = evaluation_rows(feature_rows, scaler, TEST_START, TEST_END)
    _validate_test_rows(rows)
    patterns = pd.DataFrame(model.get("patterns", []))
    _validate_locked_patterns(patterns)
    metrics, signals = backtest_patterns(
        patterns,
        rows,
        model.get("weights"),
        float(model.get("similarity_threshold", 0)),
    )
    signals = _mark_conflicts(signals)
    trades = _trade_level_signals(signals)
    overall = _overall_metrics(trades)

    pattern_metrics = metrics.rename(
        columns={
            "occurrence_count": "number_of_matches",
            "average_directional_profit": "test_average_directional_profit",
            "accuracy": "test_accuracy",
        }
    )
    if trades.empty:
        observed_stock_metrics = pd.DataFrame(
            columns=[
                "ticker",
                "number_of_signals",
                "accuracy",
                "average_directional_profit",
            ]
        )
    else:
        observed_stock_metrics = (
            trades.groupby("ticker", observed=True)
            .agg(
                number_of_signals=("success", "size"),
                accuracy=("success", "mean"),
                average_directional_profit=("directional_profit", "mean"),
            )
            .reset_index()
        )
    stock_metrics = pd.DataFrame({"ticker": TEST_TICKERS}).merge(
        observed_stock_metrics,
        on="ticker",
        how="left",
        validate="one_to_one",
    )
    stock_metrics["number_of_signals"] = (
        pd.to_numeric(stock_metrics["number_of_signals"], errors="coerce")
        .astype("float64")
        .fillna(0)
        .astype("int64")
    )
    for column in ("accuracy", "average_directional_profit"):
        stock_metrics[column] = (
            pd.to_numeric(stock_metrics[column], errors="coerce")
            .astype("float64")
            .fillna(0.0)
        )

    result_dir = root / "data" / "results"
    _write_csv(signals, result_dir / "test_2026_signals.csv")
    _write_csv(pattern_metrics, result_dir / "test_2026_pattern_metrics.csv")
    _write_csv(stock_metrics, result_dir / "test_2026_stock_metrics.csv")
    _write_json(overall, result_dir / "test_2026_overall_metrics.json")
    generate_figures(root)
    logger.info("2026 test complete: %s", overall)
    return overall


def relative_candles(features: Any) -> list[tuple[float, float, float, float]]:
    """Reconstruct two relative candles for display only."""
    values = np.asarray(features, dtype=float)
    if values.shape != (len(FEATURE_COLUMNS),) or not np.isfinite(values).all():
        raise ValueError("centroid_raw must contain ten finite values")
    (
        upper,
        lower,
        _body,
        prev_upper,
        prev_lower,
        prev_body,
        open_style,
        close_style,
        _volume,
        _trend,
    ) = values
    previous_close = 100.0
    previous_open = previous_close * (1.0 - prev_body / 100.0)
    previous_high = max(previous_open, previous_close) + prev_upper
    previous_low = min(previous_open, previous_close) - prev_lower
    denominator = 1.0 - close_style / 100.0
    current_close = (
        previous_close / denominator
        if denominator > np.finfo(float).eps
        else previous_close
    )
    current_open = previous_close + open_style * current_close / 100.0
    current_high = max(current_open, current_close) + upper * current_close / 100.0
    current_low = min(current_open, current_close) - lower * current_close / 100.0
    return [
        (previous_open, previous_high, previous_low, previous_close),
        (current_open, current_high, current_low, current_close),
    ]


def _load_optional_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path)
    for column in ("centroid_z", "centroid_raw", "source_candidates"):
        if column in frame.columns:
            frame[column] = frame[column].map(
                lambda value: json.loads(value) if isinstance(value, str) else value
            )
    return frame


def _draw_candle(axis: Any, x: float, candle: tuple[float, float, float, float]) -> None:
    open_price, high, low, close = candle
    color = "#d62728" if close >= open_price else "#2ca02c"
    axis.vlines(x, low, high, color=color, linewidth=1.2)
    height = close - open_price
    axis.bar(
        x,
        height if not np.isclose(height, 0.0) else 0.03,
        bottom=open_price,
        width=0.5,
        color=color,
    )


def _save_pattern_grid(frame: pd.DataFrame, title: str, path: Path) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(2, 5, figsize=(15, 6), constrained_layout=True)
    axes_flat = axes.ravel()
    for axis in axes_flat:
        axis.set_visible(False)
    for axis, (_, row) in zip(axes_flat, frame.head(10).iterrows(), strict=False):
        axis.set_visible(True)
        for x, candle in enumerate(relative_candles(_decode_vector(row["centroid_raw"]))):
            _draw_candle(axis, x, candle)
        axis.set_xticks([0, 1], ["Prev", "Now"])
        profit = float(row.get("average_directional_profit", 0)) * 100
        axis.set_title(f"{row['pattern_id']}\nprofit {profit:.2f}%", fontsize=9)
    figure.suptitle(title, fontsize=16)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=160)
    plt.close(figure)


def _save_bar(
    frame: pd.DataFrame,
    label_column: str,
    value_column: str,
    title: str,
    path: Path,
) -> None:
    import matplotlib.pyplot as plt

    figure, axis = plt.subplots(figsize=(10, 5), constrained_layout=True)
    if frame.empty or value_column not in frame.columns:
        axis.text(0.5, 0.5, "No 2026 result yet", ha="center", va="center")
        axis.set_axis_off()
    else:
        values = frame.sort_values(value_column, ascending=False)
        axis.bar(values[label_column].astype(str), values[value_column].astype(float))
        axis.tick_params(axis="x", rotation=55)
        axis.set_ylabel(value_column)
    axis.set_title(title)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=160)
    plt.close(figure)


def generate_figures(project_root: Path) -> list[Path]:
    """Write the four figures needed by the simplified report."""
    root = Path(project_root)
    result_dir = root / "data" / "results"
    figure_dir = root / "outputs" / "figures"
    bullish = _load_optional_csv(result_dir / "top10_bullish.csv")
    bearish = _load_optional_csv(result_dir / "top10_bearish.csv")
    pattern_test = _load_optional_csv(result_dir / "test_2026_pattern_metrics.csv")
    stock_test = _load_optional_csv(result_dir / "test_2026_stock_metrics.csv")
    paths = [
        figure_dir / "top10_bullish.png",
        figure_dir / "top10_bearish.png",
        figure_dir / "2026_pattern_performance.png",
        figure_dir / "2026_stock_performance.png",
    ]
    _save_pattern_grid(bullish, "Top 10 Bullish Patterns", paths[0])
    _save_pattern_grid(bearish, "Top 10 Bearish Patterns", paths[1])
    _save_bar(
        pattern_test,
        "pattern_id",
        "test_average_directional_profit",
        "2026 Pattern Performance",
        paths[2],
    )
    _save_bar(
        stock_test,
        "ticker",
        "average_directional_profit",
        "2026 Stock Performance",
        paths[3],
    )
    return paths
