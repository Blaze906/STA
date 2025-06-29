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

## Esempio di Output

L'output dell'analisi di un file sarà simile al seguente:

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

## Come Contribuire al Progetto

Le contribuzioni sono benvenute! Se desideri contribuire, per favore apri una issue o una pull request.
