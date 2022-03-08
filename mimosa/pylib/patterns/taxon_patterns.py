"""Get mimosa taxon notations."""
from traiter.const import DOT
from traiter.patterns.matcher_patterns import MatcherPatterns


TAXON = MatcherPatterns(
    "taxon",
    decoder={
        ".": {"TEXT": {"IN": DOT}},
        "genus": {"ENT_TYPE": "genus"},
        "species": {"ENT_TYPE": "species"},
        "m": {"LOWER": "m"},
        "subsp": {"LOWER": "subsp"},
        "var": {"LOWER": "var"},
        "word": {"LOWER": {"REGEX": r"^[\w\d-]+$"}},
    },
    patterns=[
        "genus species",
        "genus species var . word",
        "genus species subsp . word",
        "genus species subsp . word var . word",
        "m . species",
        "m . species var . word",
        "m . species subsp . word",
        "m . species subsp . word var . word",
        "species var . word",
        "species subsp . word",
    ],
)
