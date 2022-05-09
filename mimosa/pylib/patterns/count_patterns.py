"""Common count snippets."""
from spacy import registry
from traiter import actions
from traiter import const as t_const
from traiter import util as t_util
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

# ####################################################################################
NOT_COUNT_WORDS = (
    t_const.CROSS + t_const.SLASH + """ average side times days weeks by """.split()
)
NOT_COUNT_ENTS = """ imperial_length metric_mass imperial_mass """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "adp": {"POS": {"IN": ["ADP"]}},
    "count_word": {"ENT_TYPE": "count_word"},
    "not_count_ent": {"ENT_TYPE": {"IN": NOT_COUNT_ENTS}},
    "not_count_word": {"LOWER": {"IN": NOT_COUNT_WORDS}},
    "per_count": {"ENT_TYPE": "per_count"},
    "subpart": {"ENT_TYPE": "subpart"},
    "x": {"LOWER": {"IN": ["x", "X"]}},
    "=": {"TEXT": {"IN": ["=", ":"]}},
}

# ####################################################################################
COUNT = MatcherPatterns(
    "count",
    on_match="mimosa.count.v1",
    decoder=DECODER,
    patterns=[
        "99-99",
        "99-99 -* per_count",
        "( 99-99 ) per_count",
    ],
)


@registry.misc(COUNT.on_match)
def count(ent):
    ent._.new_label = "count"

    range_ = [t for t in ent if t.ent_type_ == "range"][0]
    ent._.data = range_._.data

    for key in ["min", "low", "high", "max"]:
        if key in ent._.data:
            ent._.data[key] = t_util.to_positive_int(ent._.data[key])

    if ent._.data.get("range"):
        del ent._.data["range"]

    if pc := [e for e in ent.ents if e.label_ == "per_count"]:
        pc = pc[0]
        pc_text = pc.text.lower()
        pc._.new_label = "count_group"
        ent._.data["count_group"] = term_patterns.REPLACE.get(pc_text, pc_text)


# ####################################################################################
COUNT_WORD = MatcherPatterns(
    "count_word",
    on_match="mimosa.count_word.v1",
    decoder=DECODER,
    patterns=[
        "count_word",
    ],
)


@registry.misc(COUNT_WORD.on_match)
def count_word(ent):
    ent._.new_label = "count"
    word = [e for e in ent.ents if e.label_ == "count_word"][0]
    word._.data = {
        "low": t_util.to_positive_int(term_patterns.REPLACE[word.text.lower()])
    }


# ####################################################################################
NOT_A_COUNT = MatcherPatterns(
    "not_a_count",
    on_match=actions.REJECT_MATCH,
    decoder=DECODER,
    patterns=[
        "99-99 not_count_ent",
        "99-99 not_count_word 99-99? not_count_ent?",
        "9 / 9",
        "x =? 99-99",
    ],
)
