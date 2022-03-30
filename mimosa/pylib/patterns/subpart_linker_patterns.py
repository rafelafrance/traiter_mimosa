"""Link subparts to traits.

We are linking a subpart like "hairs" to a trait like "length" or "color".
For example: "leaves are covered with white hairs 1-(1.5) mm long."
Should link "hairs" with the color "white" and to the length "1 to 1.5 mm".
Named entity recognition (NER) must be run first.
"""
import copy

from traiter import const as t_const
from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes import dependency

from .. import consts
from .. import utils

TRAITS_ = utils.remove_traits(consts.TRAITS, "subpart")

punct_penalty = copy.deepcopy(t_const.PUNCT_PENALTY)
punct_penalty[";"] = t_const.NEVER

SUBPART_LINKER = DependencyPatterns(
    "subpart_linker",
    on_match={
        "func": dependency.LINK_NEAREST,
        "kwargs": {"anchor": "subpart", "exclude": "part", "penalty": punct_penalty},
    },
    decoder={
        "subpart": {"ENT_TYPE": "subpart"},
        "part": {"ENT_TYPE": "part"},
        "trait": {"ENT_TYPE": {"IN": TRAITS_}},
        "count": {"ENT_TYPE": "count"},
        "dash": {"TEXT": {"IN": t_const.DASH}},
        "link": {"POS": {"IN": ["ADJ", "AUX", "VERB", "PART"]}},
    },
    patterns=[
        "subpart ; dash ; count",
        "subpart >> trait",
        "subpart <  trait",
        "subpart .  trait",
        "subpart .  trait >> trait",
        "subpart .  link  >> trait",
        "subpart >  link  >> trait",
        "subpart <  trait >> trait",
        "subpart ;  part  <  link >> trait",
        "subpart . trait . link . trait",
    ],
)
