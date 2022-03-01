"""Literals used in the system."""
import os
from pathlib import Path

from traiter.terms.csv_ import Csv

# #########################################################################
CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path(".." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
VOCAB_DIR = ROOT_DIR / "mimosa" / "vocabulary"


# #########################################################################
TERMS = Csv.shared('colors')  # units plant_treatment')
# TERMS += Csv.hyphenate_terms(TERMS)
# TERMS += Csv.trailing_dash(TERMS, label='color')
TERMS += Csv.read_csv(VOCAB_DIR / "taxa.csv")
TERMS.drop('imperial_length')

# #########################################################################
# Tokenizer constants
ABBREVS = """
    Jan. Feb. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
    ca. al. """.split()
