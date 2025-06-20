# Configurare

1. Copiați fișierul `env.example` sub numele `.env` în rădăcina proiectului:
   ```bash
   cp env.example .env
   ```
2. Deschideți `.env` și completați valorile pentru:
   - `INFURA_PROJECT_ID`
   - `ETHERSCAN_API_KEY`
   - `SOLSCAN_API_KEY` (opțional, pentru integrarea Solana)
   Pentru obținerea acestor chei este necesară crearea unui cont pe [Infura](https://infura.io/) și pe [Etherscan](https://etherscan.io/).

### Chei API suplimentare

Pentru a adăuga suport pentru alte rețele care necesită chei dedicate,
introduceți variabilele corespunzătoare în fișierul `.env`.
De exemplu, pentru Solscan se folosește `SOLSCAN_API_KEY`.
Noile chei sunt expuse automat în modulele `web3_connector.py` și
`web3-integration.py`.

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
