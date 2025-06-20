# Configurare

1. Copiați fișierul `env.example` sub numele `.env` în rădăcina proiectului:
   ```bash
   cp env.example .env
   ```
2. Deschideți `.env` și completați valorile pentru:
   - `INFURA_PROJECT_ID`
   - `ETHERSCAN_API_KEY`
   - `SOLANA_RPC_URL` *(opțional, pentru rețeaua Solana)*
   - `SOLSCAN_API_KEY` *(opțional)*
   Pentru obținerea cheilor `INFURA_PROJECT_ID` și `ETHERSCAN_API_KEY` este necesară crearea unui cont pe [Infura](https://infura.io/) și pe [Etherscan](https://etherscan.io/). Pentru rețeaua Solana se poate folosi un RPC public sau unul propriu și, dacă este disponibil, un API key Solscan.

## Instalarea dependențelor

Rulați următoarea comandă pentru a instala pachetele necesare:
```bash
pip install -r requirements.txt
```

**Notă pentru Google Colab:** mediul Colab include deja anumite pachete cu
versiuni blocate, în special `pandas` și `requests`. Pentru a evita mesaje de
conflict la instalare este recomandat să păstrați versiunile existente în Colab
prin rularea comenzii de mai sus fără opțiunea `--upgrade`.

## Rulare

Aplicația poate fi utilizată local sau în Google Colab. Pentru rularea locală executați:
```bash
python vesting_analyzer.py
```
În Colab, încărcați fișierele proiectului și rulați aceleași comenzi în celule.


## Testare

Pentru a rula testele unitare se foloseste `pytest`. Unele module externe pot incarca automat pluginuri care nu sunt necesare, asa ca recomandam dezactivarea autoload-ului:
```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest
```
