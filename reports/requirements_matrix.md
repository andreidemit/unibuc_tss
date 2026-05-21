# Matrice cerinta - dovada

| Cerinta | Fisier / comanda / dovada | Status | Observatii |
| --- | --- | --- | --- |
| Subject Under Test clar | `src/shipping_calculator.py`, `calculate_shipping_cost` | Indeplinit | Echivalent practic pentru exemplul `linear_search`. |
| Specificatie input/output | `README.md`, sectiunile Subject Under Test si Reguli de calcul | Indeplinit | Include inputuri valide, output numeric si reguli de validare. |
| Black-box tests | `tests/test_manual_basic.py`, `tests/test_ai_improved_cases.py`, `tests/test_random.py` | Indeplinit | Acopera clase valide si invalide. |
| Partitionare de echivalenta | `README.md`, sectiunea Black-box testing | Indeplinit | Sunt documentate partitiile principale. |
| Valori de frontiera | `tests/test_mutation_focused_cases.py` | Indeplinit | Include `0`, valori negative si valori pozitive foarte mici. |
| White-box tests | `tests/test_ai_improved_cases.py`, `tests/test_mutation_focused_cases.py` | Indeplinit | Sunt acoperite ramurile `express`, `same_day`, `premium`, `rural` si validarile. |
| Random tests | `tests/test_random.py` | Indeplinit | 500 cazuri valide si 120 cazuri invalide, seed 42. |
| Oracol independent | `src/oracle.py` | Indeplinit | Nu apeleaza `calculate_shipping_cost`. |
| Statement coverage | `python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-fail-under=90` | Indeplinit | Rulare locala: 99.19% total pe `src`, 100% pe SUT. |
| Branch coverage | Aceeasi comanda coverage | Indeplinit | Branch coverage activ prin `--cov-branch` si `pyproject.toml`. |
| Prag coverage | `pyproject.toml`, `--cov-fail-under=90` | Indeplinit | Pipeline-ul esueaza sub 90%. |
| Mutation testing | `pyproject.toml`, `mutmut run --max-children 1` | Indeplinit local | Comanda stabila pentru Python 3.14/macOS. |
| Raport mutation | `scripts/generate_mutation_report.py`, `reports/mutation.html` | Indeplinit | Genereaza raport HTML din metadata mutmut. |
| Mutanti supravietuitori analizati | `reports/mutation.html` | Indeplinit pentru rularea curenta | Rularea locala curenta indica 0 supravietuitori. |
| Sistem identificare puncte critice | `src/risk_prioritizer.py` | Indeplinit | Analizeaza AST si identifica validari, formule, decizii si output. |
| Prioritizare teste | `python scripts/prioritize_tests.py` | Indeplinit | Ordoneaza testele dupa punctele critice acoperite. |
| CI/CD la push | `.github/workflows/ci.yml` | Necesita rulare in GitHub Actions | Workflow-ul este definit pentru `push` si `pull_request`. |
| Instalare dependente in CI | `.github/workflows/ci.yml` | Necesita rulare in GitHub Actions | Foloseste `python -m pip install -r requirements.txt`. |
| Fail daca testele pica | `.github/workflows/ci.yml` | Necesita rulare in GitHub Actions | Pasul pytest esueaza pipeline-ul. |
| Coverage artifact | `.github/workflows/ci.yml`, artifact `coverage-html` | Necesita rulare in GitHub Actions | Upload pentru `htmlcov/`. |
| Mutation artifact | `.github/workflows/ci.yml`, artifact `tss-reports` | Necesita rulare in GitHub Actions | Upload pentru `reports/` si `mutants/`. |
| Badge README | `README.md` | Indeplinit | Badge GitHub Actions adaugat. |
| Notificare esec pipeline | GitHub Actions UI / email | Necesita dovada manuala | Se demonstreaza printr-un commit/branch cu bug intentionat. |
| Screenshots prezentare | `reports/presentation_checklist.md` | Indeplinit ca lista | Capturile trebuie facute dupa rularea in GitHub. |
| Raport AI | `AI_USAGE_REPORT.md`, `reports/ai_usage.html` | Indeplinit | Include prompturi, rolul AI si interpretare. |
| Comparatie manual vs random | `reports/manual_vs_random.md` | Indeplinit | Include numar teste, statement coverage si branch coverage. |
