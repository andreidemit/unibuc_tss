"""Static risk analyzer and test prioritizer for the T10 project."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CriticalPoint:
    line: int
    kind: str
    description: str
    risk: int
    terms: tuple[str, ...]


@dataclass(frozen=True)
class PrioritizedTest:
    path: str
    name: str
    line: int
    suite: str
    score: int
    matched_points: tuple[str, ...]


def _tokens(value: str) -> set[str]:
    return {token for token in re.split(r"[^a-zA-Z0-9_]+", value.lower()) if token}


def _string_constants(node: ast.AST) -> set[str]:
    values: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            values.update(_tokens(child.value))
    return values


def _has_raise(node: ast.AST) -> bool:
    return any(isinstance(child, ast.Raise) for child in ast.walk(node))


def _changes_cost(node: ast.AST) -> bool:
    for child in ast.walk(node):
        if isinstance(child, ast.AugAssign) and isinstance(child.target, ast.Name):
            if child.target.id == "cost":
                return True
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name) and target.id == "cost":
                    return True
    return False


def analyze_source(source_path: Path) -> list[CriticalPoint]:
    """Identify risky code points from the production source using AST rules."""
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    points: list[CriticalPoint] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = [target.id for target in node.targets if isinstance(target, ast.Name)]
            if "cost" in targets:
                points.append(
                    CriticalPoint(
                        line=node.lineno,
                        kind="formula",
                        description="Formula de baza pentru cost",
                        risk=5,
                        terms=("standard", "cost", "weight_kg", "distance_km"),
                    )
                )

        if isinstance(node, ast.If):
            condition = ast.unparse(node.test)
            condition_terms = tuple(sorted(_tokens(condition) | _string_constants(node.test)))
            if _has_raise(node):
                points.append(
                    CriticalPoint(
                        line=node.lineno,
                        kind="validation",
                        description=f"Validare input: {condition}",
                        risk=5,
                        terms=condition_terms,
                    )
                )
            elif _changes_cost(node):
                points.append(
                    CriticalPoint(
                        line=node.lineno,
                        kind="decision",
                        description=f"Ramura de calcul: {condition}",
                        risk=4,
                        terms=condition_terms,
                    )
                )

        if isinstance(node, ast.Return):
            expression = ast.unparse(node.value) if node.value else ""
            if "round" in expression:
                points.append(
                    CriticalPoint(
                        line=node.lineno,
                        kind="output",
                        description="Rotunjire rezultat final la 2 zecimale",
                        risk=4,
                        terms=("round", "rounding", "decimals", "stable"),
                    )
                )

    return sorted(points, key=lambda point: (-point.risk, point.line))


def _suite_for_path(path: Path) -> str:
    if "manual" in path.name:
        return "manual"
    if "ai" in path.name:
        return "ai"
    if "mutation" in path.name:
        return "final"
    return "other"


def collect_tests(tests_dir: Path) -> list[tuple[Path, ast.FunctionDef]]:
    tests: list[tuple[Path, ast.FunctionDef]] = []
    for path in sorted(tests_dir.glob("test_*.py")):
        if "prioritizer" in path.name:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                tests.append((path, node))
    return tests


def prioritize_tests(source_path: Path, tests_dir: Path) -> list[PrioritizedTest]:
    """Rank tests by how many high-risk source points they exercise."""
    critical_points = analyze_source(source_path)
    prioritized: list[PrioritizedTest] = []

    for path, test in collect_tests(tests_dir):
        test_terms = _tokens(test.name) | _string_constants(test)
        matched: list[CriticalPoint] = []

        for point in critical_points:
            if test_terms.intersection(point.terms):
                matched.append(point)

        score = sum(point.risk for point in matched)
        if _suite_for_path(path) == "final":
            score += 2
        elif _suite_for_path(path) == "ai":
            score += 1

        prioritized.append(
            PrioritizedTest(
                path=str(path),
                name=test.name,
                line=test.lineno,
                suite=_suite_for_path(path),
                score=score,
                matched_points=tuple(point.description for point in matched),
            )
        )

    return sorted(prioritized, key=lambda test: (-test.score, test.path, test.line))


def render_markdown(source_path: Path, tests_dir: Path) -> str:
    critical_points = analyze_source(source_path)
    prioritized = prioritize_tests(source_path, tests_dir)

    lines = [
        "# Raport prioritizare teste",
        "",
        "## Puncte critice identificate automat",
        "",
        "| Linie | Tip | Risc | Descriere |",
        "| --- | --- | ---: | --- |",
    ]
    for point in critical_points:
        lines.append(f"| {point.line} | {point.kind} | {point.risk} | {point.description} |")

    lines.extend(
        [
            "",
            "## Teste prioritizate",
            "",
            "| Prioritate | Suita | Test | Scor | Puncte acoperite |",
            "| ---: | --- | --- | ---: | --- |",
        ]
    )
    for index, test in enumerate(prioritized, start=1):
        matched = "; ".join(test.matched_points) or "fara punct critic detectat"
        lines.append(f"| {index} | {test.suite} | `{test.name}` | {test.score} | {matched} |")

    return "\n".join(lines) + "\n"
