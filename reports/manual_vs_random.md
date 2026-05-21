# Raport comparativ: teste manuale vs teste aleatoare

Comenzile folosite pentru masurare:

```bash
python -m pytest tests/test_manual_basic.py --cov=shipping_calculator --cov-branch --cov-report=json:reports/coverage-manual.json --cov-fail-under=0
python -m pytest tests/test_random.py --cov=shipping_calculator --cov-branch --cov-report=json:reports/coverage-random.json --cov-fail-under=0
```

| Criteriu | Teste manuale | Teste aleatoare |
|---|---:|---:|
| Numar de teste | 3 | 621 |
| Statement coverage pe SUT | 71% | 100% |
| Branch coverage pe SUT | 61% | 100% |
| Mutanti eliminati | necesita rulare dedicata pe aceasta suita | necesita rulare dedicata pe aceasta suita |
| Efort de scriere | mic, dar acoperire incompleta | mediu: generator + oracol independent |

## Interpretare

Testele manuale de baza sunt usor de scris si bune pentru validarea formulei principale, dar nu acopera suficient validari, combinatii si ramuri. Random testing-ul cu seed fix extinde rapid spatiul de inputuri si acopera toate ramurile SUT-ului, insa are nevoie de un oracol independent ca sa nu compare functia cu ea insasi.

Pentru mutation score separat pe suite, `mutmut` trebuie rulat cu runner dedicat pentru fiecare suita. In proiect, mutation testing-ul principal este evaluat pe suita completa, unde raportul local curent indica 43/43 mutanti omorati.
