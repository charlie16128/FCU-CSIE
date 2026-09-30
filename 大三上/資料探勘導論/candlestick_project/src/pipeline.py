from __future__ import annotations

import json
import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from .backtest_patterns import backtest_patterns
from .build_features import FEATURE_COLUMNS, build_features
from .clean_data import clean_ohlcv
from .cluster_patterns import cluster_candidates, fit_discovery_scaler
from .download_data import download_universe
from .find_candidates import find_candidates
from .optimize_similarity import WEIGHT_COLUMNS, optimize_similarity
from .select_top10 import select_top_patterns
from .settings import load_settings
from .similarity import expand_group_weights
from .test_2026 import evaluate_final_test
from .utils import (
    configure_logging,
    ensure_project_directories,
    load_tickers,
    write_csv,
    write_json,
)
from .visualization import generate_required_figures


def _require(path: Path, instruction: str) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. {instruction}")
    return path


def _load_processed(project_root: Path) -> pd.DataFrame:
    paths = sorted((project_root / "data" / "processed").glob("*.csv"))
    if not paths:
        raise FileNotFoundError("No processed data. Run --prepare first")

    frames: list[pd.DataFrame] = []
    for path in paths:
        frame = pd.read_csv(path)
        if "Date" in frame.columns:
            frame = frame.rename(columns={"Date": "date"})
        if "date" not in frame.columns:
            raise ValueError(f"Processed file {path} has no Date column")
        frame["date"] = pd.to_datetime(frame["date"], errors="raise")
        if "return_3d_date" in frame.columns:
            frame["return_3d_date"] = pd.to_datetime(
                frame["return_3d_date"],
                errors="coerce",
            )
        frame["ticker"] = path.stem
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def _decode_vectors(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    for column in ("centroid_z", "centroid_raw", "source_candidates"):
        if column in result.columns:
            result[column] = result[column].map(
                lambda value: json.loads(value) if isinstance(value, str) else value
            )
    return result


def download_data(project_root: Path) -> dict[str, list[str]]:
    root = Path(project_root).resolve()
    ensure_project_directories(root)
    settings = load_settings(root / "config" / "settings.yaml")
    tickers = load_tickers(root / "config" / "tickers.txt")
    logger = configure_logging(root / "logs")
    summary = download_universe(
        tickers,
        root / "data" / "raw",
        retries=settings.download_retries,
        retry_backoff_seconds=settings.retry_backoff_seconds,
        start=settings.dates.download_start.isoformat(),
        end=settings.dates.download_end.isoformat(),
        logger=logger,
    )
    if len(summary["successful"]) < len(tickers):
        logger.warning(
            "Only %d of %d tickers downloaded successfully",
            len(summary["successful"]),
            len(tickers),
        )
    return summary


def prepare_data(
    project_root: Path,
    *,
    logger: logging.Logger | None = None,
) -> dict[str, object]:
    root = Path(project_root).resolve()
    ensure_project_directories(root)
    logger = logger or configure_logging(root / "logs")
    raw_paths = sorted((root / "data" / "raw").glob("*.csv"))
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
            write_csv(featured.reset_index(), root / "data" / "processed" / path.name)
            eligible_rows = int(
                (
                    featured["pattern_eligible"].fillna(False)
                    & featured[list(FEATURE_COLUMNS)].notna().all(axis=1)
                ).sum()
            )
            successful += 1
            total_valid_rows += int(cleaning_summary["valid_rows"])
            total_corporate_action_excluded += int(
                cleaning_summary["corporate_action_excluded"]
            )
            total_feature_rows += eligible_rows
            logger.info(
                "Prepared %s: %d valid rows, %d eligible feature rows",
                ticker,
                cleaning_summary["valid_rows"],
                eligible_rows,
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


def train_patterns(project_root: Path) -> dict[str, int]:
    root = Path(project_root).resolve()
    ensure_project_directories(root)
    settings = load_settings(root / "config" / "settings.yaml")
    logger = configure_logging(root / "logs")
    data = _load_processed(root)
    effective_tickers = int(data["ticker"].nunique())
    if effective_tickers < 50:
        logger.warning(
            "Effective modeling universe has only %d stocks; at least 50 are required for the formal run",
            effective_tickers,
        )
    discovery = data.loc[
        data["date"].between(
            pd.Timestamp(settings.dates.discovery_start),
            pd.Timestamp(settings.dates.discovery_end),
        )
        & data["pattern_eligible"].fillna(False)
        & data[list(FEATURE_COLUMNS)].notna().all(axis=1)
    ].copy()
    scaler = fit_discovery_scaler(discovery)
    model_dir = root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, model_dir / "scaler.pkl")

    candidates = find_candidates(
        data,
        pd.Timestamp(settings.dates.discovery_start),
        pd.Timestamp(settings.dates.discovery_end),
    )
    bullish = candidates.loc[candidates["direction"].eq("bullish")]
    bearish = candidates.loc[candidates["direction"].eq("bearish")]
    write_csv(bullish, root / "data" / "results" / "bullish_candidates.csv")
    write_csv(bearish, root / "data" / "results" / "bearish_candidates.csv")

    patterns = cluster_candidates(
        candidates,
        scaler,
        settings.cluster_distance_threshold,
    )
    write_csv(
        patterns.loc[patterns["direction"].eq("bullish")],
        root / "data" / "results" / "all_bullish_patterns.csv",
    )
    write_csv(
        patterns.loc[patterns["direction"].eq("bearish")],
        root / "data" / "results" / "all_bearish_patterns.csv",
    )
    for direction in ("bullish", "bearish"):
        count = int(patterns["direction"].eq(direction).sum())
        if not (
            settings.cluster_warning_minimum
            <= count
            <= settings.cluster_warning_maximum
        ):
            logger.warning(
                "%s cluster count %d is outside %d..%d",
                direction,
                count,
                settings.cluster_warning_minimum,
                settings.cluster_warning_maximum,
            )
    logger.info(
        "Training summary: %d bullish candidates, %d bearish candidates, %d patterns",
        len(bullish),
        len(bearish),
        len(patterns),
    )
    return {
        "bullish_candidates": len(bullish),
        "bearish_candidates": len(bearish),
        "patterns": len(patterns),
    }


def _evaluation_rows(
    data: pd.DataFrame,
    scaler,
    start,
    end,
) -> pd.DataFrame:
    data = data.copy()
    if "return_3d_date" in data.columns:
        data["return_3d_date"] = pd.to_datetime(
            data["return_3d_date"],
            errors="coerce",
        )
    else:
        ordered = data.sort_values(["ticker", "date"], kind="stable")
        ordered["return_3d_date"] = ordered.groupby(
            "ticker",
            observed=True,
        )["date"].shift(-3)
        data["return_3d_date"] = ordered["return_3d_date"]
    rows = data.loc[
        data["date"].between(pd.Timestamp(start), pd.Timestamp(end))
        & data["return_3d_date"].between(
            pd.Timestamp(start),
            pd.Timestamp(end),
        )
        & data["pattern_eligible"].fillna(False)
        & data[list(FEATURE_COLUMNS)].notna().all(axis=1)
        & data["return_3d"].notna()
    ].copy()
    if rows.empty:
        raise ValueError(f"No valid rows are available from {start} through {end}")
    rows["features_z"] = scaler.transform(rows[list(FEATURE_COLUMNS)]).tolist()
    return rows


def _load_all_patterns(root: Path) -> pd.DataFrame:
    result_dir = root / "data" / "results"
    bullish = _decode_vectors(
        pd.read_csv(
            _require(
                result_dir / "all_bullish_patterns.csv",
                "Run --train first",
            )
        )
    )
    bearish = _decode_vectors(
        pd.read_csv(
            _require(
                result_dir / "all_bearish_patterns.csv",
                "Run --train first",
            )
        )
    )
    return pd.concat([bullish, bearish], ignore_index=True)


def _group_weights(best: dict[str, object]) -> tuple[float, ...]:
    return tuple(float(best[column]) for column in WEIGHT_COLUMNS)


def validate_patterns(project_root: Path) -> dict[str, object]:
    root = Path(project_root).resolve()
    ensure_project_directories(root)
    settings = load_settings(root / "config" / "settings.yaml")
    logger = configure_logging(root / "logs")
    scaler = joblib.load(
        _require(root / "models" / "scaler.pkl", "Run --train first")
    )
    patterns = _load_all_patterns(root)
    rows = _evaluation_rows(
        _load_processed(root),
        scaler,
        settings.dates.validation_start,
        settings.dates.validation_end,
    )
    best, search = optimize_similarity(
        patterns,
        rows,
        weight_values=settings.weight_values,
        thresholds=settings.similarity_thresholds,
        minimum_occurrence=settings.minimum_occurrences[0],
        minimum_accuracy=settings.minimum_accuracies[0],
        chunk_size=settings.distance_chunk_size,
    )
    weights = expand_group_weights(_group_weights(best))
    metrics, _ = backtest_patterns(
        patterns,
        rows,
        weights,
        float(best["similarity_threshold"]),
        chunk_size=settings.distance_chunk_size,
    )
    metrics = metrics.merge(
        patterns,
        on=["pattern_id", "direction"],
        how="left",
        validate="one_to_one",
    )
    selected, policy = select_top_patterns(
        metrics,
        weights,
        occurrences=settings.minimum_occurrences,
        accuracies=settings.minimum_accuracies,
        dedup_thresholds=settings.dedup_thresholds,
    )

    parameter_keys = (*WEIGHT_COLUMNS, "similarity_threshold")
    best_params: dict[str, object] = {
        **{key: best[key] for key in parameter_keys},
        **policy,
        "feature_weights": weights.tolist(),
    }
    final_model = {
        "scaler_path": "models/scaler.pkl",
        "group_weights": {
            key: float(best[key]) for key in WEIGHT_COLUMNS
        },
        "feature_weights": weights.tolist(),
        "similarity_threshold": float(best["similarity_threshold"]),
        "minimum_occurrence": policy["minimum_occurrence"],
        "minimum_accuracy": policy["minimum_accuracy"],
        "dedup_threshold": policy["dedup_threshold"],
        "patterns": selected.to_dict("records"),
    }

    result_dir = root / "data" / "results"
    write_csv(search, result_dir / "validation_results.csv")
    write_csv(
        selected.loc[selected["direction"].eq("bullish")],
        result_dir / "top10_bullish.csv",
    )
    write_csv(
        selected.loc[selected["direction"].eq("bearish")],
        result_dir / "top10_bearish.csv",
    )
    write_json(best_params, root / "models" / "best_params.json")
    write_json(final_model, root / "models" / "final_patterns.json")

    if (
        policy["minimum_occurrence"] != settings.minimum_occurrences[0]
        or policy["minimum_accuracy"] != settings.minimum_accuracies[0]
        or policy["dedup_threshold"] != settings.dedup_thresholds[0]
    ):
        logger.warning("Top 10 selection thresholds were relaxed: %s", policy)
    else:
        logger.info("Top 10 selection policy: %s", policy)
    logger.info(
        "Best validation parameters: weights=%s threshold=%s score=%s",
        _group_weights(best),
        best["similarity_threshold"],
        best["parameter_set_score"],
    )
    return best_params


def _validation_labels(frame: pd.DataFrame) -> pd.Series:
    columns = [*WEIGHT_COLUMNS, "similarity_threshold"]
    if not set(columns).issubset(frame.columns):
        return pd.Series(np.arange(len(frame)).astype(str), index=frame.index)
    return frame[columns].apply(
        lambda row: "/".join(f"{float(value):g}" for value in row),
        axis=1,
    )


def _validate_test_coverage(
    configured_tickers: list[str],
    rows: pd.DataFrame,
) -> None:
    if len(configured_tickers) < 10:
        raise ValueError("Final test requires at least 10 configured tickers")
    available = set(rows["ticker"].astype(str)) if "ticker" in rows.columns else set()
    missing = sorted(set(configured_tickers) - available)
    if missing:
        raise ValueError(
            "Final test is missing valid 2026 rows for configured tickers: "
            + ", ".join(missing)
        )


def test_patterns(project_root: Path) -> dict[str, float | int]:
    root = Path(project_root).resolve()
    ensure_project_directories(root)
    settings = load_settings(root / "config" / "settings.yaml")
    model_path = _require(
        root / "models" / "final_patterns.json",
        "Run --validate first",
    )
    model = json.loads(model_path.read_text(encoding="utf-8"))
    scaler = joblib.load(
        _require(root / "models" / "scaler.pkl", "Run --train first")
    )
    configured_tickers = load_tickers(root / "config" / "test_tickers.txt")
    if len(configured_tickers) < 10:
        raise ValueError("Final test requires at least 10 configured tickers")
    test_tickers = set(configured_tickers)
    data = _load_processed(root)
    data = data.loc[data["ticker"].isin(test_tickers)].copy()
    rows = _evaluation_rows(
        data,
        scaler,
        settings.dates.test_start,
        settings.dates.test_end,
    )
    _validate_test_coverage(configured_tickers, rows)
    result = evaluate_final_test(
        model,
        rows,
        chunk_size=settings.distance_chunk_size,
    )

    result_dir = root / "data" / "results"
    write_csv(result.signals, result_dir / "test_2026_signals.csv")
    write_csv(
        result.pattern_metrics,
        result_dir / "test_2026_pattern_metrics.csv",
    )
    write_csv(result.stock_metrics, result_dir / "test_2026_stock_metrics.csv")
    write_json(
        result.overall_metrics,
        result_dir / "test_2026_overall_metrics.json",
    )

    validation = pd.read_csv(
        _require(
            result_dir / "validation_results.csv",
            "Run --validate first",
        )
    )
    validation["label"] = _validation_labels(validation)
    generate_required_figures(
        {
            "bullish": pd.read_csv(
                _require(result_dir / "top10_bullish.csv", "Run --validate first")
            ),
            "bearish": pd.read_csv(
                _require(result_dir / "top10_bearish.csv", "Run --validate first")
            ),
            "validation": validation.nlargest(30, "parameter_set_score"),
            "pattern_test": result.pattern_metrics,
            "stock_test": result.stock_metrics,
        },
        root / "outputs" / "figures",
    )
    configure_logging(root / "logs").info(
        "2026 final-test summary: %s",
        result.overall_metrics,
    )
    return result.overall_metrics
