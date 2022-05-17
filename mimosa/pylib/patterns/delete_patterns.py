"""Remove entities when they meet these criteria."""
from spacy import registry

from . import term_patterns

# Delete traits that are supposed to be a part of a larger trait
PARTIAL_TRAITS = """ about cross color_mod dim dimension imperial_length imperial_mass
    margin_leader metric_length metric_mass not_a_range per_count
    quest shape_leader shape_suffix units joined range
    level month skip
    """.split()


# ####################################################################################
# Delete traits based upon special rules

DELETE_MISSING_PARTS = "mimosa.missing_parts.v1"


@registry.misc(DELETE_MISSING_PARTS)
def delete_missing_parts(ent):
    """Remove trait if it is missing both the part and subpart."""
    data = ent._.data
    has_part = set(data.keys()) & term_patterns.PARTS_SET
    return not has_part and not data.get("subpart")


# ####################################################################################
# Delete count traits based on special rules

DELETE_PAGE_NO = "mimosa.page_no.v1"

TITLE_SHAPES = """ Xxxxx Xxxx Xxx Xx X. Xx. X """.split()


@registry.misc(DELETE_PAGE_NO)
def delete_page_no(ent):
    """Remove a count if looks like a page number."""
    # Is it the last trait in the doc?
    if ent.end != len(ent.doc) - 1 or ent.doc[-1].text != ".":
        return False

    # Is it the only trait in the doc?
    if len(ent.doc.ents) == 1:
        return False

    # Are the previous 2 tokens title case?
    if (
        ent.start > 1
        and ent.doc[ent.start - 2].shape_ in TITLE_SHAPES
        and ent.doc[ent.start - 1].shape_ in TITLE_SHAPES
    ):
        return True

    # Is there a semicolon between the two traits?
    prev = ent.doc.ents[-2]
    for token in ent.doc[prev.end : ent.start]:
        if token.text in [";", ":", "."]:
            return True

    return False


# ####################################################################################
DELETE_UNLINKED = """surface_leader location""".split()

DELETE_WHEN = {
    "count": [DELETE_MISSING_PARTS, DELETE_PAGE_NO],
    "count_group": DELETE_MISSING_PARTS,
}
