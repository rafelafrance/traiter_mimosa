"""Remove entities when they meet these criteria."""
from spacy import registry

from . import term_patterns

# Forget traits were supposed to be parts of a larger trait
PARTIAL_TRAITS = """ about cross color_mod dim dimension imperial_length imperial_mass
    margin_leader metric_length metric_mass not_a_range per_count
    quest shape_leader shape_suffix units joined
    range.low range.min.low range.low.high range.low.max range.min.low.high
    range.min.low.max range.low.high.max range.min.low.high.max range
    level month
    """.split()


# ####################################################################################
# Forget traits based upon special rules

DELETE_MISSING_PARTS = "mimosa.missing_parts.v1"


@registry.misc(DELETE_MISSING_PARTS)
def delete_missing_parts(ent):
    """Remove trait if it is missing both the part and subpart."""
    data = ent._.data
    has_part = set(data.keys()) & term_patterns.PARTS_SET
    return not has_part and not data.get("subpart")


# ####################################################################################
DELETE_UNLINKED = """surface_leader location""".split()

DELETE_WHEN = {
    "count": DELETE_MISSING_PARTS,
    "count_group": DELETE_MISSING_PARTS,
}
