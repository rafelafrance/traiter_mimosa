"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes import dependency

from . import linker_utils

TRAITS_ = linker_utils.remove_traits("part")

PART_LINKER = DependencyPatterns(
    "part_linker",
    on_match={
        "func": dependency.LINK_NEAREST,
        "kwargs": {"anchor": "part"},
    },
    decoder={
        "part": {"ENT_TYPE": "part"},
        "trait": {"ENT_TYPE": {"IN": TRAITS_}},
        "adv": {"POS": "ADV"},
        "link": {"POS": {"IN": ["ADJ", "AUX", "VERB"]}},
        "subpart": {"ENT_TYPE": "subpart"},
    },
    patterns=[
        "trait >> part",
        "part  <  trait",
        "part  .  trait",
        "part  >> trait",
        "part  .  trait   >> trait",
        "part  .  link    >> trait",
        "part  <  link    >> trait",
        "part  >  link    >> trait",
        "part  <  trait   >> trait",
        "part  .  adv     .  trait",
        "part  <  subpart <  trait",
        "part  <  subpart <  subpart < trait",
        "part  <  trait   <  trait",
        "part  .  link    .  trait",
    ],
)
