"""Parse the trait."""
import re

from spacy import registry
from traiter import const as t_const
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

TEMP = ["\\" + c for c in t_const.DASH[:2]]
MULTIPLE_DASHES = rf'[{"".join(TEMP)}]{{2,}}'

LEADERS = """ leaf_shape shape shape_leader margin_leader """.split()
FOLLOWERS = """ leaf_margin margin_follower """.split()
SHAPES = """ leaf_margin shape leaf_shape """.split()

LEAF_MARGIN = MatcherPatterns(
    "leaf_margin",
    on_match="mimosa.margin.v1",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "leaf_margin": {"ENT_TYPE": "leaf_margin"},
        "shape": {"ENT_TYPE": {"IN": SHAPES}},
        "leader": {"ENT_TYPE": {"IN": LEADERS}},
        "follower": {"ENT_TYPE": {"IN": FOLLOWERS}},
    },
    patterns=[
        "leader* -* leaf_margin+",
        "leader* -* leaf_margin -* follower*",
        "leader* -* leaf_margin -* shape? follower+ shape?",
        "shape+ -* follower+",
    ],
)


@registry.misc(LEAF_MARGIN.on_match)
def margin(ent):
    value = {
        r: 1
        for t in ent
        if (r := term_patterns.REPLACE.get(t.text, t.text))
        and t._.cached_label in SHAPES
    }
    value = "-".join(value.keys())
    value = re.sub(rf"\s*{MULTIPLE_DASHES}\s*", r"-", value)
    ent._.data["leaf_margin"] = term_patterns.REPLACE.get(value, value)
