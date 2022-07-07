from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns

ON_TAXON_LIKE_MATCH = "mimosa.taxon_like.v1"


SIMILAR = """ like similar exactly sympatric affini resembling resembles
    vicinis """.split()


TAXON_LIKE = MatcherPatterns(
    "taxon_like",
    on_match=ON_TAXON_LIKE_MATCH,
    decoder={
        "any": {},
        "prep": {"DEP": "prep"},
        "similar": {"LOWER": {"IN": SIMILAR}},
        "taxon": {"ENT_TYPE": "taxon"},
    },
    patterns=[
        "similar+ taxon+",
        "similar+ any? prep taxon+",
    ],
)


@registry.misc(ON_TAXON_LIKE_MATCH)
def on_taxon_like_match(ent):
    ent._.data = next((e._.data for e in ent.ents if e.label_ == "taxon"), {})
    relations = [t.text.lower() for t in ent if t.text in SIMILAR]
    ent._.data["relation"] = " ".join(relations)
