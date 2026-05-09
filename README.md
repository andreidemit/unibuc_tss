# T10 - Imbunatatirea testarii unitare cu IA

Proiect demonstrativ pentru tema T10: folosirea unui tool AI pentru imbunatatirea unei suite de teste unitare.

Modulul testat este `ShippingCostCalculator`, implementat prin functia:

```python
calculate_shipping_cost(weight_kg, distance_km, delivery_type, customer_type, area_type) -> float
```

## Reguli de calcul

- `weight_kg` si `distance_km` trebuie sa fie mai mari decat 0.
- `delivery_type` poate fi `standard`, `express` sau `same_day`.
- `customer_type` poate fi `regular` sau `premium`.
- `area_type` poate fi `urban` sau `rural`.
- Costul de baza este `10 + weight_kg * 2 + distance_km * 0.5`.
- `express` adauga 50%.
- `same_day` adauga 100%.
- `premium` aplica o reducere de 20%.
- `rural` adauga o taxa fixa de 15.
- Rezultatul este rotunjit la 2 zecimale.

## Instalare

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Rulare demonstrativa

```bash
python -m pytest tests/test_manual_basic.py --cov=shipping_calculator --cov-report=term-missing
```

In aceasta etapa ruleaza doar testele manuale de baza. Testele trec, dar coverage-ul este incomplet.

Pentru etapa AI:

```bash
python -m pytest tests/test_manual_basic.py tests/test_ai_generated.py --cov=shipping_calculator --cov-report=term-missing
```

Pentru etapa finala:

```bash
python -m pytest tests/test_manual_basic.py tests/test_ai_generated.py tests/test_mutation_killers.py --cov=shipping_calculator --cov-report=term-missing
mutmut run --max-children 1
mutmut results
python scripts/generate_mutation_report.py
```

Rezultatele experimentului sunt disponibile ca fisiere HTML simple:

- [reports/index.html](reports/index.html)
- [reports/manual.html](reports/manual.html)
- [reports/ai.html](reports/ai.html)
- [reports/final.html](reports/final.html)
- [reports/mutation.html](reports/mutation.html)
- [reports/priority.html](reports/priority.html)

Raportul privind folosirea tool-urilor AI este disponibil in [AI_USAGE_REPORT.md](AI_USAGE_REPORT.md).

## Strategia de testare

Etapa initiala foloseste o suita manuala minima:

| Caz | Scop |
| --- | --- |
| livrare standard valida | verifica formula de baza |
| greutate negativa | verifica o validare |
| livrare express | verifica o ramura de decizie |

Ramuri omise intentionat in etapa initiala:

- `same_day`;
- `premium`;
- `rural`;
- validarea distantei;
- validarea tipurilor necunoscute.

## Imbunatatirea cu ChatGPT

Promptul folosit si comparatia dintre suite sunt documentate in [AI_USAGE_REPORT.md](AI_USAGE_REPORT.md) si in [reports/ai.html](reports/ai.html).

| Etapa | Ce demonstreaza |
| --- | --- |
| Manual | Suita manuala minima, coverage incomplet |
| AI | Teste inspirate de ChatGPT pentru ramuri si validari omise |
| Final | Teste suplimentare orientate spre mutation testing |

Pentru raport se vor include capturi de ecran cu rezultatele comenzilor:

```bash
python -m pytest tests/test_manual_basic.py --cov=shipping_calculator --cov-report=term-missing
python -m pytest tests/test_manual_basic.py tests/test_ai_generated.py --cov=shipping_calculator --cov-report=term-missing
python -m pytest tests/test_manual_basic.py tests/test_ai_generated.py tests/test_mutation_killers.py --cov=shipping_calculator --cov-report=term-missing
mutmut run --max-children 1
mutmut results
python scripts/generate_mutation_report.py
```

## Sistem automat de prioritizare

Proiectul include si un sistem care identifica automat punctele critice ale codului si prioritizeaza testele:

```bash
python scripts/prioritize_tests.py
```

Sistemul din `src/test_prioritizer.py` foloseste `ast` pentru a detecta:

- validarile de input;
- formula de calcul;
- ramurile de decizie;
- rotunjirea rezultatului final.

Fiecare punct critic primeste un scor de risc, apoi testele sunt ordonate dupa punctele critice pe care le acopera. Rezultatul este prezentat in [reports/priority.html](reports/priority.html).

## Teste finale pentru mutanti

Etapa finala adauga teste orientate spre mutanti:

| Test | Mutatie vizata |
| --- | --- |
| valori pozitive foarte mici | schimbari in comparatiile `<= 0` |
| multiplicator express exact | schimbari ale multiplicatorului `1.5` |
| multiplicator same_day exact | schimbari ale multiplicatorului `2` |
| premium dupa multiplicator | schimbarea ordinii de aplicare a regulilor |
| rural dupa discount | schimbarea ordinii taxei rurale |
| rotunjire la 2 zecimale | eliminarea sau modificarea `round(..., 2)` |
| mesaje exacte pentru erori | mutanti care modifica mesajele `ValueError` |

## Cazuri greu de prins manual

Un rezultat important al proiectului este diferenta dintre coverage si calitatea asertiunilor. O suita poate executa codul, dar poate rata mutanti daca testele sunt prea generale.

Exemple tratate in suita finala:

| Problema | De ce poate scapa | Test care o detecteaza |
| --- | --- | --- |
| `weight_kg <= 0` devine `weight_kg < 0` | Un test cu `-1` nu verifica frontiera `0` | teste pentru `0` si valori pozitive foarte mici |
| multiplicatorul express este modificat | O comparatie de tip “mai scump decat standard” nu verifica formula exacta | `test_express_multiplier_is_exactly_one_point_five` |
| premium si rural interactioneaza gresit | Testele separate nu verifica ordinea aplicarii regulilor | `test_rural_fee_is_added_after_premium_discount` |
| rotunjirea este eliminata | Valorile intregi nu expun problema | `test_rounding_to_two_decimals_is_stable` |

## Referinte

[1] pytest, Documentation, https://docs.pytest.org/, Data ultimei accesari: 8 mai 2026.  
[2] Coverage.py, Documentation, https://coverage.readthedocs.io/, Data ultimei accesari: 8 mai 2026.  
[3] Mutmut, Documentation, https://mutmut.readthedocs.io/, Data ultimei accesari: 8 mai 2026.  
[4] OpenAI, ChatGPT, https://chatgpt.com/, Data generarii: 8 mai 2026.
