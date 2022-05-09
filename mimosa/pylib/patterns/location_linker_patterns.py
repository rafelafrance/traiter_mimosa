from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns

LOCATION_PARENTS = ["location"]
LOCATION_CHILDREN = term_patterns.remove_traits("location shape sex taxon")

LOCATION_LINKER = matcher_patterns.MatcherPatterns(
    "location_linker",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "location": {"ENT_TYPE": {"IN": LOCATION_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LOCATION_CHILDREN}},
    },
    patterns=[
        "trait    word* location",
        "location word* trait",
    ],
)
