import numpy as np


def test_gui_loader_merges_validation_and_2026_metrics(display_fixture):
    from src.gui import load_gui_records

    records = load_gui_records(display_fixture)

    assert {
        "pattern_id",
        "validation_accuracy",
        "test_accuracy",
        "centroid_raw",
    } <= set(records.columns)
    assert len(records) == 2
    assert records["test_accuracy"].notna().all()


def test_relative_candles_return_valid_ohlc():
    from src.gui import relative_candles

    candles = relative_candles(
        [2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 1.0, 0.0, 0.0]
    )

    assert len(candles) == 2
    for open_, high, low, close in candles:
        assert high >= max(open_, close)
        assert low <= min(open_, close)
        assert np.isfinite([open_, high, low, close]).all()
