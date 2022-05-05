"""Common linker pattern utilities."""

TRAITS = set(
    """ color color_mod count location margin_shape part surface
    size shape sex subpart woodiness part_as_loc subpart_as_loc """.split()
)


def remove_traits(*remove: str) -> list:
    """Remove an element from a copy of the set."""
    removes = {r for r in remove}
    new_set = {e for e in TRAITS if e not in removes}
    return list(new_set)
