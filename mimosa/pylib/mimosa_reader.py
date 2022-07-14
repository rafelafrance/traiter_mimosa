from collections import namedtuple

from tqdm import tqdm

from . import mimosa_pipeline
from . import sentence_pipeline
from .patterns import term_patterns


TAXON_FIND = term_patterns.TAXA
TAXON_SKIP = TAXON_FIND + """ taxon_like """.split()

SentenceTraits = namedtuple("SentenceTraits", "text traits")


def read(args):
    with open(args.in_text, encoding="utf_8") as in_file:
        lines = in_file.readlines()

    if args.limit:
        lines = lines[: args.limit]

    nlp = mimosa_pipeline.pipeline()
    sent_nlp = sentence_pipeline.pipeline()

    data = []

    curr_taxon = None

    for ln in tqdm(lines):
        ln = ln.strip()
        sent_doc = sent_nlp(ln)
        for sent in sent_doc.sents:
            doc = nlp(sent.text)
            traits = []
            for ent in doc.ents:
                trait = ent._.data
                trait["start"] += sent.start_char
                trait["end"] += sent.start_char

                if trait["trait"] in TAXON_FIND:
                    curr_taxon = trait
                elif curr_taxon and trait["trait"] not in TAXON_SKIP:
                    ...

                traits.append(trait)
            data.append(SentenceTraits(text=sent.text, traits=traits))

    return data
