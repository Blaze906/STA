#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
import shutil
from pathlib import Path
from typing import Iterable, Tuple, List

# Configurazione e costanti                                                   
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ']+")

# Spaziatura interna della cornice
PAD = 2

# Caratteri della cornice
FRAME = {
    "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
    "h":  "═", "v": "║", "sep_l": "╠", "sep_r": "╣",
}

# Funzioni di utilità                                                         
def term_width(default: int = 120) -> int:
    """Ritorna la larghezza (in colonne) del terminale, con fallback."""
    try:
        return shutil.get_terminal_size().columns
    except OSError:
        return default


def stream_words(lines: Iterable[str]) -> Iterable[str]:
    for line in lines:
        for m in WORD_RE.finditer(line):
            yield m.group(0).lower().strip("'")


def analyze_text_file(path: Path) -> Tuple[int, float]:
    total_len = total_words = 0
    with path.open(encoding="utf-8", errors="ignore") as fh:
        for word in stream_words(fh):
            total_words += 1
            total_len += len(word)

    avg_len = (total_len / total_words) if total_words else 0.0
    return total_words, avg_len


# Pretty-printing                                                             
def _wrap(text: str, width: int) -> List[str]:
    import textwrap
    return textwrap.wrap(text, width) or [""]


def print_frame(title: str, lines: List[str]) -> None:
    """Stampa un riquadro ‑ stile ‘box’ ‑ che si adatta al terminale."""
    all_text = [title] + lines
    longest_raw = max(len(s) for s in all_text)

    # Larghezza massima consentita (interno + bordi)
    max_inner_allowed = term_width() - 2       # -2 per i bordi sinistro/destro
    desired_inner     = longest_raw + PAD * 2  # padding interno

    # Se il contenuto entra tutto, usiamo la larghezza reale; altrimenti facciamo wrapping
    inner_width = desired_inner if desired_inner <= max_inner_allowed else max_inner_allowed
    wrap_width  = inner_width - PAD * 2

    h, v = FRAME["h"], FRAME["v"]

    print(f"{FRAME['tl']}{h * inner_width}{FRAME['tr']}")
    for ln in _wrap(title, wrap_width):
        print(f"{v}{' ' * PAD}{ln.center(wrap_width)}{' ' * PAD}{v}")
    print(f"{FRAME['sep_l']}{h * inner_width}{FRAME['sep_r']}")
    for raw in lines:
        for ln in _wrap(raw, wrap_width):
            print(f"{v}{' ' * PAD}{ln.ljust(wrap_width)}{' ' * PAD}{v}")
    print(f"{FRAME['bl']}{h * inner_width}{FRAME['br']}")


# Layer CLI                                                                  
def cmd_analyze(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.is_file():
        sys.exit(f"Errore: '{path}' non è un file valido.")

    n_words, avg = analyze_text_file(path)
    print_frame(
        f"ANALISI FILE: {path.name}",
        [
            f"Numero totale di parole : {n_words}",
            f"Lunghezza media parole : {avg:.2f} caratteri",
        ],
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Strumenti per l’analisi di file di testo (.txt)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # comando: sta text_analyzer <file>
    pa = sub.add_parser(
        "text_analyzer",
       help="Conta le parole e calcola la lunghezza media di un file .txt",
    )
    pa.add_argument("file", help="Percorso del file di testo")
    pa.set_defaults(func=cmd_analyze)
    return parser


def main() -> None:
    parser = build_parser()

    # Mostra un piccolo “dashboard” se lanciato senza argomenti
    if len(sys.argv) == 1:
        print_frame(
            "STA (System Task Automator)",
            [
                "Questo programma analizza file di testo per contare",
                "le parole e calcolare la loro lunghezza media.",
                "",
                "COMANDO PRINCIPALE:",
                "  text_analyzer <percorso_file>",
                "",
                "Esempio:",
                "  python sta.py text_analyzer 'percorso_del_file'",
            ],
        )
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
