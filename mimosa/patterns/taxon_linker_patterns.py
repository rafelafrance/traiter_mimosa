"""Link traits to taxa."""
from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes.dependency import LINK_NEAREST

from mimosa.pylib import consts

TRAITS_ = list(consts.TRAITS)

TAXON_LINKER = DependencyPatterns(
    "taxon_linker",
    on_match={
        "func": LINK_NEAREST,
        "kwargs": {"anchor": "taxon"},
    },
    decoder={
        "trait": {"ENT_TYPE": {"IN": TRAITS_}},
        "taxon": {"ENT_TYPE": "taxon"},
    },
    patterns=[
        "trait >> taxon",
        "taxon >> trait",
    ],
)
