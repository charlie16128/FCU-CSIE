from __future__ import annotations

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


STOCK_METRIC_COLUMNS = (
    "ticker",
    "number_of_signals",
    "accuracy",
    "average_directional_profit",
)


def _empty_stock_metrics() -> pd.DataFrame:
    return pd.DataFrame(columns=STOCK_METRIC_COLUMNS)


def _mean_or_zero(frame: pd.DataFrame, column: str) -> float:
    if frame.empty:
        return 0.0
    return float(frame[column].mean())


def _overall_metrics(trades: pd.DataFrame) -> dict[str, float | int]:
    bullish = trades.loc[trades["direction"].eq("bullish")]
    bearish = trades.loc[trades["direction"].eq("bearish")]
    return {
        "total_signals": int(len(trades)),
        "successful_signals": int(trades["success"].sum()) if len(trades) else 0,
        "overall_accuracy": _mean_or_zero(trades, "success"),
        "average_directional_profit": _mean_or_zero(
            trades,
            "directional_profit",
        ),
        "median_directional_profit": (
            float(trades["directional_profit"].median()) if len(trades) else 0.0
        ),
        "bullish_signal_count": int(len(bullish)),
        "bullish_accuracy": _mean_or_zero(bullish, "success"),
        "bullish_average_return": _mean_or_zero(bullish, "return_3d"),
        "bullish_average_directional_profit": _mean_or_zero(
            bullish,
            "directional_profit",
        ),
        "bearish_signal_count": int(len(bearish)),
        "bearish_accuracy": _mean_or_zero(bearish, "success"),
        "bearish_average_return": _mean_or_zero(bearish, "return_3d"),
        "bearish_average_directional_profit": _mean_or_zero(
            bearish,
            "directional_profit",
        ),
    }


def evaluate_final_test(
    model: dict[str, object],
    rows: pd.DataFrame,
    *,
    chunk_size: int = 25_000,
) -> FinalTestResult:
    required_model_keys = {"patterns", "feature_weights", "similarity_threshold"}
    missing_model_keys = sorted(required_model_keys - set(model))
    if missing_model_keys:
        raise ValueError(
            f"Locked model is missing fields: {', '.join(missing_model_keys)}"
        )
    required_row_columns = {"ticker", "date", "features_z", "return_3d"}
    missing_row_columns = sorted(required_row_columns - set(rows.columns))
    if missing_row_columns:
        raise ValueError(
            f"Final test rows are missing columns: {', '.join(missing_row_columns)}"
        )
    if rows.empty:
        raise ValueError("Final test rows must not be empty")

    dates = pd.to_datetime(rows["date"], errors="raise")
    if not dates.dt.year.eq(2026).all():
        raise ValueError("Final test rows must all be from 2026")

    patterns = pd.DataFrame(model["patterns"])
    weights = np.asarray(model["feature_weights"], dtype=float)
    threshold = float(model["similarity_threshold"])
    pattern_metrics, hits = backtest_patterns(
        patterns,
        rows.copy(),
        weights,
        threshold,
        chunk_size=chunk_size,
    )
    pattern_metrics = pattern_metrics.rename(
        columns={"occurrence_count": "number_of_matches"}
    )

    signals = hits.copy()
    if signals.empty:
        signals["conflict_signal"] = pd.Series(dtype=bool)
        trades = signals.copy()
        stock_metrics = _empty_stock_metrics()
    else:
        direction_count = signals.groupby(
            ["ticker", "date"],
            observed=True,
        )["direction"].nunique()
        conflicts = direction_count.loc[direction_count.gt(1)].index
        signal_keys = pd.MultiIndex.from_frame(signals[["ticker", "date"]])
        signals["conflict_signal"] = signal_keys.isin(conflicts)
        trades = (
            signals.loc[~signals["conflict_signal"]]
            .sort_values("distance", kind="stable")
            .drop_duplicates(["ticker", "date", "direction"])
        )
        if trades.empty:
            stock_metrics = _empty_stock_metrics()
        else:
            stock_metrics = (
                trades.groupby("ticker", observed=True)
                .agg(
                    number_of_signals=("success", "size"),
                    accuracy=("success", "mean"),
                    average_directional_profit=("directional_profit", "mean"),
                )
                .reset_index()
            )

    return FinalTestResult(
        signals=signals.reset_index(drop=True),
        pattern_metrics=pattern_metrics,
        stock_metrics=stock_metrics,
        overall_metrics=_overall_metrics(trades),
    )
