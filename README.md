# Configurare

1. Copiați fișierul `env.example` sub numele `.env` în rădăcina proiectului:
   ```bash
   cp env.example .env
   ```
2. Deschideți `.env` și completați valorile pentru:
   - `INFURA_PROJECT_ID`
   - `ETHERSCAN_API_KEY`
   Pentru obținerea acestor chei este necesară crearea unui cont pe [Infura](https://infura.io/) și pe [Etherscan](https://etherscan.io/).

## Instalarea dependențelor

Rulați următoarea comandă pentru a instala pachetele necesare:
```bash
pip install -r requirements.txt
```

## Rulare

Aplicația poate fi utilizată local sau în Google Colab. Pentru rularea locală executați:
```bash
python vesting_analyzer.py
```
În Colab, încărcați fișierele proiectului și rulați aceleași comenzi în celule.

