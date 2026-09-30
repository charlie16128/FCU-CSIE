import pandas as pd

from src.pipeline import _decode_vectors
from src.utils import write_csv


def test_structured_pattern_columns_round_trip_as_json(tmp_path):
    frame = pd.DataFrame(
        [
            {
                "pattern_id": "bullish_01",
                "centroid_z": [0.0] * 10,
                "centroid_raw": [1.0] * 10,
                "source_candidates": [
                    {"ticker": "2330.TW", "date": "2023-01-03"}
                ],
            }
        ]
    )
    path = tmp_path / "patterns.csv"

    write_csv(frame, path)
    decoded = _decode_vectors(pd.read_csv(path))

    assert decoded.loc[0, "centroid_z"] == [0.0] * 10
    assert decoded.loc[0, "source_candidates"] == [
        {"ticker": "2330.TW", "date": "2023-01-03"}
    ]
