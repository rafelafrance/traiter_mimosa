"""Parse PDFs about mimosas."""
from tqdm import tqdm

from .. import mimosa_pipeline
from .. import sentence_pipeline
from ..parsed_data import Datum


def read(args):
    with open(args.in_text) as in_file:
        lines = in_file.readlines()

    if args.limit:
        lines = lines[: args.limit]

    nlp = mimosa_pipeline.pipeline()
    sent_nlp = sentence_pipeline.pipeline()

    data = []

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
                traits.append(trait)
            data.append(Datum(text=sent.text, traits=traits))

    return data
