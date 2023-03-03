import regex as re
from spacy.lang.en import English
from traiter.pylib import tokenizer
from traiter.pylib import tokenizer_util
from traiter.pylib.pipes.sentence_pipe import SENTENCE


def setup_tokenizer(nlp):
    not_letter = re.compile(r"[^a-zA-Z.']")
    removes = [{"pattern": s} for s in nlp.tokenizer.rules if not_letter.search(s)]
    tokenizer_util.remove_special_case(nlp, removes)
    tokenizer_util.append_tokenizer_regexes(nlp)
    tokenizer_util.append_abbrevs(nlp, tokenizer.ABBREVS)


def pipeline():
    nlp = English()
    tokenizer.setup_tokenizer(nlp)
    nlp.add_pipe(SENTENCE, config={"abbrev": tokenizer.ABBREVS})
    return nlp
