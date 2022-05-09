"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns


PART_PARENT = "part"
PART_CHILDREN = term_patterns.remove_traits("part location")

PART_LINKER = matcher_patterns.MatcherPatterns(
    "part_linker",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "part": {"ENT_TYPE": PART_PARENT},
        "trait": {"ENT_TYPE": {"IN": PART_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)
