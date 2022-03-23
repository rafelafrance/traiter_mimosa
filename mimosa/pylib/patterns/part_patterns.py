"""Part patterns."""
from traiter.patterns.matcher_patterns import MatcherPatterns

from ..consts import COMMON_PATTERNS

PART = MatcherPatterns(
    "part",
    decoder=COMMON_PATTERNS
    | {
        "part": {"ENT_TYPE": "part"},
    },
    patterns=[
        "part - part",
    ],
)
