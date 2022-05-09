"""Link subparts to traits.

We are linking a subpart like "hairs" to a trait like "length" or "color".
For example: "leaves are covered with white hairs 1-(1.5) mm long."
Should link "hairs" with the color "white" and to the length "1 to 1.5 mm".
Named entity recognition (NER) must be run first.
"""
from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns

SUBPART_PARENT = "subpart"
SUBPART_CHILDREN = term_patterns.remove_traits("subpart part location sex habit")

SUBPART_LINKER = matcher_patterns.MatcherPatterns(
    "subpart_linker",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "subpart": {"ENT_TYPE": SUBPART_PARENT},
        "trait": {"ENT_TYPE": {"IN": SUBPART_CHILDREN}},
    },
    patterns=[
        "trait   word* subpart",
        "subpart word* trait",
    ],
)
