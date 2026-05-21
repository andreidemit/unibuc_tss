# T10 - Imbunatatirea testarii unitare cu IA

[![TSS Tests](https://github.com/andreidemit/unibuc_tss/actions/workflows/ci.yml/badge.svg)](https://github.com/andreidemit/unibuc_tss/actions/workflows/ci.yml)

Proiect pentru tema T10: imbunatatirea unei suite de teste unitare existente cu ajutorul IA, masurand efectul prin coverage, mutation testing si prioritizarea automata a testelor.

Badge-ul de mai sus indica starea pipeline-ului GitHub Actions. Verde inseamna ca instalarea, testele, coverage-ul si generarea artefactelor au trecut pe ultimul commit rulat in GitHub.

## Subject Under Test

Modulul testat este `src/shipping_calculator.py`, prin functia:

```python
calculate_shipping_cost(weight_kg, distance_km, delivery_type, customer_type, area_type) -> float
```

Acest modul este echivalentul practic al exemplului `linear_search` din cerinta deoarece are:

- inputuri controlabile: greutate, distanta, tip livrare, tip client, tip zona;
- output numeric verificabil: costul final de livrare;
- validari clare pentru input invalid;
- ramuri logice testabile pentru `express`, `same_day`, `premium` si `rural`;
- comportament suficient de simplu pentru evaluare academica.

## Reguli de calcul

- `weight_kg` si `distance_km` trebuie sa fie mai mari decat 0.
- `delivery_type` poate fi `standard`, `express` sau `same_day`.
- `customer_type` poate fi `regular` sau `premium`.
- `area_type` poate fi `urban` sau `rural`.
- Costul de baza este `10 + weight_kg * 2 + distance_km * 0.5`.
- `express` adauga 50%.
- `same_day` adauga 100%.
- `premium` aplica reducere de 20%.
- `rural` adauga taxa fixa de 15.
- Rezultatul este rotunjit la 2 zecimale.

## Structura proiectului

```text
src/
  shipping_calculator.py   # subject under test
  oracle.py                # oracol independent pentru random testing
  risk_prioritizer.py      # identificare puncte critice si prioritizare teste
tests/
  test_manual_basic.py
  test_ai_improved_cases.py
  test_mutation_focused_cases.py
  test_random.py
  test_risk_prioritizer.py
reports/
  *.html
  requirements_matrix.md
  manual_vs_random.md
  presentation_checklist.md
.github/workflows/ci.yml
```

## Instalare locala

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Rulare teste

```bash
python -m pytest -q
```

Sau:

```bash
scripts/run_tests.sh
```

## Coverage

Comanda principala folosita local si in CI:

```bash
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-fail-under=90
```

Aceasta masoara statement coverage si branch coverage. Pragul minim este 90%, configurat si in `pyproject.toml`.

Rezultatul HTML este generat in:

```text
htmlcov/index.html
```

## Black-box testing

Testele black-box verifica functia prin inputuri si outputuri asteptate, fara a depinde de implementarea interna.

| Clasa / partitie | Exemple |
| --- | --- |
| livrare valida standard | `standard`, `regular`, `urban` |
| tipuri de livrare valide | `standard`, `express`, `same_day` |
| tipuri client valide | `regular`, `premium` |
| tipuri zona valide | `urban`, `rural` |
| input numeric invalid | greutate sau distanta `<= 0` |
| input textual invalid | `overnight`, `gold`, `remote` |

Teste relevante: `tests/test_manual_basic.py`, `tests/test_ai_improved_cases.py`, `tests/test_random.py`.

## White-box testing

Testele white-box urmaresc ramurile din cod:

- validarea greutatii;
- validarea distantei;
- validarea tipului de livrare;
- validarea tipului de client;
- validarea tipului de zona;
- ramura `express`;
- ramura `same_day`;
- ramura `premium`;
- ramura `rural`;
- rotunjirea rezultatului final.

Teste relevante: `tests/test_ai_improved_cases.py` si `tests/test_mutation_focused_cases.py`.

## Random testing si oracol independent

Random testing-ul este in `tests/test_random.py` si foloseste seed fix:

```python
RANDOM_SEED = 42
VALID_RANDOM_CASES = 500
INVALID_RANDOM_CASES = 120
```

Oracolul independent este `src/oracle.py`. Testele random nu folosesc functia testata ca oracol; ele compara rezultatul din `calculate_shipping_cost` cu rezultatul calculat separat de `expected_shipping_cost`.

Rulare doar random testing:

```bash
python -m pytest tests/test_random.py -q
```

## Mutation testing

Tool-ul folosit este `mutmut`. Comanda stabila pentru Python 3.14/macOS este:

```bash
mutmut run --max-children 1
mutmut results
python scripts/generate_mutation_report.py
```

Raportul HTML este generat in:

```text
reports/mutation.html
```

Pentru rulare rapida:

```bash
scripts/run_mutation.sh
```

## Prioritizarea automata a testelor

Sistemul din `src/risk_prioritizer.py` foloseste `ast` pentru a identifica puncte critice:

- validari;
- formule;
- ramuri de decizie;
- rotunjirea rezultatului.

Rulare:

```bash
python scripts/prioritize_tests.py
```

Rezultatul este folosit ca dovada pentru cerinta T10 privind identificarea automata a punctelor critice si prioritizarea testelor.

## CI/CD

Pipeline-ul este definit in `.github/workflows/ci.yml` si ruleaza la:

- `push`;
- `pull_request`.

Pipeline-ul executa:

- checkout;
- setup Python 3.12;
- instalare dependente;
- teste cu statement si branch coverage;
- fail daca coverage < 90%;
- generare `htmlcov/`;
- upload artifact pentru coverage HTML;
- rulare mutation testing cu `continue-on-error: true`;
- generare raport mutation;
- upload artifact pentru `reports/` si `mutants/`.

Mutation testing-ul este pas separat deoarece poate dura mai mult si poate fi sensibil la platforma.

## Rapoarte

- [reports/index.html](reports/index.html)
- [reports/manual.html](reports/manual.html)
- [reports/ai.html](reports/ai.html)
- [reports/ai_usage.html](reports/ai_usage.html)
- [reports/final.html](reports/final.html)
- [reports/mutation.html](reports/mutation.html)
- [reports/priority.html](reports/priority.html)
- [reports/requirements_matrix.md](reports/requirements_matrix.md)
- [reports/manual_vs_random.md](reports/manual_vs_random.md)
- [reports/presentation_checklist.md](reports/presentation_checklist.md)

Raportul privind folosirea tool-urilor AI este disponibil in `AI_USAGE_REPORT.md` si `reports/ai_usage.html`.

## Matrice cerinta - dovada

Matricea completa este in [reports/requirements_matrix.md](reports/requirements_matrix.md).

## Dovezi necesare pentru prezentare

Checklist-ul complet este in [reports/presentation_checklist.md](reports/presentation_checklist.md).

## Referinte

[1] pytest, Documentation, https://docs.pytest.org/, Data ultimei accesari: 8 mai 2026.  
[2] Coverage.py, Documentation, https://coverage.readthedocs.io/, Data ultimei accesari: 8 mai 2026.  
[3] Mutmut, Documentation, https://mutmut.readthedocs.io/, Data ultimei accesari: 8 mai 2026.  
[4] OpenAI, ChatGPT, https://chatgpt.com/, Data generarii: 8 mai 2026.
