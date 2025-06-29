# This file makes 'modules' a Python package.
# Rende 'modules' un pacchetto importabile da sta.py
from importlib import import_module

# Re-export dei sotto-moduli per semplicità
text_analyzer = import_module(".text_analyzer", package=__name__)
cleaner = import_module(".cleaner", package=__name__)
