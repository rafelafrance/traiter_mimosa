"""Part patterns."""
from traiter.patterns.matcher_patterns import MatcherPatterns

from .. import consts

PART = MatcherPatterns(
    "part",
    decoder=consts.COMMON_PATTERNS
    | {
        "part": {"ENT_TYPE": "part"},
    },
    patterns=[
        "part - part",
    ],
)
