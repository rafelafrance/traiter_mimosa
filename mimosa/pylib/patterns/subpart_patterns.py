"""Part patterns."""
from traiter.patterns.matcher_patterns import MatcherPatterns

from .. import consts

SUBPART = MatcherPatterns(
    "subpart",
    decoder=consts.COMMON_PATTERNS
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
