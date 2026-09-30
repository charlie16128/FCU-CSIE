from __future__ import annotations

import argparse
from pathlib import Path
from collections.abc import Sequence

from src import gui, pipeline


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Candlestick pattern discovery pipeline"
    )
    value.add_argument("--download", action="store_true", help="Download raw OHLCV")
    value.add_argument("--prepare", action="store_true", help="Clean and build features")
    value.add_argument("--train", action="store_true", help="Discover and cluster patterns")
    value.add_argument("--validate", action="store_true", help="Search and lock Top 10")
    value.add_argument("--test", action="store_true", help="Run locked 2026 evaluation")
    value.add_argument("--gui", action="store_true", help="Open the read-only explorer")
    value.add_argument(
        "--all",
        action="store_true",
        help="Run all data stages in order (does not open GUI)",
    )
    return value


def run(
    argv: Sequence[str] | None = None,
    *,
    project_root: Path | None = None,
) -> int:
    args = parser().parse_args(argv)
    root = (project_root or Path(__file__).resolve().parent).resolve()
    if args.all or args.download:
        pipeline.download_data(root)
    if args.all or args.prepare:
        pipeline.prepare_data(root)
    if args.all or args.train:
        pipeline.train_patterns(root)
    if args.all or args.validate:
        pipeline.validate_patterns(root)
    if args.all or args.test:
        pipeline.test_patterns(root)
    if args.gui:
        gui.launch_gui(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
