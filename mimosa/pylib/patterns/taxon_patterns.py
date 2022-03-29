"""Get mimosa taxon notations."""
from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns

DECODER = {
    "family": {"ENT_TYPE": "family"},
    "genus": {"ENT_TYPE": "genus"},
    "m.": {"LOWER": "m."},
    "roman": {"TEXT": {"REGEX": r"^[ivx]+\.?$"}},
    "sect.": {"LOWER": {"IN": ["sect.", "section"]}},
    "section": {"ENT_TYPE": "section"},
    "ser.": {"LOWER": {"IN": ["ser.", "series"]}},
    "series": {"ENT_TYPE": "series"},
    "species": {"ENT_TYPE": "species"},
    "subsect.": {"LOWER": {"IN": ["subsect.", "subsection"]}},
    "subsection": {"ENT_TYPE": "subsection"},
    "subser.": {"LOWER": {"IN": ["subser.", "subseries"]}},
    "subseries": {"ENT_TYPE": "subseries"},
    "subsp.": {"LOWER": {"IN": ["subsp.", "subspecies"]}},
    "subspecies": {"ENT_TYPE": "subspecies"},
    "subtribe": {"ENT_TYPE": "subtribe"},
    "tribe": {"ENT_TYPE": "tribe"},
    "var.": {"LOWER": {"IN": ["var.", "variant"]}},
    "variant": {"ENT_TYPE": "variant"},
    "word": {"LOWER": {"REGEX": r"^[\w\d-]{4,}$"}},
}

TAXON_ON_MATCH = "mimosa.taxon.v1"

SPECIES = MatcherPatterns(
    "species",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "genus species",
        "m. species",
    ],
)

SUBSPECIES = MatcherPatterns(
    "subspecies",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "genus species subsp. word",
        "genus species subspecies",
        "m. species subsp. word",
    ],
)

VARIANT = MatcherPatterns(
    "variant",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "genus species subsp. word var. word",
        "genus species subspecies variant",
        "genus species var. word",
        "genus species variant",
        "m. species subsp. word var. word",
        "m. species var. word",
        "var. word",
    ],
)

FAMILY = MatcherPatterns(
    "family",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "family",
    ],
)

TRIBE = MatcherPatterns(
    "tribe",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "tribe",
    ],
)

SUBTRIBE = MatcherPatterns(
    "subtribe",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "subtribe",
    ],
)

GENUS = MatcherPatterns(
    "genus",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "genus",
    ],
)

SECTION = MatcherPatterns(
    "section",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "sect. word",
        "section",
    ],
)

SUBSECTION = MatcherPatterns(
    "subsection",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "subsect. word",
        "subsection",
    ],
)

SERIES = MatcherPatterns(
    "series",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "ser. roman word",
        "ser. word",
        "series",
    ],
)

SUBSERIES = MatcherPatterns(
    "subseries",
    on_match=TAXON_ON_MATCH,
    decoder=DECODER,
    patterns=[
        "subser. word",
        "subseries",
    ],
)


@registry.misc(TAXON_ON_MATCH)
def taxon_match(ent):
    """Enrich a taxon match."""
    ent._.new_label = "taxon"
    ent._.data = {
        "level": ent.label_,
        "taxon": ent.text,
    }
