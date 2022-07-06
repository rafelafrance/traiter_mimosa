from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns

ON_TAXON_LIKE_MATCH = "mimosa.taxon_like.v1"


SIMILAR = """ like similar as than exactly sympatric """.split()


TAXON_LIKE = MatcherPatterns(
    "taxon_like",
    on_match=ON_TAXON_LIKE_MATCH,
    decoder={
        "prep": {"DEP": "prep"},
        "similar": {"LOWER": {"IN": SIMILAR}},
        "taxon": {"ENT_TYPE": "taxon"},
    },
    patterns=[
        "similar prep? taxon+",
    ],
)


@registry.misc(ON_TAXON_LIKE_MATCH)
def on_taxon_like_match(ent):
    ent._.data = next((e._.data for e in ent.ents), {})
    ent._.data["relation"] = next((t.text for t in ent if t.text in SIMILAR), "unknown")
