"""Remove entities when they meet these criteria."""
from spacy import registry

FORGET = """ about cross color_mod dim dimension imperial_length imperial_mass
    margin_leader metric_length metric_mass not_a_range per_count
    quest shape_leader shape_suffix surface units
    range.low range.min.low range.low.high range.low.max range.min.low.high
    range.min.low.max range.low.high.max range.min.low.high.max
    level
    """.split()

FORGET_WHEN = "mimosa.forget_when.v1"

WHEN_MISSING = """
    part tribe genus section series subseries species subspecies variant
    """.split()


@registry.misc(FORGET_WHEN)
def forget_when(ent):
    """Remove entities without a part."""
    for key in WHEN_MISSING:
        if ent._.data.get(key):
            return False
    return True
