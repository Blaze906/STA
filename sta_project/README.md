# STA (System Task Automator)

STA è un'applicazione a riga di comando progettata per automatizzare task comuni di sistema, semplificando operazioni ripetitive e fornendo strumenti utili per la gestione dei file e l'analisi dei dati.

## Funzionalità

Attualmente, STA include le seguenti funzionalità:

### 1. Analisi di File di Testo (`text_analyzer`)

Questa funzionalità permette di analizzare un file di testo specificato per:
- Contare il numero totale di parole.
- Calcolare la lunghezza media delle parole.

**Utilizzo:**
```bash
python sta.py text_analyzer " percorso/del/tuo/file.txt"
```

**Esempio di Output:**
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║ ANALISI FILE: Documento_STA.txt                           ║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║ Numero Totale di Parole: 150                              ║
║ Lunghezza Media Parole: 5.25 caratteri                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### 2. Smart Clean-up (`clean`)

Questo modulo esegue una pulizia intelligente di directory specificate (o quella corrente di default).

**Utilizzo:**
```bash
python sta.py clean [directory1 directory2 ...] [opzioni]
```

**Argomenti e Opzioni:**
- `directories`: (Opzionale) Una o più directory da scansionare. Se omesso, utilizza la directory di lavoro corrente (`.`).
- `--dupes`: Trova file duplicati (basati sul contenuto) e chiede conferma prima di eliminare le copie (mantenendo l'originale con il percorso più breve o il primo incontrato).
- `--tmp`: Rimuove file e cartelle temporanee comuni (es. `*.tmp`, `__pycache__/`, `node_modules/`).
- `--empty`: Elimina le cartelle che sono diventate vuote dopo le operazioni di pulizia, o quelle già vuote.
- `--dry-run`: Mostra quali file e cartelle sarebbero eliminati/modificati senza eseguire alcuna azione reale. È utile per testare i comandi.

**Operazioni Combinate:**
Puoi combinare le opzioni `--dupes`, `--tmp`, e `--empty` per eseguire più operazioni di pulizia in un unico comando.

**Esempi:**

- **Analizzare e pulire la directory corrente (solo dry run):**
  ```bash
  python sta.py clean --dupes --tmp --empty --dry-run
  ```

- **Rimuovere file temporanei e cartelle vuote da `~/Downloads` e `~/Desktop` (esecuzione reale):**
  ```bash
  python sta.py clean ~/Downloads ~/Desktop --tmp --empty
  ```

- **Trovare ed eliminare duplicati nella cartella `my_project/` (esecuzione reale):**
  ```bash
  python sta.py clean my_project/ --dupes
  ```

**Resoconto Finale:**
Al termine delle operazioni, `clean` fornirà un resoconto che include:
- Numero totale di file/cartelle cancellati.
- Spazio su disco recuperato (in bytes e MB).
- Eventuali errori riscontrati o file/cartelle saltati.

## Installazione e Avvio

1.  Assicurati di avere Python 3.6+ installato.
2.  Clona questo repository o scarica i file.
3.  Naviga nella directory `sta_project/`.
4.  Esegui i comandi come mostrato negli esempi sopra.

   ```bash
   cd sta_project
   python sta.py --help
   ```

## Struttura del Progetto
```
sta_project/
├── sta.py                   # Script principale per la gestione dei comandi.
├── modules/                 # Cartella per i moduli specifici.
│   ├── __init__.py          # Rende 'modules' un package Python.
│   ├── text_analyzer.py     # Logica per l'analisi dei file di testo.
│   └── cleaner.py           # Logica per lo smart clean-up.
└── README.md                # Questo file.
```

## TODO (Miglioramenti Futuri)
- [ ] **Cleaner - Strategia di Merge per Duplicati**: Implementare una strategia di merge più sofisticata per i file duplicati (es. conservare il più recente, unire contenuti se possibile per file di testo).
- [ ] **Cleaner - Configurazione Estendibile**: Permettere agli utenti di definire pattern personalizzati per file/cartelle temporanee tramite un file di configurazione.
- [ ] **Test**: Aggiungere test unitari e di integrazione più completi.
- [ ] **Logging**: Implementare un sistema di logging più robusto per tracciare le operazioni.
- [ ] **Internazionalizzazione**: Supporto per output in diverse lingue.
```
