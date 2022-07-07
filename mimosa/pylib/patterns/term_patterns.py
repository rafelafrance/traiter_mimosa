from traiter.terms.db import Db

from .. import consts

TERM_DB = consts.DATA_DIR / "plant_terms.sqlite"
if not TERM_DB.exists():
    TERM_DB = consts.MOCK_DIR / "plant_terms.sqlite"

# #########################################################################
TERMS = Db.shared("colors units taxon_levels time")
TERMS += Db.select_term_set(TERM_DB, "plant_treatment")
TERMS += Db.trailing_dash(TERMS, label="color")
TERMS += Db.select_term_set(TERM_DB, "plant_taxa")
TERMS.drop("imperial_length")
TERMS.drop("time_units")

REPLACE = TERMS.pattern_dict("replace")
REMOVE = TERMS.pattern_dict("remove")
SUFFIX_TERM = TERMS.pattern_dict("suffix_term")

LEVELS = TERMS.pattern_dict("level")
LEVELS = {k: v.split() for k, v in LEVELS.items()}


# #########################################################################
PARTS = """
    female_flower_part
    flower_part
    fruit_part
    inflorescence
    leaf_part
    male_flower_part
    multiple_parts
    part
    """.split()
PARTS_SET = set(PARTS)

LOCATIONS = """ flower_location location """.split()
MORPHOLOGIES = """ flower_morphology plant_morphology """.split()
PLANT_TRAITS = """ plant_duration plant_habit """.split()

TRAITS = (
    PARTS
    + LOCATIONS
    + """
    color
    color_mod
    count
    duration
    joined
    shape
    size
    habitat
    leaf_duration
    leaf_folding
    margin
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


def remove_traits(removes: list[str]) -> list:
    return [t for t in TRAITS if t not in removes]
