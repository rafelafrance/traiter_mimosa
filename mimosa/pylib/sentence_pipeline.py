import regex as re
from spacy.lang.en import English
from traiter.pipes.sentence import SENTENCES
from traiter.pylib import tokenizer


def setup_tokenizer(nlp):
    not_letter = re.compile(r"[^a-zA-Z.']")
    removes = [s for s in nlp.tokenizer.rules if not_letter.search(s)]
    tokenizer.remove_special_case(nlp, removes)
    tokenizer.append_abbrevs(nlp, tokenizer.ABBREVS)


def pipeline():
    nlp = English()
    tokenizer.setup_tokenizer(nlp)
    nlp.add_pipe(SENTENCES, config={"abbrev": tokenizer.ABBREVS})
    return nlp
