from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns

SUBPART = MatcherPatterns(
    "subpart",
    decoder=common_patterns.COMMON_PATTERNS
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
