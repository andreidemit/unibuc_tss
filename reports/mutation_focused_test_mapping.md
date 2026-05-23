# Raport: teste focalizate pe mutanti

Acest raport explica ce teste din `tests/test_mutation_focused_cases.py` acopera
si omoara mutantii generati pentru `src/shipping_calculator.py`.

`mutmut` arata statusul mutantilor, dar nu expune intotdeauna direct testul exact
care a omorat fiecare mutant. Pentru acest raport, mutantii au fost inspectati
si rulati impotriva testelor focalizate, iar tabelul de mai jos arata testul sau
grupul de teste relevant pentru fiecare tip de mutatie.

## Rezumat

| Zona mutata | Mutanti | Teste relevante |
| --- | --- | --- |
| Validari numerice pentru greutate si distanta | 1-6 | `test_positive_boundary_values_are_accepted`, `test_validation_error_messages_are_exact` |
| Validari pentru tipuri necunoscute | 7-12 | `test_validation_error_messages_are_exact` si testele cu inputuri valide care pica atunci cand validarea este inversata |
| Formula de baza | 13-20 | `test_positive_boundary_values_are_accepted`, `test_express_multiplier_is_exactly_one_point_five`, `test_rounding_to_two_decimals_is_stable` |
| Ramura `express` | 21-25 | `test_express_multiplier_is_exactly_one_point_five`, `test_premium_discount_is_applied_after_delivery_multiplier`, `test_rural_fee_is_added_after_premium_discount` |
| Ramura `same_day` | 26-30 | `test_same_day_multiplier_is_exactly_double` |
| Ramura `premium` | 31-35 | `test_premium_discount_is_applied_after_delivery_multiplier`, `test_rural_fee_is_added_after_premium_discount` |
| Ramura `rural` | 36-40 | `test_rural_fee_is_added_after_premium_discount` |
| Rotunjirea rezultatului final | 41-43 | `test_rounding_to_two_decimals_is_stable` si teste care asteapta valori numerice exacte |

## Mapping detaliat

| Mutant | Mutatie observata | Test focalizat relevant |
| ---: | --- | --- |
| 1 | `weight_kg <= 0` devine `weight_kg < 0` | `test_validation_error_messages_are_exact` |
| 2 | `weight_kg <= 0` devine `weight_kg <= 1` | `test_positive_boundary_values_are_accepted` |
| 3 | mesajul pentru `weight_kg` este modificat | `test_validation_error_messages_are_exact` |
| 4 | `distance_km <= 0` devine `distance_km < 0` | `test_validation_error_messages_are_exact` |
| 5 | `distance_km <= 0` devine `distance_km <= 1` | `test_positive_boundary_values_are_accepted` |
| 6 | mesajul pentru `distance_km` este modificat | `test_validation_error_messages_are_exact` |
| 7 | validarea `delivery_type not in ...` este inversata | testele cu input valid, in special `test_express_multiplier_is_exactly_one_point_five` |
| 8 | mesajul pentru `delivery_type` este modificat | `test_validation_error_messages_are_exact` |
| 9 | validarea `customer_type not in ...` este inversata | testele cu input valid, in special `test_premium_discount_is_applied_after_delivery_multiplier` |
| 10 | mesajul pentru `customer_type` este modificat | `test_validation_error_messages_are_exact` |
| 11 | validarea `area_type not in ...` este inversata | testele cu input valid, in special `test_rural_fee_is_added_after_premium_discount` |
| 12 | mesajul pentru `area_type` este modificat | `test_validation_error_messages_are_exact` |
| 13 | constanta de baza `10` devine `11` | `test_positive_boundary_values_are_accepted` |
| 14 | `10 + weight_kg * 2` devine `10 - weight_kg * 2` | `test_positive_boundary_values_are_accepted` |
| 15 | `weight_kg * 2` devine `weight_kg / 2` | `test_positive_boundary_values_are_accepted` |
| 16 | multiplicatorul greutatii `2` devine `3` | `test_positive_boundary_values_are_accepted` |
| 17 | `+ distance_km * 0.5` devine `- distance_km * 0.5` | `test_positive_boundary_values_are_accepted` |
| 18 | `distance_km * 0.5` devine `distance_km / 0.5` | `test_positive_boundary_values_are_accepted` |
| 19 | multiplicatorul distantei `0.5` devine `1.5` | `test_positive_boundary_values_are_accepted` |
| 20 | formula seteaza `cost = None` | orice test cu calcul valid; de exemplu `test_express_multiplier_is_exactly_one_point_five` |
| 21 | conditia `delivery_type == "express"` devine `!=` | `test_express_multiplier_is_exactly_one_point_five` |
| 22 | literalul `"express"` este modificat | `test_express_multiplier_is_exactly_one_point_five` |
| 23 | `cost *= 1.5` devine `cost /= 1.5` | `test_express_multiplier_is_exactly_one_point_five` |
| 24 | ramura express seteaza `cost = 1.5` | `test_express_multiplier_is_exactly_one_point_five` |
| 25 | multiplicatorul express `1.5` devine `2.5` | `test_express_multiplier_is_exactly_one_point_five` |
| 26 | conditia `same_day` este inversata | `test_same_day_multiplier_is_exactly_double` |
| 27 | literalul `"same_day"` este modificat | `test_same_day_multiplier_is_exactly_double` |
| 28 | `cost *= 2` devine `cost /= 2` | `test_same_day_multiplier_is_exactly_double` |
| 29 | ramura same_day seteaza `cost = 2` | `test_same_day_multiplier_is_exactly_double` |
| 30 | multiplicatorul same_day `2` devine `3` | `test_same_day_multiplier_is_exactly_double` |
| 31 | conditia `customer_type == "premium"` devine `!=` | `test_premium_discount_is_applied_after_delivery_multiplier` |
| 32 | literalul `"premium"` este modificat | `test_premium_discount_is_applied_after_delivery_multiplier` |
| 33 | `cost *= 0.8` devine `cost /= 0.8` | `test_premium_discount_is_applied_after_delivery_multiplier` |
| 34 | ramura premium seteaza `cost = 0.8` | `test_premium_discount_is_applied_after_delivery_multiplier` |
| 35 | reducerea premium `0.8` devine `1.8` | `test_premium_discount_is_applied_after_delivery_multiplier` |
| 36 | conditia `area_type == "rural"` devine `!=` | `test_rural_fee_is_added_after_premium_discount` |
| 37 | literalul `"rural"` este modificat | `test_rural_fee_is_added_after_premium_discount` |
| 38 | `cost += 15` devine `cost -= 15` | `test_rural_fee_is_added_after_premium_discount` |
| 39 | ramura rural seteaza `cost = 15` | `test_rural_fee_is_added_after_premium_discount` |
| 40 | taxa rurala `15` devine `16` | `test_rural_fee_is_added_after_premium_discount` |
| 41 | `round(cost, 2)` devine `round(None, 2)` | orice test cu calcul valid; de exemplu `test_rounding_to_two_decimals_is_stable` |
| 42 | rotunjirea la `2` zecimale devine rotunjire la `3` zecimale | `test_rounding_to_two_decimals_is_stable` |
| 43 | apelul `round(cost, 2)` este corupt | orice test cu calcul valid; de exemplu `test_rounding_to_two_decimals_is_stable` |

## Observatii pentru prezentare

- Testele de frontieră sunt importante pentru mutanti de tip `<= 0` schimbat in `< 0` sau `<= 1`.
- Testele cu valori exacte omoara mutanti care modifica multiplicatorii, de exemplu `1.5`, `2`, `0.8` sau `15`.
- Testele de combinatie omoara mutanti care aplica regulile in alta ordine sau afecteaza interactiunea dintre reguli.
- Testul de rotunjire foloseste valori fractionare deoarece valorile intregi pot ascunde mutanti in `round(cost, 2)`.
- `test_validation_error_messages_are_exact` omoara mutanti care schimba mesajele `ValueError`, nu doar conditiile.
