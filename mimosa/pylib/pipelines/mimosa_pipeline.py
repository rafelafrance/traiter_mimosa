"""Create a trait pipeline."""

import spacy
from traiter.pipes.simple_entity_data import SIMPLE_ENTITY_DATA
from traiter.tokenizer_util import append_abbrevs
from traiter.tokenizer_util import append_tokenizer_regexes

from .. import consts


def pipeline():
    """Create a pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner'])

    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, consts.ABBREVS)

    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(consts.TERMS.for_entity_ruler())
    # add_ruler_patterns(term_ruler, TERM_RULES)

    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe(SIMPLE_ENTITY_DATA, after='term_merger')

    return nlp
