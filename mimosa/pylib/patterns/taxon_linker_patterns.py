from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns

TAXON_PARENTS = ["taxon"]
TAXON_CHILDREN = term_patterns.all_traits_except(["taxon"])

TAXON_LINKER = matcher_patterns.MatcherPatterns(
    "taxon_linker",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "taxon": {"ENT_TYPE": {"IN": TAXON_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": TAXON_CHILDREN}},
    },
    patterns=[
        "trait any* taxon",
        "taxon any* trait",
    ],
)
