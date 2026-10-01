"""Small, explicit configuration for the candlestick assignment."""

from __future__ import annotations


DOWNLOAD_START = "2018-01-01"
DOWNLOAD_END = "2027-01-01"

DISCOVERY_START = "2018-01-01"
DISCOVERY_END = "2023-12-31"
VALIDATION_START = "2024-01-01"
VALIDATION_END = "2025-12-31"
TEST_START = "2026-01-01"
TEST_END = "2026-12-31"


# Fixed Yuanta Taiwan 50 snapshot used by the assignment.
STOCK_TICKERS = (
    "1216.TW",
    "1303.TW",
    "2059.TW",
    "2301.TW",
    "2303.TW",
    "2308.TW",
    "2317.TW",
    "2327.TW",
    "2330.TW",
    "2344.TW",
    "2345.TW",
    "2357.TW",
    "2360.TW",
    "2368.TW",
    "2382.TW",
    "2383.TW",
    "2395.TW",
    "2408.TW",
    "2412.TW",
    "2449.TW",
    "2454.TW",
    "2603.TW",
    "2880.TW",
    "2881.TW",
    "2882.TW",
    "2883.TW",
    "2884.TW",
    "2885.TW",
    "2886.TW",
    "2887.TW",
    "2890.TW",
    "2891.TW",
    "2892.TW",
    "3008.TW",
    "3017.TW",
    "3037.TW",
    "3045.TW",
    "3231.TW",
    "3443.TW",
    "3653.TW",
    "3665.TW",
    "3711.TW",
    "4904.TW",
    "4958.TW",
    "5880.TW",
    "6446.TW",
    "6505.TW",
    "6669.TW",
    "7769.TW",
    "8046.TW",
)


# Fixed before viewing any 2026 result to avoid cherry-picking.
TEST_TICKERS = (
    "2330.TW",
    "2454.TW",
    "2308.TW",
    "2317.TW",
    "3711.TW",
    "2303.TW",
    "3037.TW",
    "2383.TW",
    "2881.TW",
    "2891.TW",
)


WEIGHT_PRESETS = {
    "equal": (1.0,) * 10,
    "shape_first": (
        1.5,
        1.5,
        1.5,
        1.0,
        1.0,
        1.0,
        1.25,
        1.25,
        0.75,
        0.75,
    ),
    "position_trend": (
        1.0,
        1.0,
        1.0,
        0.75,
        0.75,
        0.75,
        1.5,
        1.5,
        1.0,
        1.5,
    ),
}

SIMILARITY_THRESHOLDS = (0.6, 0.8, 1.0)
CLUSTER_DISTANCE_THRESHOLD = 1.0
MIN_OCCURRENCES = 10
MIN_ACCURACY = 0.55
RANDOM_SEED = 42
