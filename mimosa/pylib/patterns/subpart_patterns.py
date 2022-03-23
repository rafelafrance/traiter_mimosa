"""Part patterns."""
from traiter.patterns.matcher_patterns import MatcherPatterns

from ..consts import COMMON_PATTERNS

SUBPART = MatcherPatterns(
    "subpart",
    decoder=COMMON_PATTERNS
    | {
        "part": {"ENT_TYPE": "part"},
        "subpart": {"ENT_TYPE": "subpart"},
    },
    patterns=[
        "subpart - subpart",
        "part - subpart",
        "subpart - part",
    ],
)
