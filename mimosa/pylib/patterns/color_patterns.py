"""Common color snippets."""
import re

from spacy import registry
from traiter.const import DASH
from traiter.const import DASH_CHAR
from traiter.patterns.matcher_patterns import MatcherPatterns

from .. import consts

MULTIPLE_DASHES = ["\\" + c for c in DASH_CHAR]
MULTIPLE_DASHES = fr'\s*[{"".join(MULTIPLE_DASHES)}]{{2,}}\s*'

SKIP = DASH + consts.MISSING

COLOR = MatcherPatterns(
    "color",
    on_match="mimosa.color.v1",
    decoder=consts.COMMON_PATTERNS
    | {
        "color_words": {"ENT_TYPE": {"IN": ["color", "color_mod"]}},
        "color": {"ENT_TYPE": "color"},
        "to": {"POS": {"IN": ["AUX"]}},
    },
    patterns=[
        "missing? color_words* -* color+ -* color_words*",
        "missing? color_words+ to color_words+ color+ -* color_words*",
    ],
)


@registry.misc(COLOR.on_match)
def color(ent):
    """Enrich a color match."""
    parts = []
    for token in ent:
        replace = consts.REPLACE.get(token.lower_, token.lower_)
        if replace in SKIP:
            continue
        if consts.REMOVE.get(token.lower_):
            continue
        if token.pos_ in ["AUX"]:
            continue
        parts.append(replace)
    value = "-".join(parts)
    value = re.sub(MULTIPLE_DASHES, r"-", value)
    ent._.data["color"] = consts.REPLACE.get(value, value)
    if any(t for t in ent if t.lower_ in consts.MISSING):
        ent._.data["missing"] = True
