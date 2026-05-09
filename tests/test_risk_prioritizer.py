from pathlib import Path

import pytest

test_prioritizer = pytest.importorskip("test_prioritizer")
analyze_source = test_prioritizer.analyze_source
prioritize_tests = test_prioritizer.prioritize_tests


ROOT = Path(__file__).resolve().parents[1]


def test_analyzer_finds_validation_decision_formula_and_output_points():
    points = analyze_source(ROOT / "src" / "shipping_calculator.py")
    kinds = {point.kind for point in points}

    assert {"validation", "decision", "formula", "output"}.issubset(kinds)


def test_prioritizer_places_high_risk_tests_first():
    prioritized = prioritize_tests(
        source_path=ROOT / "src" / "shipping_calculator.py",
        tests_dir=ROOT / "tests",
    )

    assert prioritized[0].score >= prioritized[-1].score
    assert any(test.suite == "final" for test in prioritized[:5])
