# STA - System Task Automator

## Descrizione

STA (System Task Automator) è un'applicazione a riga di comando progettata per automatizzare task comuni di sistema, semplificando operazioni ripetitive e fornendo strumenti utili per la gestione dei file e l'analisi dei dati.
## Funzionalità

### Analisi di File di Testo (`analizza_testo`)

Questa funzionalità permette di analizzare un file di testo specificato per:

*   Contare il numero totale di parole.
*   Calcolare la lunghezza media delle parole.

I risultati vengono presentati in un formato chiaro e incorniciato direttamente nel terminale.

## Prerequisiti

*   Python 3.6 o superiore installato sul sistema
*   Il file sta deve essere un eseguibile o richiamato tramite l'interprete python

## Installazione

1.  Clona il repository dal tuo terminale:
    ```bash
    git clone https://github.com/Blaze906/STA.git
    cd sta_project
    ```
2.  Scarica il file .zip e estrai tutto in una cartella.

## Utilizzo

Il comando principale per interagire con STA è `python sta.py`.

### `analizza_testo`

Per analizzare un file di testo, usa il seguente comando dalla directory `sta_project`:

```bash
python sta.py analizza_testo "percorso_del_file_txt"
```

Sostituisci `<percorso_del_file_txt>` con il percorso effettivo del file di testo che desideri analizzare.

**Esempio:**

```bash
python sta.py analizza_testo "C:\Users\Documents\STA\Documentazione_STA.txt"
```

(Assumendo che `esempio.txt` si trovi nella directory principale del progetto, una sopra `sta_project`)

### `pulisci_sistema`

Questa funzionalità permette di pulire il sistema da file duplicati, file temporanei e directory vuote.

Per utilizzare il cleaner, usa il seguente comando dalla directory `sta_project`:

```bash
python sta.py pulisci_sistema <percorso_o_percorsi> [opzioni]
```

Sostituisci `<percorso_o_percorsi>` con il percorso o i percorsi (separati da spazio) che desideri analizzare.

**Opzioni disponibili:**

*   `--dupes`: Ricerca e rimuove file duplicati (mantenendo una copia).
*   `--tmp`: Rimuove file e directory temporanee (es. `.tmp`, `.log`, `__pycache__`).
*   `--empty`: Elimina directory vuote.
*   `--dry-run`: Simula l'operazione di pulizia senza apportare modifiche effettive al filesystem. Mostra cosa verrebbe eliminato.

È possibile combinare le opzioni `--dupes`, `--tmp`, e `--empty`. Se non viene specificata nessuna di queste, il comando non eseguirà alcuna azione di pulizia specifica, ma potrà comunque scansionare le directory (utile con `--dry-run` per una panoramica).

**Esempi:**

1.  **Trovare e rimuovere duplicati in una specifica cartella (simulazione):**
    ```bash
    python sta.py pulisci_sistema "/percorso/alla/cartella" --dupes --dry-run
    ```

2.  **Rimuovere file temporanei e directory vuote da più percorsi:**
    ```bash
    python sta.py pulisci_sistema "/percorso/cartella1" "/un/altro/percorso" --tmp --empty
    ```

3.  **Eseguire una pulizia completa (duplicati, temporanei, vuote) di una cartella:**
    ```bash
    python sta.py pulisci_sistema "./documenti" --dupes --tmp --empty
    ```

## Esempio di Output

L'output dell'analisi di un file di testo (`analizza_testo`) sarà simile al seguente:

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                      ANALISI FILE: Documento.txt                         ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   Numero Totale di Parole: 150                                           ║
║   Lunghezza Media Parole: 5.25 caratteri                                 ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```
*(Nota: i valori numerici sono puramente illustrativi)*

L'output della pulizia del sistema (`pulisci_sistema`) sarà simile al seguente:
```
[FILE] (dry) deleted  -> /percorso/esempio/tmp/file_temporaneo.tmp
[DIR ] (dry) deleted  -> /percorso/esempio/vuota/__pycache__
[FILE] deleted  -> /percorso/esempio/documenti_duplicati/copia_documento.txt

============================================================
RESOCONTO SMART CLEAN-UP
============================================================
 File eliminati : 3
 Cartelle elim. : 1
 Spazio recup.  : 1.25 MB
Nessun errore rilevato.
============================================================
```
*(Nota: i percorsi e i valori sono puramente illustrativi)*

## Come Contribuire al Progetto

Le contribuzioni sono benvenute! Se desideri contribuire, per favore apri una issue o una pull request.
