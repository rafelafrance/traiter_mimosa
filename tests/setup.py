"""Setup for all tests."""
from typing import Dict
from typing import List

from traiter.util import shorten

from mimosa.pylib.pipelines.mimosa_pipeline import pipeline

NLP = pipeline()  # Singleton for testing


def test(text: str) -> List[Dict]:
    """Find entities in the doc."""
    text = shorten(text)
    doc = NLP(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    # from spacy import displacy
    # displacy.serve(doc, options={'collapse_punct': False, 'compact': True})

    return traits