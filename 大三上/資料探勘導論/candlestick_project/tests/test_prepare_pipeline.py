import pandas as pd

from src.build_features import FEATURE_COLUMNS
from src.pipeline import prepare_data


def test_prepare_writes_one_processed_file(tmp_project, sample_ohlcv):
    sample_ohlcv.drop(columns=["pattern_eligible"]).to_csv(
        tmp_project / "data/raw/2330.TW.csv"
    )

    summary = prepare_data(tmp_project)

    assert summary["successful"] == 1
    assert summary["failed"] == 0
    output_path = tmp_project / "data/processed/2330.TW.csv"
    assert output_path.exists()
    processed = pd.read_csv(output_path)
    assert {"Date", "pattern_eligible", "return_3d", *FEATURE_COLUMNS} <= set(
        processed.columns
    )


def test_prepare_continues_after_malformed_file(tmp_project, sample_ohlcv):
    sample_ohlcv.drop(columns=["pattern_eligible"]).to_csv(
        tmp_project / "data/raw/GOOD.TW.csv"
    )
    pd.DataFrame({"Date": ["2020-01-01"], "Close": [100]}).to_csv(
        tmp_project / "data/raw/BAD.TW.csv", index=False
    )

    summary = prepare_data(tmp_project)

    assert summary["successful"] == 1
    assert summary["failed"] == 1
    assert summary["failed_tickers"] == ["BAD.TW"]
    assert (tmp_project / "data/processed/GOOD.TW.csv").exists()
