#!/usr/bin/env python3
"""Print the automatic critical-point and test-priority report."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from test_prioritizer import render_markdown


def main() -> int:
    report = render_markdown(
        source_path=ROOT / "src" / "shipping_calculator.py",
        tests_dir=ROOT / "tests",
    )
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
