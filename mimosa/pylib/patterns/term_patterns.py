from traiter.terms.db import Db

from .. import consts

TERM_DB = consts.DATA_DIR / "plant_terms.sqlite"
if not TERM_DB.exists():
    TERM_DB = consts.MOCK_DIR / "plant_terms.sqlite"

# #########################################################################
TERMS = Db.shared("colors units taxon_levels time")
TERMS += Db.select_term_set(TERM_DB, "plant_treatment")
TERMS += Db.hyphenate_terms(TERMS)
TERMS += Db.trailing_dash(TERMS, label="color")
TERMS += Db.select_term_set(TERM_DB, "plant_taxa")
TERMS.drop("imperial_length")
TERMS.drop("time_units")

REPLACE = TERMS.pattern_dict("replace")
REMOVE = TERMS.pattern_dict("remove")

LEVELS = TERMS.pattern_dict("level")
LEVELS = {k: v.split() for k, v in LEVELS.items()}
