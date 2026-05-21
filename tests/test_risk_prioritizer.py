from pathlib import Path

import pytest

risk_prioritizer = pytest.importorskip("risk_prioritizer")
analyze_source = risk_prioritizer.analyze_source
prioritize_tests = risk_prioritizer.prioritize_tests
render_markdown = risk_prioritizer.render_markdown


ROOT = Path(__file__).resolve().parents[1]


def test_analyzer_finds_validation_decision_formula_and_output_points():
    points = analyze_source(ROOT / "src" / "shipping_calculator.py")
    kinds = {point.kind for point in points}

    assert {"validation", "decision", "formula", "output"}.issubset(kinds)


def test_risk_prioritizer_places_high_risk_tests_first():
    prioritized = prioritize_tests(
        source_path=ROOT / "src" / "shipping_calculator.py",
        tests_dir=ROOT / "tests",
    )

    assert prioritized[0].score >= prioritized[-1].score
    assert any(test.suite == "final" for test in prioritized[:5])


def test_render_markdown_contains_critical_points_and_prioritized_tests():
    report = render_markdown(
        source_path=ROOT / "src" / "shipping_calculator.py",
        tests_dir=ROOT / "tests",
    )

    assert "# Raport prioritizare teste" in report
    assert "Puncte critice identificate automat" in report
    assert "Teste prioritizate" in report
    assert "Validare input" in report


def test_analyzer_detects_assignment_based_cost_changes(tmp_path):
    source = tmp_path / "assignment_based_calculator.py"
    source.write_text(
        """
def calculate(flag):
    cost = 10
    if flag:
        cost = 20
    if flag is None:
        ignored = 30
    return round(cost, 2)
""",
        encoding="utf-8",
    )

    points = analyze_source(source)
    descriptions = [point.description for point in points]

    assert any("flag" in description for description in descriptions)
    assert any(point.kind == "decision" for point in points)
