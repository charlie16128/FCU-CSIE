"""Command-line entry point for the simplified candlestick assignment."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from data_loader import download_project
from gui import launch_gui
from kline_analysis import analyze_project, test_project


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Discover and test candlestick patterns"
    )
    value.add_argument("--download", action="store_true", help="Download 50 stocks")
    value.add_argument(
        "--analyze",
        action="store_true",
        help="Build features and select bullish/bearish Top 10",
    )
    value.add_argument(
        "--test",
        action="store_true",
        help="Evaluate the locked patterns on fixed 2026 stocks",
    )
    value.add_argument("--gui", action="store_true", help="Open saved results")
    value.add_argument(
        "--all",
        action="store_true",
        help="Run download, analysis, and 2026 test in order",
    )
    return value


def run(
    argv: Sequence[str] | None = None,
    *,
    project_root: Path | None = None,
) -> int:
    command = parser()
    args = command.parse_args(argv)
    root = (project_root or Path(__file__).resolve().parent).resolve()
    if not any((args.download, args.analyze, args.test, args.gui, args.all)):
        command.print_help()
        return 0
    if args.all or args.download:
        print(download_project(root))
    if args.all or args.analyze:
        print(analyze_project(root))
    if args.all or args.test:
        print(test_project(root))
    if args.gui:
        launch_gui(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
