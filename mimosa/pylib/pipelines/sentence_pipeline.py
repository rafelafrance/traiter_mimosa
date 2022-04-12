"""Create a trait pipeline."""
import spacy
from traiter.pipes.sentence_pipe import SENTENCE
from traiter.tokenizer_util import append_abbrevs
from traiter.tokenizer_util import append_tokenizer_regexes

from ..patterns import terms_utils


def pipeline():
    exclude = """ tagger ner lemmatizer """.split()
    nlp = spacy.load("en_core_web_sm", exclude=exclude)

    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, terms_utils.ABBREVS)

    config = {"phrase_matcher_attr": "LOWER"}
    term_ruler = nlp.add_pipe(
        "entity_ruler", name="term_ruler", config=config, before="parser"
    )
    term_ruler.add_patterns(terms_utils.TERMS.for_entity_ruler())

    nlp.add_pipe(SENTENCE, before="parser")

    return nlp
