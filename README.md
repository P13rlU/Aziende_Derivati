# Aziende_Derivati — Documentazione Python

Autore: [P13rlU](https://github.com/P13rlU)

Repo: [Aziende_Derivati](https://github.com/P13rlU/Aziende_Derivati)

---

## Indice

1. [Introduzione](#introduzione)
2. [Struttura del progetto](#struttura-del-progetto)
3. [Requisiti](#requisiti)
4. [Installazione](#installazione)
5. [Configurazione](#configurazione)
6. [Esecuzione](#esecuzione)
7. [Dipendenze principali](#dipendenze-principali)
8. [Testing (se presente)](#testing-se-presente)
9. [License](#license)

---

## Introduzione

La parte Python del progetto *Aziende_Derivati* fa da backend / logica lato server / script per il progetto finale ITS, integrandosi con React (frontend) e Oracle DB.
Questa documentazione descrive come installarla, configurarla, quali sono i requisiti, e come usarla.

---

## Struttura del progetto

```
python/
├── <Flask>/
│   ├── __init__.py
│   └── ... (altri file .py con funzioni, classi, etc.)
├── requirements.txt
└── (altri script utili, ad esempio per migrazioni, setup, ecc.)
```

---

## Requisiti

Per far funzionare la parte Python servono:

- Python versione **3.x** (consigliato 3.8 o superiore)
- Accesso al database Oracle (versione compatibile)
- (Opzionale) Ambiente virtuale (virtualenv, venv, conda, etc.)
- I pacchetti elencati in `requirements.txt`

---

## Installazione

Passaggi consigliati:

1. Clona la repo:

   ```bash
   git clone https://github.com/P13rlU/Aziende_Derivati.git
   ```

2. Entra nella cartella python:

   ```bash
   cd Aziende_Derivati/python
   ```

3. Crea un ambiente virtuale:

   ```bash
   python3 -m venv venv
   source venv/bin/activate     # su Unix/macOS
   # oppure
   venv\Scripts\activate        # su Windows
   ```

4. Installa le dipendenze:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configurazione

- Impostare le variabili di ambiente necessarie, ad esempio le credenziali per Oracle DB (host, utente, password, nome del DB).
- Eventuali file di configurazione (es: `.env`, `config.py`) necessari vanno popolati.

---

## Esecuzione

Descrizione di come lanciare il backend / gli script Python:

- Se c’è un file principale (es: `main.py` o simile), esegui:

  ```bash
  python main.py
  ```

- Se fai uso di script specifici (migrazioni, caricamento dati, etc.), usare:

  ```bash
  python scripts/nome_script.py
  ```

- (Se applicabile) indica endpoint della API, porte, etc.

---

## Dipendenze principali

Le librerie più importanti che il progetto Python usa:

- Oracle driver per Python (es: `cx_Oracle` o equivalente)  
- Qualche ORM o driver DB  
- Altre librerie utili (es: gestione JSON, parsing, logging, etc.)  

> Vedi `requirements.txt` per la lista completa.

---
