"""Create a trait pipeline."""
import spacy
from traiter.pipes.sentence_pipe import SENTENCE
from traiter.pipes.term_pipe import TERM_PIPE

from . import tokenizer
from .patterns import term_patterns


def pipeline():
    exclude = """ tagger ner lemmatizer """.split()
    nlp = spacy.load("en_core_web_sm", exclude=exclude)

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(
        TERM_PIPE,
        before="parser",
        config={
            "terms": term_patterns.TERMS.terms,
            "replace": term_patterns.REPLACE,
        },
    )

    nlp.add_pipe(SENTENCE, before="parser")

    return nlp
