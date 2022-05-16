"""For when plant parts are being used as a location."""
from spacy import registry
from traiter import actions
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import size_patterns
from . import term_patterns

DECODER = common_patterns.COMMON_PATTERNS | {
    "adj": {"POS": "ADJ"},
    "cm": {"ENT_TYPE": "metric_length"},
    "joined": {"ENT_TYPE": "joined"},
    "leader": {"LOWER": {"IN": """to at embracing""".split()}},
    "location": {"ENT_TYPE": "location"},
    "not_loc": {"ENT_TYPE": {"IN": ["sex"] + term_patterns.LOCATIONS}},
    "of": {"LOWER": "of"},
    "part": {"ENT_TYPE": {"IN": term_patterns.PARTS}},
    "prep": {"POS": "ADP"},
    "sex": {"ENT_TYPE": "sex"},
    "subpart": {"ENT_TYPE": "subpart"},
}


def add_joined(ent):
    """Add joined field."""
    if joined := [e for e in ent.ents if e.label_ == "joined"]:
        text = joined[0].text.lower()
        ent._.data["joined"] = term_patterns.REPLACE.get(text, text)


# ####################################################################################
ON_AS_LOCATION_MATCH = "mimosa.as_location.v1"

PART_AS_LOCATION = MatcherPatterns(
    "part_as_loc",
    on_match=ON_AS_LOCATION_MATCH,
    decoder=DECODER,
    patterns=[
        "joined?  leader part",
        "location leader part",
    ],
)

SUBPART_AS_LOCATION = MatcherPatterns(
    "subpart_as_loc",
    on_match=ON_AS_LOCATION_MATCH,
    decoder=DECODER,
    patterns=[
        "joined?  leader subpart",
        "joined?  leader subpart of adj? subpart",
        "location leader subpart",
        "location leader subpart of adj? subpart",
    ],
)


@registry.misc(ON_AS_LOCATION_MATCH)
def on_as_location_match(ent):
    add_joined(ent)
    actions.text_action(ent)


# ####################################################################################
PART_AS_DISTANCE = MatcherPatterns(
    "part_as_distance",
    on_match="mimosa.part_as_distance.v1",
    decoder=DECODER,
    patterns=[
        "joined?  leader part prep? 99-99 cm",
        "location leader part prep? 99-99 cm",
    ],
)


@registry.misc(PART_AS_DISTANCE.on_match)
def part_as_distance(ent):
    add_joined(ent)
    size_patterns.size(ent)
    ent._.new_label = "part_as_loc"
