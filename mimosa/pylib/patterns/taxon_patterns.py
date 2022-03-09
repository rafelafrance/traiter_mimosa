"""Get mimosa taxon notations."""
from traiter.patterns.matcher_patterns import MatcherPatterns

TAXON = MatcherPatterns(
    "taxon",
    decoder={
        "genus": {"ENT_TYPE": "genus"},
        "species": {"ENT_TYPE": "species"},
        "m": {"LOWER": "m."},
        "ser": {"LOWER": {"IN": ["ser.", "serial"]}},
        "subser": {"LOWER": {"IN": ["subser.", "subsection"]}},
        "sect": {"LOWER": {"IN": ["sect.", "section"]}},
        "subsect": {"LOWER": {"IN": ["subsect.", "subsection"]}},
        "subsp": {"LOWER": {"IN": ["subsp.", "subspecies"]}},
        "var": {"LOWER": {"IN": ["var.", "variant"]}},
        "word": {"LOWER": {"REGEX": r"^[\w\d-]+$"}},
    },
    patterns=[
        "genus species",
        "genus species var word",
        "genus species subsp word",
        "genus species subsp word var word",
        "m species",
        "m species var word",
        "m species subsp word",
        "m species subsp word var word",
        "species var word",
        "species subsp word",
        "sect word ser word",
        "ser word subser word",
        "ser word",
        "subser word",
        "sect word",
        "subsect word",
    ],
)
