from datetime import date
from pathlib import Path

from src.settings import DateRanges, Settings, load_settings
from src.utils import load_tickers


def test_periods_are_non_overlapping():
    ranges = DateRanges()

    assert ranges.discovery_end < ranges.validation_start
    assert ranges.validation_end < ranges.test_start


def test_fixed_universes_have_required_sizes(project_root: Path):
    tickers = load_tickers(project_root / "config/tickers.txt")
    test_tickers = load_tickers(project_root / "config/test_tickers.txt")

    assert len(tickers) == 50
    assert len(set(tickers)) == 50
    assert len(test_tickers) >= 10
    assert set(test_tickers) <= set(tickers)


def test_load_settings_resolves_paths_and_exact_ranges(project_root: Path):
    settings = load_settings(project_root / "config/settings.yaml")

    assert isinstance(settings, Settings)
    assert settings.project_root == project_root
    assert settings.dates.discovery_start == date(2018, 1, 1)
    assert settings.dates.discovery_end == date(2023, 12, 31)
    assert settings.dates.validation_start == date(2024, 1, 1)
    assert settings.dates.validation_end == date(2025, 12, 31)
    assert settings.dates.test_start == date(2026, 1, 1)
    assert settings.similarity_thresholds == tuple(
        round(value / 10, 1) for value in range(4, 15)
    )
