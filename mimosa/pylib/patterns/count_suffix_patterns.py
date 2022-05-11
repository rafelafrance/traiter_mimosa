from spacy import registry
from traiter import util as t_util
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

COUNT_SUFFIX = MatcherPatterns(
    "count_suffix",
    on_match="mimosa.count_suffix.v1",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "count_suffix": {"ENT_TYPE": "count_suffix"},
    },
    patterns=[
        "99-99 count_suffix",
    ],
)


@registry.misc(COUNT_SUFFIX.on_match)
def on_count_suffix_match(ent):
    ent._.new_label = "count"
    range_ = [t for t in ent if t.ent_type_ == "range"][0]
    suffix = [t for t in ent if t.ent_type_ == "count_suffix"][0]

    ent._.data = range_._.data

    for key in ["min", "low", "high", "max"]:
        if key in ent._.data:
            ent._.data[key] = t_util.to_positive_int(ent._.data[key])

    if ent._.data.get("range"):
        del ent._.data["range"]

    lower = suffix.text.lower()
    label = term_patterns.SUFFIX_TERM.get(lower, "subpart")
    ent._.data[label] = term_patterns.REPLACE.get(lower, lower)
