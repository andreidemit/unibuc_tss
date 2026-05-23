# Raport privind folosirea tool-urilor AI

## Context

Proiectul are ca scop imbunatatirea unei suite de teste unitare pentru modulul `ShippingCostCalculator`. Modulul calculeaza costul de livrare in functie de greutate, distanta, tipul livrarii, tipul clientului si zona de livrare.

Tool-ul AI folosit a fost ChatGPT. Acesta a fost utilizat ca instrument de asistare pentru:

- identificarea ramurilor netestate;
- propunerea unor cazuri de test pentru cresterea coverage-ului;
- identificarea unor mutanti care pot supravietui unor teste prea generale;
- structurarea ideii de prioritizare a testelor dupa puncte critice;
- organizarea raportului de prezentare.

AI-ul nu a fost folosit ca sursa finala de adevar. Codul, valorile asteptate si rezultatele au fost validate prin rulare locala cu `pytest`, `pytest-cov` si `mutmut`.

## Tool AI utilizat

| Tool | Scop | Perioada utilizarii |
| --- | --- | --- |
| ChatGPT | Generare idei, imbunatatire teste unitare, analiza mutanti, structurare raport | 9-23 mai 2026 |

Nu au fost preluate automat rezultate fara verificare. Valorile asteptate din teste au fost recalculate pe baza formulei din specificatie, iar fiecare modificare a fost verificata prin testare automata.

## Prompt 1: cresterea acoperirii codului

```text
Am urmatoarea functie Python pentru calculul costului de livrare:

def calculate_shipping_cost(weight_kg, distance_km, delivery_type, customer_type, area_type):
    # weight_kg si distance_km trebuie sa fie > 0
    # delivery_type: standard, express, same_day
    # customer_type: regular, premium
    # area_type: urban, rural
    # base cost = 10 + weight_kg * 2 + distance_km * 0.5
    # express adauga 50%, same_day adauga 100%
    # premium aplica reducere 20%, rural adauga taxa fixa 15

Te rog sa propui teste unitare pytest care cresc acoperirea codului. Include cazuri pentru:
- same_day;
- premium;
- rural;
- combinatii intre reguli;
- inputuri numerice invalide;
- tipuri necunoscute pentru delivery_type, customer_type si area_type.
```

## Raspuns AI sintetizat

ChatGPT a propus:

- teste pentru `same_day`, `premium` si `rural`;
- teste pentru combinatii intre reguli;
- teste parametrizate pentru valori numerice invalide;
- teste pentru tipuri necunoscute de livrare, client si zona;
- folosirea `pytest.raises` pentru validari.

Aceste idei au fost transformate in testele din `tests/test_ai_improved_cases.py`.

## Prompt 2: imbunatatirea testelor pe baza mutation testing

```text
Am obtinut coverage bun, dar vreau teste mai puternice pentru mutation testing.
Ce tipuri de mutanti ar putea supravietui daca testele sunt prea generale?

Functia are:
- validari de tip <= 0;
- multiplicatori pentru express si same_day;
- reducere premium;
- taxa rurala;
- rotunjire la doua zecimale.

Propune teste pytest care verifica frontiere, valori exacte, combinatii de reguli si rotunjire.
```

## Raspuns AI sintetizat

ChatGPT a sugerat ca testele generale pot rata:

- mutanti de frontiera, de exemplu `<= 0` schimbat in `< 0`;
- mutanti care modifica multiplicatorii;
- mutanti care schimba ordinea aplicarii reducerii premium si a taxei rurale;
- mutanti care elimina sau modifica rotunjirea;
- mutanti care modifica mesajele de eroare.

Aceste idei au fost transformate in testele din `tests/test_mutation_focused_cases.py`.

## Prompt 3: puncte critice si prioritizarea testelor

```text
Pentru aceeasi functie de calcul al costului de livrare, vreau o metoda simpla
prin care sa identific automat punctele critice din cod si sa prioritizez testele.

Punctele importante sunt:
- validari de input;
- formula de baza;
- ramuri de decizie pentru express, same_day, premium si rural;
- rotunjirea rezultatului final.

Propune o abordare implementabila in Python, usor de explicat la prezentare.
```

## Raspuns AI sintetizat

ChatGPT a sugerat o abordare bazata pe analiza statica:

- parsarea codului cu `ast`;
- detectarea validarii prin ramuri care contin `raise`;
- detectarea formulei prin atribuiri catre `cost`;
- detectarea deciziilor prin ramuri care modifica `cost`;
- acordarea unui scor de risc pentru fiecare punct;
- prioritizarea testelor in functie de termenii pe care ii acopera.

Ideea a fost implementata in `src/risk_prioritizer.py` si verificata prin `tests/test_risk_prioritizer.py`. Rezultatul este generat cu:

```bash
python scripts/prioritize_tests.py
```

## Contributie AI vs validare umana

| Contributie AI | Validare umana | Rezultat in proiect |
| --- | --- | --- |
| A propus teste pentru ramuri omise | Valorile asteptate au fost recalculate dupa formula oficiala | `tests/test_ai_improved_cases.py` |
| A sugerat categorii de mutanti greu de prins | Testele au fost rulate cu `mutmut` | `tests/test_mutation_focused_cases.py` |
| A sugerat analiza punctelor critice | Implementarea a fost adaptata la codul proiectului si testata | `src/risk_prioritizer.py` |
| A ajutat la structurarea rapoartelor | Au fost pastrate doar informatiile relevante pentru cerinta | `reports/requirements_matrix.md`, `reports/manual_vs_random.md` |
| A sugerat clarificarea rolului fiecarei suite | README-ul a fost actualizat pentru prezentare | `README.md` |

## Comparatie intre suitele de teste

| Aspect | Suita manuala initiala | Suita imbunatatita cu AI | Suita orientata pe mutanti | Suita completa proiect |
| --- | --- | --- | --- | --- |
| Numar teste | 3 | 13 | 25 | 650 |
| Coverage pe `shipping_calculator.py` | 67% | 100% | 100% | 100% |
| Teste pentru `same_day` | Nu | Da | Da | Da |
| Teste pentru `premium` | Nu | Da | Da | Da |
| Teste pentru `rural` | Nu | Da | Da | Da |
| Teste pentru inputuri invalide | Partial | Da | Da | Da |
| Teste pentru valori de frontiera | Nu | Partial | Da | Da |
| Teste pentru mutation testing | Nu | Partial | Da | Da |
| Random testing | Nu | Nu | Nu | Da |
| Oracol independent | Nu | Nu | Nu | Da |
| Mutanti omorati | Nu a fost scopul suitei initiale | Imbunatatire partiala | 43/43 | 43/43 |

## Exemple de cazuri greu de prins manual

| Mutatie posibila | De ce poate scapa | Test adaugat |
| --- | --- | --- |
| `weight_kg <= 0` devine `weight_kg < 0` | Testul cu `-1` ramane valid; doar frontiera `0` expune diferenta | teste pentru `0` si valori pozitive foarte mici |
| `cost *= 1.5` este modificat | Un test care verifica doar ca express este mai scump nu verifica formula exacta | `test_express_multiplier_is_exactly_one_point_five` |
| Regulile premium si rural sunt aplicate in alta ordine | Testele separate pot trece, dar combinatia produce alt rezultat | `test_rural_fee_is_added_after_premium_discount` |
| `round(cost, 2)` este eliminat | Valorile intregi nu arata problema | `test_rounding_to_two_decimals_is_stable` |

## Interpretare

Folosirea ChatGPT a fost utila in trei etape:

1. A extins suita initiala cu teste pentru ramuri omise, ceea ce a crescut coverage-ul pe modulul testat de la 67% la 100%.
2. A ajutat la identificarea unor categorii de mutanti greu de observat prin teste manuale simple, precum mutanti de frontiera, mutanti ai multiplicatorilor si mutanti ai rotunjirii.
3. A contribuit la structurarea unui sistem simplu de prioritizare a testelor pe baza punctelor critice identificate in cod.

Rezultatele generate de AI nu au fost acceptate direct. Fiecare test a fost verificat prin rulare, valorile asteptate au fost recalculate, iar rezultatele finale au fost confirmate prin instrumente automate. In final, suita obtine 100% coverage pe modulul testat si 43/43 mutanti omorati.

## Limitari

ChatGPT poate propune teste incomplete sau valori asteptate gresite daca promptul nu contine toate regulile de business. De asemenea, AI-ul nu poate confirma singur ca un mutant este echivalent sau ca un rezultat local este corect. Din acest motiv, raspunsurile AI au fost tratate ca sugestii, iar validarea finala a fost facuta prin:

- `pytest`;
- `pytest-cov`;
- `mutmut`;
- verificarea manuala a formulelor si a rapoartelor.

## Concluzie

AI-ul a fost util pentru cresterea eficientei procesului de testare, dar calitatea finala a suitei a venit din combinarea sugestiilor AI cu validare umana si instrumente automate. Aceasta corespunde temei T10: imbunatatirea testarii unitare existente prin AI, masurata prin coverage, mutation testing si prioritizare automata.

## Referinte

[1] OpenAI, ChatGPT, https://chatgpt.com/, Data generarii: 9-23 mai 2026.  
[2] pytest, Documentation, https://docs.pytest.org/, Data ultimei accesari: 23 mai 2026.  
[3] Coverage.py, Documentation, https://coverage.readthedocs.io/, Data ultimei accesari: 23 mai 2026.  
[4] Mutmut, Documentation, https://mutmut.readthedocs.io/, Data ultimei accesari: 23 mai 2026.
