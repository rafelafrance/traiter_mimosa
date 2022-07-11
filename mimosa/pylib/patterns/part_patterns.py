from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

DECODER = common_patterns.COMMON_PATTERNS | {
    "part": {"ENT_TYPE": {"IN": term_patterns.PARTS}},
}

# ####################################################################################
PART = MatcherPatterns(
    "part",
    on_match="mimosa.part.v1",
    decoder=DECODER,
    patterns=[
        "part - part",
        "part and part",
    ],
)


@registry.misc(PART.on_match)
def on_part_match(ent):
    if any(t.lower_ in common_patterns.AND for t in ent):
        ent._.new_label = "multiple_parts"
        ent._.data["multiple_parts"] = [
            term_patterns.REPLACE.get(t.lower_, t.lower_)
            for t in ent
            if t.ent_type_ in term_patterns.PARTS_SET
        ]


# ####################################################################################
MISSING_PART = MatcherPatterns(
    "missing_part",
    decoder=DECODER,
    patterns=[
        "missing part",
        "missing part - part",
        "missing part and part",
    ],
)
