"""Parse PDFs about mimosas."""
from tqdm import tqdm

from .. import mimosa_pipeline
from ..parsed_data import Datum


def read(args):
    with open(args.in_text) as in_file:
        lines = in_file.readlines()

    if args.limit:
        lines = lines[: args.limit]

    nlp = mimosa_pipeline.pipeline()

    data = []

    for ln in tqdm(lines):
        ln = ln.strip()
        doc = nlp(ln)
        traits = [e._.data for e in doc.ents]
        data.append(Datum(text=ln, traits=traits))

    return data
