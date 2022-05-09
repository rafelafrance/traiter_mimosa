"""Parse shape traits."""
import re

from spacy import registry
from traiter import const as t_const
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns


TEMP = ["\\" + c for c in t_const.DASH[:2]]
MULTIPLE_DASHES = rf'[{"".join(TEMP)}]{{2,}}'

SHAPE_LOC = term_patterns.SHAPES + ["shape_leader", "location"]
SHAPE_WORD = term_patterns.SHAPES + ["shape_leader"]

DECODER = common_patterns.COMMON_PATTERNS | {
    "shape": {"ENT_TYPE": {"IN": term_patterns.SHAPES}},
    "shape_leader": {"ENT_TYPE": "shape_leader"},
    "shape_loc": {"ENT_TYPE": {"IN": SHAPE_LOC}},
    "shape_word": {"ENT_TYPE": {"IN": SHAPE_WORD}},
    "angular": {"LOWER": {"IN": ["angular", "angulate"]}},
}

# #####################################################################################
SHAPE = MatcherPatterns(
    "shape",
    on_match="mimosa.shape.v1",
    decoder=DECODER,
    patterns=[
        "shape_loc* -* shape+",
        "shape_loc* -* shape -* shape+",
        "shape_leader -/to shape_word+ -* shape+",
        "shape_word+ -* shape+",
    ],
)


@registry.misc(SHAPE.on_match)
def shape(ent):
    # Sets do not preserve order
    cached_labels = term_patterns.SHAPES + ["shape_suffix"]
    parts = {
        r: 1
        for t in ent
        if (r := term_patterns.REPLACE.get(t.lower_, t.lower_))
        and t._.cached_label in cached_labels
    }

    value = "-".join(parts.keys())
    value = re.sub(rf"\s*{MULTIPLE_DASHES}\s*", r"-", value)
    label = "leaf_shape" if "leaf_shape" in ent._.data.keys() else "shape"
    ent._.new_label = label
    ent._.data[label] = term_patterns.REPLACE.get(value, value)
    loc = [t.lower_ for t in ent if t._.cached_label == "location"]
    if loc:
        ent._.data["location"] = loc[0]


# #####################################################################################
N_SHAPE = MatcherPatterns(
    "n_shape",
    on_match="mimosa.n_shape.v1",
    decoder=DECODER,
    patterns=[
        "shape_loc* 9 - angular",
    ],
)


@registry.misc(N_SHAPE.on_match)
def n_shape(ent):
    """Handle 5-angular etc."""
    ent._.new_label = "shape"
    ent._.data = {"shape": "polygonal"}
