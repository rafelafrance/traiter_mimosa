"""Literals used in the system."""
import os
from pathlib import Path

from traiter import const

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
MOCK_DIR = ROOT_DIR / "tests" / "mock_data"

TITLE_SHAPES = set(""" Xxxxx Xxxx Xxx Xx X. Xx. X """.split())

LOWER_TAXON_LEVEL = """ species subspecies variety subvariety form subform """.split()

TOKEN_WEIGHTS = const.TOKEN_WEIGHTS | {"with": 10, "of": 3}
