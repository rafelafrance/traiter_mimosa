"""For when plant parts are being used as a location."""
from spacy import registry
from traiter import actions
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import size_patterns

DECODER = common_patterns.COMMON_PATTERNS | {
    "adj": {"POS": "ADJ"},
    "cm": {"ENT_TYPE": "metric_length"},
    "leader": {"LOWER": {"IN": """to at embracing""".split()}},
    "not_loc": {"ENT_TYPE": {"IN": ["sex", "location"]}},
    "of": {"LOWER": "of"},
    "part": {"ENT_TYPE": "part"},
    "prep": {"POS": "ADP"},
    "sex": {"ENT_TYPE": "sex"},
    "subpart": {"ENT_TYPE": "subpart"},
}

PART_AS_LOCATION = MatcherPatterns(
    "part_as_loc",
    on_match=actions.TEXT_ACTION,
    decoder=DECODER,
    patterns=[
        "leader part",
    ],
)

PART_AS_DISTANCE = MatcherPatterns(
    "part_as_distance",
    on_match="mimosa.part_as_distance.v1",
    decoder=DECODER,
    patterns=[
        "leader part prep? 99-99 cm",
    ],
)

SUBPART_AS_LOCATION = MatcherPatterns(
    "subpart_location",
    on_match="mimosa.subpart_location.v1",
    decoder=DECODER,
    patterns=[
        "leader subpart",
        "leader subpart of adj? subpart",
    ],
)


@registry.misc(PART_AS_DISTANCE.on_match)
def part_as_distance(ent):
    size_patterns.size(ent)
    ent._.new_label = "part_as_loc"
    for e in [e for e in ent.ents if e._.cached_label != "metric_length"]:
        e._.merge = True


@registry.misc(SUBPART_AS_LOCATION.on_match)
def subpart_location(ent):
    ent._.new_label = "part_as_loc"
    actions.text_action(ent)
