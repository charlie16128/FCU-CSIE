from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml


def _as_date(value: Any, default: date) -> date:
    if value is None:
        return default
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


@dataclass(frozen=True)
class DateRanges:
    download_start: date = date(2018, 1, 1)
    download_end: date = date(2027, 1, 1)
    discovery_start: date = date(2018, 1, 1)
    discovery_end: date = date(2023, 12, 31)
    validation_start: date = date(2024, 1, 1)
    validation_end: date = date(2025, 12, 31)
    test_start: date = date(2026, 1, 1)
    test_end: date = date(2026, 12, 31)

    def __post_init__(self) -> None:
        if self.discovery_end >= self.validation_start:
            raise ValueError("Discovery and validation ranges overlap")
        if self.validation_end >= self.test_start:
            raise ValueError("Validation and final-test ranges overlap")


@dataclass(frozen=True)
class Settings:
    project_root: Path
    dates: DateRanges = field(default_factory=DateRanges)
    cluster_distance_threshold: float = 1.0
    cluster_warning_minimum: int = 20
    cluster_warning_maximum: int = 300
    weight_values: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0)
    similarity_thresholds: tuple[float, ...] = tuple(
        round(value / 10, 1) for value in range(4, 15)
    )
    minimum_occurrences: tuple[int, ...] = (30, 25, 20)
    minimum_accuracies: tuple[float, ...] = (0.60, 0.58, 0.55)
    dedup_thresholds: tuple[float, ...] = (0.30, 0.25, 0.20)
    download_retries: int = 3
    retry_backoff_seconds: float = 1.0
    random_seed: int = 42
    distance_chunk_size: int = 25_000


def load_settings(path: Path) -> Settings:
    path = path.resolve()
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    dates_raw = raw.get("dates", {})
    defaults = DateRanges()
    ranges = DateRanges(
        download_start=_as_date(
            dates_raw.get("download_start"), defaults.download_start
        ),
        download_end=_as_date(dates_raw.get("download_end"), defaults.download_end),
        discovery_start=_as_date(
            dates_raw.get("discovery_start"), defaults.discovery_start
        ),
        discovery_end=_as_date(
            dates_raw.get("discovery_end"), defaults.discovery_end
        ),
        validation_start=_as_date(
            dates_raw.get("validation_start"), defaults.validation_start
        ),
        validation_end=_as_date(
            dates_raw.get("validation_end"), defaults.validation_end
        ),
        test_start=_as_date(dates_raw.get("test_start"), defaults.test_start),
        test_end=_as_date(dates_raw.get("test_end"), defaults.test_end),
    )
    clustering = raw.get("clustering", {})
    validation = raw.get("validation", {})
    selection = raw.get("selection", {})
    download = raw.get("download", {})
    runtime = raw.get("runtime", {})
    return Settings(
        project_root=path.parent.parent,
        dates=ranges,
        cluster_distance_threshold=float(
            clustering.get("distance_threshold", 1.0)
        ),
        cluster_warning_minimum=int(clustering.get("warning_minimum", 20)),
        cluster_warning_maximum=int(clustering.get("warning_maximum", 300)),
        weight_values=tuple(
            map(float, validation.get("weight_values", (0.5, 1.0, 1.5, 2.0)))
        ),
        similarity_thresholds=tuple(
            map(
                float,
                validation.get(
                    "similarity_thresholds",
                    tuple(round(value / 10, 1) for value in range(4, 15)),
                ),
            )
        ),
        minimum_occurrences=tuple(
            map(int, selection.get("minimum_occurrences", (30, 25, 20)))
        ),
        minimum_accuracies=tuple(
            map(float, selection.get("minimum_accuracies", (0.60, 0.58, 0.55)))
        ),
        dedup_thresholds=tuple(
            map(float, selection.get("dedup_thresholds", (0.30, 0.25, 0.20)))
        ),
        download_retries=int(download.get("retries", 3)),
        retry_backoff_seconds=float(download.get("retry_backoff_seconds", 1.0)),
        random_seed=int(runtime.get("random_seed", 42)),
        distance_chunk_size=int(runtime.get("distance_chunk_size", 25_000)),
    )
