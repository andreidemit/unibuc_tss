# Checklist dovezi pentru prezentare

## Capturi locale

- `python -m pytest -q` cu toate testele verzi.
- `python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-fail-under=90`.
- `htmlcov/index.html` deschis in browser.
- `python -m pytest tests/test_manual_basic.py --cov=shipping_calculator --cov-branch --cov-report=term-missing --cov-fail-under=0`.
- `python -m pytest tests/test_random.py --cov=shipping_calculator --cov-branch --cov-report=term-missing --cov-fail-under=0`.
- `mutmut run --max-children 1`.
- `mutmut results`.
- `reports/mutation.html`.
- `python scripts/prioritize_tests.py`.
- `reports/manual_vs_random.md`.
- `reports/requirements_matrix.md`.

## Capturi GitHub Actions

- Pipeline verde pe `main`.
- Badge verde in README.
- Artifact `coverage-html`.
- Artifact `tss-reports`.
- Continut artifact: `reports/mutation.html`.
- Pipeline rosu dupa introducerea unui bug intentionat.
- Notificare de esec GitHub Actions sau ecranul din tab-ul Actions care arata failure.

## Bug intentionat recomandat pentru pipeline rosu

Pentru demonstratie, schimba temporar in `src/shipping_calculator.py`:

```python
cost *= 1.5
```

in:

```python
cost *= 1.4
```

Testele de mutation killers ar trebui sa pice, iar pipeline-ul trebuie sa devina rosu. Dupa captura, revino la valoarea corecta.

## Tabele / grafice de inclus in raport

- Tabel manual vs AI vs final.
- Tabel manual vs random.
- Grafic statement coverage: manual 71%, random 100%, final 100%.
- Grafic branch coverage: manual 61%, random 100%, final 100%.
- Grafic mutation testing: killed 43, survived 0.
- Matrice cerinta - dovada.
