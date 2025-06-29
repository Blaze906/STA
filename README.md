# STA - System Task Automator

## Descrizione

STA (System Task Automator) è un'applicazione a riga di comando progettata per automatizzare task comuni di sistema, semplificando operazioni ripetitive e fornendo strumenti utili per la gestione dei file e l'analisi dei dati.
## Funzionalità

### Analisi di File di Testo (`analizza_testo`)

Questa funzionalità permette di analizzare un file di testo specificato per:

*   Contare il numero totale di parole.
*   Calcolare la lunghezza media delle parole.

## Smart Clean-up (`clean`)

Questa funzionalità analizza e permette di ripulire il file system da:

* directory vuote
* file vuoti
* file temporanei

Inoltre, se l'opzione `--dry-run` è attivato, simula le operazioni di eliminazione senza modificare effettivamente il file system.

## Prerequisiti

*   Python 3.6 o superiore installato sul sistema
*   Il file sta.py deve essere richiamato tramite l'interprete python

## Installazione

Ci sono due possibili modi di installazione:
1.  Clona il repository dal tuo terminale:
    ```bash
    git clone https://github.com/Blaze906/STA.git
    cd sta_project
    ```
2.  Scarica il file .zip e estrai tutto in una cartella.

## Utilizzo

Il comando principale per interagire con STA è `python sta.py` se si è gia nella directory `sta_project`.
Altrimenti bisogna usare `python "percorso_completo_fino_a_sta_project/sta.py"`.

### `analizza_testo`

Per analizzare un file di testo, usa il seguente comando (se ti trovi nella directory `sta_project`):

```bash
python sta.py text_analyzer "percorso_del_file_txt"
```

Sostituisci `"percorso_del_file_txt"` con il percorso effettivo del file di testo che desideri analizzare.

**Esempio:**
(Il file da analizzare è in un altra directory, quindi specifichiamo `sta_project/sta.py`)
```bash
python "percorso_completo_fino_a_sta_project/sta.py" text_analyzer "C:\Users\Documents\STA\Documentazione_STA.txt"
```


### `clean`

Per utilizzare il cleaner, usa il seguente comando (se ti trovi nella directory `sta_project`):

```bash
python sta.py clean [OPZIONI] [PERCORSI_FILE]
```

Sostituisci `[PERCORSI_FILE]` con il percorso o i percorsi (separati da spazio) che desideri analizzare.

**Opzioni disponibili:**

*   `--dupes`: Ricerca e rimuove file duplicati (mantenendo una copia).
*   `--tmp`: Rimuove file e directory temporanee (es. `.tmp`, `.log`, `__pycache__`).
*   `--empty`: Elimina directory vuote.
*   `--dry-run`: Simula l'operazione di pulizia senza apportare modifiche effettive al filesystem. Mostra cosa verrebbe eliminato.

È possibile combinare le opzioni `--dupes`, `--tmp`, e `--empty`. Se non viene specificata nessuna di queste, il comando non eseguirà alcuna azione di pulizia specifica, ma potrà comunque scansionare le directory (utile con `--dry-run` per una panoramica).

**Esempi:**

1.  **Simulare la rimozione di file temporanei nella directory corrente:**
    ```bash
    python "percorso_completo_fino_a_sta_project/sta.py" clean --tmp --dry-run
    ```

2.  **Rimuovere file temporanei e le directory che diventano vuote nella cartella ~/Downloads:**
    ```bash
    python "percorso_completo_fino_a_sta_project/sta.py" clean --tmp --empty ~/Downloads
    ```

3.  **Trovare e rimuovere file duplicati (mantenendo il primo trovato) e file temporanei nella directory corrente e in ~/Documenti, mostrando solo cosa verrebbe fatto (dry run):**
    ```bash
    python "percorso_completo_fino_a_sta_project/sta.py" clean --dupes --tmp --dry-run . ~/Documenti
    ```

## Esempio di Output

L'output dell'analisi di un file di testo (`text_analyzer`) sarà simile al seguente:

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

L'output della pulizia del sistema (`clean`) sarà simile al seguente:
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
