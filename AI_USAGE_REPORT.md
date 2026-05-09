# Raport privind folosirea tool-urilor AI

## Context

Proiectul are ca scop imbunatatirea unei suite de teste unitare pentru modulul `ShippingCostCalculator`. Modulul calculeaza costul de livrare in functie de greutate, distanta, tipul livrarii, tipul clientului si zona de livrare.

Tool-ul AI folosit a fost ChatGPT. Acesta a fost utilizat pentru generarea de idei de teste, identificarea unor cazuri limita si rafinarea suitei de teste dupa analiza rezultatelor de coverage si mutation testing.

## Tool AI utilizat

| Tool | Scop | Data utilizarii |
| --- | --- | --- |
| ChatGPT | Generare si imbunatatire teste unitare pytest | 9 mai 2026 |

Nu au fost preluate automat rezultate fara verificare. Valorile asteptate din teste au fost recalculate manual pe baza formulei din cod, iar testele au fost rulate cu `pytest`, `pytest-cov` si `mutmut`.

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

Aceste idei au fost transformate in testele din `tests/test_ai_generated.py`.

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

Aceste idei au fost transformate in testele din `tests/test_mutation_killers.py`.

## Comparatie intre suitele de teste

| Aspect | Suita manuala initiala | Suita imbunatatita cu AI | Suita finala |
| --- | --- | --- | --- |
| Numar teste | 3 | 13 | 25 |
| Coverage pe `shipping_calculator.py` | 67% | 100% | 100% |
| Teste pentru `same_day` | Nu | Da | Da |
| Teste pentru `premium` | Nu | Da | Da |
| Teste pentru `rural` | Nu | Da | Da |
| Teste pentru inputuri invalide | Partial | Da | Da |
| Teste pentru valori de frontiera | Nu | Partial | Da |
| Teste pentru mutation testing | Nu | Partial | Da |
| Mutanti omorati | Nu a fost scopul suitei initiale | Imbunatatire partiala | 43/43 |

## Exemple de cazuri greu de prins manual

| Mutatie posibila | De ce poate scapa | Test adaugat |
| --- | --- | --- |
| `weight_kg <= 0` devine `weight_kg < 0` | Testul cu `-1` ramane valid; doar frontiera `0` expune diferenta | teste pentru `0` si valori pozitive foarte mici |
| `cost *= 1.5` este modificat | Un test care verifica doar ca express este mai scump nu verifica formula exacta | `test_express_multiplier_is_exactly_one_point_five` |
| Regulile premium si rural sunt aplicate in alta ordine | Testele separate pot trece, dar combinatia produce alt rezultat | `test_rural_fee_is_added_after_premium_discount` |
| `round(cost, 2)` este eliminat | Valorile intregi nu arata problema | `test_rounding_to_two_decimals_is_stable` |

## Interpretare

Folosirea ChatGPT a fost utila in doua etape:

1. A extins suita initiala cu teste pentru ramuri omise, ceea ce a crescut coverage-ul de la 67% la 100%.
2. A ajutat la identificarea unor categorii de mutanti greu de observat prin teste manuale simple, precum mutanti de frontiera, mutanti ai multiplicatorilor si mutanti ai rotunjirii.

Rezultatele generate de AI nu au fost acceptate direct. Fiecare test a fost verificat prin rulare, iar valorile asteptate au fost recalculate manual. In final, suita a obtinut 100% coverage pe modulul testat si 43/43 mutanti omorati.

## Limitari

ChatGPT poate propune teste incomplete sau valori asteptate gresite daca promptul nu contine toate regulile de business. De aceea, raspunsurile au fost tratate ca sugestii, nu ca sursa finala de adevar. Validarea finala a fost facuta prin `pytest`, `pytest-cov` si `mutmut`.

## Referinte

[1] OpenAI, ChatGPT, https://chatgpt.com/, Data generarii: 9 mai 2026.  
[2] pytest, Documentation, https://docs.pytest.org/, Data ultimei accesari: 9 mai 2026.  
[3] Coverage.py, Documentation, https://coverage.readthedocs.io/, Data ultimei accesari: 9 mai 2026.  
[4] Mutmut, Documentation, https://mutmut.readthedocs.io/, Data ultimei accesari: 9 mai 2026.
