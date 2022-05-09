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


# #########################################################################
PARTS = set(
    """
    female_flower_part
    flower_part
    fruit_part
    inflorescence
    leaf_part
    male_flower_part
    part
    """.split()
)
LOCATIONS = set(""" flower_location location """.split())
MORPHOLOGIES = set(""" flower_morphology plant_morphology """.split())
SHAPES = set(""" leaf_shape shape """.split())
TRAITS = PARTS | set(
    """
    habitat
    leaf_duration
    leaf_folding
    leaf_margin
    plant_duration
    plant_habit
    reproduction
    sex
    subpart
    surface
    venation
    woodiness
    part_as_loc
    subpart_as_loc
    """.split()
)


def remove_traits(remove: str) -> list:
    return list(set(TRAITS) - set(remove.split()))
