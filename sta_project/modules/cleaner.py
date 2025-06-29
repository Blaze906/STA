# -*- coding: utf-8 -*-
"""
modules.cleaner
Smart Clean-up:
    • ricerca duplicati (--dupes)
    • rimozione file temporanei (--tmp)
    • eliminazione directory vuote (--empty)
    • --dry-run: simulazione
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


# ---------------------------------------------------------
# Configurazione “temporanei”
# ---------------------------------------------------------
TMP_EXTENSIONS = {
    ".tmp",
    ".temp",
    ".bak",
    ".old",
    ".swp",
    ".swo",
    ".~",
    ".log",
    ".pyc",
    ".pyo",
}

TMP_DIRNAMES = {"__pycache__", ".pytest_cache", ".mypy_cache"}


# ---------------------------------------------------------
# Utilities
# ---------------------------------------------------------
def human(bytes_n: int) -> str:
    """Converte byte in stringa leggibile (KB/MB/GB)."""
    step = 1024.0
    units = ("B", "KB", "MB", "GB", "TB")
    size = float(bytes_n)
    for unit in units:
        if size < step:
            return f"{size:,.2f} {unit}"
        size /= step
    return f"{size:,.2f} PB"


def sha256_of_file(path: Path, chunk: int = 8192) -> str:
    """Calcola hash SHA-256 del file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


@dataclass
class CleanReport:
    deleted_files: int = 0
    deleted_dirs: int = 0
    space_reclaimed: int = 0  # byte
    errors: List[str] = None

    def __post_init__(self):
        self.errors = self.errors or []

    def log_error(self, msg: str):
        self.errors.append(msg)


# ---------------------------------------------------------
# Core
# ---------------------------------------------------------
class SmartCleaner:
    def __init__(
        self,
        paths: List[Path],
        find_dupes: bool,
        remove_tmp: bool,
        remove_empty: bool,
        dry_run: bool,
    ):
        self.paths = [p.expanduser().resolve() for p in paths]
        self.find_dupes = find_dupes
        self.remove_tmp = remove_tmp
        self.remove_empty = remove_empty
        self.dry_run = dry_run

        # Memorizziamo info
        self._duplicates: Dict[str, List[Path]] = defaultdict(list)
        self._tmp_files: List[Path] = []
        self._candidate_dirs: Set[Path] = set()

        self.report = CleanReport()

    # ----------------------------- scan -----------------------------
    def scan(self):
        for root in self.paths:
            if not root.exists():
                self.report.log_error(f"Percorso non trovato: {root}")
                continue
            self._walk(root)

        if self.find_dupes:
            self._process_duplicates()

        if self.remove_empty:
            self._process_empty_dirs()

    def _walk(self, root: Path):
        for dirpath, dirnames, filenames in os.walk(root):
            dpath = Path(dirpath)

            # --- eventuale rimozione cartelle “tmp” ---
            if self.remove_tmp and dpath.name in TMP_DIRNAMES:
                self._delete_dir(dpath)
                # Non scendere dentro la cartella appena eliminata
                dirnames[:] = []
                continue

            # Conserviamo per eventuale check directory vuote
            if self.remove_empty:
                self._candidate_dirs.add(dpath)

            # --- file ---
            for f in filenames:
                fpath = dpath / f
                # tmp?
                if self.remove_tmp and self._is_tmp(fpath):
                    self._delete_file(fpath)
                    continue

                # duplicati?
                if self.find_dupes and fpath.is_file():
                    try:
                        h = sha256_of_file(fpath)
                        self._duplicates[h].append(fpath)
                    except Exception as exc:  # noqa: BLE001
                        self.report.log_error(f"Errore lettura {fpath}: {exc}")

    # --------------------- process duplicates -----------------------
    def _process_duplicates(self):
        for hash_, files in self._duplicates.items():
            if len(files) < 2:
                continue  # nessun duplicato

            # Manteniamo il primo file, gli altri vengono eliminati
            keeper = files[0]
            dups = files[1:]

            for dup in dups:
                self._delete_file(dup)

            if not self.dry_run:
                # Aggiorna hash di riferimento, non serve ma lo lasciamo
                # nel caso si volesse estendere con link simbolici
                self._duplicates[hash_] = [keeper]

    # -------------------- remove empty dirs ------------------------
    def _process_empty_dirs(self):
        # Ordine inverso -> bottom-up
        for d in sorted(self._candidate_dirs, key=lambda p: len(p.parts), reverse=True):
            try:
                if d.exists() and not any(d.iterdir()):
                    self._delete_dir(d)
            except Exception as exc:  # noqa: BLE001
                self.report.log_error(f"Errore su {d}: {exc}")

    # ----------------------- helpers --------------------------------
    @staticmethod
    def _is_tmp(path: Path) -> bool:
        return path.suffix.lower() in TMP_EXTENSIONS

    # ----------- safe delete / dry-run aware ------------------------
    def _delete_file(self, path: Path):
        try:
            size = path.stat().st_size if path.exists() else 0
            if not self.dry_run:
                path.unlink(missing_ok=True)
            self.report.deleted_files += 1
            self.report.space_reclaimed += size
            print(f"[FILE] {'(dry) ' if self.dry_run else ''}deleted  -> {path}")
        except Exception as exc:  # noqa: BLE001
            self.report.log_error(f"Errore eliminazione file {path}: {exc}")

    def _delete_dir(self, path: Path):
        try:
            size = self._dir_size(path)
            if not self.dry_run:
                shutil.rmtree(path, ignore_errors=True)
            self.report.deleted_dirs += 1
            self.report.space_reclaimed += size
            print(f"[DIR ] {'(dry) ' if self.dry_run else ''}deleted  -> {path}")
        except Exception as exc:  # noqa: BLE001
            self.report.log_error(f"Errore eliminazione dir {path}: {exc}")

    @staticmethod
    def _dir_size(path: Path) -> int:
        total = 0
        for p in path.rglob("*"):
            if p.is_file():
                try:
                    total += p.stat().st_size
                except Exception:  # noqa: BLE001
                    pass
        return total

    # --------------------------- run --------------------------------
    def execute(self) -> CleanReport:
        self.scan()
        return self.report


# ---------------------------------------------------------
# API esterna (richiamata da sta.py)
# ---------------------------------------------------------
def run_cleaner(
    paths,
    find_dupes: bool,
    remove_tmp: bool,
    remove_empty: bool,
    dry_run: bool,
):
    cleaner = SmartCleaner(
        paths=paths,
        find_dupes=find_dupes,
        remove_tmp=remove_tmp,
        remove_empty=remove_empty,
        dry_run=dry_run,
    )
    report = cleaner.execute()

    # ---------------- Stampa resoconto finale ----------------
    print("\n" + "=" * 60)
    print("RESOCONTO SMART CLEAN-UP")
    print("=" * 60)
    print(f" File eliminati : {report.deleted_files:,}")
    print(f" Cartelle elim. : {report.deleted_dirs:,}")
    print(f" Spazio recup.  : {human(report.space_reclaimed)}")
    if report.errors:
        print("\n⚠️  Errori / Skip:")
        for err in report.errors:
            print("  •", err)
    else:
        print("\nNessun errore rilevato.")
    print("=" * 60)

    # Valore di uscita: 0 ok, 1 se errori
    sys.exit(1 if report.errors else 0)

