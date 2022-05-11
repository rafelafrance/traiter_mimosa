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


def part_and_subpart(ent):
    """Remove trait if it is missing both the part and subpart."""
    data = ent._.data
    has_part = set(data.keys()) & term_patterns.PARTS_SET
    return not has_part and not data.get("subpart")


def always(_):
    """Always forget this trait after it's been linked."""
    return True


# ####################################################################################
DELETE_WHEN = "mimosa.delete_when.v1"

WHEN_MISSING = {
    "count": part_and_subpart,
    "count_group": part_and_subpart,
    "surface_leader": always,
    "location": always,
}


@registry.misc(DELETE_WHEN)
def delete_when(ent):
    """Remove entities without enough information."""
    func = WHEN_MISSING.get(ent.label_, lambda _: False)
    return func(ent)
