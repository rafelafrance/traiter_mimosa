"""Part patterns."""
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

PART = MatcherPatterns(
    "part",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": term_patterns.PARTS}},
    },
    patterns=[
        "part - part",
    ],
)
