"""Parse the trait."""
import re

from spacy import registry
from traiter.const import DASH
from traiter.patterns.matcher_patterns import MatcherPatterns

from ..consts import COMMON_PATTERNS
from ..consts import REPLACE

TEMP = ["\\" + c for c in DASH[:2]]
MULTIPLE_DASHES = fr'[{"".join(TEMP)}]{{2,}}'

LEADERS = """ shape shape_leader margin_leader """.split()
FOLLOWERS = """ margin_shape margin_follower """.split()
SHAPES = """ margin_shape shape """.split()

MARGIN_SHAPE = MatcherPatterns(
    "margin_shape",
    on_match="mimosa.margin.v1",
    decoder=COMMON_PATTERNS
    | {
        "margin_shape": {"ENT_TYPE": "margin_shape"},
        "shape": {"ENT_TYPE": {"IN": SHAPES}},
        "leader": {"ENT_TYPE": {"IN": LEADERS}},
        "follower": {"ENT_TYPE": {"IN": FOLLOWERS}},
    },
    patterns=[
        "leader* -* margin_shape+",
        "leader* -* margin_shape -* follower*",
        "leader* -* margin_shape -* shape? follower+ shape?",
        "shape+ -* follower+",
    ],
)


@registry.misc(MARGIN_SHAPE.on_match)
def margin(ent):
    """Enrich a phrase match."""
    value = {
        r: 1
        for t in ent
        if (r := REPLACE.get(t.text, t.text)) and t._.cached_label in SHAPES
    }
    value = "-".join(value.keys())
    value = re.sub(rf"\s*{MULTIPLE_DASHES}\s*", r"-", value)
    ent._.data["margin_shape"] = REPLACE.get(value, value)
