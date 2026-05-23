"""Analizor static de risc si prioritizator de teste pentru proiectul T10.

Modulul acopera cerinta T10 care cere un sistem capabil sa identifice automat
punctele critice din cod si sa prioritizeze testele in functie de acestea.
Foloseste AST-ul Python in loc de cautare simpla in text, pentru a putea analiza
structurat atribuiri, conditii, exceptii ridicate si expresii de return.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CriticalPoint:
    """Locatie din cod care merita acoperire de testare mai atenta."""

    line: int
    kind: str
    description: str
    risk: int
    terms: tuple[str, ...]


@dataclass(frozen=True)
class PrioritizedTest:
    """Functie de test imbogatita cu scor de risc si puncte critice acoperite."""

    path: str
    name: str
    line: int
    suite: str
    score: int
    matched_points: tuple[str, ...]


def _tokens(value: str) -> set[str]:
    """Imparte nume si expresii in termeni normalizati folositi la potrivire."""
    return {token for token in re.split(r"[^a-zA-Z0-9_]+", value.lower()) if token}


def _string_constants(node: ast.AST) -> set[str]:
    """Extrage literali string dintr-un nod AST, de exemplu 'express' sau 'rural'."""
    values: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            values.update(_tokens(child.value))
    return values


def _has_raise(node: ast.AST) -> bool:
    """Detecteaza daca o ramura ridica o exceptie, semn de logica de validare."""
    return any(isinstance(child, ast.Raise) for child in ast.walk(node))


def _changes_cost(node: ast.AST) -> bool:
    """Detecteaza daca o ramura modifica calculul costului de livrare."""
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
    """Identifica punctele riscante din codul sursa folosind reguli bazate pe AST."""
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    points: list[CriticalPoint] = []

    for node in ast.walk(tree):
        # O atribuire directa catre "cost" este tratata ca punct de tip formula.
        # In acest proiect, formula de baza este centrala: o modificare mica aici
        # afecteaza toate calculele valide ale costului de livrare.
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

        # Fiecare "if" poate reprezenta fie o validare de input, fie o regula
        # de business. O ramura cu "raise" este validare; o ramura care modifica
        # "cost" este o decizie de calcul.
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

        # Rotunjirea finala este importanta deoarece erorile de precizie pot
        # ramane invizibile cand testele folosesc doar valori intregi.
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
    """Asociaza numele fisierului de test cu suita afisata in raport."""
    if "manual" in path.name:
        return "manual"
    if "ai" in path.name:
        return "ai"
    if "random" in path.name:
        return "random"
    if "mutation" in path.name:
        return "final"
    return "other"


def collect_tests(tests_dir: Path) -> list[tuple[Path, ast.FunctionDef]]:
    """Colecteaza functiile de test pytest din directorul de teste."""
    tests: list[tuple[Path, ast.FunctionDef]] = []
    for path in sorted(tests_dir.glob("test_*.py")):
        # Testele prioritizatorului sunt excluse din raportul demo deoarece
        # valideaza acest tool, nu calculatorul de costuri de livrare.
        if "prioritizer" in path.name:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                tests.append((path, node))
    return tests


def prioritize_tests(source_path: Path, tests_dir: Path) -> list[PrioritizedTest]:
    """Ordoneaza testele dupa cate puncte riscante din sursa acopera."""
    critical_points = analyze_source(source_path)
    prioritized: list[PrioritizedTest] = []

    for path, test in collect_tests(tests_dir):
        # O euristica simpla leaga testele de punctele din sursa folosind termeni
        # din numele testului si constante string din corpul testului.
        test_terms = _tokens(test.name) | _string_constants(test)
        matched: list[CriticalPoint] = []

        for point in critical_points:
            if test_terms.intersection(point.terms):
                matched.append(point)

        # Scorul de baza este suma riscurilor punctelor acoperite. Suitele finale
        # si cele imbunatatite cu AI primesc un mic bonus deoarece au fost adaugate
        # explicit dupa analiza de coverage si mutation testing.
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
    """Randeaza analiza ca tabel Markdown potrivit pentru rapoarte si artefacte."""
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
