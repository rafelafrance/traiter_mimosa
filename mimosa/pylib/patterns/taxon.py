"""Get mimosa taxon notations."""
# from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns


TAXON = MatcherPatterns(
    "taxon",
)
