"""Remove entities when they meet these criteria."""
from spacy import registry

FORGET_WHEN = "mimosa.forget_when.v1"

# Forget traits were supposed to be parts of a larger trait
FORGET = """ about cross color_mod dim dimension imperial_length imperial_mass
    margin_leader metric_length metric_mass not_a_range per_count
    quest shape_leader shape_suffix surface units
    range.low range.min.low range.low.high range.low.max range.min.low.high
    range.min.low.max range.low.high.max range.min.low.high.max
    level
    """.split()


# Forget traits based upon special rules
def part_and_subpart(ent):
    """Remove trait if it is missing both the part and subpart."""
    data = ent._.data
    return not data.get("part") and not data.get("subpart")


def always(_):
    """Always forget this trait after it's been linked."""
    return True


WHEN_MISSING = {
    "count": part_and_subpart,
    "count_group": part_and_subpart,
    "surface_leader": always,
    "location": always,
}


@registry.misc(FORGET_WHEN)
def forget_when(ent):
    """Remove entities without enough information."""
    func = WHEN_MISSING.get(ent.label_, lambda _: False)
    return func(ent)
