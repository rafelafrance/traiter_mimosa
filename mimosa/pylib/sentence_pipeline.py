"""Create a trait pipeline."""
import spacy
from traiter.pipes.sentence_pipe import SENTENCE
from traiter.pipes.term_pipe import TERM_PIPE
from traiter.tokenizer_util import append_abbrevs
from traiter.tokenizer_util import append_tokenizer_regexes

from .patterns import term_utils


def pipeline():
    exclude = """ tagger ner lemmatizer """.split()
    nlp = spacy.load("en_core_web_sm", exclude=exclude)

    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, term_utils.ABBREVS)

    nlp.add_pipe(
        TERM_PIPE,
        before="parser",
        config={
            "terms": term_utils.TERMS.terms,
            "replace": term_utils.REPLACE,
        },
    )

    nlp.add_pipe(SENTENCE, before="parser")

    return nlp
