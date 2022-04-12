"""Link traits to body parts."""
from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes import dependency

from . import linker_utils

TRAITS_ = linker_utils.remove_traits("location")

LOCATION_LINKER = DependencyPatterns(
    "location_linker",
    on_match={"func": dependency.LINK_NEAREST, "kwargs": {"anchor": "location"}},
    decoder={
        "location": {"ENT_TYPE": "location"},
        "trait": {"ENT_TYPE": {"IN": TRAITS_}},
        "link": {"POS": {"IN": ["ADJ", "AUX", "VERB"]}},
    },
    patterns=[
        "location <  trait",
        "location .  trait",
        "location >> trait",
        "location .  trait >> trait",
        "location .  link  >> trait",
        "location <  link  >> trait",
        "location >  link  >> trait",
        "location <  trait >> trait",
    ],
)
